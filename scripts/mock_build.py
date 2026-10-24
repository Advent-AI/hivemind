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
from hivemind import service  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default_data = ROOT / 'poc/mock/data.en.json'
    if not default_data.exists():
        default_data = ROOT / 'poc/mock/data.json'
    parser.add_argument('--data', type=Path, default=default_data)
    parser.add_argument('--ledger', type=Path, default=ROOT / 'poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite')
    parser.add_argument('--out', type=Path, default=ROOT / 'poc/mock/index.html')
    args = parser.parse_args()
    data = json.loads(args.data.read_text())
    if not data.get('schema_version') and args.ledger.exists():
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
    template = (ROOT / 'poc/mock/index.template.html').read_text()
    page = template.replace('__STYLES__', built['style']).replace('__SCRIPT__', built['script'].replace('</script', '<\\/script'))
    page = page.replace('__DATA__', prepared.stdout.replace('<', '\\u003c'))
    output = args.out.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + '.tmp')
    temporary.write_text(page)
    temporary.replace(output)
    print(f'UI: {len(built["script"].encode()):,} JS bytes; wrote {output} ({len(page.encode()):,} bytes)')


if __name__ == '__main__':
    main()
