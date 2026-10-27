"""Validate data and bundle the modular Thesis UI into the portable mock HTML.

Install build dependencies once with ``npm ci --prefix poc/ui``. No model or network
calls are made by this build. Existing source data and translation caches are not changed.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import bundle, service  # noqa: E402
from hivemind.views import store  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, help='explicit legacy JSON export; otherwise read the current ledger')
    parser.add_argument('--ledger', type=Path, default=ROOT / 'poc/data/english-v29-nvda-3m-2026-10-27/snapshots/2026-10-27T0736/views.sqlite')
    parser.add_argument('--items', type=Path, default=ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')
    parser.add_argument('--out', type=Path, default=ROOT / 'poc/mock/index.html')
    parser.add_argument('--composite-trials', type=Path, help='explicit JSON trial baskets for the Idea score preview')
    parser.add_argument('--market-data', type=Path, default=ROOT / 'poc/ui/data/nvda-2026-10-27.json', help='dated real stock-price snapshot for the Action preview')
    args = parser.parse_args()
    if args.data:
        data = json.loads(args.data.read_text())
    else:
        conn, items = service.open_ledger(str(args.ledger)), store.open_read_only(str(args.items))
        try:
            data = bundle.library(conn, items)
        finally:
            conn.close()
            items.close()
    if args.data and not data.get('schema_version') and args.ledger.exists():
        conn = service.open_ledger(str(args.ledger))
        try:
            data['sequence_days'] = service.seq_day_map(conn)
        finally:
            conn.close()
    ui = ROOT / 'poc/ui'
    bundled = subprocess.run(['node', str(ui / 'build.mjs'), '--json'], capture_output=True, text=True)
    if bundled.returncode:
        print('UI build failed. Install its pinned dependencies with: npm ci --prefix poc/ui', file=sys.stderr)
        print(bundled.stderr, file=sys.stderr)
        bundled.check_returncode()
    built = json.loads(bundled.stdout)
    prepared = subprocess.run(['node', str(ui / 'prepare-data.mjs')], input=json.dumps(data, ensure_ascii=False), capture_output=True, text=True)
    if prepared.returncode:
        print(prepared.stderr, file=sys.stderr)
        prepared.check_returncode()
    print(prepared.stderr.strip())
    market = subprocess.run(['node', str(ui / 'prepare-data.mjs'), '--market'], input=args.market_data.read_text(), capture_output=True, text=True)
    if market.returncode:
        print(market.stderr, file=sys.stderr)
        market.check_returncode()
    print(market.stderr.strip())
    template = (ROOT / 'poc/mock/index.template.html').read_text()
    page = template.replace('__STYLES__', built['style']).replace('__SCRIPT__', built['script'].replace('</script', '<\\/script'))
    page = page.replace('__DATA__', prepared.stdout.replace('<', '\\u003c'))
    page = page.replace('__MARKET_DATA__', market.stdout.replace('<', '\\u003c'))
    trials = json.loads(args.composite_trials.read_text()) if args.composite_trials else []
    page = page.replace('__COMPOSITE_TRIALS__', json.dumps(trials, ensure_ascii=False).replace('<', '\\u003c'))
    output = args.out.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + '.tmp')
    temporary.write_text(page)
    temporary.replace(output)
    print(f'UI: {len(built["script"].encode()):,} JS bytes; wrote {output} ({len(page.encode()):,} bytes)')


if __name__ == '__main__':
    main()
