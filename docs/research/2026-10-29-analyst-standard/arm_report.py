"""Side-by-side sheet for the one-change arms: per arm, its target pages, control draws against arm draws, with what code can
count (candidates, due days, sift drops, records) and the records a hand read must judge. Writes arms-2026-10-29/sheet.md.

    python3 arm_report.py
"""
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import arm_week as aw  # noqa: E402

FOCUS = {   # per arm: which records to show in full (regex over one_line), the rest only counted
    'V': r'(times|multiple|P/E|price target|\$3\d\d\b|valu)',
    'D': r'Kyber|Rubin Ultra|NVL144',
    'Q': r'$^',
    'G': r'(82%|41%)',
    'L': r'$^',
}


def main():
    sifted = json.loads((aw.RUN / 'sifted.json').read_text())
    ids = aw.input_ids()
    lines = ['# One-change arms beside a fresh control (Haiku 5.5, 16k, three draws each)', '']
    for name, arm in aw.ARMS.items():
        old, new = arm['edit']
        lines += [f'## Arm {name}: {arm["failure"]}', f'- old: {old}', f'- new: {new}', '']
        for page in arm['pages']:
            input_id = ids[page]
            lines.append(f'### call {page} · {input_id}')
            for which in ('control', name):
                for draw in range(1, aw.DRAWS + 1):
                    rec = sifted.get(f'{which}-{draw}', {}).get(input_id)
                    tag = f'{which}-{draw}'
                    if rec is None or rec['sift'] is None:
                        lines.append(f'- {tag}: NO SIFTED ANSWER ({None if rec is None else rec["error"] or rec["schema_errors"]})')
                        continue
                    raw_c = rec['answer'].get('candidates', [])
                    kept_c = {c['id'] for c in rec['sift']['candidates']}
                    ev = rec['sift']['evidence']
                    drops = [f'{i}: {why[:70]}' for i, why in rec['sift']['dropped']]
                    lines.append(f'- {tag}: evidence kept {len(ev)} of {len(rec["answer"].get("evidence", []))}; candidates kept {len(kept_c)} of {len(raw_c)}'
                                 + (f'; dropped [{"; ".join(drops)}]' if drops else ''))
                    for e in ev:
                        if re.search(FOCUS[name], e['one_line'], re.I):
                            lines.append(f'    - {e["id"]} | {e["tier"]} | {e["one_line"]}')
                    for c in raw_c:
                        mark = '' if c['id'] in kept_c else ' [DROPPED]'
                        lines.append(f'    - cand {c["id"]}{mark} {c.get("opens_as")}/{c.get("measure")} due {c["due_day"]} | {c["question"][:170]}'
                                     + (f' | rungs: {", ".join(r["label"] for r in c["rungs"])}' if name == 'L' and c.get('opens_as') == 'binding_obligation' else ''))
            lines.append('')
    (aw.RUN / 'sheet.md').write_text('\n'.join(lines) + '\n')
    print('wrote', aw.RUN / 'sheet.md', len(lines), 'lines')


if __name__ == '__main__':
    main()
