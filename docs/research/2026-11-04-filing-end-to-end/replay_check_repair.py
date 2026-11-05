"""$0 replay of every stored coverage-start reading through the repaired check (hivemind.baseline.check_figures; baseline-design.md round 24):
each figure the model wrote, as written, is checked again against its item's page text, and every figure whose kept flag changes is printed with
the class the census (census_all_reads.class_of) gives it. Expected before running: the six right figures the old check refused (a footnote mark
left off, cells left out of a table row) become kept, and nothing else changes.

usage: python3 replay_check_repair.py
"""
import json
import sqlite3
import sys

HERE = '/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = ['/Users/lchingen/hivemind/src', '/Users/lchingen/hivemind/scripts', HERE]
import baseline_read as br  # noqa: E402
import census_all_reads as census  # noqa: E402
from hivemind.baseline import check_figures  # noqa: E402

FIELDS = ('quote', 'value', 'unit', 'period', 'basis', 'one_line')


def main():
    pages = sqlite3.connect(f'file:{br.PAGES}?mode=ro', uri=True)
    text = lambda input_id: pages.execute('select text from items where input_id=?', (input_id,)).fetchone()[0]
    flips, judged = [], 0
    for name, path, _ in census.READINGS:
        data = json.load(open(f'{HERE}/{path}'))
        if path == 'baseline-read.json':
            day, report = '2026-05-20', [br.RELEASE]
            results = {v: {br.RELEASE: sends} for v, sends in data['results'].items()}
            old_kept = lambda f: br.check_figures([{k: f[k] for k in FIELDS}], text(br.RELEASE))[0]['kept'] if False else None
        else:
            day, report, results = data['report_day'], data['report'], data['results']
        for view_id, by_item in results.items():
            for input_id in report:
                for n, r in enumerate(by_item.get(input_id, [])):
                    raw = [{k: f[k] for k in FIELDS} for f in r['figures']]
                    new = check_figures(raw, text(input_id))
                    for f_old, f_new in zip(r['figures'], new):
                        judged += 1
                        before = f_old['kept'] if path != 'baseline-read.json' else census.br.kept_figures({'figures': [{k: f_old[k] for k in FIELDS}]}, text(input_id))[0]['kept'] if False else f_old['kept']
                        if before != f_new['kept']:
                            flips.append(f'{name}: {view_id} {input_id.rsplit(":", 1)[-1][:12]} send {n}: kept {before} -> {f_new["kept"]} | '
                                         f'class {census.class_of(day, view_id, f_new)} | value {f_new["value"]!r} | as written {f_old["quote"][:70]!r} | stored {f_new["quote"][:110]!r}')
    print(f'{judged} figures checked again; {len(flips)} changed')
    for line in flips:
        print('  ' + line)


if __name__ == '__main__':
    main()
