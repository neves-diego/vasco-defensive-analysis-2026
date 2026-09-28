"""Executa as etapas locais depois da coleta dos dados."""
import subprocess
import sys

for script in ["src/analyze.py", "src/visualize.py"]:
    print(f"\n>>> Executando {script}")
    subprocess.run([sys.executable, script], check=True)

print("\nPipeline concluído.")
