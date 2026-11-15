"""One-command reproduction of W07, W11 and validator probe experiments."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for cmd in [["-m","src.analyze"],["run_all.py"],["-m","src.probes"]]:
 print("RUN",cmd,flush=True)
 subprocess.run([sys.executable,*cmd],cwd=root,check=True)
print("REPRODUCED all planned conditions")
