from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .detector import detect_anomalies


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Detect anomalies in a CSV file.")
    parser.add_argument("csv_path", type=Path, help="Input CSV path.")
    parser.add_argument("--csv-out", type=Path, help="Optional output path for anomalies only.")
    parser.add_argument(
        "--contamination",
        type=float,
        default=0.1,
        help="Expected fraction of anomalies. Must be between 0 and 0.5.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if not 0 < args.contamination < 0.5:
        raise SystemExit("contamination must be between 0 and 0.5")

    frame = pd.read_csv(args.csv_path)
    result = detect_anomalies(frame, contamination=args.contamination)

    print(f"Rows analyzed: {len(frame)}")
    print(f"Numeric columns used: {len(result.numeric_columns)}")
    print(f"Detected anomalies: {len(result.anomaly_frame)}")

    if args.csv_out:
        args.csv_out.parent.mkdir(parents=True, exist_ok=True)
        result.anomaly_frame.to_csv(args.csv_out, index=False)
        print(f"Anomalies written to: {args.csv_out}")


if __name__ == "__main__":
    main()
