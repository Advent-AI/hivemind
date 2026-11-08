#!/usr/bin/env python3
"""Exercise Step 1 with recorded provider responses, without network access."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from runner import RecordedTransport, run


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source', 'output', 'manifest', 'initial', 'settings', 'responses'):
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output, read(args.manifest), read(args.initial), read(args.settings), RecordedTransport(read(args.responses)),
                 ROOT / 'clean-arch/PRD.md')
    print(f'Trace written to {args.output}')
    if result['status'] != 'complete':
        print(f"Failed on {result['input_id']}: {result['error']}", file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
