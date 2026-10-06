"""Ferramentas que o agente local pode chamar. Tudo confinado a uma pasta-raiz (sandbox).

Por que confinar? O modelo de 8B erra caminho, inventa arquivo e às vezes tenta "limpar" coisas.
Cada ferramenta valida que o caminho resolvido está DENTRO de `SANDBOX` antes de tocar no disco.

Modelo de ameaça (vale para o arquivo todo): o risco aqui é ERRO de um modelo 8B (caminho
errado, "limpeza" exagerada, `pip install` que ninguém pediu), não um atacante. As guardas
abaixo pegam o erro comum; não são isolamento de segurança contra código feito para escapar.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

SANDBOX = Path(os.environ.get("AGENT_SANDBOX", Path.cwd() / "outputs" / "agent_sandbox")).resolve()
SANDBOX.mkdir(parents=True, exist_ok=True)

# Tetos fixos no código. O modelo não sobe nenhum deles: argumento fora do schema é descartado
# em `executar`, e mesmo chamando a função direto o valor é cortado aqui.
TETO_CHARS = 4000        # saída de ferramenta: o 8B perde o fio com resposta longa
TETO_TIMEOUT_S = 60      # rodar_python
TETO_ITENS = 200         # listar_pasta


def _dentro(rel: str) -> Path:
    p = (SANDBOX / rel).resolve()
    if SANDBOX != p and SANDBOX not in p.parents:
        raise PermissionError(f"caminho fora do sandbox: {rel}")
    return p


def _cortar(txt: str, teto: int = TETO_CHARS) -> str:
    return txt if len(txt) <= teto else txt[:teto] + "\n...(truncado)"


def listar_pasta(caminho: str = ".") -> str:
    p = _dentro(caminho)
    if not p.exists():
        return f"(não existe: {caminho})"
    if p.is_file():
        return f"f {p.relative_to(SANDBOX)}"
    itens = sorted(p.iterdir())
    linhas = [f"{'d' if i.is_dir() else 'f'} {i.relative_to(SANDBOX)}" for i in itens[:TETO_ITENS]]
    if len(itens) > TETO_ITENS:
        linhas.append(f"... (+{len(itens) - TETO_ITENS} itens não mostrados)")
    return _cortar("\n".join(linhas)) or "(vazio)"


def ler_arquivo(caminho: str, max_chars: int = TETO_CHARS) -> str:
    max_chars = max(1, min(int(max_chars), TETO_CHARS))
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


# Prelúdio que roda no processo filho ANTES do código do modelo. Instala um audit hook
# (PEP 578): o CPython avisa o hook antes de abrir arquivo, apagar, renomear, abrir socket,
# criar processo; o hook levanta PermissionError e a operação não acontece. O código do
# modelo chega pelo stdin (sem limite de linha de comando nem problema de aspas).
_PRELUDIO = r'''
import os, sys, threading
_SB_REAL = os.path.realpath(sys.argv[1])
_SB = os.path.normcase(_SB_REAL)
_LIVRES = {os.path.normcase(os.path.realpath(os.devnull))}
_codigo = sys.stdin.read()
sys.stdin = open(os.devnull, encoding="utf-8")
sys.argv[:] = ["<agente>"]
sys.path.insert(0, _SB_REAL)   # -I tira o cwd do sys.path; o modelo pode importar o que gravou

# rede e processo: bloqueio total
_BLOQ = {"subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.startfile",
         "os.fork", "os.forkpty", "os.kill", "os.killpg", "_winapi.CreateProcess",
         "_winapi.TerminateProcess", "winreg.CreateKey", "winreg.DeleteKey", "winreg.DeleteValue",
         "winreg.SetValue", "winreg.SaveKey", "winreg.LoadKey"}
_LIBERADOS = {"socket.gethostname"}   # local, e platform.machine() chama
# evento -> posição dos argumentos que são caminho de destino (tem que estar no sandbox)
_CAMINHOS = {"os.remove": (0,), "os.rmdir": (0,), "os.rename": (0, 1), "os.mkdir": (0,),
             "os.chmod": (0,), "os.chown": (0,), "os.truncate": (0,), "os.utime": (0,),
             "os.link": (1,), "os.symlink": (1,), "shutil.rmtree": (0,), "shutil.copyfile": (1,),
             "shutil.copymode": (1,), "shutil.copystat": (1,), "shutil.copytree": (1,),
             "shutil.chown": (0,), "shutil.make_archive": (0,), "shutil.unpack_archive": (1,),
             "sqlite3.connect": (0,)}
_FLAGS_ESCRITA = os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC

def _dentro(p):
    if p is None or isinstance(p, int):          # descritor já aberto
        return True
    try:
        s = os.fsdecode(p)
        if s in ("", ":memory:"):
            return True
        r = os.path.normcase(os.path.realpath(s))   # resolve .., symlink e junction
        return r in _LIVRES or os.path.commonpath([_SB, r]) == _SB
    except (TypeError, ValueError, OSError):        # drive diferente, tipo estranho: fora
        return False

def _escreve(modo, flags):
    if isinstance(modo, str):
        return any(c in modo for c in "wax+")
    return isinstance(flags, int) and bool(flags & _FLAGS_ESCRITA)

def _checar(ev, args):
    if (ev in _BLOQ or ev.startswith("socket.")) and ev not in _LIBERADOS:
        raise PermissionError(f"[guarda do lab] {ev} bloqueado: rodar_python não acessa rede nem cria processo")
    if ev == "open":
        p, modo, flags = (tuple(args) + (None, None, None))[:3]
        if _escreve(modo, flags) and not _dentro(p):
            raise PermissionError(f"[guarda do lab] escrita fora do sandbox bloqueada: {p}")
        return
    for i in _CAMINHOS.get(ev, ()):
        if i < len(args) and not _dentro(args[i]):
            raise PermissionError(f"[guarda do lab] {ev} fora do sandbox bloqueado: {args[i]}")

_tl = threading.local()
def _hook(ev, args):
    if getattr(_tl, "ocupado", False):           # o próprio hook (realpath) não reentra
        return
    _tl.ocupado = True
    try:
        _checar(ev, args)
    finally:
        _tl.ocupado = False

sys.addaudithook(_hook)
try:
    exec(compile(_codigo, "<agente>", "exec"), {"__name__": "__main__", "__builtins__": __builtins__})
except SystemExit:
    raise
except BaseException as _e:
    import traceback
    traceback.print_exception(type(_e), _e, _e.__traceback__.tb_next)   # sem o frame do prelúdio
    sys.exit(1)
'''


def rodar_python(codigo: str, timeout_s: int = 30) -> str:
    """Executa um trecho Python num processo filho, cwd = sandbox, com uma GUARDA CONTRA ERRO.

    O filho roda `python -I -B -X utf8` (sem PYTHONPATH/site do usuário, sem .pyc, UTF-8) e,
    antes do código do modelo, instala um audit hook que levanta PermissionError em:
      - escrita fora do sandbox: `open` em modo w/a/x/+ (ou flags de escrita em `os.open`);
      - apagar/renomear/criar/alterar fora do sandbox: os.remove/unlink, os.rmdir, os.rename/
        replace, os.mkdir, os.chmod, os.utime, os.truncate, os.link/symlink, shutil.rmtree,
        shutil.copyfile/copytree/make_archive/unpack_archive, sqlite3.connect (arquivo);
      - rede: qualquer evento `socket.*` (exceto gethostname), o que cobre urllib/requests/http;
      - processo: subprocess, os.system, os.exec*/spawn*, os.startfile (inclui webbrowser), kill;
      - escrita no registro do Windows (winreg).
    Leitura fora do sandbox continua LIVRE. Também: stdin vazio, timeout com teto
    `TETO_TIMEOUT_S`, saída cortada em `TETO_CHARS`.

    Isto NÃO é isolamento de segurança: o processo tem os direitos do usuário, e código feito
    para escapar escapa (ctypes, extensão em C que abre arquivo sem passar pelo `open` do
    Python, p.ex. pyarrow/h5py). Serve para pegar o erro de um modelo 8B; não expor a terceiros.
    """
    timeout_s = max(1, min(int(timeout_s), TETO_TIMEOUT_S))
    try:
        r = subprocess.run(
            [sys.executable, "-I", "-B", "-X", "utf8", "-c", _PRELUDIO, str(SANDBOX)],
            input=codigo, capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout_s, cwd=SANDBOX,
        )
    except subprocess.TimeoutExpired:
        return f"(timeout após {timeout_s}s)"
    out = (r.stdout or "") + (("\n[stderr]\n" + r.stderr) if r.stderr else "")
    if len(out) > TETO_CHARS:  # o fim (erro, resultado final) importa mais que o começo
        out = "...(truncado)\n" + out[-TETO_CHARS:]
    return out or "(sem saída)"


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


def executar(nome: str, args: Any) -> str:
    """Chama a ferramenta com SÓ os argumentos que o schema declara.

    Por quê: o modelo às vezes inventa argumento (`max_chars=10**9`, `timeout_s=99999`) e,
    repassado cru com `fn(**args)`, isso mudava o comportamento da função. Argumento fora das
    `properties` é descartado e o descarte é avisado no resultado, para o modelo ver.
    """
    if nome not in REGISTRO:
        return f"(ferramenta desconhecida: {nome})"
    fn, schema = REGISTRO[nome]
    if not isinstance(args, dict):
        return f"(argumentos inválidos para {nome}: esperado objeto JSON, veio {type(args).__name__})"
    props = schema["function"]["parameters"].get("properties", {})
    aceitos = {k: v for k, v in args.items() if k in props}
    ignorados = sorted(str(k) for k in args if k not in props)
    try:
        out = _cortar(str(fn(**aceitos)), TETO_CHARS + 100)  # rede de segurança; cada fn já corta
    except TypeError as e:
        out = f"(argumentos inválidos para {nome}: {e})"
    except PermissionError as e:
        out = f"(bloqueado: {e})"
    except Exception as e:  # noqa: BLE001
        out = f"(erro em {nome}: {type(e).__name__}: {e})"
    if ignorados:
        out += f"\n[aviso: argumento(s) fora do schema ignorado(s): {', '.join(ignorados)}]"
    return out
