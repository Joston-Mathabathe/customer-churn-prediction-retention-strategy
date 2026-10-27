from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
for script in ['cleaning.py','eda.py','model.py','business_impact.py']:
 print('Running',script,flush=True)
 subprocess.run([sys.executable,str(root/'src'/script)],cwd=root,check=True)
print('Pipeline completed.')
