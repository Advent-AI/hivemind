"""The slice's four conditions (PLAN.md, written before the send), checked on its finished trace ($0). Exit 1 when one fails.

  python3 check_slice.py <run root>
"""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model  # noqa: E402

STORED_PER_ARTICLE = 2.099 / 235
LIMIT = 1.5 * STORED_PER_ARTICLE


def main(run_root):
    run_root = Path(run_root)
    trace = run_root / 'slice/trace.sqlite'
    conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
    manifest = json.loads(conn.execute('select manifest from run').fetchone()[0])
    rows = conn.execute('select sequence, status, error, request from trace order by sequence').fetchall()
    calls = conn.execute('select model, input_tokens, output_tokens from model_calls').fetchall()
    conn.close()
    results = []
    went_on = lambda status, error: status == 'failed' and str(error or '').startswith('FormatFailure')
    complete = len(rows) == len(manifest['item_ids']) and all(status == 'complete' or went_on(status, error) for _, status, error, _ in rows)
    results.append(('every article complete (or the one failure the runner goes on after)', complete,
                    f"{sum(1 for r in rows if r[1] == 'complete')} complete of {len(manifest['item_ids'])}"))
    ledger = json.loads((run_root / 'ledger.json').read_text())
    results.append(('no ledger refusal', ledger['refused'] == 0 and not ledger['stopped'], f"refused {ledger['refused']}, stopped {ledger['stopped']}"))
    price_in, price_out = model.PRICES['deepseek-flash']
    cost = sum(((tin or 0) * price_in + (tout or 0) * price_out) / 1e6 for name, tin, tout in calls)
    per_article = cost / max(1, len(rows))
    results.append((f'cost per article at most ${LIMIT:.4f}', per_article <= LIMIT, f'${per_article:.4f} an article, ${cost:.3f} in all, {len(calls)} calls'))
    first = json.loads(rows[0][3])
    shown = [topic['id'] for topic in json.JSONDecoder().raw_decode(first['messages'][1]['content'])[0]['open_theses']]
    library = [topic['id'] for topic in json.loads((run_root / 'slice/initial.json').read_text())]
    results.append(("the first request holds week 1's library", shown == library and len(library) == 7, f'{shown}'))
    for name, holds, detail in results:
        print(('  ok    ' if holds else '  FAIL  ') + name + f' | {detail}')
    return 0 if all(holds for _, holds, _ in results) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
