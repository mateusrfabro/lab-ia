"""Compara base × base+adapter nas mesmas perguntas. É o "antes/depois" obrigatório.

Sem isto, não dá pra dizer que o fine-tuning fez algo. Roda um conjunto de prompts de
avaliação (JSONL com {"instruction","input","output"}) nos dois modelos e imprime lado a lado.
Julgamento aqui é humano (você lê); para escala, trocar por uma métrica (exact match,
ROUGE, ou um modelo-juiz).

Uso: python -m lab.finetune.comparar --adapter outputs/lora-adapter --eval data/processed/eval.jsonl --n 5
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def montar_prompts(exs: list[dict]) -> list[str]:
    """Prompt de avaliação = o MESMO texto que o treino viu antes da resposta.

    Antes era `_formatar({..., "output": ""}).rstrip()`: o rstrip cortava o "\\n" depois de
    "### Resposta:", e o modelo era avaliado num prompt que nunca viu no treino.
    """
    from lab.finetune.qlora import formatar_prompt
    return [formatar_prompt(ex) for ex in exs]


def gerar(model, tok, prompt: str, max_new: int = 200) -> str:
    import torch
    ids = tok(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(**ids, max_new_tokens=max_new, do_sample=False, pad_token_id=tok.eos_token_id)
    return tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--eval", required=True)
    ap.add_argument("--n", type=int, default=5)
    a = ap.parse_args(argv)
    try:
        import torch
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    except ImportError as e:
        print(f"ERRO: {e}. Rode .\\setup.ps1 -Llm"); return 2

    cfg = json.loads((Path(a.adapter) / "adapter_config.json").read_text())
    base_nome = cfg["base_model_name_or_path"]
    tok = AutoTokenizer.from_pretrained(a.adapter)
    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.float16)
    base = AutoModelForCausalLM.from_pretrained(base_nome, quantization_config=bnb, device_map={"": 0})
    exs = [json.loads(l) for l in Path(a.eval).read_text(encoding="utf-8").splitlines() if l.strip()][: a.n]

    prompts = montar_prompts(exs)
    antes = [gerar(base, tok, p) for p in prompts]
    tuned = PeftModel.from_pretrained(base, a.adapter)
    depois = [gerar(tuned, tok, p) for p in prompts]

    for ex, b, d in zip(exs, antes, depois):
        print("=" * 80)
        print("PERGUNTA :", ex["instruction"][:200])
        print("ESPERADO :", ex["output"][:200])
        print("BASE     :", b[:200])
        print("AJUSTADO :", d[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
