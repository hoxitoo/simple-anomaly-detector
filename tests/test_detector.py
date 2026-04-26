import pandas as pd

from src.detector import detect_anomalies


def test_detect_anomalies() -> None:
    frame = pd.DataFrame(
        {
            "amount": [10, 11, 12, 13, 200],
            "items": [1, 1, 2, 1, 10],
        }
    )

    result = detect_anomalies(frame, contamination=0.2)

    assert len(result.numeric_columns) == 2
    assert result.scored_frame["is_anomaly"].sum() >= 1
