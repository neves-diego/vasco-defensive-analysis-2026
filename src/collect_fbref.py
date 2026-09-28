"""Coleta reproduzível da tabela de jogos do Vasco no FBref.

O FBref pode alterar URLs/HTML e aplicar limites de acesso. Por isso, a URL fica
configurável e o script preserva uma cópia bruta antes de qualquer análise.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import time
import pandas as pd
import requests

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def download(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; educational-data-analysis/1.0)"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    time.sleep(3)
    return response.text


def choose_schedule_table(html: str) -> pd.DataFrame:
    tables = pd.read_html(html)
    for table in tables:
        cols = {str(c).strip().lower() for c in table.columns}
        if {"date", "opponent"}.issubset(cols) and ("ga" in cols or "gf" in cols):
            return table
    raise ValueError("Tabela de jogos não encontrada no HTML recebido do FBref.")


def normalize(table: pd.DataFrame) -> pd.DataFrame:
    df = table.copy()
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    rename = {
        "ga": "goals_against",
        "gf": "goals_for",
        "comp": "competition",
        "venue": "venue",
        "opponent": "opponent",
    }
    df = df.rename(columns=rename)
    wanted = [
        c for c in ["date", "competition", "venue", "opponent", "goals_for", "goals_against"]
        if c in df.columns
    ]
    df = df[wanted]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    for col in ["goals_for", "goals_against"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="URL da página de jogos do Vasco no FBref")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    html = download(args.url)
    (RAW_DIR / "fbref_schedule_2026.html").write_text(html, encoding="utf-8")
    df = normalize(choose_schedule_table(html))
    df.to_csv(PROCESSED_DIR / "vasco_matches_2026.csv", index=False)
    print(f"{len(df)} partidas salvas.")


if __name__ == "__main__":
    main()
