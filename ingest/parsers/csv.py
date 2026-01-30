# ingest/parsers/csv.py
import pandas as pd


def parse_csv(path: str) -> str:
    df = pd.read_csv(path)
    return "\n".join(
        " | ".join(map(str, row))
        for row in df.values
    )
