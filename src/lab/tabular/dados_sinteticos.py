"""Gera um dataset sintético de churn de jogador para exercitar o baseline SEM dado real.

As features imitam o que existe no P4T (depósitos, apostas, dias desde o último login), mas
os números são inventados com uma regra conhecida — assim dá pra verificar que o pipeline
recupera o sinal. Inclui de propósito uma coluna vazada (`dias_ate_churn`) para a skill
`ml-tabular-baseline` mostrar o que leakage faz com a métrica.

Uso: python -m lab.tabular.dados_sinteticos --n 5000 --out data/processed/churn_sintetico.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def gerar(n: int = 5000, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dep_n = rng.poisson(3, n)
    dep_valor = np.round(rng.gamma(2.0, 1500, n) * (dep_n > 0), 0)
    bets_n = rng.poisson(40, n) * (dep_n > 0)
    dias_login = rng.integers(0, 60, n)
    canal = rng.choice(["apk", "web", "afiliado"], n, p=[0.5, 0.35, 0.15])
    bonus = rng.random(n) < 0.4
    # regra "verdadeira": churn sobe com dias sem login e cai com depósitos/apostas
    logit = -1.0 + 0.06 * dias_login - 0.25 * dep_n - 0.01 * bets_n + 0.4 * (canal == "afiliado") - 0.3 * bonus
    p = 1 / (1 + np.exp(-logit))
    churn = (rng.random(n) < p).astype(int)
    dias_ate_churn = np.where(churn == 1, rng.integers(1, 30, n), 999)  # VAZAMENTO proposital
    return pd.DataFrame({
        "user_id": np.arange(1, n + 1),
        "dep_n": dep_n, "dep_valor_pkr": dep_valor, "bets_n": bets_n,
        "dias_desde_login": dias_login, "canal": canal, "recebeu_bonus": bonus,
        "dias_ate_churn": dias_ate_churn, "churn": churn,
    })


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5000)
    ap.add_argument("--out", default="data/processed/churn_sintetico.csv")
    a = ap.parse_args()
    df = gerar(a.n)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.out, index=False)
    print(f"{a.out}: n={len(df)} churn={df.churn.mean():.1%}")
    print("Rode com e sem --drop dias_ate_churn para ver o efeito do vazamento.")
