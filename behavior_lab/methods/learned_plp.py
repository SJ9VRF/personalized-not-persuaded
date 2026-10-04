from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

LICENSE_COLS = ["presentation_license", "personalization_license", "evidence_license"]
CATEGORICAL = ["scope", "provenance", "task_kind", "domain", "tier"]
NUMERIC = ["confidence", "current", "relevant"]
TEXT = "signal_content"


@dataclass
class HeadResult:
    threshold: float
    val_accuracy: float
    val_brier: float
    val_auc: float | None


class PLPRouter:
    """Learn a three-channel standing vector for personal context.

    The historical implementation name is PLP. Each head predicts whether a
    context signal has standing to influence presentation, personalization, or
    evidence. Thresholds are selected only on validation and frozen for
    test/OOD evaluation.
    """

    def __init__(self, include_provenance: bool = True, random_state: int = 0):
        self.include_provenance = include_provenance
        self.random_state = random_state
        cats = CATEGORICAL if include_provenance else [c for c in CATEGORICAL if c != "provenance"]
        self.categorical = cats
        self.heads: Dict[str, Pipeline] = {}
        self.thresholds: Dict[str, float] = {}
        self.head_results: Dict[str, HeadResult] = {}

    def _pipeline(self) -> Pipeline:
        prep = ColumnTransformer(
            [
                ("text", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=12000), TEXT),
                ("cat", OneHotEncoder(handle_unknown="ignore"), self.categorical),
                ("num", StandardScaler(), NUMERIC),
            ],
            sparse_threshold=0.3,
        )
        clf = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=self.random_state)
        return Pipeline([("features", prep), ("clf", clf)])

    @staticmethod
    def _best_threshold(y: np.ndarray, p: np.ndarray) -> float:
        best_t, best_score = 0.5, -1.0
        for t in np.linspace(0.05, 0.95, 181):
            pred = (p >= t).astype(int)
            score = accuracy_score(y, pred)
            # prefer thresholds closer to 0.5 on ties
            if score > best_score + 1e-12 or (abs(score-best_score) < 1e-12 and abs(t-0.5) < abs(best_t-0.5)):
                best_t, best_score = float(t), float(score)
        return best_t

    def fit(self, train: pd.DataFrame, val: pd.DataFrame) -> "PLPRouter":
        for target in LICENSE_COLS:
            pipe = self._pipeline()
            pipe.fit(train, train[target].astype(int))
            p = pipe.predict_proba(val)[:, 1]
            y = val[target].astype(int).to_numpy()
            t = self._best_threshold(y, p)
            pred = (p >= t).astype(int)
            try:
                auc = float(roc_auc_score(y, p)) if len(np.unique(y)) == 2 else None
            except ValueError:
                auc = None
            self.heads[target] = pipe
            self.thresholds[target] = t
            self.head_results[target] = HeadResult(
                threshold=t,
                val_accuracy=float(accuracy_score(y, pred)),
                val_brier=float(brier_score_loss(y, p)),
                val_auc=auc,
            )
        return self

    def predict_proba(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        for target, pipe in self.heads.items():
            out[target + "_prob"] = pipe.predict_proba(df)[:, 1]
        return out

    def predict(self, df: pd.DataFrame, hybrid: bool = False) -> pd.DataFrame:
        probs = self.predict_proba(df)
        out = pd.DataFrame(index=df.index)
        for target in LICENSE_COLS:
            out[target] = (probs[target + "_prob"] >= self.thresholds[target]).astype(int)
        if hybrid:
            # Auditable validity constraints. They do not decide whether a source
            # type is evidentiary; they only prevent stale, low-confidence, or
            # task-irrelevant context from receiving any license.
            invalid = (df["current"].astype(int) == 0) | (df["relevant"].astype(int) == 0) | (df["confidence"].astype(float) < 0.5)
            out.loc[invalid, LICENSE_COLS] = 0
        return out


def metric_bundle(df: pd.DataFrame, pred: pd.DataFrame) -> Dict[str, float]:
    y = df[LICENSE_COLS].astype(int).to_numpy()
    p = pred[LICENSE_COLS].astype(int).to_numpy()
    exact = (y == p).all(axis=1).mean()
    truth_e = df["evidence_license"].astype(int).to_numpy()
    pred_e = pred["evidence_license"].astype(int).to_numpy()
    positives = truth_e == 1
    negatives = truth_e == 0
    uptake = pred_e[positives].mean() if positives.any() else np.nan
    leakage = pred_e[negatives].mean() if negatives.any() else np.nan
    starvation = 1.0 - uptake if not np.isnan(uptake) else np.nan
    return {
        "exact_license_match": float(exact),
        "evidence_uptake": float(uptake),
        "unsupported_leakage": float(leakage),
        "evidence_starvation": float(starvation),
    }


def baseline_predictions(df: pd.DataFrame, kind: str) -> pd.DataFrame:
    out = pd.DataFrame(0, index=df.index, columns=LICENSE_COLS, dtype=int)
    if kind == "naive":
        out["presentation_license"] = (df["scope"].astype(str) == "style").astype(int)
        out["personalization_license"] = df["scope"].isin(["style", "preference", "constraint", "goal", "personal_state"]).astype(int)
        out["evidence_license"] = df["relevant"].astype(int)
    elif kind == "firewall":
        out["presentation_license"] = (df["scope"].astype(str) == "style").astype(int)
        out["personalization_license"] = df["scope"].isin(["style", "preference", "constraint", "goal", "personal_state"]).astype(int)
        out["evidence_license"] = 0
    elif kind == "provenance_only":
        out["presentation_license"] = (df["scope"].astype(str) == "style").astype(int)
        out["personalization_license"] = df["scope"].isin(["style", "preference", "constraint", "goal", "personal_state"]).astype(int)
        trusted = df["provenance"].isin(["tool_verified", "external_verified"])
        out["evidence_license"] = (trusted & (df["relevant"].astype(int) == 1) & (df["current"].astype(int) == 1)).astype(int)
    elif kind == "oracle":
        out = df[LICENSE_COLS].astype(int).copy()
    else:
        raise ValueError(kind)
    return out


def calibration_table(y: np.ndarray, p: np.ndarray, bins: int = 10) -> pd.DataFrame:
    edges = np.linspace(0, 1, bins + 1)
    rows = []
    for i in range(bins):
        lo, hi = edges[i], edges[i+1]
        mask = (p >= lo) & ((p < hi) if i < bins-1 else (p <= hi))
        if not mask.any():
            continue
        rows.append({
            "bin_low": lo,
            "bin_high": hi,
            "count": int(mask.sum()),
            "mean_probability": float(p[mask].mean()),
            "empirical_rate": float(y[mask].mean()),
            "abs_gap": float(abs(p[mask].mean() - y[mask].mean())),
        })
    return pd.DataFrame(rows)
