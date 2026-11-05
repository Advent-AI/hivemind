"""The numbers behind predictions-step2.md for one finished run of poc-v109 (judging-v8), against the frozen v108 draw it was paired
with. Read-only; run after the run has ended (or on a snapshot).

usage: python3 analyze_run.py <v8 run folder> <paired v108 run folder> [copied archive rows, default the paired archive's row count]
"""
import collections
import json
import re
import sqlite3
import statistics
import sys

ROOT = '/Users/lchingen/hivemind'
sys.path.insert(0, f'{ROOT}/src')
from hivemind import model  # noqa: E402


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def main():
    run, paired = sys.argv[1], sys.argv[2]
    views, archive = ro(f'{run}/views.sqlite'), ro(f'{run}/archive.sqlite')
    base_views, base_archive = ro(f'{paired}/views.sqlite'), ro(f'{paired}/archive.sqlite')
    copied = int(sys.argv[3]) if len(sys.argv) > 3 else base_archive.execute('select count(*) from model_calls').fetchone()[0]
    days = [r[0] for r in views.execute('select day from days_completed order by id')]
    print(f'P1 days completed: {len(days)} ({days[0] if days else "-"} .. {days[-1] if days else "-"})')

    new_rows = archive.execute('select call_id, purpose, request_sha256, input_tokens, output_tokens from model_calls where call_id > ? order by call_id', (copied,)).fetchall()
    by_purpose = collections.Counter(r['purpose'] for r in new_rows)
    judge_rows = [r for r in new_rows if r['purpose'] == 'judge']
    refused = [r for r in judge_rows if ':refused:' in r['request_sha256']]
    judgements = views.execute('select count(*) from judgements').fetchone()[0]
    print(f'P3 new archive rows by purpose (paid calls): {dict(by_purpose)}')
    print(f'P2 judging answers sent {len(judge_rows)}; refused by code {len(refused)} ({len(refused) / max(len(judge_rows), 1):.1%}); judgements written {judgements}')

    sizes = []
    for r in archive.execute("select request_json from model_calls where purpose='judge' and call_id > ?", (copied,)):
        sizes.append(len(json.loads(r[0])['messages'][1]['content']))
    base_sizes = [len(json.loads(r[0])['messages'][1]['content']) for r in base_archive.execute("select request_json from model_calls where purpose='judge' and request_sha256 not like '%:%'")]
    accepted_sizes = []
    for r in views.execute('select request_sha256 from judgements'):
        row = archive.execute('select request_json from model_calls where request_sha256=?', (r[0],)).fetchone()
        if row:
            accepted_sizes.append(len(json.loads(row[0])['messages'][1]['content']))
    print(f'P5 judging request characters: largest {max(sizes, default=0):,} (v7 {max(base_sizes, default=0):,}); total of accepted requests {sum(accepted_sizes):,} '
          f'= {sum(accepted_sizes) / max(sum(base_sizes), 1):.0%} of v7 {sum(base_sizes):,}')

    cards = views.execute('select view_id, seq, card_json from arguments order by id').fetchall()
    claims = [len(json.loads(c['card_json'])['for']) + len(json.loads(c['card_json'])['against']) for c in cards]
    removed = [(c['view_id'], c['seq'], r) for c in cards for r in json.loads(c['card_json'])['removed']]
    read_kept = sum(1 for c in cards if json.loads(c['card_json']).get('read'))
    print(f'P6 cards {len(cards)} for judgements {judgements}; claims per card median {statistics.median(claims) if claims else 0} (min {min(claims, default=0)}, max {max(claims, default=0)}); '
          f'claims removed with a reason {len(removed)}; cards recording what they read {read_kept}')
    for vid, seq, r in removed[:3]:
        print(f'    removed on {vid} seq {seq}: {r["id"]} — {r["reason"][:120]}')

    last, moved, rejudged = {}, 0, 0
    for r in views.execute('select view_id, rung from judgements order by seq, judgement_id'):
        if r['view_id'] in last:
            rejudged += 1
            moved += r['rung'] != last[r['view_id']]
        last[r['view_id']] = r['rung']
    print(f'P7 re-judgements {rejudged}, rung moved {moved} ({moved / max(rejudged, 1):.0%})')

    price_in, price_out = model.PRICES['gpt-6-luna']
    tokens_in = sum(r['input_tokens'] or 0 for r in judge_rows)
    tokens_out = sum(r['output_tokens'] or 0 for r in judge_rows)
    base_judge = base_archive.execute("select sum(input_tokens), sum(output_tokens), count(*) from model_calls where purpose='judge'").fetchone()
    print(f'P8 judging tokens in {tokens_in:,} out {tokens_out:,} = ${tokens_in / 1e6 * price_in + tokens_out / 1e6 * price_out:.2f} at published rates '
          f'(v7: in {base_judge[0]:,} out {base_judge[1]:,} = ${base_judge[0] / 1e6 * price_in + base_judge[1] / 1e6 * price_out:.2f}); '
          f'mean output per call {tokens_out / max(len(judge_rows), 1):.0f} (v7 {base_judge[1] / max(base_judge[2], 1):.0f})')

    same_upstream = [t for t in ('views', 'evidence', 'evidence_links', 'view_keys', 'thesis_groups')
                     if sorted(map(tuple, views.execute(f'select * from {t}'))) != sorted(map(tuple, base_views.execute(f'select * from {t}')))]
    print(f'pairing check: upstream tables that differ from the paired v108 draw: {same_upstream or "none"}')


if __name__ == '__main__':
    main()
