"""Análise defensiva do Vasco no Brasileirão 2026."""
from pathlib import Path
import pandas as pd

MATCHES = Path("data/processed/vasco_matches_2026.csv")
KEEPERS = Path("data/processed/vasco_goalkeeping_2026.csv")
OUTPUT = Path("data/processed/manager_summary.csv")
MATCH_OUTPUT = Path("data/processed/serie_a_matches_with_manager.csv")

MANAGER_PERIODS = [
    ("Fernando Diniz", "2026-01-01", "2026-02-22"),
    ("Renato Gaúcho", "2026-03-12", "2026-06-18"),
    ("Pedro Emanuel", "2026-07-16", "2026-12-31"),
]
MANAGERS = [x[0] for x in MANAGER_PERIODS]


def assign_manager(date: pd.Timestamp) -> str:
    for manager, start, end in MANAGER_PERIODS:
        if pd.Timestamp(start) <= date <= pd.Timestamp(end):
            return manager
    return "Interino/fora do recorte"


def is_serie_a(value: object) -> bool:
    text = str(value).lower()
    return "série a" in text or "serie a" in text


def prepare_matches(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["goals_against"] = pd.to_numeric(df["goals_against"], errors="coerce")
    df = df.dropna(subset=["date", "goals_against"])
    if "competition" in df.columns:
        df = df[df["competition"].map(is_serie_a)]
    df["manager"] = df["date"].apply(assign_manager)
    df["clean_sheet"] = (df["goals_against"] == 0).astype(int)
    return df.sort_values("date")


def validate_matches(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Nenhuma partida válida da Série A foi encontrada.")
    keys = [c for c in ["date", "opponent"] if c in df.columns]
    if keys and df.duplicated(subset=keys).any():
        raise ValueError("Há partidas duplicadas na base processada.")
    if (df["goals_against"] < 0).any():
        raise ValueError("Foram encontrados gols sofridos negativos.")
    print(f"Controle da base: {len(df)} jogos, {int(df['goals_against'].sum())} gols sofridos.")


def add_goalkeeping(matches: pd.DataFrame) -> pd.DataFrame:
    if not KEEPERS.exists():
        return matches
    keepers = pd.read_csv(KEEPERS)
    keepers["date"] = pd.to_datetime(keepers["date"], errors="coerce")
    if "competition" in keepers.columns:
        keepers = keepers[keepers["competition"].map(is_serie_a)]
    numeric = ["shots_on_target_against", "saves"]
    for col in numeric:
        if col in keepers.columns:
            keepers[col] = pd.to_numeric(keepers[col], errors="coerce")
    cols = ["date", "opponent", *numeric]
    cols = [c for c in cols if c in keepers.columns]
    keys = [c for c in ["date", "opponent"] if c in matches.columns and c in keepers.columns]
    if not keys:
        return matches
    keepers = keepers[cols].drop_duplicates(subset=keys)
    return matches.merge(keepers, on=keys, how="left", validate="one_to_one")


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    main = df[df["manager"].isin(MANAGERS)].copy()
    agg = {
        "matches": ("date", "count"),
        "goals_against": ("goals_against", "sum"),
        "goals_against_per_match": ("goals_against", "mean"),
        "clean_sheets": ("clean_sheet", "sum"),
        "clean_sheet_rate": ("clean_sheet", "mean"),
    }
    if "shots_on_target_against" in main.columns:
        agg["shots_on_target_against"] = ("shots_on_target_against", "sum")
        agg["shots_on_target_against_per_match"] = ("shots_on_target_against", "mean")
    if "saves" in main.columns:
        agg["saves"] = ("saves", "sum")
        agg["saves_per_match"] = ("saves", "mean")

    summary = main.groupby("manager", sort=False).agg(**agg).reset_index()
    summary["clean_sheet_rate"] *= 100

    # Save% agregado evita a distorção de tirar média simples do percentual jogo a jogo.
    if {"saves", "shots_on_target_against"}.issubset(summary.columns):
        summary["save_pct_aggregated"] = (
            summary["saves"] / summary["shots_on_target_against"] * 100
        )
    if {"goals_against", "shots_on_target_against"}.issubset(summary.columns):
        summary["ga_per_sota"] = (
            summary["goals_against"] / summary["shots_on_target_against"]
        )
        summary["sota_per_goal_against"] = (
            summary["shots_on_target_against"] / summary["goals_against"].replace(0, pd.NA)
        )
    return summary.round(2)


def main() -> None:
    if not MATCHES.exists():
        raise FileNotFoundError(f"Base não encontrada: {MATCHES}")
    matches = prepare_matches(pd.read_csv(MATCHES))
    validate_matches(matches)
    matches = add_goalkeeping(matches)
    MATCH_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    matches.to_csv(MATCH_OUTPUT, index=False)
    summary = summarize(matches)
    summary.to_csv(OUTPUT, index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
