param([switch]$Llm)
# Cria a venv e instala os pacotes. Base = ML tabular + cliente Ollama (rapido, ~200 MB).
# -Llm = torch com CUDA + stack de fine-tuning (~3 GB de download).
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Test-Path .venv)) { python -m venv .venv; Write-Host "venv criada" }
$py = ".\.venv\Scripts\python.exe"
& $py -m pip install --upgrade pip
& $py -m pip install -r requirements-base.txt
& $py -m pip install -e .
if ($Llm) {
  # torch PRIMEIRO e SOZINHO, com --index-url (nao --extra-index-url): com extra-index o pip
  # escolhe a versao mais alta entre PyPI e o indice do PyTorch, e no Windows o PyPI so tem o
  # build CPU. Foi o que aconteceu em 10/09/2026 (instalou 2.14.0+cpu, cuda=False).
  # cu126 e o build mais novo compativel com o driver 573.22 (CUDA 12.8). Se atualizar o
  # driver, conferir em https://download.pytorch.org/whl/ qual cuXXX existe para o torch atual.
  Write-Host "Instalando torch CUDA 12.6..."
  & $py -m pip install "torch==2.14.0+cu126" --index-url https://download.pytorch.org/whl/cu126
  Write-Host "Instalando transformers/peft/trl/bitsandbytes..."
  & $py -m pip install -r requirements-llm.txt
}
& $py scripts\check_env.py
