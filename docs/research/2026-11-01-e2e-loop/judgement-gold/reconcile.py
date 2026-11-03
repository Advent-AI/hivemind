"""Reconcile the two readers of the judgement ruler (ruler-v1.md §1, §2 item 2): code aligns the two answers per question and writes
gold-v1.json with the agreed entries and the disagreements left open, plus reconcile-v1.md listing every disagreement with both readers'
reasoning and items, for resolution against the material (a resolution and its reason are added to gold-v1.json by hand, each marked; an
unresolved one goes to Alex). Nothing here judges a question.

    python3 reconcile.py            # reader-A.json + reader-B.json -> gold-v1.json (draft) + reconcile-v1.md
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOLERANCE = 0.0    # ranges must overlap; a direction call must match


def rng(answer):
    io = answer.get('implied_outcome') or {}
    return io.get('low'), io.get('high'), io.get('yes_no')


def overlap(a, b):
    (al, ah, _), (bl, bh, _) = a, b
    if None in (al, ah, bl, bh):
        return False
    return max(al, bl) <= min(ah, bh)


def main():
    A = {a['question_id']: a for a in json.loads((HERE / 'reader-A.json').read_text(encoding='utf-8'))['answers']}
    B = {a['question_id']: a for a in json.loads((HERE / 'reader-B.json').read_text(encoding='utf-8'))['answers']}
    questions = json.loads((HERE / 'questions-v1.json').read_text(encoding='utf-8'))['questions']
    gold, lines, agreed = [], ['# Reconciliation of readers A and B, ruler v1\n'], 0
    for q in questions:
        qid, a, b = q['id'], A.get(q['id']), B.get(q['id'])
        entry = {'question_id': qid, 'question': q['question'], 'unit': q['unit'], 'kind': q['kind']}
        if a is None or b is None:
            entry.update(source='missing', status='unresolved', note=f'reader {"A" if a is None else "B"} gave no answer'); gold.append(entry); continue
        if a.get('no_view') and b.get('no_view'):
            entry.update(source='A+B', status='no_view', no_view=True); gold.append(entry); agreed += 1; continue
        same_dir = a.get('direction') == b.get('direction')      # recorded; the ranges decide (ruler-v1 §1: the score is a range overlap)
        ra, rb = rng(a), rng(b)
        if q['unit'] == 'yes/no':
            agree = ra[2] == rb[2] and ra[2] is not None
        else:
            agree = overlap(ra, rb)
        if agree and not a.get('no_view') and not b.get('no_view'):
            agreed += 1
            implied = {'yes_no': ra[2]} if q['unit'] == 'yes/no' else {'low': max(ra[0], rb[0]), 'high': min(ra[1], rb[1])}
            entry.update(source='A+B', status='agreed', direction=a.get('direction') if same_dir else {'A': a.get('direction'), 'B': b.get('direction')}, implied_outcome=implied,
                         reference={'A': a.get('reference'), 'B': b.get('reference')},
                         decisive_items=sorted(set(a.get('decisive_items') or []) | set(b.get('decisive_items') or [])),
                         reasoning={'A': a.get('reasoning'), 'B': b.get('reasoning')})
        else:
            entry.update(source='disagreement', status='unresolved', A=a, B=b)
            lines.append(f'## {qid} {q["question"]}\n')
            for name, ans in (('A', a), ('B', b)):
                io = ans.get('implied_outcome') or {}
                lines.append(f'- **{name}**: no_view {ans.get("no_view")}; direction {ans.get("direction")}; implied {io.get("low")}..{io.get("high")} yes_no {io.get("yes_no")}; '
                             f'confidence {ans.get("confidence")}; items {ans.get("decisive_items")}\n  - reference: {(ans.get("reference") or {}).get("text")}\n'
                             f'  - implied: {io.get("text")}\n  - reasoning: {ans.get("reasoning")}\n  - against: {(ans.get("against") or {}).get("text")}\n')
        gold.append(entry)
    out = {'ruler_version': 1, 'status': 'draft, not reviewed, not signed', 'readers': ['reader-A.json', 'reader-B.json'],
           'agreed': agreed, 'unresolved': sum(1 for g in gold if g['status'] == 'unresolved'), 'entries': gold}
    (HERE / 'gold-v1.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    lines.insert(1, f'agreed {agreed} of {len(questions)}; unresolved {out["unresolved"]}\n')
    (HERE / 'reconcile-v1.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'agreed {agreed} of {len(questions)}; unresolved {out["unresolved"]} (reconcile-v1.md)')


if __name__ == '__main__':
    main()
