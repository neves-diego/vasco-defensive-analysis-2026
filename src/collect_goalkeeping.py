"""Coleta e prepara os match logs de goleiros do Vasco no FBref.

Essa tabela adiciona chutes no alvo sofridos (SoTA), defesas, percentual de
defesas e clean sheets à análise de gols sofridos.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from io import StringIO
import pandas as pd
import requests

OUT = Path("data/processed/vasco_goalkeeping_2026.csv")


def fetch_tables(url: str) -> list[pd.DataFrame]:
    headers = {"User-Agent": "Mozilla/5.0 (educational football analytics project)"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    # FBref frequentemente mantém tabelas dentro de comentários HTML.
    html = r.text.replace("<!--", "").replace("-->", "")
    return pd.read_html(StringIO(html))


def select_table(tables: list[pd.DataFrame]) -> pd.DataFrame:
    for df in tables:
        flat = [str(c[-1] if isinstance(c, tuple) else c).strip() for c in df.columns]
        if "SoTA" in flat and "Saves" in flat and "Opponent" in flat:
            df = df.copy()
            df.columns = flat
            return df
    raise ValueError("Tabela de goalkeeping não encontrada.")


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    rename = {
        "Date": "date", "Comp": "competition", "Venue": "venue",
        "Opponent": "opponent", "GA": "goals_against", "SoTA": "shots_on_target_against",
        "Saves": "saves", "Save%": "save_pct", "CS": "clean_sheet"
    }
    df = df.rename(columns=rename)
    keep = [c for c in rename.values() if c in df.columns]
    df = df[keep].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    for c in ["goals_against", "shots_on_target_against", "saves", "save_pct", "clean_sheet"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    df = normalize(select_table(fetch_tables(args.url)))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"{len(df)} registros de goalkeeping salvos em {OUT}")


if __name__ == "__main__":
    main()
