"""QLoRA em modelo pequeno (1,5B–4B) na RTX 4060 Laptop de 8 GB de VRAM.

O que está acontecendo, em uma frase cada:
- **Quantização 4-bit (bitsandbytes NF4)**: os pesos do modelo base ficam em 4 bits em vez de
  16. Um 3B passa de ~6 GB para ~2 GB. É o que faz 3B–4B caber em 8 GB junto com o treino.
- **LoRA**: em vez de treinar os bilhões de pesos, congela o modelo e treina duas matrizes
  pequenas (rank r) por camada de atenção/MLP. Treina 0,5–2% dos parâmetros; o adapter final
  tem dezenas de MB.
- **QLoRA** = os dois juntos: base congelada em 4-bit + adapters LoRA em 16-bit.
- **Gradient checkpointing**: troca compute por memória (recomputa ativações no backward).
  Mais lento, mas é o que faz caber com sequência de 1024 tokens.

Tetos na 4060 8 GB (ESTIMATIVA, nenhum medido nesta máquina; ver skill qlora-6gb):
1,5B e 3B com folga; 4B é o teto confortável; 7–8B só como experimento (--max-len 512 --r 8).
No Windows, VRAM cheia NÃO dá OOM: transborda para a memória compartilhada e fica 5–20x mais
lento. O script avisa no fim se o pico encostou no total da placa.

Formato do treino: `### Instrução:` / `### Entrada:` / `### Resposta:` (constantes CAB_* abaixo,
fonte ÚNICA). O Ollama, por padrão, aplicaria o chat template do modelo (ChatML no Qwen) e o
adapter receberia um prompt que nunca viu. Por isso o Modelfile é GERADO daqui (--modelfile),
nunca escrito à mão.

Dataset: JSONL com {"instruction": ..., "input": ..., "output": ...} por linha. Comece com
200–500 exemplos BONS; qualidade importa mais que volume.

Uso:
    python -m lab.finetune.qlora --data data/processed/treino.jsonl --dry-run
    python -m lab.finetune.qlora --data data/processed/treino.jsonl --out outputs/lora-v1
    python -m lab.finetune.qlora --data ... --model Qwen/Qwen2.5-3B-Instruct --epochs 2
    python -m lab.finetune.qlora --modelfile outputs/gguf/lora-v1-q4_k_m.gguf --adapter outputs/lora-v1

Antes de rodar: .\\setup.ps1 -Llm e `huggingface-cli login` se o modelo for gated (Llama).
Regra 6 do CLAUDE.md: antes disto, provar que few-shot no mesmo modelo NÃO resolve.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

MODELOS_SUGERIDOS = {
    # QLoRA, seq 1024, batch 1, grad_accum 8. VRAM = estimativa, não medida na 4060.
    "Qwen/Qwen2.5-1.5B-Instruct": "~3 GB; mais folga, bom pra começar",
    "Qwen/Qwen2.5-3B-Instruct": "~5 GB; folga na 4060 8 GB",
    "meta-llama/Llama-3.2-3B-Instruct": "~5 GB; gated no HF; sem pad próprio (ver AVISO pad=eos)",
    "Qwen/Qwen3-4B-Instruct-2507": "~6-7 GB; teto confortável da 4060 8 GB",
}

# --- Formato do treino: FONTE ÚNICA ------------------------------------------------------
# Treino (_formatar), inferência no comparar.py (via _formatar) e o TEMPLATE do Modelfile do
# Ollama (gerar_modelfile) derivam destas três strings. Mudar aqui muda tudo junto.
CAB_INSTRUCAO = "### Instrução:\n"
CAB_ENTRADA = "\n\n### Entrada:\n"
CAB_RESPOSTA = "\n\n### Resposta:\n"


def prompt_ollama(ex: dict) -> str:
    """O que se envia como `prompt` ao modelo no Ollama: instrução (+ entrada, se houver).

    O TEMPLATE do Modelfile põe CAB_INSTRUCAO antes e CAB_RESPOSTA depois disto.
    """
    inp = f"{CAB_ENTRADA}{ex['input']}" if ex.get("input") else ""
    return f"{ex['instruction']}{inp}"


def formatar_prompt(ex: dict) -> str:
    """Prefixo exato que o modelo vê antes de gerar a resposta (termina em '### Resposta:\\n')."""
    return f"{CAB_INSTRUCAO}{prompt_ollama(ex)}{CAB_RESPOSTA}"


def _formatar(ex: dict) -> str:
    """Texto de treino = prefixo + resposta. (O EOS é concatenado no main, com o token do tokenizer.)"""
    return formatar_prompt(ex) + ex["output"]


def template_ollama() -> str:
    """TEMPLATE (Go template) do Ollama que reproduz formatar_prompt.

    `{{ .Response }}` fica no fim de propósito: assim a string não termina em '\\n' e nenhum
    trim do parser do Modelfile come a quebra de linha depois de '### Resposta:'.
    """
    return f"{CAB_INSTRUCAO}{{{{ .Prompt }}}}{CAB_RESPOSTA}{{{{ .Response }}}}"


def gerar_modelfile(gguf_nome: str, eos_token: str) -> str:
    """Modelfile do Ollama com TEMPLATE e stop derivados das constantes do treino.

    gguf_nome: nome do .gguf (o .Modelfile é gravado na mesma pasta; FROM é relativo a ela).
    eos_token: token de fim que o treino concatenou (tokenizer_config.json do adapter).
    """
    tpl = template_ollama()
    if '"""' in tpl or '"' in eos_token:
        raise ValueError("aspas no template/eos quebram o Modelfile")
    stop_cabecalho = CAB_INSTRUCAO.strip()  # se o modelo começar um exemplo novo, corta
    return (
        "# Gerado por lab.finetune.qlora.gerar_modelfile a partir de CAB_INSTRUCAO/CAB_RESPOSTA.\n"
        "# NÃO editar o TEMPLATE à mão: regenerar com `python -m lab.finetune.qlora --modelfile`.\n"
        "# Sem este TEMPLATE o Ollama aplicaria o chat template do modelo base (ChatML no Qwen),\n"
        "# formato que o adapter nunca viu no treino.\n"
        f"FROM ./{gguf_nome}\n"
        f'TEMPLATE """{tpl}"""\n'
        f'PARAMETER stop "{stop_cabecalho}"\n'
        f'PARAMETER stop "{eos_token}"\n'
    )


def eos_do_adapter(adapter_dir: Path) -> str:
    """Lê o eos_token salvo por tok.save_pretrained (tokenizer_config.json ou special_tokens_map.json)."""
    for nome in ("tokenizer_config.json", "special_tokens_map.json"):
        p = Path(adapter_dir) / nome
        if p.exists():
            eos = json.loads(p.read_text(encoding="utf-8")).get("eos_token")
            if isinstance(eos, dict):
                eos = eos.get("content")
            if eos:
                return eos
    raise FileNotFoundError(f"eos_token não encontrado em {adapter_dir}; passe --eos explicitamente")


def aviso_vram(pico_gb: float, total_gb: float, fracao: float = 0.92) -> str | None:
    """Pico perto (ou acima) do total = provável transbordo para a memória compartilhada no Windows."""
    if pico_gb >= fracao * total_gb:
        return (f"AVISO: pico de VRAM {pico_gb:.1f} GB de {total_gb:.1f} GB. No Windows o driver transborda "
                "para a memória compartilhada em vez de dar OOM: o treino fica muito mais lento e 'cabe' "
                "sem caber. Conferir 'Memória compartilhada da GPU' no Gerenciador de Tarefas; reduzir "
                "--max-len, depois --r, depois o modelo.")
    return None


def linha_log(*, modelo: str, r: int, epochs: float, lr: float, max_len: int, dado: str, n: int,
              loss_final: float | None, vram_gb: float, minutos: float, out: str) -> str:
    """Linha de experiments/log.md com o carimbo da rodada (n eval e baseline ficam para o comparar)."""
    loss = f"{loss_final:.3f}" if loss_final is not None else "?"
    return (f"| AAAA-MM-DD | B | {modelo} + QLoRA r={r}, {epochs:g} ep, lr {lr:g}, seq {max_len} | "
            f"{dado} (n treino={n}, n eval=?) | loss final {loss}; VRAM pico {vram_gb:.1f} GB; {minutos:.1f} min | "
            f"few-shot no Ollama: ... | ... | `{out}` |")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", help="JSONL instruction/input/output (obrigatório, exceto com --modelfile)")
    ap.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct",
                    help="; ".join(f"{k} ({v})" for k, v in MODELOS_SUGERIDOS.items()))
    ap.add_argument("--out", default="outputs/lora-adapter")
    ap.add_argument("--epochs", type=float, default=2)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--r", type=int, default=16, help="rank do LoRA (8-32; maior = mais capacidade e VRAM)")
    ap.add_argument("--max-len", type=int, default=1024)
    ap.add_argument("--batch", type=int, default=1)
    ap.add_argument("--grad-accum", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true", help="só valida dataset e imprime o plano")
    ap.add_argument("--modelfile", metavar="GGUF",
                    help="não treina: grava <nome>.Modelfile ao lado deste .gguf, com TEMPLATE e stop "
                         "derivados do formato do treino")
    ap.add_argument("--adapter", help="pasta do adapter, para ler o eos_token (padrão: --out)")
    ap.add_argument("--eos", help="eos_token explícito (pula a leitura do adapter)")
    a = ap.parse_args(argv)

    if a.modelfile:
        gguf = Path(a.modelfile)
        eos = a.eos or eos_do_adapter(Path(a.adapter or a.out))
        destino = gguf.with_suffix(".Modelfile")  # um por GGUF: Q8_0 e Q4_K_M na mesma pasta não se sobrescrevem
        destino.write_text(gerar_modelfile(gguf.name, eos), encoding="utf-8")
        print(f"Modelfile gravado em {destino} (eos={eos!r})")
        print(f"próximo: ollama create <nome> -f {destino}   e rodar o teste de concordância peft x GGUF")
        return 0
    if not a.data:
        ap.error("--data é obrigatório (exceto com --modelfile)")

    linhas = [json.loads(l) for l in Path(a.data).read_text(encoding="utf-8").splitlines() if l.strip()]
    faltando = [i for i, ex in enumerate(linhas) if not (ex.get("instruction") and ex.get("output"))]
    if faltando:
        print(f"ERRO: {len(faltando)} exemplos sem instruction/output (ex.: linhas {faltando[:5]})")
        return 2
    print(f"dataset: {len(linhas)} exemplos  modelo: {a.model}  r={a.r}  epochs={a.epochs}  "
          f"batch efetivo={a.batch * a.grad_accum}")
    if len(linhas) < 100:
        print("AVISO: menos de 100 exemplos; o adapter vai decorar, não aprender.")
    if a.dry_run:
        print("exemplo formatado:\n" + _formatar(linhas[0])[:600])
        return 0

    try:
        import torch
        from datasets import Dataset
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        from transformers import (AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig,
                                  DataCollatorForLanguageModeling, Trainer, TrainingArguments)
    except ImportError as e:
        print(f"ERRO: stack de fine-tuning não instalada ({e}). Rode .\\setup.ps1 -Llm")
        return 2
    if not torch.cuda.is_available():
        print("ERRO: CUDA indisponível; QLoRA em CPU é inviável.")
        return 2

    tok = AutoTokenizer.from_pretrained(a.model)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
        print("AVISO: tokenizer sem pad próprio; pad=eos. O DataCollatorForLanguageModeling mascara os "
              "tokens de pad no label, então o EOS também sai do label e o modelo pode não aprender a "
              "PARAR (Llama-3.2 cai aqui; Qwen2.5 tem pad próprio). Conferir no comparar se a saída termina.")
    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.float16, bnb_4bit_use_double_quant=True)
    model = AutoModelForCausalLM.from_pretrained(a.model, quantization_config=bnb, device_map={"": 0})
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)
    lcfg = LoraConfig(r=a.r, lora_alpha=2 * a.r, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"])
    model = get_peft_model(model, lcfg)
    model.print_trainable_parameters()

    ds = Dataset.from_list([{"text": _formatar(ex) + tok.eos_token} for ex in linhas])
    ds = ds.map(lambda b: tok(b["text"], truncation=True, max_length=a.max_len), batched=True,
                remove_columns=["text"])

    args = TrainingArguments(
        output_dir=a.out, num_train_epochs=a.epochs, learning_rate=a.lr,
        per_device_train_batch_size=a.batch, gradient_accumulation_steps=a.grad_accum,
        fp16=True, logging_steps=10, save_strategy="epoch", report_to=[],
        optim="paged_adamw_8bit", warmup_ratio=0.03, lr_scheduler_type="cosine",
        gradient_checkpointing=True,
    )
    tr = Trainer(model=model, args=args, train_dataset=ds,
                 data_collator=DataCollatorForLanguageModeling(tok, mlm=False))
    t0 = time.time()
    tr.train()
    minutos = (time.time() - t0) / 60
    model.save_pretrained(a.out)
    tok.save_pretrained(a.out)
    # reserved (não allocated): é o que o driver de fato segurou, mais perto do que o nvidia-smi mostra
    vram = torch.cuda.max_memory_reserved() / 2**30
    total = torch.cuda.get_device_properties(0).total_memory / 2**30
    perdas = [h["loss"] for h in tr.state.log_history if "loss" in h]
    print(f"\nadapter salvo em {a.out}  tempo {minutos:.1f} min  VRAM pico (reservada) {vram:.1f} de {total:.1f} GB")
    if (msg := aviso_vram(vram, total)):
        print(msg)
    print("\nlinha para experiments/log.md:")
    print(linha_log(modelo=a.model, r=a.r, epochs=a.epochs, lr=a.lr, max_len=a.max_len, dado=Path(a.data).name,
                    n=len(linhas), loss_final=perdas[-1] if perdas else None, vram_gb=vram, minutos=minutos,
                    out=a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
