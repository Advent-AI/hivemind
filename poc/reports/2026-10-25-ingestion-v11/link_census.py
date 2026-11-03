"""Read the selected sources in completed trial archives; target links are review leads."""
import json
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    'nvidianews:sk-group-and-nvidia-expand-strategic-partnership-across-ai-factories-and-next-generation-memory',
    'nvidianews:naver-nvidia-and-brookfield-to-expand-koreas-national-ai-factory-infrastructure-buildout',
    'nvblog:ai-summit-korea-partners-and-nvidia',
}
archives = [ROOT / '2026-10-25-ingestion-smoke/control-1/archive.sqlite']
archives += [ROOT / '2026-10-25-naver-admission' / name / 'archive.sqlite'
             for name in ('control-1', 'control-2', 'control-3', 'treatment-1', 'treatment-2', 'treatment-3')]
archives += [ROOT / '2026-10-25-ingestion-v11/control-1/archive.sqlite']
rows = []
for path in archives:
    with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as conn:
        count = 0
        for request, answer in conn.execute("select request_json,answer_json from model_calls where purpose='extract'"):
            request, answer = json.loads(request), json.loads(answer)
            match = re.search(r'^\[Item\] id (.+?), category ', request['messages'][1]['content'], re.M)
            assert match, path
            if match[1] not in INPUTS:
                continue
            count += 1
            links = [{'id': e['id'], 'links': e['links'], 'one_line': e['one_line']}
                     for e in answer['evidence'] if {'v3', 'v7'} & set(e['links'])]
            rows.append({'archive': str(path.relative_to(ROOT)), 'input_id': match[1],
                         'links_to_revenue_or_rubin': links})
        assert count > 0, path
assert len(rows) == 12, len(rows)
known = next(r for r in rows if r['archive'] == '2026-10-25-naver-admission/control-3/archive.sqlite')
assert known['links_to_revenue_or_rubin'][0]['links'] == ['v7']
print(json.dumps({
    'scope': 'The three selected sources across completed D174, D177 and D178 trials; links are leads requiring source interpretation, not an automatic global defect count.',
    'extraction_answers': len(rows),
    'answers_with_links_to_v3_or_v7': sum(bool(r['links_to_revenue_or_rubin']) for r in rows),
    'answers': rows,
}, indent=2, ensure_ascii=False))
