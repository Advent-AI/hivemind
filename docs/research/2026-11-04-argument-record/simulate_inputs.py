"""Logical simulation of the argument-record inputs on a stored run, at no cost (design.md §10 step 1).

For every stored judgement it compares what the judge was shown (parsed from the archived request) with what the card design would
show for the same judgement: the card's basis, taken as the 40 pieces of the question most recently cited by its earlier judgements
(the card's limit; still in force; the same memory reach_back.py uses), plus the arrivals linked since the question's last ARRIVAL_WINDOW
judgements (1: since the previous judgement, the design; 3: a variant that keeps a new piece in view for three judgements; on a first
judgement, everything in force). Dependencies, themes, the header and the previous conclusion are kept as the stored request had them; the card text is
counted at CARD_CHARS. Sizes are in characters of the user message; an evidence line is costed at its own length as the stored request
printed it. The proxy for the card's basis is the judge's own citations: a card cites what the analyst relies on.

usage: python3 simulate_inputs.py <views.sqlite> <archive.sqlite> [--window N] [question ids ...]
"""
import collections
import json
import re
import sqlite3
import sys

CARD_LIMIT = 40
CARD_CHARS = 3000          # an estimate: 10 claims of about 250 characters, the watch and gap items, the removed reasons
EVIDENCE_BLOCK = re.compile(r'\n\[Evidence (?:in force|in view) under this thesis, (\d+) items\]\n(.*?)(?=\n\n\[|\n\[Previous|\n\nAnswer)', re.S)
PIECE = re.compile(r'^- (e\d+) \[', re.M)


def open_ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def main():
    views_path, archive_path, *rest = sys.argv[1:]
    window = 1
    if rest[:1] == ['--window']:
        window, rest = int(rest[1]), rest[2:]
    only = rest
    views, archive = open_ro(views_path), open_ro(archive_path)
    links = collections.defaultdict(list)                  # view → [(seq, evidence id)]
    for r in views.execute('select view_id, evidence_id, seq from evidence_links order by id'):
        links[r['view_id']].append((r['seq'], r['evidence_id']))
    replaced = {r[0] for r in views.execute('select old_evidence_id from replacements')} if views.execute(
        "select 1 from sqlite_master where name='replacements'").fetchone() else set()
    memory, judged_seqs = {}, collections.defaultdict(list)
    rows = []
    for j in views.execute('select view_id, seq, publication_day, cited_evidence_json, request_sha256 from judgements order by seq, judgement_id'):
        vid = j['view_id']
        req = archive.execute('select request_json from model_calls where request_sha256=?', (j['request_sha256'],)).fetchone()
        if not req:
            continue
        user = json.loads(req['request_json'])['messages'][1]['content']
        block = EVIDENCE_BLOCK.search(user)
        shown_ids = PIECE.findall(block.group(2)) if block else []
        per_piece = {}
        if block:
            parts = re.split(r'(?m)^(?=- e\d+ \[)', block.group(2))
            for part in parts:
                m = PIECE.match(part)
                if m:
                    per_piece[m.group(1)] = len(part)
        mean_piece = (sum(per_piece.values()) / len(per_piece)) if per_piece else 400
        in_force = {e for s, e in links[vid] if s <= j['seq'] and e not in replaced}
        first = vid not in memory
        if not first:
            basis = [e for e in list(memory[vid])[-CARD_LIMIT:] if e in in_force]
            since = judged_seqs[vid][-window] if len(judged_seqs[vid]) >= window else -1
            arrivals = [e for s, e in links[vid] if since < s <= j['seq'] and e not in replaced]
        else:
            basis, arrivals = [], sorted(in_force)
        card_ids = list(dict.fromkeys(basis + arrivals))
        evidence_chars = sum(per_piece.get(e, mean_piece) for e in card_ids)
        other_chars = len(user) - (len(block.group(0)) if block else 0)
        simulated = other_chars + evidence_chars + (0 if first else CARD_CHARS)
        themes = re.search(r'\[Themes in force, (\d+)\]', user)
        deps = user.split('[Current conclusions of the theses it depends on]', 1)
        dep_count = len(re.findall(r'^- ', deps[1].split('\n\n[', 1)[0], re.M)) if len(deps) == 2 else 0
        same_as = max([len(m.split(', ')) for m in re.findall(r'same claim as ([^;]+);', user)] or [0])
        rows.append(dict(view=vid, day=j['publication_day'], linked=len(in_force), shown=len(shown_ids), actual=len(user),
                         basis=len(basis), arrivals=len(arrivals), simulated=simulated, themes=int(themes.group(1)) if themes else 0,
                         deps=dep_count, same_as=same_as))
        held = memory.setdefault(vid, collections.OrderedDict())
        for e in json.loads(j['cited_evidence_json'] or '[]'):
            held.pop(e, None)
            held[e] = True
        judged_seqs[vid].append(j['seq'])
    if not rows:
        sys.exit('no judgement could be matched to its archived request')
    selected = [r for r in rows if not only or r['view'] in only]
    print(f'{len(rows)} judgements matched to their requests; card memory {CARD_LIMIT} most recently cited, arrivals over the last {window} judgement(s)')
    print('largest actual request vs simulated, per question (characters):')
    by_view = collections.defaultdict(list)
    for r in rows:
        by_view[r['view']].append(r)
    for vid, rs in sorted(by_view.items(), key=lambda kv: -max(r['actual'] for r in kv[1]))[:8]:
        big = max(rs, key=lambda r: r['actual'])
        print(f"  {vid}: {len(rs)} judgements; on {big['day']} linked {big['linked']}, shown {big['shown']}, actual {big['actual']:,} → "
              f"simulated {big['simulated']:,} (basis {big['basis']}, arrivals {big['arrivals']}, deps {big['deps']}, themes {big['themes']}); "
              f"largest simulated {max(r['simulated'] for r in rs):,}")
    print('all judgements: actual max {:,}, simulated max {:,}; arrivals max {}; themes max {}; deps max {}; same-claim list max {}'.format(
        max(r['actual'] for r in rows), max(r['simulated'] for r in rows), max(r['arrivals'] for r in rows), max(r['themes'] for r in rows),
        max(r['deps'] for r in rows), max(r['same_as'] for r in rows)))
    print('total characters of all judging requests: actual {:,}, simulated {:,} ({:.0%})'.format(
        sum(r['actual'] for r in rows), sum(r['simulated'] for r in rows), sum(r['simulated'] for r in rows) / sum(r['actual'] for r in rows)))
    if only:
        print('day by day for', ', '.join(only))
        for r in selected:
            print(f"  {r['day']} {r['view']}: linked {r['linked']:4d} shown {r['shown']:4d} actual {r['actual']:7,} | basis {r['basis']:2d} "
                  f"arrivals {r['arrivals']:3d} simulated {r['simulated']:7,} | themes {r['themes']} deps {r['deps']} same-claim {r['same_as']}")


if __name__ == '__main__':
    main()
