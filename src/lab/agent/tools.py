"""Ferramentas que o agente local pode chamar. Tudo confinado a uma pasta-raiz (sandbox).

Por que confinar? O modelo de 8B erra caminho, inventa arquivo e às vezes tenta "limpar" coisas.
Cada ferramenta valida que o caminho resolvido está DENTRO de `SANDBOX` antes de tocar no disco.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

SANDBOX = Path(os.environ.get("AGENT_SANDBOX", Path.cwd() / "outputs" / "agent_sandbox")).resolve()
SANDBOX.mkdir(parents=True, exist_ok=True)


def _dentro(rel: str) -> Path:
    p = (SANDBOX / rel).resolve()
    if SANDBOX != p and SANDBOX not in p.parents:
        raise PermissionError(f"caminho fora do sandbox: {rel}")
    return p


def listar_pasta(caminho: str = ".") -> str:
    p = _dentro(caminho)
    if not p.exists():
        return f"(não existe: {caminho})"
    itens = sorted(p.iterdir())
    return "\n".join(f"{'d' if i.is_dir() else 'f'} {i.relative_to(SANDBOX)}" for i in itens) or "(vazio)"


def ler_arquivo(caminho: str, max_chars: int = 4000) -> str:
    p = _dentro(caminho)
    if not p.is_file():
        return f"(arquivo não existe: {caminho})"
    txt = p.read_text(encoding="utf-8", errors="replace")
    return txt[:max_chars] + ("\n...(truncado)" if len(txt) > max_chars else "")


def escrever_arquivo(caminho: str, conteudo: str) -> str:
    p = _dentro(caminho)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(conteudo, encoding="utf-8")
    return f"gravado {p.relative_to(SANDBOX)} ({len(conteudo)} chars)"


def rodar_python(codigo: str, timeout_s: int = 30) -> str:
    """Executa um trecho Python num subprocesso, com cwd no sandbox. Sem rede, sem sudo.

    Não é isolamento de segurança de verdade (o processo tem os mesmos direitos do usuário).
    Serve para o laboratório; não expor isso a terceiros.
    """
    try:
        r = subprocess.run(
            [sys.executable, "-c", codigo], capture_output=True, text=True,
            timeout=timeout_s, cwd=SANDBOX,
        )
    except subprocess.TimeoutExpired:
        return f"(timeout após {timeout_s}s)"
    out = (r.stdout or "") + (("\n[stderr]\n" + r.stderr) if r.stderr else "")
    return out[-4000:] or "(sem saída)"


# Registro: nome -> (função, schema no formato OpenAI/Ollama)
REGISTRO: dict[str, tuple[Callable[..., str], dict[str, Any]]] = {
    "listar_pasta": (listar_pasta, {
        "type": "function",
        "function": {
            "name": "listar_pasta",
            "description": "Lista arquivos e pastas dentro do sandbox. Use '.' para a raiz.",
            "parameters": {"type": "object", "properties": {
                "caminho": {"type": "string", "description": "caminho relativo ao sandbox"}},
                "required": []},
        },
    }),
    "ler_arquivo": (ler_arquivo, {
        "type": "function",
        "function": {
            "name": "ler_arquivo",
            "description": "Lê um arquivo de texto do sandbox.",
            "parameters": {"type": "object", "properties": {
                "caminho": {"type": "string"}}, "required": ["caminho"]},
        },
    }),
    "escrever_arquivo": (escrever_arquivo, {
        "type": "function",
        "function": {
            "name": "escrever_arquivo",
            "description": "Cria ou sobrescreve um arquivo de texto no sandbox.",
            "parameters": {"type": "object", "properties": {
                "caminho": {"type": "string"}, "conteudo": {"type": "string"}},
                "required": ["caminho", "conteudo"]},
        },
    }),
    "rodar_python": (rodar_python, {
        "type": "function",
        "function": {
            "name": "rodar_python",
            "description": "Executa código Python e devolve stdout/stderr. cwd = sandbox.",
            "parameters": {"type": "object", "properties": {
                "codigo": {"type": "string"}}, "required": ["codigo"]},
        },
    }),
}


def schemas() -> list[dict[str, Any]]:
    return [s for _, s in REGISTRO.values()]


def executar(nome: str, args: dict[str, Any]) -> str:
    if nome not in REGISTRO:
        return f"(ferramenta desconhecida: {nome})"
    fn, _ = REGISTRO[nome]
    try:
        return fn(**args)
    except TypeError as e:
        return f"(argumentos inválidos para {nome}: {e})"
    except PermissionError as e:
        return f"(bloqueado: {e})"
    except Exception as e:  # noqa: BLE001
        return f"(erro em {nome}: {type(e).__name__}: {e})"
