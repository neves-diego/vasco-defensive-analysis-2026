"""Gera visualizações comparativas para o projeto Vasco Defensive Analysis 2026."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

SUMMARY = Path("data/processed/manager_summary.csv")
MATCHES = Path("data/processed/serie_a_matches_with_manager.csv")
OUT = Path("images")
MANAGERS = ["Fernando Diniz", "Renato Gaúcho", "Pedro Emanuel"]


def bar_metric(df: pd.DataFrame, metric: str, ylabel: str, filename: str, decimals: int = 2) -> None:
    plot = df[df["manager"].isin(MANAGERS)].copy()
    plot["manager"] = pd.Categorical(plot["manager"], categories=MANAGERS, ordered=True)
    plot = plot.sort_values("manager")

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(plot["manager"].astype(str), plot[metric])
    ax.set_title("Vasco 2026 — comparação defensiva por treinador")
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.2)

    for bar, value in zip(bars, plot[metric]):
        if pd.notna(value):
            label = f"{value:.{decimals}f}"
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), label,
                    ha="center", va="bottom")

    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=200, bbox_inches="tight")
    plt.close(fig)


def renato_pedro_comparison(df: pd.DataFrame) -> None:
    """Gráfico-síntese da principal hipótese: volume permitido x eficiência do goleiro."""
    managers = ["Renato Gaúcho", "Pedro Emanuel"]
    plot = df[df["manager"].isin(managers)].set_index("manager").reindex(managers)

    required = ["shots_on_target_against_per_match", "goals_against_per_match", "save_pct_aggregated"]
    if plot.empty or not set(required).issubset(plot.columns):
        return

    renato = plot.loc["Renato Gaúcho"]
    pedro = plot.loc["Pedro Emanuel"]
    sota_change = (pedro["shots_on_target_against_per_match"] / renato["shots_on_target_against_per_match"] - 1) * 100
    ga_change = (pedro["goals_against_per_match"] / renato["goals_against_per_match"] - 1) * 100

    fig, ax = plt.subplots(figsize=(10, 5.8))
    x = [0, 1]
    width = 0.34
    bars1 = ax.bar([i - width / 2 for i in x],
                   [renato["shots_on_target_against_per_match"], pedro["shots_on_target_against_per_match"]],
                   width, label="SoTA/jogo")
    bars2 = ax.bar([i + width / 2 for i in x],
                   [renato["goals_against_per_match"], pedro["goals_against_per_match"]],
                   width, label="GA/jogo")

    ax.set_xticks(x, managers)
    ax.set_ylabel("Por partida")
    ax.set_title("Com Pedro, o Vasco permite menos chutes no alvo")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    ax.legend(frameon=False)

    for bars in (bars1, bars2):
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f"{bar.get_height():.2f}", ha="center", va="bottom")

    note = (
        f"SoTA/jogo: {sota_change:.1f}% | GA/jogo: {ga_change:.1f}%\n"
        f"Save% agregado: {renato['save_pct_aggregated']:.1f}% → {pedro['save_pct_aggregated']:.1f}%"
    )
    ax.text(0.5, -0.18, note, transform=ax.transAxes, ha="center", va="top", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "renato_vs_pedro_sistema_defensivo.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def rolling_goals_against() -> None:
    if not MATCHES.exists():
        return

    df = pd.read_csv(MATCHES, parse_dates=["date"])
    df = df[df["manager"].isin(MANAGERS)].sort_values("date").copy()
    if df.empty:
        return

    df["ga_rolling_3"] = df["goals_against"].rolling(3, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(df["date"], df["goals_against"], marker="o", alpha=0.45, label="Gols sofridos")
    ax.plot(df["date"], df["ga_rolling_3"], linewidth=2.2, label="Média móvel (3 jogos)")

    previous = None
    for _, row in df.iterrows():
        if row["manager"] != previous:
            ax.axvline(row["date"], linestyle="--", alpha=0.35)
            ax.text(row["date"], ax.get_ylim()[1] * 0.92, row["manager"], rotation=90,
                    va="top", ha="right", fontsize=8)
            previous = row["manager"]

    ax.set_title("Vasco 2026 — evolução dos gols sofridos no Brasileirão")
    ax.set_ylabel("Gols sofridos")
    ax.set_xlabel("")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    ax.legend(frameon=False)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUT / "evolucao_gols_sofridos.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    if not SUMMARY.exists():
        raise FileNotFoundError(f"Resumo não encontrado: {SUMMARY}. Execute src/analyze.py primeiro.")

    df = pd.read_csv(SUMMARY)
    OUT.mkdir(parents=True, exist_ok=True)

    bar_metric(df, "goals_against_per_match", "Gols sofridos por jogo", "gols_sofridos_por_jogo.png")
    bar_metric(df, "clean_sheet_rate", "Clean sheets (%)", "taxa_clean_sheets.png", decimals=1)

    if "shots_on_target_against_per_match" in df.columns:
        bar_metric(df, "shots_on_target_against_per_match", "Chutes no alvo sofridos por jogo", "sota_por_jogo.png")
    if "save_pct_aggregated" in df.columns:
        bar_metric(df, "save_pct_aggregated", "Save% agregado", "save_pct_agregado.png", decimals=1)
    if "sota_per_goal_against" in df.columns:
        bar_metric(df, "sota_per_goal_against", "SoTA necessários por gol sofrido", "sota_por_gol_sofrido.png")

    renato_pedro_comparison(df)
    rolling_goals_against()
    print(f"Visualizações salvas em {OUT.resolve()}")


if __name__ == "__main__":
    main()
