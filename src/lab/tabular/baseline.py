"""Baseline de classificação binária tabular: 3 modelos + baseline burro + CV estratificada.

Por que assim:
- **Baseline burro (DummyClassifier)** primeiro: AUC 0,5 / acurácia da classe majoritária. Se o
  modelo real não bate isso por margem, não há sinal nos dados.
- **Regressão logística** depois: linear, interpretável, rápido. Se o gradient boosting só ganha
  0,01 de AUC dela, a complexidade não paga.
- **LightGBM e XGBoost** por último: o "estado da arte" em tabular. Ganham quase sempre, mas
  precisam de mais cuidado com leakage e overfit.
- **CV estratificada (5 folds)** em vez de um split só: com poucos milhares de linhas um split
  único varia ±0,03 de AUC só por sorte.
- **AUC + PR-AUC + Brier**: AUC ordena; PR-AUC importa quando a classe positiva é rara (churn,
  fraude); Brier mede calibração (se "0,8" quer dizer 80%).

Uso:
    python -m lab.tabular.baseline data/processed/churn.csv --target churn
    python -m lab.tabular.baseline x.csv --target y --drop user_id,data_ref --group user_id
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def _preprocessador(X: pd.DataFrame) -> ColumnTransformer:
    num = X.select_dtypes(include=["number", "bool"]).columns.tolist()
    cat = [c for c in X.columns if c not in num]
    return ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh", OneHotEncoder(handle_unknown="ignore", min_frequency=20))]), cat),
    ])


def modelos(X: pd.DataFrame, seed: int) -> dict[str, Pipeline]:
    pre = _preprocessador(X)
    out: dict[str, Pipeline] = {
        "dummy_majoritaria": Pipeline([("pre", pre), ("m", DummyClassifier(strategy="prior"))]),
        "logistica": Pipeline([("pre", pre), ("m", LogisticRegression(max_iter=2000, class_weight="balanced"))]),
    }
    try:
        from lightgbm import LGBMClassifier
        out["lightgbm"] = Pipeline([("pre", pre), ("m", LGBMClassifier(
            n_estimators=400, learning_rate=0.03, num_leaves=31, subsample=0.8, colsample_bytree=0.8,
            random_state=seed, verbose=-1))])
    except ImportError:
        pass
    try:
        from xgboost import XGBClassifier
        out["xgboost"] = Pipeline([("pre", pre), ("m", XGBClassifier(
            n_estimators=400, learning_rate=0.03, max_depth=5, subsample=0.8, colsample_bytree=0.8,
            random_state=seed, eval_metric="logloss", n_jobs=-1))])
    except ImportError:
        pass
    return out


def avaliar(df: pd.DataFrame, target: str, drop: list[str] | None = None, group: str | None = None,
            folds: int = 5, seed: int = 42) -> pd.DataFrame:
    drop = drop or []
    y = df[target].astype(int).to_numpy()
    X = df.drop(columns=[target, *drop, *([group] if group and group not in drop else [])], errors="ignore")
    groups = df[group].to_numpy() if group else None

    if groups is not None:
        cv = StratifiedGroupKFold(n_splits=folds, shuffle=True, random_state=seed)
        splits = list(cv.split(X, y, groups))
    else:
        cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
        splits = list(cv.split(X, y))

    linhas = []
    for nome, pipe in modelos(X, seed).items():
        aucs, prs, briers = [], [], []
        t0 = time.time()
        for tr, te in splits:
            pipe.fit(X.iloc[tr], y[tr])
            p = pipe.predict_proba(X.iloc[te])[:, 1]
            aucs.append(roc_auc_score(y[te], p))
            prs.append(average_precision_score(y[te], p))
            briers.append(brier_score_loss(y[te], p))
        linhas.append({
            "modelo": nome,
            "auc": np.mean(aucs), "auc_dp": np.std(aucs),
            "pr_auc": np.mean(prs), "brier": np.mean(briers),
            "seg": round(time.time() - t0, 1),
        })
    res = pd.DataFrame(linhas).sort_values("auc", ascending=False).reset_index(drop=True)
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--target", required=True)
    ap.add_argument("--drop", default="", help="colunas a ignorar, separadas por vírgula (ids, datas, vazamentos)")
    ap.add_argument("--group", default=None, help="coluna de grupo (ex.: user_id) para não vazar o mesmo sujeito entre folds")
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default=None, help="salva resultado em JSON")
    a = ap.parse_args(argv)

    df = pd.read_csv(a.csv)
    drop = [c for c in a.drop.split(",") if c]
    pos = df[a.target].mean()
    print(f"n={len(df):,}  positivos={pos:.1%}  features={df.shape[1] - 1 - len(drop)}  folds={a.folds}"
          + (f"  group={a.group}" if a.group else ""))
    if pos < 0.02 or pos > 0.98:
        print("AVISO: classe muito desbalanceada; olhe PR-AUC, não AUC.")

    res = avaliar(df, a.target, drop=drop, group=a.group, folds=a.folds, seed=a.seed)
    with pd.option_context("display.float_format", "{:.4f}".format):
        print(res.to_string(index=False))
    base = res.loc[res.modelo == "dummy_majoritaria", "auc"].iloc[0]
    melhor = res.iloc[0]
    print(f"\nmelhor: {melhor.modelo} AUC {melhor.auc:.3f} ± {melhor.auc_dp:.3f} (baseline {base:.3f})")
    if melhor.auc - base < 0.05:
        print("CONCLUSÃO: ganho sobre o baseline é marginal — provavelmente não há sinal útil nessas features.")
    if a.out:
        Path(a.out).write_text(json.dumps(res.to_dict(orient="records"), indent=2), encoding="utf-8")
        print(f"salvo em {a.out}")
    print("\nlinha para experiments/log.md:")
    print(f"| AAAA-MM-DD | C | {melhor.modelo} | {Path(a.csv).name} (n={len(df)}) | AUC {melhor.auc:.3f} PR {melhor.pr_auc:.3f} | AUC {base:.3f} | ... | `lab.tabular.baseline` |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
