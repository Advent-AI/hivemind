"""Scoring the bench (bench_v23.py) with the D229 ruler, reference v2, exactly as the baseline: structure by code, meaning by hand.
Draw names: L1..L3 = luna-1..3, the stored role-v22 answers re-sifted with the current code; H1..H3 = v23-1..3, the scrubbed
request (the letters H/haiku in score_meaning.py are reused for the v23 draws in this bench only).

    python3 bench_score.py structure      # bench structure.json + reading sheets (v23 rows) in bench-v23-2026-10-29/
    python3 bench_score.py seed-labels    # labels-bench-<set>.txt seeded with the baseline's L labels (H labels are written by hand)
    python3 bench_score.py score          # scores-bench-<set>.json, both sets
"""
import collections
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_meaning as sm  # noqa: E402
import score_week as sw  # noqa: E402

RUN = HERE / 'bench-v23-2026-10-29'
DRAWS = ['luna-1', 'luna-2', 'luna-3', 'v23-1', 'v23-2', 'v23-3']
sm.DRAWS.update({'H1': 'v23-1', 'H2': 'v23-2', 'H3': 'v23-3'})
sm.MODELS.clear()
sm.MODELS.update({'role-v22': ['L1', 'L2', 'L3'], 'role-v23': ['H1', 'H2', 'H3']})


def structure():
    sifted = json.loads((RUN / 'sifted.json').read_text())
    refs = {}
    for name, label in (('reference-week-v2.json', 'week'), ('reference-holdout-v2.json', 'holdout')):
        for art in json.loads((HERE / name).read_text())['articles']:
            refs[art['input_id']] = dict(art, set=label)
    per_item, unmatched, candidates = {}, collections.defaultdict(dict), collections.defaultdict(dict)
    totals = {d: collections.Counter() for d in DRAWS}
    for draw in DRAWS:
        for input_id, art in refs.items():
            rec = sifted.get(draw, {}).get(input_id)
            t = totals[draw]
            if rec is None or rec['sift'] is None:
                t['answers_failed'] += 1
                ev, kept, cands = [], set(), []
            else:
                ev = (rec['answer'] or {}).get('evidence', [])
                kept = {e['id'] for e in rec['sift']['evidence']}
                cands = rec['sift']['candidates']
                t['answers'] += 1
            t['records_written'] += len(ev)
            t['records_kept'] += len(kept)
            raw_c = (rec or {}).get('answer') or {}
            candidates[input_id][draw] = [{k: c.get(k) for k in ('id', 'opens_as', 'object', 'measure', 'scope', 'question', 'due_day', 'year')}
                                          for c in cands]
            candidates[input_id][draw + ':refused'] = [{k: c.get(k) for k in ('id', 'opens_as', 'measure', 'question', 'due_day')}
                                                       for c in raw_c.get('candidates', []) if c['id'] not in {x['id'] for x in cands}]
            items = art.get('statements', []) + [dict(x, weight='exclude') for x in art.get('exclude', [])]
            used = set()
            for item in items:
                hits = [e for e in ev if sw.matches(e['quote'], item)]
                used.update(e['id'] for e in hits)
                k = [e for e in hits if e['id'] in kept]
                state = 'kept' if k else ('refused' if hits else 'omitted')
                per_item.setdefault(f"{input_id}|{item['id']}", {})[draw] = {'state': state, 'records': [
                    {x: e.get(x) for x in ('id', 'one_line', 'speaker', 'original_who', 'original_day', 'tier', 'event_time')} for e in (k or hits)]}
                t[f"{art['set']}:{item['weight']}:{state}"] += 1
            rest = [e for e in ev if e['id'] not in used]
            unmatched[input_id][draw] = [{x: e.get(x) for x in ('id', 'quote', 'one_line', 'speaker', 'tier')} | {'kept': e['id'] in kept} for e in rest]
            t[f"{art['set']}:unmatched_kept"] += sum(1 for e in rest if e['id'] in kept)
    (RUN / 'structure.json').write_text(json.dumps({'per_item': per_item, 'unmatched': unmatched, 'candidates': candidates,
                                                    'totals': {d: dict(c) for d, c in totals.items()}}, ensure_ascii=False, indent=1) + '\n')
    for label in ('week', 'holdout'):
        lines = [f'# Bench reading sheet ({label}), role-v23 draws (v23-1..3) with the reference', '']
        for input_id, art in refs.items():
            if art['set'] != label:
                continue
            lines.append(f"## {input_id}" + (f" · call {art['call_id']}" if 'call_id' in art else ''))
            for item in art.get('statements', []) + [dict(x, weight='exclude') for x in art.get('exclude', [])]:
                lines.append(f"### {item['id']} [{item['weight']}] {item['note'][:160]}")
                for d in DRAWS[3:]:
                    cell = per_item[f"{input_id}|{item['id']}"][d]
                    lines.append(f'- {d}: —' if cell['state'] == 'omitted' else f"- {d}: {cell['state']} " + ' ‖ '.join(
                        f"{r['id']} | {r['tier']} | who={r['original_who']} | day={r['original_day']} | {r['one_line']}" for r in cell['records']))
            for d in DRAWS[3:]:
                rest = unmatched[input_id][d]
                if rest:
                    lines.append(f'- {d} unmatched ({len(rest)}): ' + ' ‖ '.join(f"{e['id']}{'' if e['kept'] else ' [refused]'}: {e['one_line']}" for e in rest))
            for d in DRAWS[3:]:
                cs = candidates[input_id][d]
                if cs:
                    lines.append(f'- {d} candidates: ' + ' ‖ '.join(f"{c['opens_as']}/{c['measure']}: {c['question']} (due {c['due_day']})" for c in cs))
                cr = candidates[input_id][d + ':refused']
                if cr:
                    lines.append(f'- {d} candidates refused by the sift: ' + ' ‖ '.join(f"{c['opens_as']}/{c['measure']}: {c['question']} (due {c['due_day']})" for c in cr))
            for m in art.get('must_propose', []):
                lines.append(f"- REF must propose: {m['gist']}")
            for m in art.get('must_not_propose', []):
                lines.append(f"- REF must not propose: {m}")
            lines.append('')
        (RUN / f'reading-{label}.md').write_text('\n'.join(lines) + '\n')
    keys = sorted({k for c in totals.values() for k in c})
    for k in keys:
        print(k.ljust(34), ' '.join(str(totals[d].get(k, 0)).rjust(7) for d in DRAWS))


def seed_labels():
    """Copy every L (role-v22) label of labels-<set>.txt; H cells there belong to the parked Haiku pass and are left out."""
    for label in ('week', 'holdout'):
        out = [f'# Bench labels ({label}): L1..L3 = role-v22 baseline, copied from labels-{label}.txt (same answers, same record ids);',
               '# H1..H3 = role-v23 bench draws (v23-1..3), read by hand from bench-v23-2026-10-29/reading-' + label + '.md.']
        for raw in (HERE / f'labels-{label}.txt').read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith('#') or line.startswith('@'):
                out.append(raw)
                continue
            if line.startswith('+') or line.startswith('!'):
                if line[1:].strip().startswith('L'):
                    out.append(raw)
                continue
            if line.startswith('?'):
                head, *cells = line.split()
                if line.startswith('?d'):
                    keep = [c for c in cells[1:] if c.startswith('L')]
                    if keep:
                        out.append(' '.join([head, cells[0]] + keep))
                    continue
                keep = [c for c in cells[1:] if c.startswith('L')]
                if keep:
                    out.append(' '.join([head, cells[0]] + keep))
                continue
            item, _, cells = line.partition(' ')
            keep = [m.group(0) for m in re.finditer(r'L[123]:[cpwkx-]!?(?:\([^)]*\))?', cells)]
            if keep:
                out.append(item + ' ' + ' '.join(keep))
        (HERE / f'labels-bench-{label}.txt').write_text('\n'.join(out) + '\n')
        print('seeded', f'labels-bench-{label}.txt')


def score():
    for label in ('week', 'holdout'):
        sm.main(label, 'v2', structure_path=RUN / 'structure.json', labels_path=HERE / f'labels-bench-{label}.txt',
                out_path=RUN / f'scores-{label}.json')


if __name__ == '__main__':
    {'structure': structure, 'seed-labels': seed_labels, 'score': score}[sys.argv[1]]()
