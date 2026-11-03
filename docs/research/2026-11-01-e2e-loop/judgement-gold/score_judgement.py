"""D3, the judgement score (ruler-v1.md §1): for each gold question, the run's last judgement on or before the window end; a numeric
question agrees when the gold's implied range overlaps the band of the rung the judge chose, a yes/no question when the answers match.
Prints every question, the totals, the two null baselines (the rung containing the gold's reference figure; always the neutral rung) and
the gold's own reader-disagreement count. Refuses a gold whose sha256 or ruler version is not the one written here (D261).

    python3 score_judgement.py <run folder> [--day 2026-07-14] [--map q23=v25 ...]
"""
import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
RULER_VERSION = 1
GOLD_SHA256 = '636c056d1e4252fa759660803067e6ccd67a81067b012905e918aa9dec4005f2'   # frozen 2026-11-02 (D262); gold-v1.sha256 holds the same value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run'); ap.add_argument('--day', default='2026-07-14'); ap.add_argument('--map', nargs='*', default=[])
    args = ap.parse_args()
    gold_path = HERE / 'gold-v1.json'
    sha = hashlib.sha256(gold_path.read_bytes()).hexdigest()
    gold = json.loads(gold_path.read_text(encoding='utf-8'))
    if gold.get('ruler_version') != RULER_VERSION:
        raise SystemExit(f'gold ruler_version {gold.get("ruler_version")} != scorer {RULER_VERSION}: refused')
    frozen = (HERE / 'gold-v1.sha256').read_text().split()[0] if (HERE / 'gold-v1.sha256').exists() else None
    if GOLD_SHA256 and frozen != GOLD_SHA256:
        raise SystemExit(f'gold-v1.sha256 {frozen} != the frozen value in this scorer {GOLD_SHA256}: refused')
    if frozen and frozen != sha:
        raise SystemExit(f'gold sha256 {sha} != frozen {frozen}: refused')
    corrections = json.loads((HERE / 'corrections-v1.json').read_text()) if (HERE / 'corrections-v1.json').exists() else []
    label = 'FROZEN' if frozen else f'DRAFT, {gold.get("status")}'
    print(f'gold v{RULER_VERSION} sha256 {sha[:16]}… [{label}]; corrections on record, not applied: {len(corrections)}; run {args.run}; window end {args.day}')
    conn = sqlite3.connect(f'file:{args.run}/views.sqlite?mode=ro', uri=True); conn.row_factory = sqlite3.Row
    mapping = {k: v for k, v in (m.split('=') for m in args.map)}
    seeds = {f'q{k:02d}': f'v{k}' for k in range(1, 23)}
    questions = {q['id']: q for q in json.loads((HERE / 'questions-v1.json').read_text(encoding='utf-8'))['questions']}
    for qid, vid in seeds.items():     # the seeds keep their ids in every run: check the text, refuse a run that differs
        row = conn.execute('select question from views where view_id=?', (vid,)).fetchone()
        if not row or row['question'] != questions[qid]['question']:
            raise SystemExit(f'{vid} in the run is not the seed question {qid}: refused')
    mapping = {**seeds, **mapping}
    if 'q23' not in mapping:
        hit = conn.execute("select view_id from views where question like '%Ohio%' and question like '%guarantee%' order by created_seq limit 1").fetchone()
        if hit:
            mapping['q23'] = hit['view_id']
    totals = {'agree': 0, 'disagree': 0, 'no judgement': 0, 'not in run': 0, 'gold open': 0, 'no_view': 0}
    base_lookup = [0, 0]; base_neutral = [0, 0]
    print(f'{"q":<4}{"outcome":<14}{"gold implied":<28}{"judge rung / band":<40}{"lookup":<8}{"neutral":<8}question')
    for entry in gold['entries']:
        qid = entry['question_id']; q = questions[qid]
        if entry.get('no_view'):
            totals['no_view'] += 1; print(f'{qid:<4}{"no_view":<14}{"":<28}{"":<40}{"":<8}{"":<8}{q["question"][:60]}'); continue
        if not entry.get('implied_outcome'):
            totals['gold open'] += 1; print(f'{qid:<4}{"gold open":<14}{"":<28}{"":<40}{"":<8}{"":<8}{q["question"][:60]}'); continue
        resolved = entry.get('resolution') or entry
        implied, direction = resolved['implied_outcome'], resolved.get('direction')
        vid = mapping.get(qid)
        if not vid:
            totals['not in run'] += 1; print(f'{qid:<4}{"not in run":<14}{"":<28}{"":<40}{"":<8}{"":<8}{q["question"][:60]}'); continue
        j = conn.execute('select rung from judgements where view_id=? and publication_day<=? order by judgement_id desc limit 1', (vid, args.day)).fetchone()
        rungs = [dict(r) for r in conn.execute('select position, label, lo, hi from rungs where view_id=? order by position', (vid,))]
        if j is None:
            totals['no judgement'] += 1; print(f'{qid:<4}{"no judgement":<14}{str(implied):<28}{vid + " never judged":<40}{"":<8}{"":<8}{q["question"][:60]}'); continue
        chosen = rungs[j['rung'] - 1]
        if q['unit'] == 'yes/no':
            agree = (chosen['label'].lower() == 'yes') == bool(implied['yes_no'])
            gold_text = 'yes' if implied['yes_no'] else 'no'; band = chosen['label']
            lookup = neutral = None
        else:
            lo, hi = chosen['lo'], chosen['hi']
            agree = (lo is None or implied['high'] >= lo) and (hi is None or implied['low'] < hi)
            gold_text = f'{implied["low"]:,.4g}..{implied["high"]:,.4g}'; band = f'{lo if lo is not None else "-inf"}..{hi if hi is not None else "inf"}'
            ref = ((entry.get('reference') or {}).get('A') or {}).get('value') if isinstance(entry.get('reference'), dict) and 'A' in entry['reference'] else (entry.get('reference') or {}).get('value')
            lookup = None
            if ref is not None:
                for r in rungs:
                    if (r['lo'] is None or ref >= r['lo']) and (r['hi'] is None or ref < r['hi']):
                        lookup = (r['lo'] is None or implied['high'] >= r['lo']) and (r['hi'] is None or implied['low'] < r['hi']); break
            neutral = None
            n = next((r for r in rungs if r['label'].lower() == 'neutral'), None)
            if n:
                neutral = (n['lo'] is None or implied['high'] >= n['lo']) and (n['hi'] is None or implied['low'] < n['hi'])
        totals['agree' if agree else 'disagree'] += 1
        if lookup is not None:
            base_lookup[0] += lookup; base_lookup[1] += 1
        if neutral is not None:
            base_neutral[0] += neutral; base_neutral[1] += 1
        print(f'{qid:<4}{("agree" if agree else "DISAGREE"):<14}{gold_text:<28}{(vid + " rung " + str(j["rung"]) + " " + chosen["label"][:12] + " " + band)[:39]:<40}'
              f'{("" if lookup is None else ("yes" if lookup else "no")):<8}{("" if neutral is None else ("yes" if neutral else "no")):<8}{q["question"][:60]}')
    judged = totals['agree'] + totals['disagree']
    print(f'\ntotals: {totals}; agreement {totals["agree"]}/{judged} of judged questions')
    print(f'null baselines: the rung containing the gold reference agrees {base_lookup[0]}/{base_lookup[1]}; always neutral agrees {base_neutral[0]}/{base_neutral[1]}')
    noise = (gold.get('readers') or {}).get('stick_noise') or {}
    print(f'gold = reader B (D262); control reader A differs on {len(noise.get("range_or_yesno_disagreements", []))} questions by range or yes/no and on {len(noise.get("direction_label_splits", []))} direction labels; [{label}]')


if __name__ == '__main__':
    main()
