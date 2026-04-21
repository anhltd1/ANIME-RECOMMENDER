"""Load raw anime CSV and write processed CSV with ``combined_column``."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT_CSV = PROJECT_ROOT / "data" / "anime_with_synopsis.csv"
DEFAULT_OUTPUT_CSV = PROJECT_ROOT / "data" / "processed_data.csv"


class DataLoader:
    """Read **`input_csv`**, filter rows, append **`combined_column`**, write **`output_csv`**."""

    COLS = ["Name", "Genres", "sypnopsis"]

    def __init__(self, input_csv: str | Path, output_csv: str | Path) -> None:
        self.input_csv = Path(input_csv)
        self.output_csv = Path(output_csv)

    def process(self) -> Path:
        cols = self.COLS
        df = pd.read_csv(self.input_csv, usecols=cols)
        df = df.dropna(subset=cols)
        for c in cols:
            s = df[c].astype(str).str.strip()
            df = df[s.ne("") & s.ne("nan")]
        df = df.assign(
            combined_column=lambda d: (
                "Title "
                + d["Name"].astype(str)
                + " \n\n Genres: "
                + d["Genres"].astype(str)
                + " \n\n Overview: "
                + d["sypnopsis"].astype(str)
            )
        )
        self.output_csv.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.output_csv, index=False)
        return self.output_csv


def main() -> None:
    DataLoader(DEFAULT_INPUT_CSV, DEFAULT_OUTPUT_CSV).process()


if __name__ == "__main__":
    main()


__all__ = ["DEFAULT_INPUT_CSV", "DEFAULT_OUTPUT_CSV", "DataLoader", "main"]
