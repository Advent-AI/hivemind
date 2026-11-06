"""$0: the classes the 2026-11-05 predictions name, for the items of 2026-08-29 and 2026-08-30, in finished split ledgers (the production-path
run against the confirmation run of the research runner, both from the same 68-question starting ledger), restricted to the items every run
given dispatched (the confirmation run cut its first 100 rows inside these days). Code counts structure; whether a
question is worth opening or a ladder's favourable end is right is read (the ladders are printed for that).

    python3 two_day_compare.py <name>=<views.sqlite> [<name>=<views.sqlite> ...]"""
import collections
import json
import re
import sqlite3
import sys

DAYS = ('2026-08-29', '2026-08-30')


def normal(text):
    return re.sub(r'\s+', ' ', (text or '').lower()).strip()


def dispatched(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    return {r[0]: r[1] for r in conn.execute("select input_id, sequence_no from processing_steps where step='dispatched' and publication_day in (?, ?)", DAYS)}


def census(path, common):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    seqs = {seq for input_id, seq in dispatched(path).items() if input_id in common}
    out = collections.Counter()
    out['items dispatched'] = len(seqs)
    out['items failed'] = len({r[0] for r in conn.execute("select sequence_no from processing_steps where result='failed'") if r[0] in seqs})
    per_item = collections.defaultdict(list)
    for r in conn.execute('select e.quote, s.input_id, s.seq from evidence e join evidence_sources s using(evidence_id)'):
        if r['seq'] in seqs:
            per_item[r['input_id']].append(normal(r['quote']))
    out['records written'] = sum(len(v) for v in per_item.values())
    out['same quote stored twice in one item'] = sum(len(v) - len(set(v)) for v in per_item.values())
    for r in conn.execute('select handover_json, seq from handovers'):
        if r['seq'] not in seqs:
            continue
        for entry in json.loads(r['handover_json']).get('dropped', []):
            reason = str(entry[1]) if isinstance(entry, (list, tuple)) and len(entry) > 1 else str(entry)
            if 'quote' in reason and ('absent' in reason or 'not in' in reason):
                out['quote refusals'] += 1
            elif 'no home' in reason:
                out['no-home drops'] += 1
            elif 'same statement' in reason:
                out['same statement merged'] += 1
    views = [dict(r) for r in conn.execute('select view_id, object_id, kind, question, due_day, year, looks_at, created_seq from views order by created_seq') if r['created_seq'] in seqs]
    out['new questions'] = len(views)
    out['new questions with a due day'] = sum(1 for v in views if v['due_day'])
    ladders = []
    for v in views:
        rungs = [dict(r) for r in conn.execute('select label, lo, hi, condition from rungs where view_id=? order by position', (v['view_id'],))]
        out['new questions with a ladder'] += bool(rungs)
        numeric = [r for r in rungs if r['lo'] is not None or r['hi'] is not None]
        out['numeric ladders'] += bool(numeric)
        out['empty or inverted rungs'] += sum(1 for r in numeric if r['lo'] is not None and r['hi'] is not None and r['lo'] >= r['hi'])
        ladders.append((v, rungs))
    out['groups created'] = sum(1 for r in conn.execute('select created_seq from thesis_groups') if r[0] in seqs)
    new_ids = {v['view_id'] for v in views}
    out['group memberships of new questions'] = sum(1 for r in conn.execute('select view_id from thesis_group_members') if r[0] in new_ids)
    return out, ladders


def main():
    runs = dict(a.split('=', 1) for a in sys.argv[1:])
    common = set.intersection(*(set(dispatched(path)) for path in runs.values()))
    results = {name: census(path, common) for name, path in runs.items()}
    keys = list(dict.fromkeys(k for out, _ in results.values() for k in out))
    print(f'{"items of " + " and ".join(DAYS):44}' + ''.join(f'{n:>16}' for n in runs))
    for k in keys:
        print(f'{k:44}' + ''.join(f'{results[n][0][k]:>16}' for n in runs))
    for name, (_, ladders) in results.items():
        print(f'\n== {name}: new questions and ladders')
        for v, rungs in ladders:
            print(f'{v["view_id"]} [{v["object_id"]}, {v["kind"]}, due {v["due_day"] or "-"}] {v["question"]}')
            for r in rungs:
                bounds = '' if r['lo'] is None and r['hi'] is None else f' ({r["lo"]}, {r["hi"]})'
                print(f'    {r["label"]}: {r["condition"][:150]}{bounds}')


if __name__ == '__main__':
    main()
