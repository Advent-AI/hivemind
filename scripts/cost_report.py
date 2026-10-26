#!/usr/bin/env python3
"""Price a run's model calls from its archive at the published rates (model.PRICES; cached input at CACHED_INPUT_SHARE), per
purpose and model, and print a Markdown table. The token columns are the measurement; the provider's bill is the truth.

  python3 scripts/cost_report.py /abs/run-dir [/abs/run-dir ...]
"""
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import model  # noqa: E402


def price(run):
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    rows = {}
    for purpose, name, response, input_tokens, output_tokens in archive.execute('select purpose, model, response_json, input_tokens, output_tokens from model_calls'):
        try:
            usage = json.loads(response).get('usage') or {}
        except (TypeError, ValueError):
            usage = {}
        cached = min(input_tokens or 0, int((usage.get('prompt_tokens_details') or {}).get('cached_tokens') or 0))
        if name.startswith('jev'):
            input_tokens = int(usage.get('input_tokens') or input_tokens or 0)
        d = rows.setdefault((purpose, name), {'calls': 0, 'input': 0, 'cached': 0, 'output': 0})
        d['calls'] += 1
        d['input'] += input_tokens or 0
        d['cached'] += cached
        d['output'] += output_tokens or 0
    lines = ['| purpose | model | calls | input tokens | of them cached | output tokens | USD |', '|---|---|---|---|---|---|---|']
    total = 0.0
    for (purpose, name), d in sorted(rows.items()):
        price_in, price_out = model.PRICES.get(name, (0.0, 0.0))
        usd = (d['input'] - d['cached']) / 1e6 * price_in + d['cached'] / 1e6 * price_in * model.CACHED_INPUT_SHARE + d['output'] / 1e6 * price_out
        total += usd
        lines.append(f"| {purpose} | {name} | {d['calls']} | {d['input']:,} | {d['cached']:,} | {d['output']:,} | {usd:.3f} |")
    lines.append(f'| **total** | | | | | | **{total:.3f}** |')
    return '\n'.join(lines), total


if __name__ == '__main__':
    for run in sys.argv[1:]:
        table, total = price(run)
        print(f'## {os.path.basename(run.rstrip("/"))}\n\n{table}\n')
