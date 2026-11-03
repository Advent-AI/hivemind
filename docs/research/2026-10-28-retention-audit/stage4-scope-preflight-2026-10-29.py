"""Record the precise local inputs and output of the scope experiment's preflight."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
DATA=Path('/Users/lchingen/hivemind/poc/data')
RUN=ROOT/'docs/research/2026-10-28-retention-audit/stage4-scope-arm-2026-10-29'
SCRIPT=ROOT/'scripts/preflight.py'
inputs={'archive':DATA/'english-v38-nvda-1w-2026-10-28/archive.sqlite',
        'items':DATA/'items-nvda-2026-07-01-10-27.sqlite',
        'views':DATA/'english-v38-nvda-1w-2026-10-28/views.sqlite',
        'universe':ROOT/'poc/universe.json','script':SCRIPT}


def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


output=RUN/'preflight-v2-2026-10-29.log';manifest=RUN/'preflight-v2-manifest-2026-10-29.json'
if output.exists() or manifest.exists():raise ValueError('preflight record already exists')
if any(not p.is_file() for p in inputs.values()):raise ValueError('preflight input missing')
before={k:digest(p) for k,p in inputs.items()}
args=[sys.executable,str(SCRIPT),'--archive',str(inputs['archive']),'--items',str(inputs['items']),
      '--views',str(inputs['views']),'--universe',str(inputs['universe'])]
result=subprocess.run(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
after={k:digest(p) for k,p in inputs.items()}
if before!=after:raise ValueError('preflight input changed during run')
with output.open('xb') as f:f.write(result.stdout);f.write(result.stderr)
record={'arguments':args,'input_paths':{k:str(p) for k,p in inputs.items()},'input_sha256':before,
        'output_sha256':digest(output),'exit_code':result.returncode,
        'note':'Replays v38 extraction and matching; not a fourth-step write-path acceptance.'}
with manifest.open('x',encoding='utf-8') as f:json.dump(record,f,ensure_ascii=False,indent=2);f.write('\n')
if result.returncode:raise SystemExit(result.returncode)
print('preflight exit',result.returncode,'exact inputs and output recorded')
