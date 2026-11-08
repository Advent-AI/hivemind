#!/usr/bin/env python3
"""Run an explicitly bounded Step 1 sequence against OpenAI Luna."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from live import LiveTransport
from runner import run


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source', 'output', 'manifest', 'initial', 'settings', 'limits'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--system', help='a candidate system prompt file, with --closing; the PRD prompt otherwise')
    parser.add_argument('--closing', help='the candidate closing check, appended to the end of the user message')
    parser.add_argument('--schema', help='a candidate response schema file in place of the PRD schema')
    args = parser.parse_args()
    if bool(args.system) != bool(args.closing):
        parser.error('--system and --closing go together')
    texts = (Path(args.system).read_text(encoding='utf-8'), Path(args.closing).read_text(encoding='utf-8')) if args.system else None
    limits = read(args.limits)
    settings = read(args.settings)
    settings['live_limits'] = limits
    result = run(args.source, args.output, read(args.manifest), read(args.initial), settings, LiveTransport(limits),
                 ROOT / 'clean-arch/PRD.md', texts, read(args.schema) if args.schema else None)
    print(json.dumps({'trace': args.output, **result}))
    return 0 if result['status'] == 'complete' else 1


if __name__ == '__main__':
    sys.exit(main())
