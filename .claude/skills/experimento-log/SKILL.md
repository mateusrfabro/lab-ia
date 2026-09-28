---
name: experimento-log
description: Use ao terminar qualquer rodada (agente, fine-tuning, modelo tabular) para registrar a linha em experiments/log.md no formato do projeto — e ao começar uma rodada, para ler o que já foi tentado. Experimento sem linha no log não aconteceu.
---

# Log de experimentos (`experiments/log.md`)

## Por que
Em uma semana ninguém lembra qual seed, qual modelo, qual dataset deu 0,78. O log é a memória
do laboratório e a prova de que um resultado existiu. Também evita repetir o que já falhou.

## Formato (uma linha por rodada, tabela markdown)

| coluna | o que vai | exemplo |
|---|---|---|
| data | AAAA-MM-DD | 2026-09-12 |
| trilha | A (agente) / B (fine-tuning) / C (tabular) | C |
| modelo | nome + tag/versão + hiperparâmetro que importa | `lightgbm n=400 lr=0,03` / `qwen3:8b think=off` / `Qwen2.5-1.5B + LoRA r=16` |
| dado (n) | nome do arquivo + n de linhas/exemplos + corte se houver | `churn_pk_2026-09-01.csv (n=12.480, corte 01/09)` |
| métrica | a principal com desvio; segunda se relevante | `AUC 0,742 ± 0,011; PR 0,31` / `acerto 7/9` / `loss 0,62` |
| baseline | o número burro ou o few-shot | `AUC 0,50` / `few-shot 4/9` |
| conclusão | **uma frase**, no que foi medido | `sinal real mas fraco; dias_desde_login domina` |
| artefato | script + args, ou pasta de saída | `lab.tabular.baseline --group user_id --seed 42` |

## Regras
1. **Sem "se", "deve", "provavelmente" na conclusão.** Isso é pergunta; vai em "próximo passo",
   não em conclusão.
2. **Rodada que falhou também entra** (OOM, dataset inválido, modelo em loop). Falha registrada
   poupa a próxima tentativa.
3. **Número sem baseline na mesma linha não entra.**
4. Os scripts (`baseline.py`, `avaliar.py`, `qlora.py`) já imprimem a linha pronta; copiar e
   completar data e conclusão.
5. Antes de escrever a conclusão de algo que vai ser contado a alguém, passar pelo agente
   `revisor-experimento`.

## Ao começar uma rodada
Ler as últimas linhas da mesma trilha. Se a pergunta já foi respondida, não repetir; se a
tentativa anterior falhou, mudar algo antes de rodar de novo.
