"""Freeze two source-read research holdouts at the historical sequence; no model calls."""
import hashlib
import json
import re
import sqlite3
from pathlib import Path

from hivemind import config, extraction, model, research_context, universe

ROOT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
DATA = Path('/Users/lchingen/hivemind/poc/data')
WEEK = DATA / 'english-v38-nvda-1w-2026-10-28'
OUT = ROOT / 'docs/research/2026-10-28-retention-audit/stage4-holdout-context-2026-10-29.json'
CASES = [('cooling_capacity', 'gnews:9a13ec8bfdc32e585c1f0604', 'e1'),
         ('game_marketing', 'nvblog:geforce-now-thursday-july-2026-games-list', 'e1')]

uni = universe.load(str(ROOT/'poc/universe.json'))
cfg = config.load(str(ROOT/'poc/config/poc-v38.json'))
results = []
with sqlite3.connect(f'file:{DATA}/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True) as items, \
     sqlite3.connect(f'file:{WEEK}/views.sqlite?mode=ro', uri=True) as views, \
     sqlite3.connect(f'file:{WEEK}/archive.sqlite?mode=ro', uri=True) as archive:
    items.row_factory = sqlite3.Row
    calls = list(archive.execute("select call_id,request_json,answer_json from model_calls where purpose='extract' and answer_json is not null and request_sha256 not like '%:%'"))
    for name, input_id, target_id in CASES:
        row = items.execute('select * from items where input_id=?', (input_id,)).fetchone()
        seqs = views.execute('select seq from handovers where input_id=?', (input_id,)).fetchall()
        if row is None or len(seqs) != 1:
            raise ValueError('missing or ambiguous historical item')
        item = dict(row)
        item['object_identifiers'] = json.loads(item['object_identifiers'])
        candidates = []
        for call_id, encoded, answer in calls:
            request = json.loads(encoded)
            user = next(m['content'] for m in request['messages'] if m['role'] == 'user')
            match = re.search(r'\[Item\] id (\S+?), category ', user)
            if match and match.group(1) == input_id:
                candidates.append((call_id, request, json.loads(answer)))
        if len(candidates) != 1:
            raise ValueError('missing or ambiguous extraction call')
        call_id, request, answer = candidates[0]
        setting, system, user, schema = extraction.request_for(cfg, item, item['text'], [], uni, [])
        built = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
        if model.request_identity(built)[1] != model.request_identity(request)[1] or model.check_schema(answer, schema):
            raise ValueError('stored request or answer differs from production')
        evidence, candidates, dropped, groups = extraction.sift_with_groups(answer, item, item['text'], set(), uni,
            english=True, shown_group_ids=(), version='v22', keep_unlinked=True)
        target = [e for e in evidence if e['id'] == target_id]
        if len(target) != 1 or target[0]['quote'] not in item['text']:
            raise ValueError('target missing or quote changed')
        seq = seqs[0][0]
        objects = [x['value'] for x in item['object_identifiers'] if uni.has(x['value'])]
        with research_context.Reader(str(WEEK/'views.sqlite'), seq, objects, uni) as reader:
            catalog = reader.catalog()
            expanded = reader.expand([q['view_id'] for q in catalog['questions']])
        if any(e['created_seq'] >= seq for e in expanded['evidence']):
            raise ValueError('future evidence')
        results.append({'case':name,'input_id':input_id,'sequence':seq,'source':item['text'],
            'source_sha256':hashlib.sha256(item['text'].encode()).hexdigest(),'title':item['title'],
            'publisher':item['publisher'],'publication_day':item['publication_day'],
            'extraction_call_id':call_id,'target':target[0],'other_evidence':[e for e in evidence if e['id'] != target_id],
            'historical_catalog':catalog,'full_historical_expansion':expanded})
payload = {'note':'Source-read research holdouts; model-authored references stored separately. Not independently human gold.', 'cases':results}
if OUT.exists():
    if json.loads(OUT.read_text()) != payload:
        raise ValueError('preserve existing data and investigate difference')
else:
    with OUT.open('x', encoding='utf-8') as f:
        json.dump(payload,f,ensure_ascii=False,indent=2);f.write('\n')
for r in results:
    print(r['case'], 'sequence',r['sequence'],'questions',len(r['historical_catalog']['questions']),
          'historical evidence',len(r['full_historical_expansion']['evidence']),
          'target',r['target']['id'])
