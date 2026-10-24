"""Preflight: run every code check and every prompt against the stored model answers before a paid run ($0).

AGENTS.md §3 "Strictness is code too" and §4 "a check must judge something": a check is accepted on real data,
reports how many cases it judged, and a check over an empty population is unexercised. This script replays what
the archive and the earlier runs' views databases already hold through the current code and prints, per check,
the cases judged, the cases refused and the reasons with examples:

  A. answers the schema refused (prompt and schema disagree: a value the prompt's wording suggested but the enum lacks)
  B. extraction's code checks (extraction.sift) over every stored extraction answer
  C. matching's code checks (matching.check) over every stored matching record, with the lists shown at the time
  D. every schema enum value appears verbatim in the prompt that asks for it

Usage: python3 scripts/preflight.py [--views DB ...]   (defaults: the archive, the window test database, the
current views database and every old-*/views.sqlite under poc/data). Exit status 1 when a check judged no case.
"""
import argparse
import collections
import glob
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model, testdb, universe  # noqa: E402
from hivemind.views import judging, matching, store  # noqa: E402

SCHEMAS = {'extract': extraction.SCHEMA, 'match': matching.SCHEMA, 'judge': judging.SCHEMA}
ITEM_ID = re.compile(r'【信息】编号 (\S+?)，类别 ')
BLOCK5_VIEW = re.compile(r'^\s+- (v\d+)（', re.M)
MATCH_SHOWN = re.compile(r'^· (v\d+)（', re.M)


def normalise_reason(text):
    text = re.sub(r"'[^']*'", "'…'", text)
    text = re.sub(r'\[\d+\]', '[]', text)
    text = re.sub(r'\b[ev]\d+\b|\bc\d+\b', '#', text)
    text = re.sub(r'\d{4}-\d{2}-\d{2}', 'DATE', text)
    return text[:90]


def tally(title, judged, refused, reasons, examples):
    share = f'{refused / judged:.0%}' if judged else 'n/a'
    print(f'\n== {title}: judged {judged}, refused/dropped {refused} ({share})')
    for reason, count in reasons.most_common(20):
        print(f'   {count:5d}  {reason}')
        for example in examples.get(reason, [])[:2]:
            print(f'          e.g. {example}')


def part_a(archive_conn):
    reasons, examples, judged = collections.Counter(), collections.defaultdict(list), 0
    rows = archive_conn.execute("select purpose, request_sha256, answer_json from model_calls where request_sha256 like '%:schema:%' or request_sha256 like '%:malformed:%'")
    for purpose, sha, answer_json in (tuple(r) for r in rows):
        judged += 1
        if ':malformed:' in sha or not answer_json:
            reasons[f'{purpose}: not JSON'] += 1
            continue
        for error in model.check_schema(json.loads(answer_json), SCHEMAS.get(purpose, {})):
            key = f'{purpose}: {normalise_reason(error)}'
            reasons[key] += 1
            examples[key].append(error[:140])
    tally('A. answers the schema refused (prompt/schema disagreements; empty when the provider enforces the schema server-side)', judged, judged, reasons, examples)
    return judged


def part_b(archive_conn, items_conn):
    reasons, examples = collections.Counter(), collections.defaultdict(list)
    judged = produced_e = kept_e = produced_c = kept_c = 0
    items_by_id = {}
    for purpose, request_json, answer_json in (tuple(r) for r in archive_conn.execute("select purpose, request_json, answer_json from model_calls where purpose='extract' and request_sha256 not like '%:%'")):
        request = json.loads(request_json)
        user = request['messages'][1]['content']
        found = ITEM_ID.search(user)
        if not found:
            continue
        input_id = found.group(1)
        if input_id not in items_by_id:
            row = items_conn.execute('select * from items where input_id=?', (input_id,)).fetchone()
            items_by_id[input_id] = dict(row) if row else None
        item = items_by_id[input_id]
        if not item:
            continue
        data = json.loads(answer_json)
        shown_ids = set(BLOCK5_VIEW.findall(user))
        evidence, candidates, dropped = extraction.sift(data, item, item['text'] or '', shown_ids)
        judged += 1
        produced_e += len(data.get('evidence', [])); kept_e += len(evidence)
        produced_c += len(data.get('candidates', [])); kept_c += len(candidates)
        for ident, why in dropped:
            key = normalise_reason(why)
            reasons[key] += 1
            examples[key].append(f'{input_id[:48]} {ident}: {why[:80]}')
    print(f'\n   extraction answers {judged}: evidence produced {produced_e} kept {kept_e}; candidates produced {produced_c} kept {kept_c}')
    tally('B. extraction code checks over stored answers', produced_e + produced_c, (produced_e - kept_e) + (produced_c - kept_c), reasons, examples)
    return judged


def part_c(archive_conn, views_paths, uni):
    reasons, examples = collections.Counter(), collections.defaultdict(list)
    judged = refused_records = 0
    for path in views_paths:
        # matching.check writes suggested themes to the review pool, so it runs on a scratch copy, never on the real file
        scratch = os.path.join(tempfile.mkdtemp(), 'views.sqlite')
        shutil.copy(path, scratch)
        conn = sqlite3.connect(scratch)
        conn.row_factory = sqlite3.Row
        for rec in conn.execute('select input_id, call_no, shown_json, decisions_json, request_sha256 from match_records order by id'):
            handover_row = conn.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (rec['input_id'],)).fetchone()
            request_row = archive_conn.execute('select request_json from model_calls where request_sha256=?', (rec['request_sha256'],)).fetchone()
            if not handover_row or not request_row or not rec['decisions_json']:
                continue
            handover = json.loads(handover_row['handover_json'])
            shown = json.loads(rec['shown_json'])
            lists = matching.Lists(shown.get('candidates', {}), {tuple(k.split('|', 1)): v for k, v in shown.get('evidence', {}).items()})
            user = json.loads(request_row['request_json'])['messages'][1]['content']
            shown_views = [{'view_id': v} for v in dict.fromkeys(MATCH_SHOWN.findall(user))]
            if rec['call_no'] <= 2:
                candidates, evidence = handover['candidates'], handover['evidence']
            else:                                   # the second call: candidate-linked evidence under its destination
                wanted = {k[0] for k in lists.evidence_lists}
                candidates, evidence = [], [dict(e, links=[k[1] for k in lists.evidence_lists if k[0] == e['id']]) for e in handover['evidence'] if e['id'] in wanted]
            try:
                checked = matching.check(conn, uni, json.loads(rec['decisions_json']), candidates, evidence, lists, shown_views)
            except Exception as error:
                key = 'check raised ' + type(error).__name__
                reasons[key] += 1; examples[key].append(f'{os.path.basename(os.path.dirname(path))} {rec["input_id"][:40]}: {error!r}'[:140])
                judged += 1; refused_records += 1
                continue
            judged += 1
            if checked.refusals:
                refused_records += 1
            for refusal in checked.refusals:
                key = normalise_reason(refusal)
                reasons[key] += 1
                examples[key].append(f'{os.path.basename(os.path.dirname(path))} {rec["input_id"][:40]}: {refusal[:90]}')
    tally('C. matching code checks over stored records (database state is the final one, not the state at the time)', judged, refused_records, reasons, examples)
    return judged


def part_d():
    missing = []
    checks = [
        ('role', extraction.TIERS + ['对象观点', '主题观点', '强烈看多', '看多', '中性', '看空', '强烈看空']),
        ('matching', matching.OUTCOMES + matching.EVIDENCE_OUTCOMES),
        ('judging', judging.PUSHES),
    ]
    judged = 0
    for kind, values in checks:
        for path in sorted(glob.glob(os.path.join(config.PROMPTS, f'{kind}-v*.txt'))):
            text = open(path, encoding='utf-8').read()
            for value in values:
                judged += 1
                if value not in text:
                    missing.append(f'{os.path.basename(path)} lacks the enum value {value!r}')
    print(f'\n== D. schema enum values named in the prompts: judged {judged}, missing {len(missing)}')
    for line in missing:
        print('   ', line)
    return judged


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'archive.sqlite'))
    parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite'))
    parser.add_argument('--views', nargs='*', default=None)
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    args = parser.parse_args()
    views_paths = args.views or [p for p in [os.path.join(ROOT, 'poc', 'data', 'views.sqlite')] + sorted(glob.glob(os.path.join(ROOT, 'poc', 'data', 'old-*', 'views.sqlite'))) if os.path.exists(p)]
    archive_conn = sqlite3.connect(f'file:{args.archive}?mode=ro', uri=True)
    archive_conn.row_factory = sqlite3.Row
    items_conn = testdb.open_db(args.items)
    uni = universe.load(args.universe)
    print('preflight over', args.archive, 'and', len(views_paths), 'views databases:', ', '.join(os.path.basename(os.path.dirname(p)) for p in views_paths))
    part_a(archive_conn)
    counts = [part_b(archive_conn, items_conn), part_c(archive_conn, views_paths, uni), part_d()]
    if min(counts) == 0:
        print('\nUNEXERCISED: a check judged no case')
        sys.exit(1)
    print('\npreflight done')


if __name__ == '__main__':
    main()
