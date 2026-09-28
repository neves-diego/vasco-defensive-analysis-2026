"""Gera visualizações comparativas para o projeto."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

SUMMARY = Path("data/processed/manager_summary.csv")
OUT = Path("images")


def bar_metric(df: pd.DataFrame, metric: str, ylabel: str, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(df["manager"], df[metric])
    ax.set_title("Vasco 2026 — comparação defensiva por treinador")
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    ax.spines[["top", "right"]].set_visible(False)
    for bar, value in zip(bars, df[metric]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{value:.2f}",
                ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = pd.read_csv(SUMMARY)
    OUT.mkdir(parents=True, exist_ok=True)
    bar_metric(df, "goals_against_per_match", "Gols sofridos por jogo", "gols_sofridos_por_jogo.png")
    bar_metric(df, "clean_sheet_rate", "Clean sheets (%)", "taxa_clean_sheets.png")


if __name__ == "__main__":
    main()
