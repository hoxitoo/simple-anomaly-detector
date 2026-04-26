# Simple Anomaly Detector

A lightweight CLI tool that detects unusual rows in tabular data using Isolation Forest.

## What it does

- reads a CSV file
- selects numeric columns
- trains an Isolation Forest model
- assigns anomaly labels and scores
- exports flagged rows

## Why this is useful

This is a small but serious portfolio project because it combines:

- data cleaning
- feature selection
- machine learning
- report generation

## Usage

```bash
python -m src.main examples/transactions.csv --csv-out outputs/anomalies.csv --contamination 0.15
```

## Example output

```text
Rows analyzed: 10
Numeric columns used: 3
Detected anomalies: 2
```

## Testing

```bash
pytest
```
