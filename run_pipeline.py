"""Executa coleta, tratamento, análise e visualizações em um comando."""
import subprocess
import sys

# Recorte principal: Campeonato Brasileiro Série A 2026.
SCHEDULE_URL = "https://fbref.com/en/squads/83f55dbe/2026/matchlogs/c24/schedule/Vasco-da-Gama-Scores-and-Fixtures-Serie-A"
KEEPER_URL = "https://fbref.com/en/squads/83f55dbe/2026/matchlogs/c24/keeper/Vasco-da-Gama-Match-Logs-Serie-A"

steps = [
    [sys.executable, "src/collect_fbref.py", "--url", SCHEDULE_URL],
    [sys.executable, "src/collect_goalkeeping.py", "--url", KEEPER_URL],
    [sys.executable, "src/analyze.py"],
    [sys.executable, "src/visualize.py"],
]

for command in steps:
    print("\n>>>", " ".join(command))
    subprocess.run(command, check=True)

print("\nPipeline concluído: dados, resumo e gráficos da Série A atualizados.")
