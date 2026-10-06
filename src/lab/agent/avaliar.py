"""Avaliação do agente: roda N tarefas com verificador programático e mede taxa de acerto.

Regra 7 do CLAUDE.md: "funcionou uma vez" não é resultado. Isto aqui dá o número.

Uso: python -m lab.agent.avaliar --model qwen3:8b --repeticoes 3
Saída: tabela por tarefa + linha pronta para experiments/log.md
"""
from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from lab.agent import tools
from lab.agent.run import rodar
from lab.ollama_client import MODEL, OllamaError

# Única pasta que o avaliador aceita apagar. `AGENT_SANDBOX` vem de variável de ambiente: um
# valor errado (".", a home, a raiz do repo) viraria um `rmtree` no lugar errado.
NOME_SANDBOX = "agent_sandbox"


def _checar_sandbox(sandbox: Path | None = None) -> Path:
    sb = Path(sandbox if sandbox is not None else tools.SANDBOX).resolve()
    if sb.name != NOME_SANDBOX or sb.parent == sb:
        raise RuntimeError(
            f"recuso apagar {sb}: o sandbox do avaliador precisa ser uma pasta chamada "
            f"'{NOME_SANDBOX}' (ajuste AGENT_SANDBOX). Nada foi apagado.")
    return sb


def _zerar_sandbox() -> None:
    sb = _checar_sandbox()
    shutil.rmtree(sb, ignore_errors=True)
    sb.mkdir(parents=True, exist_ok=True)


@dataclass
class Tarefa:
    nome: str
    prompt: str
    verificar: Callable[[], bool]
    # estado inicial que a tarefa pressupõe; roda depois de zerar o sandbox
    preparar: Callable[[], None] | None = None


CAFES_FIXTURE = "Espresso\nCappuccino\nMacchiato\nCafé com leite\nCoado\n"


def _prep_cafes() -> None:
    (tools.SANDBOX / "cafes.txt").write_text(CAFES_FIXTURE, encoding="utf-8")


def _t1() -> bool:
    p = tools.SANDBOX / "cafes.txt"
    return p.is_file() and len([l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]) == 5


def _t2() -> bool:
    p = tools.SANDBOX / "soma.txt"
    return p.is_file() and p.read_text(encoding="utf-8").strip() == "5050"


def _t3() -> bool:
    p = tools.SANDBOX / "copia" / "cafes.txt"
    return p.is_file() and p.read_text(encoding="utf-8").strip() == CAFES_FIXTURE.strip()


TAREFAS = [
    Tarefa("criar_5_linhas", "Crie o arquivo cafes.txt com exatamente 5 nomes de cafés, um por linha.", _t1),
    Tarefa("calcular_e_gravar", "Calcule a soma de 1 até 100 usando Python e grave só o número em soma.txt.", _t2),
    Tarefa("ler_e_copiar", "Leia cafes.txt e grave uma cópia idêntica em copia/cafes.txt.", _t3,
           preparar=_prep_cafes),
]


@dataclass
class Placar:
    nome: str
    ok: int = 0
    n: int = 0              # rodadas concluídas (sem erro do Ollama)
    segundos: float = 0.0
    esgotou: int = 0        # rodadas que bateram max_steps sem resposta final
    chamadas: int = 0       # total de chamadas de ferramenta nas n rodadas


def _imprimir(placares: list[Placar], model: str, repeticoes: int, max_steps: int,
              interrompido: str | None) -> None:
    print(f"\nmodelo: {model}  (max_steps={max_steps})")
    print(f"{'tarefa':<20} {'acertos':>8} {'s/med':>7} {'esgotou':>8} {'chamadas':>9}")
    for p in placares:
        s_med = p.segundos / p.n if p.n else 0.0
        print(f"{p.nome:<20} {p.ok:>4}/{p.n:<3} {s_med:>7.1f} {p.esgotou:>8} {p.chamadas:>9}")
    total_ok = sum(p.ok for p in placares)
    total = sum(p.n for p in placares)
    esg = sum(p.esgotou for p in placares)
    cham = sum(p.chamadas for p in placares)
    seg = sum(p.segundos for p in placares)
    taxa = total_ok / total if total else 0
    print(f"\ntaxa de acerto: {total_ok}/{total} = {taxa:.0%}; esgotou max_steps: {esg}; "
          f"chamadas: {cham}")
    if interrompido:
        print(f"\nINTERROMPIDO (parcial, não é a bateria completa): {interrompido}")
    print("\nlinha para experiments/log.md:")
    dado = (f"{len(TAREFAS)} tarefas × {repeticoes}" if not interrompido
            else f"PARCIAL {total} rodadas de {len(TAREFAS) * repeticoes}")
    print(f"| AAAA-MM-DD | A | {model} | {dado} | {total_ok}/{total} = {taxa:.0%}; "
          f"{seg / total if total else 0:.1f} s/tarefa; esgotou {esg}; {cham} chamadas | — | ... "
          f"| `lab.agent.avaliar --repeticoes {repeticoes}` |")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--repeticoes", type=int, default=3,
                    help="mínimo 3: modelo 8B oscila entre execuções, uma rodada não é taxa")
    ap.add_argument("--max-steps", type=int, default=8)
    a = ap.parse_args(argv)

    try:  # antes de qualquer rodada: se o sandbox for suspeito, não roda nada
        _checar_sandbox()
    except RuntimeError as e:
        print(f"[avaliar] {e}")
        return 2

    placares: list[Placar] = []
    interrompido = None
    for t in TAREFAS:
        p = Placar(t.nome)
        placares.append(p)
        for _ in range(a.repeticoes):
            # toda repetição começa do zero + o estado que a tarefa declara. Antes a 3 "dependia
            # da 1", mas a 2 apagava o sandbox no meio: 0/3 forçado, o modelo nunca viu o arquivo.
            _zerar_sandbox()
            if t.preparar:
                t.preparar()
            try:
                r = rodar(t.prompt, model=a.model, max_steps=a.max_steps, verbose=False)
            except OllamaError as e:
                interrompido = f"{t.nome}, rodada {p.n + 1}: {e}"
                break
            p.n += 1
            p.segundos += r["segundos"]
            p.esgotou += int(bool(r.get("esgotou")))
            p.chamadas += int(r.get("chamadas") or 0)
            if t.verificar():
                p.ok += 1
        if interrompido:
            break

    _imprimir(placares, a.model, a.repeticoes, a.max_steps, interrompido)
    return 1 if interrompido else 0


if __name__ == "__main__":
    raise SystemExit(main())
