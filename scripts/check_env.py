"""Diagnóstico do ambiente: GPU, torch, Ollama e modelos disponíveis.

Roda sem torch instalado (só avisa). Uso: python scripts/check_env.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys


def _linha(ok: bool | None, rotulo: str, detalhe: str = "") -> None:
    icone = {True: "OK ", False: "ERR", None: "-- "}[ok]
    print(f"[{icone}] {rotulo}: {detalhe}")


def gpu() -> None:
    if not shutil.which("nvidia-smi"):
        _linha(False, "nvidia-smi", "não encontrado no PATH")
        return
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,driver_version",
             "--format=csv,noheader"], text=True, timeout=10).strip()
        _linha(True, "GPU", out)
    except Exception as e:  # noqa: BLE001
        _linha(False, "GPU", str(e))


def torch_info() -> None:
    try:
        import torch  # type: ignore
    except ImportError:
        _linha(None, "torch", "não instalado (rode .\\setup.ps1 -Llm para a trilha B)")
        return
    cuda = torch.cuda.is_available()
    det = f"{torch.__version__}, cuda={cuda}"
    if cuda:
        p = torch.cuda.get_device_properties(0)
        det += f", {p.name}, {p.total_memory / 2**30:.1f} GB"
    _linha(cuda, "torch", det)


def ollama() -> None:
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    try:
        import requests
    except ImportError:
        _linha(False, "requests", "não instalado (rode .\\setup.ps1)")
        return
    try:
        r = requests.get(f"{host}/api/tags", timeout=5)
        r.raise_for_status()
        modelos = r.json().get("models", [])
    except Exception as e:  # noqa: BLE001
        _linha(False, "ollama", f"{host} não respondeu ({e}). Abra o app Ollama ou rode `ollama serve`.")
        return
    _linha(True, "ollama", f"{host}, {len(modelos)} modelos")
    for m in modelos:
        tam = m.get("size") or 0
        # modelo cloud vem com remote_host (ex.: https://ollama.com) e ~300 bytes de manifesto
        cloud = bool(m.get("remote_host")) or m["name"].endswith("-cloud")
        local = "CLOUD (roda fora da máquina)" if cloud else "local"
        print(f"      - {m['name']:<22} {tam / 2**30:5.1f} GB  {local}")


def pacotes() -> None:
    for nome in ("pandas", "sklearn", "xgboost", "lightgbm", "transformers", "peft", "trl", "bitsandbytes"):
        try:
            mod = __import__(nome)
            _linha(True, nome, getattr(mod, "__version__", "?"))
        except ImportError:
            _linha(None, nome, "não instalado")


if __name__ == "__main__":
    try:  # console do Windows em cp1252 quebra acentos
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    print(f"python {sys.version.split()[0]}  ({sys.executable})")
    gpu()
    torch_info()
    ollama()
    pacotes()
