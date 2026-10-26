#!/usr/bin/env python3
"""Prompt-size audit (AGENTS §6): characters and o200k tokens of the extraction roles and of the response schema under two
versions for the same shown set. The user message is built by the same code for both versions, so the schema and the
role are the whole difference between a v10 and a v12 request.

  python3 scripts/prompt_size.py [--out poc/reports/<run>/prompt-size.json]
"""
import argparse
import json
import os
import sys

import tiktoken

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))

from hivemind import config, extraction  # noqa: E402

ENCODING = tiktoken.get_encoding('o200k_base')
SHOWN_VIEWS = [f'v{i}' for i in range(1, 11)]
SHOWN_GROUPS = ['g1', 'g2', 'g3']


def size(text):
    return {'chars': len(text), 'o200k_tokens': len(ENCODING.encode(text))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default=None)
    args = parser.parse_args()
    report = {'roles': {}, 'schemas': {}, 'shown': {'views': len(SHOWN_VIEWS), 'groups': len(SHOWN_GROUPS)}}
    for version in ('v10', 'v11', 'v12'):
        with open(config.prompt_path(f'role-{version}.txt'), encoding='utf-8') as handle:
            report['roles'][version] = size(handle.read())
    for version in ('v10', 'v12'):
        schema = extraction.schema_for(version, SHOWN_GROUPS, SHOWN_VIEWS)
        report['schemas'][version] = size(json.dumps(schema, separators=(',', ':')))
    text = json.dumps(report, indent=1)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as handle:
            handle.write(text)
    print(text)


if __name__ == '__main__':
    main()
