"""Análise defensiva do Vasco no Brasileirão 2026."""
from pathlib import Path
import pandas as pd

MATCHES = Path("data/processed/vasco_matches_2026.csv")
KEEPERS = Path("data/processed/vasco_goalkeeping_2026.csv")
OUTPUT = Path("data/processed/manager_summary.csv")
MATCH_OUTPUT = Path("data/processed/serie_a_matches_with_manager.csv")

# Recortes baseados no técnico efetivamente à beira do campo.
# Diniz: até 22/02; Renato estreia em 12/03; Pedro estreia em 16/07.
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
    df = df.dropna(subset=["date", "goals_against"])
    if "competition" in df.columns:
        df = df[df["competition"].map(is_serie_a)]
    df["manager"] = df["date"].apply(assign_manager)
    df["clean_sheet"] = (df["goals_against"] == 0).astype(int)
    return df.sort_values("date")


def add_goalkeeping(matches: pd.DataFrame) -> pd.DataFrame:
    if not KEEPERS.exists():
        return matches
    keepers = pd.read_csv(KEEPERS)
    keepers["date"] = pd.to_datetime(keepers["date"], errors="coerce")
    if "competition" in keepers.columns:
        keepers = keepers[keepers["competition"].map(is_serie_a)]
    cols = ["date", "opponent", "shots_on_target_against", "saves", "save_pct"]
    cols = [c for c in cols if c in keepers.columns]
    keys = [c for c in ["date", "opponent"] if c in matches.columns and c in keepers.columns]
    return matches.merge(keepers[cols], on=keys, how="left") if keys else matches


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    main = df[df["manager"].isin(MANAGERS)].copy()
    agg = {
        "date": ("date", "count"),
        "goals_against": ("goals_against", "sum"),
        "goals_against_per_match": ("goals_against", "mean"),
        "clean_sheets": ("clean_sheet", "sum"),
        "clean_sheet_rate": ("clean_sheet", "mean"),
    }
    if "shots_on_target_against" in main.columns:
        agg["shots_on_target_against_per_match"] = ("shots_on_target_against", "mean")
    if "save_pct" in main.columns:
        agg["save_pct"] = ("save_pct", "mean")
    summary = main.groupby("manager", sort=False).agg(**agg).reset_index()
    summary = summary.rename(columns={"date": "matches"})
    summary["clean_sheet_rate"] = summary["clean_sheet_rate"] * 100
    return summary.round(2)


def main() -> None:
    if not MATCHES.exists():
        raise FileNotFoundError(f"Base não encontrada: {MATCHES}")
    matches = prepare_matches(pd.read_csv(MATCHES))
    matches = add_goalkeeping(matches)
    MATCH_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    matches.to_csv(MATCH_OUTPUT, index=False)
    summary = summarize(matches)
    summary.to_csv(OUTPUT, index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
