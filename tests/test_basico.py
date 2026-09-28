"""Testes que rodam sem GPU e sem Ollama: sandbox das ferramentas, baseline tabular, parser do QLoRA."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    monkeypatch.setenv("AGENT_SANDBOX", str(tmp_path / "sb"))
    import importlib
    from lab.agent import tools
    importlib.reload(tools)
    return tools


def test_tools_confinadas_ao_sandbox(sandbox):
    assert "gravado" in sandbox.executar("escrever_arquivo", {"caminho": "a.txt", "conteudo": "oi"})
    assert sandbox.executar("ler_arquivo", {"caminho": "a.txt"}) == "oi"
    assert "a.txt" in sandbox.executar("listar_pasta", {})
    assert "bloqueado" in sandbox.executar("escrever_arquivo", {"caminho": "../fora.txt", "conteudo": "x"})
    assert "bloqueado" in sandbox.executar("ler_arquivo", {"caminho": "C:/Windows/win.ini"})
    assert sandbox.executar("ferramenta_inexistente", {}).startswith("(ferramenta desconhecida")


def test_rodar_python_no_sandbox(sandbox):
    out = sandbox.executar("rodar_python", {"codigo": "print(sum(range(101)))"})
    assert out.strip() == "5050"
    assert "timeout" in sandbox.executar("rodar_python", {"codigo": "import time;time.sleep(5)", "timeout_s": 1})


def test_baseline_recupera_sinal_e_vazamento_infla():
    from lab.tabular.baseline import avaliar
    from lab.tabular.dados_sinteticos import gerar
    df = gerar(1500, seed=1)
    limpo = avaliar(df, "churn", drop=["user_id", "dias_ate_churn"], folds=3)
    vazado = avaliar(df, "churn", drop=["user_id"], folds=3)
    base = limpo.loc[limpo.modelo == "dummy_majoritaria", "auc"].iloc[0]
    assert abs(base - 0.5) < 0.05                       # dummy fica em ~0,5
    assert limpo.auc.max() > 0.65                       # há sinal real nas features honestas
    assert vazado.auc.max() > 0.99                      # a coluna vazada "resolve" o problema (falso)


def test_qlora_dry_run_valida_dataset(tmp_path, capsys):
    from lab.finetune.qlora import main
    p = tmp_path / "d.jsonl"
    p.write_text("\n".join(json.dumps({"instruction": f"q{i}", "output": f"a{i}"}) for i in range(3)), encoding="utf-8")
    assert main(["--data", str(p), "--dry-run"]) == 0
    assert "3 exemplos" in capsys.readouterr().out
    p.write_text(json.dumps({"instruction": "sem output"}), encoding="utf-8")
    assert main(["--data", str(p), "--dry-run"]) == 2
