# lab-ia

Laboratório local de modelos de IA (Ollama + PyTorch) numa RTX 4050 de 6 GB.

```powershell
.\setup.ps1          # venv + pacotes base (pandas, sklearn, xgboost, lightgbm, requests)
.\setup.ps1 -Llm     # + torch CUDA 12.6, transformers, peft, trl, bitsandbytes (~3 GB)
.\.venv\Scripts\Activate.ps1
python scripts\check_env.py
```

Trilhas: `src/lab/agent` (agente com ferramentas sobre Ollama), `src/lab/finetune` (QLoRA),
`src/lab/tabular` (baseline de ML tabular). Contexto completo em `CLAUDE.md`.
