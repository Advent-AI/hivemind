"""Freeze a new source-read fourth-step target from the v38 archive."""
import hashlib
import importlib.util
import json
from pathlib import Path
HERE=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit')
SOURCE=HERE/'stage4-scope-arm-prepare-2026-10-29.py'
REFERENCE=HERE/'stage4-empty-history-valar-reference-2026-10-29.md'
RUN=HERE/'stage4-empty-history-valar-source-2026-10-29'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('scope_source',SOURCE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.CASES=[('valar','gnews:ad47330f25c9d5ff84ced7e2','e2',5,'holdout')]
cases=m.build();case=cases['valar-scope'];luna,haiku=m.prior.requests(case)
if case['split']!='holdout' or case['old_ids'] or case['question_ids'] or case['payload']['source_record']['quote'] not in case['payload']['source_article']:
    raise ValueError('holdout source or history differs')
RUN.mkdir(exist_ok=False)
meta={k:v for k,v in case.items() if k!='payload'};meta['request_hashes']={}
for provider,req in [('luna',luna),('haiku',haiku)]:
    path=RUN/('valar-'+provider+'-request.json')
    with path.open('x',encoding='utf-8') as f:json.dump(req,f,ensure_ascii=False,indent=2);f.write('\n')
    meta['request_hashes'][provider]=digest(path)
manifest={'cases':{'valar':meta},'reference_sha256':digest(REFERENCE),'builder_sha256':digest(SOURCE),'prepare_sha256':digest(Path(__file__)),'note':'Source-read holdout previously extracted in v38.'}
with (RUN/'manifest.json').open('x',encoding='utf-8') as f:json.dump(manifest,f,ensure_ascii=False,indent=2);f.write('\n')
print('valar holdout frozen; no model calls')
