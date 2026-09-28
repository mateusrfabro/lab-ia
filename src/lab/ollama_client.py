"""Cliente mínimo da API do Ollama (http://localhost:11434), sem SDK.

Por que não usar o pacote `ollama`? Para você ver o que acontece na rede: é só um POST em
/api/chat com uma lista de mensagens. Quando entender, trocar pelo SDK é trivial.

Uso rápido:
    from lab.ollama_client import chat
    print(chat("Explique LoRA em 2 frases")["content"])
"""
from __future__ import annotations

import json
import os
from typing import Any

import requests

HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:8b")


class OllamaError(RuntimeError):
    pass


def listar_modelos() -> list[dict[str, Any]]:
    r = requests.get(f"{HOST}/api/tags", timeout=10)
    r.raise_for_status()
    return r.json().get("models", [])


def chat_messages(
    messages: list[dict[str, Any]],
    model: str = MODEL,
    tools: list[dict[str, Any]] | None = None,
    temperature: float = 0.2,
    num_ctx: int = 8192,
    think: bool | None = None,
    timeout: int = 300,
) -> dict[str, Any]:
    """Uma rodada de /api/chat. Devolve a `message` da resposta (role, content, tool_calls?).

    - `tools`: lista no formato OpenAI (`{"type":"function","function":{...}}`). Só modelos com
      suporte (qwen3, llama3.1, mistral) devolvem `tool_calls`; deepseek-r1 ignora.
    - `num_ctx`: janela de contexto. 8192 cabe em 6 GB com modelo 8B Q4; 32k já estoura.
    - `think`: qwen3 e deepseek-r1 "pensam" antes de responder; False acelera muito tarefas
      simples (o pensamento não vai para a resposta, mas custa tokens e tempo).
    """
    body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature, "num_ctx": num_ctx},
    }
    if tools:
        body["tools"] = tools
    if think is not None:
        body["think"] = think
    try:
        r = requests.post(f"{HOST}/api/chat", json=body, timeout=timeout)
    except requests.ConnectionError as e:
        raise OllamaError(f"Ollama não respondeu em {HOST}. Abra o app ou rode `ollama serve`.") from e
    if r.status_code != 200:
        raise OllamaError(f"HTTP {r.status_code}: {r.text[:300]}")
    data = r.json()
    msg = data.get("message", {})
    # métricas úteis para o log de experimentos (tokens e tempo)
    msg["_eval_count"] = data.get("eval_count")
    msg["_eval_duration_s"] = round((data.get("eval_duration") or 0) / 1e9, 2)
    return msg


def chat(prompt: str, system: str | None = None, **kw: Any) -> dict[str, Any]:
    """Atalho: uma pergunta, uma resposta."""
    msgs: list[dict[str, Any]] = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": prompt})
    return chat_messages(msgs, **kw)


if __name__ == "__main__":
    import sys

    pergunta = " ".join(sys.argv[1:]) or "Responda em uma frase: o que é quantização de um modelo?"
    resp = chat(pergunta, think=False)
    print(resp["content"])
    print(f"\n[{MODEL}] {resp['_eval_count']} tokens em {resp['_eval_duration_s']}s")
    print(json.dumps({k: v for k, v in resp.items() if k.startswith("_")}))
