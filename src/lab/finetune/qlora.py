"""QLoRA em modelo pequeno (1,5B–3B) que cabe em 6 GB de VRAM.

O que está acontecendo, em uma frase cada:
- **Quantização 4-bit (bitsandbytes NF4)**: os pesos do modelo base ficam em 4 bits em vez de
  16. Um 3B passa de ~6 GB para ~2 GB. Sem isso não cabe na 4050.
- **LoRA**: em vez de treinar os bilhões de pesos, congela o modelo e treina duas matrizes
  pequenas (rank r) por camada de atenção. Treina 0,5–2% dos parâmetros; o adapter final tem
  dezenas de MB.
- **QLoRA** = os dois juntos: base congelada em 4-bit + adapters LoRA em 16-bit.
- **Gradient checkpointing**: troca compute por memória (recomputa ativações no backward).
  Mais lento, mas é o que faz caber com sequência de 1024 tokens.

Dataset: JSONL com {"instruction": ..., "input": ..., "output": ...} por linha. Comece com
200–500 exemplos BONS; qualidade importa mais que volume.

Uso:
    python -m lab.finetune.qlora --data data/processed/instrucoes.jsonl --out outputs/lora-qwen3b
    python -m lab.finetune.qlora --data ... --model Qwen/Qwen2.5-1.5B-Instruct --epochs 2

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
    # cabem em 6 GB com QLoRA, seq 1024, batch 1-2, grad_accum 8
    "Qwen/Qwen2.5-1.5B-Instruct": "mais folga; bom pra começar",
    "Qwen/Qwen2.5-3B-Instruct": "limite confortável da 4050",
    "meta-llama/Llama-3.2-3B-Instruct": "gated no HF; precisa aceitar licença",
}


def _formatar(ex: dict) -> str:
    """Formato simples instruction/input/output. Para chat real, usar o chat_template do tokenizer."""
    inp = f"\n\n### Entrada:\n{ex['input']}" if ex.get("input") else ""
    return f"### Instrução:\n{ex['instruction']}{inp}\n\n### Resposta:\n{ex['output']}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True, help="JSONL instruction/input/output")
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
    a = ap.parse_args(argv)

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
    tok.pad_token = tok.pad_token or tok.eos_token
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
    model.save_pretrained(a.out)
    tok.save_pretrained(a.out)
    vram = torch.cuda.max_memory_allocated() / 2**30
    print(f"\nadapter salvo em {a.out}  tempo {(time.time() - t0) / 60:.1f} min  VRAM pico {vram:.1f} GB")
    print("\nlinha para experiments/log.md:")
    print(f"| AAAA-MM-DD | B | {a.model} + LoRA r={a.r} | {Path(a.data).name} (n={len(linhas)}) | loss final ver log | few-shot: ... | ... | `{a.out}` |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
