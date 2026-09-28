# Primeiros passos no lab-ia

## Sessão 1 (30 min): sentir o modelo local
```powershell
.\.venv\Scripts\Activate.ps1
python scripts\check_env.py
python -m lab.ollama_client "explique em 3 frases o que é LoRA"
python -m lab.agent.run "crie cafes.txt com 5 nomes de cafés, um por linha"
type outputs\agent_sandbox\cafes.txt
python -m lab.agent.avaliar --repeticoes 3        # taxa de acerto do qwen3:8b
python -m lab.agent.avaliar --repeticoes 3 --model llama3.1:8b
```
Registrar as duas taxas em `experiments/log.md`. Pergunta a responder: qual dos modelos
locais é o mais confiável com ferramenta, e quanto (número, não impressão).

## Sessão 2 (1 h): ML tabular com dado sintético, depois real
```powershell
python -m lab.tabular.dados_sinteticos --n 5000
python -m lab.tabular.baseline data\processed\churn_sintetico.csv --target churn --drop user_id
python -m lab.tabular.baseline data\processed\churn_sintetico.csv --target churn --drop user_id,dias_ate_churn
```
Ver o AUC cair de 1,000 para ~0,77 quando a coluna vazada sai: isso é leakage na prática
(medido em 10/09, seed 42). Repare também que a logística ganha do LightGBM nesse dado: a
regra que gerou o churn é linear, então o modelo linear é o certo. Boosting não é sempre melhor.
Depois: extrair churn real do P4T **no analítico** (repo do play4tune, anonimizado) e repetir.

## Sessão 3 (2 h + download): fine-tuning
```powershell
.\setup.ps1 -Llm                                   # ~3 GB
python scripts\check_env.py                        # torch cuda=True?
# montar data\processed\treino.jsonl e eval.jsonl (skill qlora-6gb)
python -m lab.finetune.qlora --data data\processed\treino.jsonl --dry-run
python -m lab.finetune.qlora --data data\processed\treino.jsonl --out outputs\lora-v1
python -m lab.finetune.comparar --adapter outputs\lora-v1 --eval data\processed\eval.jsonl
```
Antes disso, provar que few-shot no `qwen3:8b` não resolve (regra 6).

## Ideias de caso de uso com dado do P4T (todas com dado anonimizado)
- **C**: churn 7d pós-FTD; propensão a STD em 48h; score de risco de abuso de bônus.
- **A**: agente que lê um CSV de relatório e escreve o resumo em 3 linhas (o que hoje é feito
  à mão no WhatsApp).
- **B**: modelo que classifica mensagem de suporte/CRM em categoria fixa, no vocabulário
  da casa (PKR, FTD, cashback, Welcome).
