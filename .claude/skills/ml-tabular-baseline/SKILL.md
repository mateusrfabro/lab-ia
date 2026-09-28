---
name: ml-tabular-baseline
description: Use ao montar, rodar ou ler qualquer modelo supervisionado tabular (churn, risco, propensão, fraude) — define unidade/janela/corte, checklist de leakage, split correto (por sujeito e por tempo), baseline burro obrigatório e qual métrica olhar. Sem isto, AUC alta é quase sempre vazamento.
---

# Baseline de ML tabular honesto

## 1. Formular antes de modelar (escrever as 5 respostas)
1. **Unidade**: uma linha é um jogador? um jogador-dia? um depósito?
2. **Data de corte** por linha: o instante em que a previsão seria feita na vida real.
3. **Janela de observação**: features só do que existia **até** o corte (ex.: 30 dias antes).
4. **Janela de alvo**: o que conta como positivo e até quando (ex.: "sem aposta nos 7 dias
   seguintes" = churn).
5. **Uso**: quem recebe o score e o que faz com ele. Decide a métrica.

Se não dá pra escrever os 5, ainda não é um problema de ML.

## 2. Checklist de leakage (rodar linha a linha nas features)
- [ ] A feature existia às 23:59 do dia de corte? (`dias_ate_churn`, `status_final`,
      `total_depositado` vitalício = **vazamento**)
- [ ] Alguma feature é o alvo com outro nome ou derivada dele?
- [ ] Coluna de ID, data, e-mail entrou como feature? (o modelo decora)
- [ ] O mesmo jogador aparece em treino e teste? → `--group user_id`
- [ ] Teste é de um período **posterior** ao treino? Se não, é otimista.
- [ ] Imputação/encoding foi ajustado só no treino? (o `Pipeline` do sklearn garante)
- [ ] Filtro de "usuário teste" aplicado antes? (no P4T: `is_test_user OR email`; a flag
      `is_possible_test_user` marca jogador real — ver memória do play4tune)

Prova rápida: `python -m lab.tabular.dados_sinteticos` cria um churn sintético com uma coluna
vazada de propósito. Rodar o baseline com e sem `--drop dias_ate_churn`: AUC 1,000 × 0,774
(medido 10/09/2026, n=5000, seed 42).

## 3. Baseline burro é obrigatório
`DummyClassifier(strategy="prior")` na mesma tabela. AUC 0,5, PR-AUC = taxa de positivos.
O que se reporta é o **ganho sobre ele** e o desvio-padrão entre folds. Ganho < 2× o desvio
é ruído.

## 4. Ordem dos modelos
1. Dummy → 2. Regressão logística (`class_weight="balanced"`) → 3. LightGBM → 4. XGBoost.
Se o boosting ganha < 0,02 de AUC da logística, ficar com a logística (explicável, estável).

## 5. Qual métrica
| Situação | Olhar |
|---|---|
| Ranquear (quem contatar primeiro) | AUC |
| Classe rara (< 10%: fraude, churn cedo) | PR-AUC, não AUC |
| Score vai virar probabilidade (ex.: "80% de chance") | Brier + curva de calibração |
| Decisão binária com custo assimétrico | precision/recall no corte escolhido pelo custo |
Acurácia quase nunca. Com 90% de negativos, "sempre não" tem 90% de acurácia.

## 6. Comando
```powershell
python -m lab.tabular.baseline data\processed\x.csv --target churn --drop user_id,data_ref --group user_id --out outputs\baseline_x.json
```
Saída já traz a linha para `experiments/log.md`.

## 7. Dado do P4T
Extração no **analítico** (`supernova_db`, réplica em `public.*`) com o conector do repo do
play4tune. Anonimizar (trocar `user_id` por hash, dropar e-mail/telefone/documento/IP) **antes**
de gravar em `data/raw/`. Nunca daqui e nunca no `supernova_bet` (banco do jogador).
