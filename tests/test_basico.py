"""Testes que rodam sem GPU e sem Ollama: sandbox das ferramentas, baseline tabular, parser do QLoRA."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    # nome "agent_sandbox": o avaliador só aceita apagar pasta com esse nome
    monkeypatch.setenv("AGENT_SANDBOX", str(tmp_path / "agent_sandbox"))
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
    # timeout_s não está no schema: o modelo não escolhe; o teste chama a função direto
    assert "timeout" in sandbox.rodar_python("import time;time.sleep(5)", timeout_s=1)


# --- guarda do rodar_python (cada teste fica vermelho se a guarda correspondente sair) ---

def test_rodar_python_bloqueia_escrita_fora_do_sandbox(sandbox, tmp_path):
    alvo = tmp_path / "fora.txt"                      # irmão do sandbox, fora dele
    vitima = tmp_path / "vitima.txt"
    vitima.write_text("intacto", encoding="utf-8")
    out = sandbox.rodar_python(
        f"open(r'{alvo}', 'w').write('x')\n")
    assert "escrita fora do sandbox bloqueada" in out
    assert not alvo.exists()
    out = sandbox.rodar_python("from pathlib import Path\nPath('../fora.txt').write_text('x')\n")
    assert "PermissionError" in out and not alvo.exists()
    out = sandbox.rodar_python(f"import os\nos.remove(r'{vitima}')\n")
    assert "bloqueado" in out and vitima.read_text(encoding="utf-8") == "intacto"
    out = sandbox.rodar_python(f"import shutil\nshutil.rmtree(r'{tmp_path}')\n")
    assert "bloqueado" in out and vitima.exists()


def test_rodar_python_bloqueia_rede_e_processo(sandbox):
    out = sandbox.rodar_python(
        "import socket\n"
        "try:\n    socket.socket(); print('ABRIU')\n"
        "except PermissionError as e:\n    print('NEGADO', e)\n")
    assert "NEGADO" in out and "ABRIU" not in out
    out = sandbox.rodar_python(
        "import subprocess, sys\n"
        "try:\n    subprocess.run([sys.executable, '-c', 'print(1)']); print('RODOU')\n"
        "except PermissionError as e:\n    print('NEGADO', e)\n")
    assert "NEGADO" in out and "RODOU" not in out


def test_rodar_python_permite_trabalho_dentro_do_sandbox(sandbox):
    out = sandbox.rodar_python(
        "import os, shutil\n"
        "open('a.txt', 'w').write('Café com ação')\n"
        "os.makedirs('sub/x')\n"
        "os.rename('a.txt', 'sub/a.txt')\n"
        "shutil.rmtree('sub/x')\n"
        "print(sorted(os.listdir('sub')))\n")
    assert out.strip() == "['a.txt']", out
    # UTF-8 dos dois lados: o que o código grava, ler_arquivo lê igual
    assert sandbox.ler_arquivo("sub/a.txt") == "Café com ação"


def test_tetos_de_argumento_nao_sobem(sandbox, monkeypatch):
    (sandbox.SANDBOX / "grande.txt").write_text("x" * 20_000, encoding="utf-8")
    # via executar: argumento fora do schema é descartado e avisado
    out = sandbox.executar("ler_arquivo", {"caminho": "grande.txt", "max_chars": 10**9})
    assert len(out) < sandbox.TETO_CHARS + 200
    assert "ignorado" in out and "max_chars" in out
    # argumento inventado que a função nem aceita: sem o filtro seria TypeError
    out = sandbox.executar("listar_pasta", {"caminho": ".", "recursivo": True})
    assert "grande.txt" in out and "argumentos inválidos" not in out and "recursivo" in out
    # chamando a função direto: o teto vale do mesmo jeito
    assert len(sandbox.ler_arquivo("grande.txt", max_chars=10**9)) <= sandbox.TETO_CHARS + 20
    monkeypatch.setattr(sandbox, "TETO_TIMEOUT_S", 1)
    assert "timeout após 1s" in sandbox.rodar_python("import time;time.sleep(5)", timeout_s=10**6)


def test_listar_pasta_corta_itens_e_args_invalidos(sandbox):
    for i in range(sandbox.TETO_ITENS + 50):
        (sandbox.SANDBOX / f"f{i:04d}.txt").write_text("", encoding="utf-8")
    out = sandbox.executar("listar_pasta", {"caminho": "."})
    assert len(out.splitlines()) == sandbox.TETO_ITENS + 1
    assert "+50 itens" in out
    assert "argumentos inválidos" in sandbox.executar("ler_arquivo", "isto não é json")


def test_avaliar_recusa_rmtree_fora_de_agent_sandbox(sandbox, tmp_path, monkeypatch):
    from lab.agent import avaliar
    qualquer = tmp_path / "qualquer"
    qualquer.mkdir()
    (qualquer / "importante.txt").write_text("não apagar", encoding="utf-8")
    monkeypatch.setattr(sandbox, "SANDBOX", qualquer)
    with pytest.raises(RuntimeError, match="recuso apagar"):
        avaliar._zerar_sandbox()
    assert (qualquer / "importante.txt").exists()
    chamou = []
    monkeypatch.setattr(avaliar, "rodar", lambda *a, **k: chamou.append(1))
    assert avaliar.main(["--repeticoes", "1"]) == 2       # aborta antes de rodar qualquer tarefa
    assert not chamou and (qualquer / "importante.txt").exists()


def test_avaliar_conta_esgotou_e_imprime_parcial_no_erro(sandbox, monkeypatch, capsys):
    from lab.agent import avaliar
    from lab.ollama_client import OllamaError
    respostas = iter([
        {"segundos": 1.0, "chamadas": 8, "esgotou": True},
        {"segundos": 2.0, "chamadas": 2, "esgotou": False},
        {"segundos": 3.0, "chamadas": 1, "esgotou": False},
    ])

    def falso(*a, **k):
        try:
            return next(respostas)
        except StopIteration:
            raise OllamaError("Ollama não respondeu") from None

    monkeypatch.setattr(avaliar, "rodar", falso)
    assert avaliar.main([]) == 1                     # default 3 repetições; cai na 4ª rodada
    saida = capsys.readouterr().out
    assert "INTERROMPIDO" in saida and "PARCIAL 3 rodadas de 9" in saida
    assert "esgotou max_steps: 1" in saida and "chamadas: 11" in saida


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
