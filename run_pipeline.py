"""Executa coleta, tratamento, análise e visualizações em um comando."""
import subprocess
import sys

SCHEDULE_URL = "https://fbref.com/en/squads/83f55dbe/2026/matchlogs/schedule/Vasco-da-Gama-Scores-and-Fixtures"
KEEPER_URL = "https://fbref.com/en/squads/83f55dbe/2026/matchlogs/all_comps/keeper/Vasco-da-Gama-Match-Logs-All-Competitions"

steps = [
    [sys.executable, "src/collect_fbref.py", "--url", SCHEDULE_URL],
    [sys.executable, "src/collect_goalkeeping.py", "--url", KEEPER_URL],
    [sys.executable, "src/analyze.py"],
    [sys.executable, "src/visualize.py"],
]

for command in steps:
    print("\n>>>", " ".join(command))
    subprocess.run(command, check=True)

print("\nPipeline concluído: dados, resumo e gráficos atualizados.")
