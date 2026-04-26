from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.ensemble import IsolationForest


@dataclass(slots=True)
class DetectionResult:
    scored_frame: pd.DataFrame
    anomaly_frame: pd.DataFrame
    numeric_columns: list[str]


def detect_anomalies(frame: pd.DataFrame, contamination: float = 0.1) -> DetectionResult:
    numeric_columns = frame.select_dtypes(include="number").columns.tolist()
    if not numeric_columns:
        raise ValueError("No numeric columns found. At least one numeric column is required.")

    model_input = frame[numeric_columns].fillna(frame[numeric_columns].median())
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=200,
    )
    predictions = model.fit_predict(model_input)
    scores = model.decision_function(model_input)

    scored_frame = frame.copy()
    scored_frame["anomaly_label"] = predictions
    scored_frame["anomaly_score"] = scores
    scored_frame["is_anomaly"] = scored_frame["anomaly_label"].eq(-1)

    anomaly_frame = scored_frame.loc[scored_frame["is_anomaly"]].sort_values(
        by="anomaly_score",
        ascending=True,
    )

    return DetectionResult(
        scored_frame=scored_frame.reset_index(drop=True),
        anomaly_frame=anomaly_frame.reset_index(drop=True),
        numeric_columns=numeric_columns,
    )
