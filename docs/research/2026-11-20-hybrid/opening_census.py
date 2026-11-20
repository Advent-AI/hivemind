"""Phase 2, step 1 (D685): where each of the 32 frozen matters falls out of the old system's opening, per old draw ($0, read-only).

  python3 opening_census.py            # writes poc/data/hybrid-2026-11-20/opening-census.json and prints one block per matter

For each matter and old draw, from the matter's articles (the frozen census numbering): the candidate questions the extraction proposed
from those articles and what matching did with each (opened new, merged into an existing question, succession, or not opened with its
reason, or refused by a check), the evidence written from those articles and the questions it was linked to, and the evidence dropped
with no home. The mapping's verdict (which old question covers the matter) is printed beside it."""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import judge_probe as jp  # noqa: E402

CENSUS = jp.ROOT / 'docs/research/2026-11-17-product-comparison/stage0/census'
MAPPING = jp.DIAG / 'mapping-out/mapping.json'
OLD = ('old-1', 'old-2', 'old-3')


def trace(draw, inputs):
    views, _ = jp.store_paths(draw)
    conn = jp.readonly(views)
    question = {r['view_id']: r['question'] for r in conn.execute('select view_id, question from views')}
    out = {'candidates': [], 'linked': Counter(), 'no_home': 0, 'evidence': 0}
    for input_id in inputs:
        handover = conn.execute('select handover_json from handovers where input_id=?', (input_id,)).fetchone()
        if handover is None:
            out.setdefault('not_handed_over', []).append(input_id)
            continue
        h = json.loads(handover[0])
        out['evidence'] += len(h['evidence'])
        out['no_home'] += sum(1 for d in h['dropped'] if d[1] == 'no home')
        decided = {}
        for r in conn.execute('select decisions_json, checks_json from match_records where input_id=? order by call_no', (input_id,)):
            d = json.loads(r['decisions_json']) if r['decisions_json'] else {}
            checks = json.loads(r['checks_json']) if r['checks_json'] else {}
            for c in d.get('candidates', []):
                decided[c['id']] = {'outcome': c.get('outcome'), 'target': c.get('target_view_id'), 'reason': c.get('reason', '')[:160]}
            for cid, why in (checks.get('not_opened') or {}).items():
                decided.setdefault(cid, {})['not_opened'] = why
            for refusal in checks.get('refusals') or []:
                cid = refusal.split(':', 1)[0].replace('candidate ', '').strip()
                decided.setdefault(cid, {})['refused'] = refusal[:200]
        for c in h['candidates']:
            fate = decided.get(c['id'], {'outcome': 'no match record'})
            target = fate.get('target')
            out['candidates'].append({'input': input_id, 'object': c['object'], 'kind': c['kind'], 'question': c['question'],
                                      'fate': fate, 'target_question': question.get(target) if target else None})
        for r in conn.execute('select distinct l.view_id from evidence_sources s join evidence_links l on l.evidence_id = s.evidence_id '
                              'where s.input_id=?', (input_id,)):
            out['linked'][question.get(r['view_id'], r['view_id'])] += 1
    out['linked'] = dict(out['linked'].most_common(8))
    return out


def main():
    matters = json.loads((CENSUS / 'matters.json').read_text())['matters']
    numbering = json.loads((CENSUS / 'numbering.json').read_text())
    mapping = json.loads(MAPPING.read_text())['mapping']
    report = []
    for m in matters:
        inputs = [numbering[str(k)] for k in m['articles']]
        covered = {d: mapping.get(d, {}).get(m['matter'], []) for d in OLD}
        row = {'matter': m['matter'], 'name': m['name'], 'question': m['question'], 'company_figure': m['company_figure'],
               'articles': len(inputs), 'covered_by': covered, 'draws': {d: trace(d, inputs) for d in OLD}}
        report.append(row)
        print(f"\n=== {m['matter']} {'[company figure] ' if m['company_figure'] else ''}{m['name']} | {len(inputs)} articles | covered: "
              + '; '.join(f"{d}: {[q['question'] + ('' if q['covers'] is True else ' (' + str(q['covers']) + ')') for q in qs]}" for d, qs in covered.items()))
        for d, t in row['draws'].items():
            print(f"  {d}: evidence {t['evidence']}, no home {t['no_home']}, candidates {len(t['candidates'])}")
            for c in t['candidates']:
                f = c['fate']
                print(f"    - [{c['object']}/{c['kind']}] {c['question'][:110]} -> {f.get('outcome')}"
                      + (f" into: {c['target_question'][:80]}" if c['target_question'] else '')
                      + (f" | NOT OPENED: {f['not_opened'][:90]}" if f.get('not_opened') else '') + (f" | REFUSED: {f['refused'][:90]}" if f.get('refused') else ''))
            if not t['candidates']:
                print(f"    linked to: {list(t['linked'].items())[:4]}")
    (jp.OUT / 'opening-census.json').write_text(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
