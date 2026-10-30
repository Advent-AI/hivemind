"""Scoring of the gpt-6-luna one-change arms (luna_arms.py), written before any arm answer is read.

Pre-registered judgements (the same rules as the D229 baseline, reference v2, D231-D233):
- A1, A2 (question pages): on the target pages {6, 24, 34, 377, 7, 140, 260, 381} every candidate the answer wrote (kept or
  refused by the sift) is judged ruled-out or not by the article's must_not_propose and the standard's §6 tests; on the
  guard pages every must_propose item is y when a candidate asks it (a sift-refused one counted apart).
- C1, C2 (evidence pages): code counts the records kept on the pages whose reference keeps nothing {355, 357, 200, 382, 378,
  396, 4} and the unmatched records kept on the partner pages {381, 277, 79, 6, 210, 83}; core and supporting items on all
  C pages are read as c/p/w/- from the records that carry them.
- V: w108-4 and w209-4 read as c/p/-; candidates on the V pages checked for price-target theses.
- G: w209-2 read (the revenue measure kept and not denied; D233 period rule).
blind writes one reading sheet per group with each page's draws under opaque codes (control and arms shuffled); the code
key is a separate file opened only after the labels are written. count prints what code can count, per condition.

    python3 luna_arm_score.py blind     # sheets + key in luna-arms-2026-10-29/score/
    python3 luna_arm_score.py count     # code counts per condition
"""
import collections
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import luna_arms as la  # noqa: E402
import score_week as sw  # noqa: E402

OUT = la.RUN / 'score'
NOTHING_PAGES = [355, 357, 200, 382, 378, 396, 4]
PARTNER_PAGES = [381, 277, 79, 6, 210, 83]
QUESTION_TARGETS = [6, 24, 34, 377, 7, 140, 260, 381]
GROUPS = {'A': (['control', 'A1', 'A2'], la.QUESTION_PAGES), 'C': (['control', 'C1', 'C2'], la.JUNK_PAGES),
          'V': (['control', 'V'], [108, 209]), 'G': (['control', 'G'], [209])}


def references():
    refs = {}
    for name in ('reference-week-v2.json',):
        for art in json.loads((HERE / name).read_text())['articles']:
            refs[art['input_id']] = art
    return refs


def answer(sifted, cond, draw, input_id):
    rec = sifted.get(f'{cond}-{draw}', {}).get(input_id)
    if rec is None or rec['sift'] is None:
        return None
    kept_ids = {e['id'] for e in rec['sift']['evidence']}
    kept_c = {c['id'] for c in rec['sift']['candidates']}
    evidence = [dict(e, kept=e['id'] in kept_ids) for e in rec['answer'].get('evidence', [])]
    cands = [dict(c, kept=c['id'] in kept_c) for c in rec['answer'].get('candidates', [])]
    return evidence, cands


def cells(art, evidence):
    out, used = {}, set()
    for item in art.get('statements', []):
        hits = [e for e in evidence if sw.matches(e['quote'], item)]
        used.update(e['id'] for e in hits)
        out[item['id']] = hits
    return out, [e for e in evidence if e['id'] not in used]


def blind():
    OUT.mkdir(parents=True, exist_ok=True)
    sifted = json.loads((la.RUN / 'sifted.json').read_text())
    refs = references()
    ids = la.input_ids()
    rng = random.Random(la.SEED)
    key = {}
    for group, (conds, pages) in GROUPS.items():
        lines = [f'# Reading sheet {group} (conditions hidden behind codes)', '']
        for page in pages:
            input_id = ids[page]
            art = refs[input_id]
            slots = [(c, d) for c in conds for d in range(1, la.DRAWS + 1)]
            rng.shuffle(slots)
            lines.append(f'## call {page} · {input_id}')
            for item in art.get('statements', []):
                if item['weight'] in ('core', 'supporting'):
                    lines.append(f"- REF {item['id']} [{item['weight']}] {item['note'][:150]}")
            for m in art.get('must_propose', []):
                lines.append(f"- REF must propose: {m['gist']}")
            for m in art.get('must_not_propose', []):
                lines.append(f"- REF must not propose: {m}")
            for n, (cond, draw) in enumerate(slots):
                code = f'{group}{page}-{chr(97 + n)}'
                key[code] = [cond, draw]
                got = answer(sifted, cond, draw, input_id)
                if got is None:
                    lines.append(f'### {code}: no sifted answer')
                    continue
                evidence, cands = got
                carried, rest = cells(art, evidence)
                lines.append(f'### {code}: records {sum(e["kept"] for e in evidence)} kept of {len(evidence)}')
                if group in ('C', 'V', 'G'):
                    for item_id, hits in carried.items():
                        if hits:
                            lines.append(f'  - {item_id}: ' + ' ‖ '.join(f"{e['id']}{'' if e['kept'] else ' [refused]'} | {e['one_line']}" for e in hits))
                    lines.append('  - unmatched: ' + ' ‖ '.join(f"{e['id']}{'' if e['kept'] else ' [refused]'}: {e['one_line']}" for e in rest))
                for c in cands:
                    lines.append(f"  - cand {c['id']}{'' if c['kept'] else ' [REFUSED BY SIFT]'} {c.get('opens_as')}/{c.get('measure')} due {c['due_day']}: {c['question']}")
            lines.append('')
        (OUT / f'sheet-{group}.md').write_text('\n'.join(lines) + '\n')
    (OUT / 'key.json').write_text(json.dumps(key, indent=1) + '\n')
    print('sheets', sorted(GROUPS), 'codes', len(key))


def count():
    sifted = json.loads((la.RUN / 'sifted.json').read_text())
    refs = references()
    ids = la.input_ids()
    table = collections.defaultdict(collections.Counter)
    for cond in ['control'] + list(la.ARMS):
        pages = la.control_pages() if cond == 'control' else la.ARMS[cond]['pages']
        for page in pages:
            input_id = ids[page]
            for draw in range(1, la.DRAWS + 1):
                got = answer(sifted, cond, draw, input_id)
                if got is None:
                    table[cond]['missing answers'] += 1
                    continue
                evidence, cands = got
                carried, rest = cells(refs[input_id], evidence)
                kept = sum(e['kept'] for e in evidence)
                if page in la.JUNK_PAGES:
                    table[cond]['records kept, C pages'] += kept
                if page in NOTHING_PAGES:
                    table[cond]['records kept, nothing-to-keep pages'] += kept
                if page in PARTNER_PAGES:
                    table[cond]['unmatched kept, partner pages'] += sum(e['kept'] for e in rest)
                if page in la.QUESTION_PAGES:
                    table[cond]['candidates, A pages'] += len(cands)
                if page in QUESTION_TARGETS:
                    table[cond]['candidates, A target pages'] += len(cands)
                table[cond]['quote refusals'] += sum(not e['kept'] for e in evidence)
                table[cond]['candidates refused by sift'] += sum(not c['kept'] for c in cands)
    for cond, c in table.items():
        print(cond, dict(c))


if __name__ == '__main__':
    {'blind': blind, 'count': count}[sys.argv[1]]()
