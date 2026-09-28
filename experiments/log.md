# Log de experimentos

Uma linha por experimento. Sem linha aqui, o experimento não aconteceu. Formato na skill `experimento-log`.

| data | trilha | modelo | dado (n) | métrica | baseline | conclusão (1 frase) | artefato |
|---|---|---|---|---|---|---|---|
| 2026-09-10 | — | — | — | — | — | projeto criado; ambiente medido (RTX 4050 6GB, 15,7GB RAM, 4 modelos Ollama locais) | `scripts/check_env.py` |
| 2026-09-10 | A | qwen3:8b think=off | 1 tarefa × 1 (criar cafes.txt 5 linhas) | 1/1 em 1 chamada, 19,9 s | — | smoke: tool-calling funciona; n=1 não é taxa, rodar `avaliar --repeticoes 3` | `lab.agent.run` |
| 2026-09-10 | C | logistica (sklearn) | churn_sintetico.csv (n=5000, 43% pos), seed 42, 5 folds | AUC 1,000 ± 0,000 | AUC 0,500 | com `dias_ate_churn` dentro: leakage total, AUC 1,0 é falso | `lab.tabular.baseline --drop user_id` |
| 2026-09-10 | C | logistica (sklearn) | churn_sintetico.csv (n=5000, 43% pos), seed 42, 5 folds | AUC 0,774 ± 0,015; PR 0,706 | AUC 0,500 | sem a coluna vazada há sinal real; logística > LightGBM (0,741) porque a regra geradora é linear | `lab.tabular.baseline --drop user_id,dias_ate_churn` |
| 2026-09-10 | B | torch 2.14.0+cu126 | — | cuda=True, RTX 4050 6,0 GB | — | 1ª instalação veio CPU (`--extra-index-url` deixa o PyPI vencer); corrigido com `--index-url` cu126 no setup.ps1 | `scripts/check_env.py` |
| 2026-09-10 | A | Claude Code 2.1.197 + qwen3:8b via `ollama launch claude` | 1 pergunta ("conseguimos fazer algo?") | sem resposta em >42 s; interrompido | — | 8B com ctx 32k = 8,1 GB, 50/50 CPU/GPU, RAM livre 0,5 GB; inviável nesta máquina | `ollama ps` |
| 2026-09-10 | A | Claude Code 2.1.197 + qwen3:4b via `ollama launch claude` | 1 pergunta ("consegue avaliar um site?") | resposta correta em PT, leu o CLAUDE.md; **6 min 49 s** (5m38 pensando) | agente do lab: 20 s | 4B com ctx 32k = 5,7 GB, 27/73 CPU/GPU; funciona mas lento demais pra uso diário; próximo: liberar RAM e testar tarefa concreta de 1 rodada | `ollama ps` |
