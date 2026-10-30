"""Continue stored date-arm conversations to understand why sourced dates were left blank."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('account_probe',HERE/'haiku-model-account-probe-2026-10-29.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
p.RUN=HERE/'haiku-known-date-probe-2026-10-29'
p.CASES={
 'policy':('haiku-date-arm-2026-10-29/policy-arm-request.json','haiku-date-arm-2026-10-29/policy-arm-2.json',
    'In the prior answer you left original_day empty for both Scott Bessent and Michael Kratsios, but event_time gave July 21 and July 22. Which task instruction and source wording explain those choices? Give the relevant source lines and two alternative interpretations you did not select. Distinguish stated information from assumptions; do not reveal hidden reasoning.'),
 'valar1':('haiku-date-arm-2026-10-29/valar_holdout-arm-request.json','haiku-date-arm-2026-10-29/valar_holdout-arm-1.json',
    'In your prior e1, the summary says the Valar announcement was on 2026-07-01 and event_time also gives that day, but original_day is empty. Which task instruction and source wording explain this distinction? Give the relevant source lines and two alternative interpretations you did not select. Distinguish stated information from assumptions; do not reveal hidden reasoning.'),
 'valar2':('haiku-date-arm-2026-10-29/valar_holdout-arm-request.json','haiku-date-arm-2026-10-29/valar_holdout-arm-2.json',
    'In your prior e1, the summary says the Valar announcement was Wednesday 2026-07-01 and event_time also gives that day, but original_day is empty. Which task instruction and source wording explain this distinction? Give the relevant source lines and two alternative interpretations you did not select. Distinguish stated information from assumptions; do not reveal hidden reasoning.')}


def launch():
 assert not (p.RUN/'run.pid').exists()
 with (p.RUN/'run.log').open('x') as log:
  child=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(p.probe.previous.ROOT/'src')))
 (p.RUN/'run.pid').write_text(str(child.pid)+'\n');print('detached pid',child.pid)

if __name__=='__main__':{'prepare':p.prepare,'worker':p.worker,'launch':launch}[sys.argv[1]]()
