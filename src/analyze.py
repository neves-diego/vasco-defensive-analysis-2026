"""Pipeline de análise defensiva do Vasco da Gama em 2026.

O módulo recebe uma base jogo a jogo já coletada/padronizada, associa o treinador
responsável pela partida e produz métricas comparáveis por período.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA = Path("data/processed/vasco_matches_2026.csv")
OUTPUT = Path("data/processed/manager_summary.csv")

# Datas de corte devem ser validadas pelas fontes antes da versão final da análise.
MANAGER_PERIODS = [
    ("Fernando Diniz", "2026-01-01", "2026-02-22"),
    ("Renato Gaúcho", "2026-03-03", "2026-06-18"),
    ("Pedro Emanuel", "2026-07-01", "2026-12-31"),
]


def assign_manager(date: pd.Timestamp) -> str:
    for manager, start, end in MANAGER_PERIODS:
        if pd.Timestamp(start) <= date <= pd.Timestamp(end):
            return manager
    return "Interino/fora do recorte"


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["manager"] = df["date"].apply(assign_manager)
    df["clean_sheet"] = (df["goals_against"] == 0).astype(int)
    return df


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    main = df[df["manager"].isin([p[0] for p in MANAGER_PERIODS])]
    summary = (
        main.groupby("manager", sort=False)
        .agg(
            matches=("date", "count"),
            goals_against=("goals_against", "sum"),
            goals_against_per_match=("goals_against", "mean"),
            clean_sheets=("clean_sheet", "sum"),
            clean_sheet_rate=("clean_sheet", "mean"),
        )
        .reset_index()
    )
    summary["clean_sheet_rate"] *= 100
    return summary


def main() -> None:
    if not DATA.exists():
        raise FileNotFoundError(
            f"Base não encontrada em {DATA}. Execute primeiro a etapa de coleta."
        )
    df = prepare(pd.read_csv(DATA))
    summary = summarize(df)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT, index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
