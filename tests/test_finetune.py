"""Testes da trilha B que não precisam de GPU nem da stack de LLM (torch/transformers).

O foco é a armadilha do template: o Modelfile do Ollama tem de reproduzir, byte a byte, o
prefixo que o modelo viu no treino. Os testes provam que isso DERIVA das mesmas constantes
(e não de uma cópia do texto), então ninguém precisa lembrar de atualizar dois lugares.
"""
from __future__ import annotations

import json
import re

import pytest

from lab.finetune import qlora

EXEMPLOS = [
    {"instruction": "Classifique o ticket.", "output": "categoria: saque"},
    {"instruction": "Resuma.", "input": "texto longo\ncom quebra", "output": "resumo curto"},
]


def _renderizar(tpl: str, prompt: str, response: str = "") -> str:
    """Renderizador mínimo do Go template do Ollama: só as duas ações que o nosso TEMPLATE usa."""
    acoes = re.findall(r"\{\{.*?\}\}", tpl)
    assert acoes == ["{{ .Prompt }}", "{{ .Response }}"], acoes  # nada além disto no template
    return tpl.replace("{{ .Prompt }}", prompt).replace("{{ .Response }}", response)


def _template_do_modelfile(mf: str) -> str:
    m = re.search(r'^TEMPLATE """(.*?)"""$', mf, flags=re.S | re.M)
    assert m, mf
    return m.group(1)


def test_formato_do_treino_nao_mudou():
    # Regressão: o refactor em constantes não pode mudar o texto que o treino sempre usou.
    ex0, ex1 = EXEMPLOS
    assert qlora._formatar(ex0) == "### Instrução:\nClassifique o ticket.\n\n### Resposta:\ncategoria: saque"
    assert qlora._formatar(ex1) == ("### Instrução:\nResuma.\n\n### Entrada:\ntexto longo\ncom quebra"
                                    "\n\n### Resposta:\nresumo curto")


@pytest.mark.parametrize("ex", EXEMPLOS)
def test_template_ollama_reproduz_o_prefixo_do_treino(ex):
    tpl = qlora.template_ollama()
    # inferência: Ollama recebe prompt_ollama(ex) e deve montar exatamente o prefixo do treino
    assert _renderizar(tpl, qlora.prompt_ollama(ex)) == qlora.formatar_prompt(ex)
    # turno com resposta: igual ao texto de treino (sem o EOS, que é token e vem do tokenizer)
    assert _renderizar(tpl, qlora.prompt_ollama(ex), ex["output"]) == qlora._formatar(ex)


@pytest.mark.parametrize("ex", EXEMPLOS)
def test_modelfile_carrega_o_mesmo_template_do_treino(ex):
    mf = qlora.gerar_modelfile("lora-v1-q4_k_m.gguf", "<|im_end|>")
    tpl = _template_do_modelfile(mf)
    assert tpl == qlora.template_ollama()
    assert _renderizar(tpl, qlora.prompt_ollama(ex)) == qlora.formatar_prompt(ex)
    assert "FROM ./lora-v1-q4_k_m.gguf" in mf
    assert 'PARAMETER stop "<|im_end|>"' in mf
    assert f'PARAMETER stop "{qlora.CAB_INSTRUCAO.strip()}"' in mf
    assert not tpl.endswith("\n")  # trim do parser não pode comer o '\n' depois de '### Resposta:'


def test_modelfile_e_derivado_nao_copiado(monkeypatch):
    # Se alguém muda o cabeçalho do treino, o Modelfile acompanha sem ninguém lembrar.
    monkeypatch.setattr(qlora, "CAB_RESPOSTA", "\n\n### Saída:\n")
    ex = EXEMPLOS[0]
    assert "### Saída:" in qlora._formatar(ex)
    tpl = _template_do_modelfile(qlora.gerar_modelfile("m.gguf", "</s>"))
    assert "### Saída:" in tpl and "### Resposta:" not in tpl
    assert _renderizar(tpl, qlora.prompt_ollama(ex)) == qlora.formatar_prompt(ex)


def test_modelfile_recusa_aspas():
    with pytest.raises(ValueError):
        qlora.gerar_modelfile("m.gguf", 'eos"quebrado')


@pytest.mark.parametrize("arquivo,conteudo", [
    ("tokenizer_config.json", {"eos_token": "<|im_end|>"}),
    ("special_tokens_map.json", {"eos_token": {"content": "<|im_end|>", "special": True}}),
])
def test_eos_do_adapter(tmp_path, arquivo, conteudo):
    (tmp_path / arquivo).write_text(json.dumps(conteudo), encoding="utf-8")
    assert qlora.eos_do_adapter(tmp_path) == "<|im_end|>"


def test_eos_do_adapter_ausente(tmp_path):
    with pytest.raises(FileNotFoundError):
        qlora.eos_do_adapter(tmp_path)


def test_cli_modelfile_grava_ao_lado_do_gguf(tmp_path, capsys):
    adapter = tmp_path / "lora-v1"
    adapter.mkdir()
    (adapter / "tokenizer_config.json").write_text(json.dumps({"eos_token": "<|im_end|>"}), encoding="utf-8")
    gguf = tmp_path / "gguf" / "lora-v1-q8_0.gguf"
    gguf.parent.mkdir()
    gguf4 = gguf.with_name("lora-v1-q4_k_m.gguf")
    assert qlora.main(["--modelfile", str(gguf), "--adapter", str(adapter)]) == 0
    assert qlora.main(["--modelfile", str(gguf4), "--eos", "<|im_end|>"]) == 0
    # um Modelfile por GGUF: o segundo não sobrescreve o primeiro
    mf = (gguf.parent / "lora-v1-q8_0.Modelfile").read_text(encoding="utf-8")
    assert mf == qlora.gerar_modelfile("lora-v1-q8_0.gguf", "<|im_end|>")
    assert "FROM ./lora-v1-q4_k_m.gguf" in (gguf.parent / "lora-v1-q4_k_m.Modelfile").read_text(encoding="utf-8")
    assert "Modelfile gravado" in capsys.readouterr().out


def test_cli_sem_data_e_sem_modelfile_falha():
    with pytest.raises(SystemExit) as e:
        qlora.main([])
    assert e.value.code == 2


def test_aviso_vram():
    assert qlora.aviso_vram(5.0, 8.0) is None
    assert "compartilhada" in qlora.aviso_vram(7.6, 8.0)
    assert qlora.aviso_vram(9.1, 8.0) is not None  # acima do total = já transbordou


def test_linha_log_tem_o_carimbo_completo():
    linha = qlora.linha_log(modelo="Qwen/Qwen2.5-1.5B-Instruct", r=16, epochs=2, lr=2e-4, max_len=1024,
                            dado="treino.jsonl", n=300, loss_final=0.8123, vram_gb=3.24, minutos=12.5,
                            out="outputs/lora-v1")
    for pedaco in ["| B |", "r=16", "2 ep", "lr 0.0002", "seq 1024", "n treino=300", "n eval=",
                   "loss final 0.812", "VRAM pico 3.2 GB", "12.5 min", "`outputs/lora-v1`"]:
        assert pedaco in linha, pedaco
    assert linha.count("|") == 9  # 8 colunas do log


def test_comparar_avalia_no_mesmo_prompt_do_treino():
    from lab.finetune import comparar
    exs = [{"instruction": "Some 2 e 3", "input": "", "output": "5"},
           {"instruction": "Traduza", "input": "cat", "output": "gato"}]
    prompts = comparar.montar_prompts(exs)
    for ex, p in zip(exs, prompts):
        # o prompt de avaliação é o texto de treino ATÉ a resposta, byte a byte
        assert qlora._formatar(ex) == p + ex["output"]
        assert p.endswith(qlora.CAB_RESPOSTA)
