"""Mede velocidade de leitura (prompt) e escrita (geração) de um servidor de LLM local.

Compara Ollama e llama-server (llama.cpp) com o MESMO modelo e o MESMO texto.
Cada repetição começa com um código aleatório para impedir que o servidor reaproveite a
leitura anterior (cache de prompt) — senão a 2ª rodada mede o cache, não o modelo.

Uso:
    python scripts/bench_servidor.py ollama --reps 3
    python scripts/bench_servidor.py llamacpp --url http://localhost:8080 --reps 3 --rotulo "n-cpu-moe 48"
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
import uuid
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[1]


def texto_longo(alvo_chars: int) -> str:
    # fonte fixa e versionada: o código do próprio lab, repetido até o tamanho-alvo
    partes = [p.read_text(encoding="utf-8") for p in sorted((RAIZ / "src").rglob("*.py"))]
    base = "\n\n".join(partes)
    return (base * (alvo_chars // len(base) + 1))[:alvo_chars]


def vram_mib() -> int:
    out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True).stdout.strip()
    return int(out.splitlines()[0])


def mensagens(alvo_chars: int) -> list[dict]:
    return [{"role": "user", "content": f"[{uuid.uuid4()}]\n" + texto_longo(alvo_chars)
             + "\n\nResuma o código acima em 10 tópicos detalhados."}]


def rodar_ollama(msgs, modelo, n_out):
    r = requests.post("http://localhost:11434/api/chat", timeout=1800, json={
        "model": modelo, "messages": msgs, "stream": False, "think": False,
        "options": {"num_ctx": 32768, "num_predict": n_out, "temperature": 0}}).json()
    return (r["prompt_eval_count"], r["prompt_eval_duration"] / 1e9,
            r["eval_count"], r["eval_duration"] / 1e9)


def rodar_llamacpp(msgs, url, n_out):
    r = requests.post(f"{url}/v1/chat/completions", timeout=1800, json={
        "messages": msgs, "max_tokens": n_out, "temperature": 0, "cache_prompt": False}).json()
    t = r["timings"]
    return t["prompt_n"], t["prompt_ms"] / 1e3, t["predicted_n"], t["predicted_ms"] / 1e3


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("lado", choices=["ollama", "llamacpp"])
    ap.add_argument("--modelo", default="qwen3-coder:30b")
    ap.add_argument("--url", default="http://localhost:8080")
    ap.add_argument("--chars", type=int, default=55000, help="~16k tokens de código")
    ap.add_argument("--saida", type=int, default=256)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--rotulo", default="")
    a = ap.parse_args()

    linhas = []
    for i in range(a.reps):
        msgs = mensagens(a.chars)
        t0 = time.time()
        if a.lado == "ollama":
            pn, ps, gn, gs = rodar_ollama(msgs, a.modelo, a.saida)
        else:
            pn, ps, gn, gs = rodar_llamacpp(msgs, a.url, a.saida)
        linha = {"lado": a.lado, "rotulo": a.rotulo, "rep": i + 1, "prompt_tokens": pn,
                 "prompt_tok_s": round(pn / ps, 1), "gen_tokens": gn, "gen_tok_s": round(gn / gs, 1),
                 "total_s": round(time.time() - t0, 1), "vram_mib": vram_mib()}
        print(json.dumps(linha, ensure_ascii=False), flush=True)
        linhas.append(linha)
    med = lambda k: sorted(l[k] for l in linhas)[len(linhas) // 2]  # noqa: E731
    print(f"MEDIANA {a.lado} {a.rotulo}: prompt {med('prompt_tok_s')} tok/s | "
          f"geração {med('gen_tok_s')} tok/s | total {med('total_s')} s | VRAM {med('vram_mib')} MiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
