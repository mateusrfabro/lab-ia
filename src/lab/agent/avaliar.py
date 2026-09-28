"""Avaliação do agente: roda N tarefas com verificador programático e mede taxa de acerto.

Regra 7 do CLAUDE.md: "funcionou uma vez" não é resultado. Isto aqui dá o número.

Uso: python -m lab.agent.avaliar --model qwen3:8b --repeticoes 3
Saída: tabela por tarefa + linha pronta para experiments/log.md
"""
from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from typing import Callable

from lab.agent import tools
from lab.agent.run import rodar
from lab.ollama_client import MODEL


@dataclass
class Tarefa:
    nome: str
    prompt: str
    verificar: Callable[[], bool]


def _t1() -> bool:
    p = tools.SANDBOX / "cafes.txt"
    return p.is_file() and len([l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]) == 5


def _t2() -> bool:
    p = tools.SANDBOX / "soma.txt"
    return p.is_file() and p.read_text(encoding="utf-8").strip() == "5050"


def _t3() -> bool:
    p = tools.SANDBOX / "copia" / "cafes.txt"
    o = tools.SANDBOX / "cafes.txt"
    return p.is_file() and o.is_file() and p.read_text(encoding="utf-8") == o.read_text(encoding="utf-8")


TAREFAS = [
    Tarefa("criar_5_linhas", "Crie o arquivo cafes.txt com exatamente 5 nomes de cafés, um por linha.", _t1),
    Tarefa("calcular_e_gravar", "Calcule a soma de 1 até 100 usando Python e grave só o número em soma.txt.", _t2),
    Tarefa("ler_e_copiar", "Leia cafes.txt e grave uma cópia idêntica em copia/cafes.txt.", _t3),
]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--repeticoes", type=int, default=1)
    a = ap.parse_args(argv)

    linhas = []
    total_ok = total = 0
    for t in TAREFAS:
        ok = 0
        seg = 0.0
        for _ in range(a.repeticoes):
            # tarefas 1 e 2 começam do zero; a 3 depende da 1 existir
            if t.nome != "ler_e_copiar":
                shutil.rmtree(tools.SANDBOX, ignore_errors=True)
                tools.SANDBOX.mkdir(parents=True, exist_ok=True)
            r = rodar(t.prompt, model=a.model, verbose=False)
            seg += r["segundos"]
            if t.verificar():
                ok += 1
        total_ok += ok
        total += a.repeticoes
        linhas.append((t.nome, ok, a.repeticoes, seg / a.repeticoes))

    print(f"\nmodelo: {a.model}")
    print(f"{'tarefa':<20} {'acertos':>8} {'s/med':>7}")
    for nome, ok, n, s in linhas:
        print(f"{nome:<20} {ok:>4}/{n:<3} {s:>7.1f}")
    taxa = total_ok / total if total else 0
    print(f"\ntaxa de acerto: {total_ok}/{total} = {taxa:.0%}")
    print("\nlinha para experiments/log.md:")
    print(f"| AAAA-MM-DD | A | {a.model} | {len(TAREFAS)} tarefas × {a.repeticoes} | acerto {taxa:.0%} | — | ... | `lab.agent.avaliar` |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
