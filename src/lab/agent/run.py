"""Agente local: modelo do Ollama + loop de ferramentas.

O que é um "agente" aqui: um loop. Manda a tarefa ao modelo junto com a lista de ferramentas;
se o modelo responde com `tool_calls`, executa cada uma, devolve o resultado como mensagem
`role=tool` e chama o modelo de novo. Para quando o modelo responde sem tool_calls ou quando
estoura o limite de passos. É exatamente o que o Claude Code faz, só que com modelo de 8B.

Uso:
    python -m lab.agent.run "crie um arquivo nomes.txt com 5 nomes de cafés"
    python -m lab.agent.run --model llama3.1:8b --max-steps 6 "liste o sandbox e resuma"

Tudo que o agente toca fica em outputs/agent_sandbox/ (ver tools.py).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any

from lab.ollama_client import MODEL, OllamaError, chat_messages
from lab.agent import tools

SYSTEM = """Você é um agente que executa tarefas usando ferramentas.
Regras:
- Use as ferramentas para AGIR; não descreva o que faria, faça.
- Caminhos são relativos ao sandbox. Não invente conteúdo de arquivo: leia antes de afirmar.
- Quando a tarefa estiver concluída, responda em 1-3 frases o que foi feito, sem chamar ferramenta.
- Se algo falhar, tente uma correção; se falhar de novo, explique o erro e pare."""

# Regra 4 do agente: loop sem teto vira modelo repetindo a mesma chamada por minutos.
TETO_PASSOS = 30


def rodar(tarefa: str, model: str = MODEL, max_steps: int = 8, verbose: bool = True,
          think: bool | None = False) -> dict[str, Any]:
    max_steps = max(1, min(int(max_steps), TETO_PASSOS))
    msgs: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": tarefa},
    ]
    chamadas = 0
    t0 = time.time()
    for passo in range(1, max_steps + 1):
        msg = chat_messages(msgs, model=model, tools=tools.schemas(), think=think)
        calls = msg.get("tool_calls") or []
        msgs.append({"role": "assistant", "content": msg.get("content", ""), "tool_calls": calls})
        if not calls:
            if verbose:
                print(f"\n[{model}] final em {passo} passo(s), {chamadas} chamada(s), {time.time() - t0:.1f}s")
            return {"resposta": msg.get("content", ""), "passos": passo, "chamadas": chamadas,
                    "segundos": round(time.time() - t0, 1), "esgotou": False}
        for c in calls:
            fn = c.get("function", {})
            nome, args = fn.get("name"), fn.get("arguments") or {}
            if isinstance(args, str):  # alguns modelos mandam string JSON
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    pass  # fica string: `executar` devolve "argumentos inválidos" e o modelo vê
            chamadas += 1
            resultado = tools.executar(nome, args)
            if verbose:
                print(f"[{passo}] {nome}({json.dumps(args, ensure_ascii=False)[:120]}) -> {resultado[:160]!r}")
            msgs.append({"role": "tool", "content": resultado, "tool_name": nome})
    if verbose:
        print(f"\n[{model}] esgotou {max_steps} passos")
    return {"resposta": msgs[-1].get("content", ""), "passos": max_steps, "chamadas": chamadas,
            "segundos": round(time.time() - t0, 1), "esgotou": True}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tarefa", nargs="+")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--max-steps", type=int, default=8)
    ap.add_argument("--think", action="store_true", help="deixa o modelo 'pensar' (mais lento)")
    a = ap.parse_args(argv)
    print(f"sandbox: {tools.SANDBOX}")
    try:
        r = rodar(" ".join(a.tarefa), model=a.model, max_steps=a.max_steps, think=True if a.think else False)
    except OllamaError as e:
        print(f"\n[erro do Ollama] {e}")
        return 2
    print("\n" + (r["resposta"] or "(sem resposta final)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
