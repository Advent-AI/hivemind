"""Freeze one source-read stage-4 holdout using the existing verified v38 builder."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit')
SOURCE=HERE/'stage4-scope-arm-prepare-2026-10-29.py'
REFERENCE=HERE/'stage4-fact-inference-science-reference-2026-10-29.md'
RUN=HERE/'stage4-fact-inference-science-source-2026-10-29'

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('scope_source',SOURCE)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.CASES=[('science','gnews:8f5a03f1dde395491fc3814b','e5',4,'holdout')]
cases=module.build();case=cases['science-scope'];luna,haiku=module.prior.requests(case)
if case['split']!='holdout' or case['old_ids'] or case['question_ids'] or case['payload']['source_record']['quote'] not in case['payload']['source_article']:
    raise ValueError('holdout source or history differs')
RUN.mkdir(exist_ok=False)
meta={k:v for k,v in case.items() if k!='payload'};meta['request_hashes']={}
for provider,request in [('luna',luna),('haiku',haiku)]:
    path=RUN/('science-'+provider+'-request.json')
    with path.open('x',encoding='utf-8') as f:json.dump(request,f,ensure_ascii=False,indent=2);f.write('\n')
    meta['request_hashes'][provider]=digest(path)
manifest={'cases':{'science':meta},'reference_sha256':digest(REFERENCE),'builder_sha256':digest(SOURCE),
          'prepare_sha256':digest(Path(__file__)),'note':'Source-read holdout; article previously extracted in v38.'}
with (RUN/'manifest.json').open('x',encoding='utf-8') as f:json.dump(manifest,f,ensure_ascii=False,indent=2);f.write('\n')
print('science holdout frozen; no model calls')
