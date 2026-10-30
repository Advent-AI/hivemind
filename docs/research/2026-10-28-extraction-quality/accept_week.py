"""Acceptance of the pushed design on one week (2026-07-01..07-07), three ledgers of the same days and the same writer:
  v34  the three-month run's week 1 (production before; snapshot 2026-10-28T1450)
  v35  A alone (themes shown)
  v36b the pushed configuration (themes shown, placement-narrow-v1 with the title line, unplaced kept)
Only the measures already defined in results.md / routing-analysis.md (no new ruler): statements kept and unplaced, items with no
evidence, theses opened and duplicates, links by thesis and to the two sinks, theme theses' evidence and judgements, the judge's
request size and citation share on the root theses, cost from the run's day lines. Plus the frozen gold's cells for the gold articles
that fall in the week, scored from each run's own handover (no send). Reads only snapshots and finished ledgers."""
import collections, json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), 'src'))
RUNS = {'v34 (before)': '/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450',
        'v35 (A)': '/Users/lchingen/hivemind/poc/data/english-v35-nvda-2w-2026-10-28',
        'v36b (pushed)': '/Users/lchingen/hivemind/poc/data/english-v36b-nvda-1w-2026-10-28',
        'v37 (D210)': '/Users/lchingen/hivemind/poc/data/english-v37-nvda-1w-2026-10-28',
        'v38 (D211)': '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28'}
RUNOUT = {'v34 (before)': ['/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/run.out.halt-2026-07-12-0132'],
          'v35 (A)': ['/Users/lchingen/hivemind/poc/data/english-v35-nvda-2w-2026-10-28/run.out'],
          'v36b (pushed)': ['/Users/lchingen/hivemind/poc/data/english-v36b-nvda-1w-2026-10-28/run.out.halt-day7', '/Users/lchingen/hivemind/poc/data/english-v36b-nvda-1w-2026-10-28/run.out'],
          'v37 (D210)': ['/Users/lchingen/hivemind/poc/data/english-v37-nvda-1w-2026-10-28/run.out'],
          'v38 (D211)': ['/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/run.out']}
UNTIL = '2026-07-07'


def facts(name, path):
    c = sqlite3.connect(f'file:{path}/views.sqlite?mode=ro', uri=True); c.row_factory = sqlite3.Row
    cutoff = c.execute("select max(sequence_no) from processing_steps where publication_day<=?", (UNTIL,)).fetchone()[0]
    f = {}
    hand = {r['input_id']: json.loads(r['handover_json']) for r in c.execute("select input_id, handover_json from handovers where seq<=? order by id", (cutoff,))}
    f['items'] = len(hand)
    f['statements kept (placed)'] = sum(len(h['evidence']) for h in hand.values())
    f['statements with no home (v36b: kept aside; v37: dropped, D209)'] = sum(len(h.get('unplaced', [])) + sum(1 for d in h['dropped'] if d[1] == 'no home') for h in hand.values())
    f['statements dropped for another reason'] = sum(1 for h in hand.values() for d in h['dropped'] if d[1] != 'no home')
    f['items with no placed evidence'] = sum(1 for h in hand.values() if not h['evidence'])
    views = {r['view_id']: dict(r) for r in c.execute("select * from views where created_seq<=?", (cutoff,))}
    f['theses opened'] = len(views)
    f['match outcomes of candidates'] = dict(collections.Counter(x['outcome'] for r in c.execute("select decisions_json from match_records") for x in json.loads(r['decisions_json']).get('candidates', [])))
    f['extraction sends / items (re-sends)'] = (a_sends := sqlite3.connect(f'file:{path}/archive.sqlite?mode=ro', uri=True).execute("select count(*) from model_calls where purpose='extract' and request_sha256 not like '%:%'").fetchone()[0], len(hand))
    f['questions'] = sorted(f"{v['view_id']} {v['question'][:70]}" for v in views.values())
    links = collections.Counter(r['view_id'] for r in c.execute("select view_id from evidence_links where seq<=?", (cutoff,)))
    f['links total'] = sum(links.values())
    sinks = [v for v, x in views.items() if 'total revenue' in x['question'].lower() or 'data center segment revenue' in x['question'].lower()]
    f['links to the two revenue sinks'] = sum(links[v] for v in sinks)
    f['links to theme theses'] = sum(links[v] for v, x in views.items() if x['kind'] == 'theme')
    judg = collections.Counter(r['view_id'] for r in c.execute("select view_id from judgements where seq<=?", (cutoff,)))
    f['judgements of theme theses'] = sum(judg[v] for v, x in views.items() if x['kind'] == 'theme')
    # the judge on the sinks: request size and the share of a sink's pieces its judgements cite
    cited = collections.defaultdict(set)
    for r in c.execute("select view_id, cited_evidence_json from judgements where seq<=?", (cutoff,)):
        cited[r['view_id']].update(json.loads(r['cited_evidence_json'] or '[]'))
    pieces = collections.defaultdict(set)
    for r in c.execute("select view_id, evidence_id from evidence_links where seq<=?", (cutoff,)):
        pieces[r['view_id']].add(r['evidence_id'])
    f['sinks: pieces / cited by own judgements'] = [(v, len(pieces[v]), len(cited[v] & pieces[v])) for v in sinks]
    a = sqlite3.connect(f'file:{path}/archive.sqlite?mode=ro', uri=True)
    shas = [r['request_sha256'] for r in c.execute("select request_sha256 from judgements where seq<=?", (cutoff,))]      # the week's judgements only
    toks = [r[0] for sha in shas for r in a.execute("select input_tokens from model_calls where request_sha256=?", (sha,)) if r[0]]
    f['judge requests (week): count / median input tokens'] = (len(shas), sorted(toks)[len(toks) // 2] if toks else 0)
    seen = {}
    for p in RUNOUT[name]:
        for line in open(p):
            m = re.match(r'^(2026-07-0[1-7]) .*day \$([0-9.]+)', line)
            if m:
                seen[m.group(1)] = float(m.group(2))
    cost = sum(seen.values()); days = len(seen)
    f['cost (day lines, $)'] = round(cost, 2); f['days'] = days
    return f, hand


def gold_cells(hand):
    """The frozen gold's statements whose articles fall in the week, scored from the run's handover: a statement is kept right when
    a kept piece covers its span and links to one of its homes (primary_home of gold v2, the one-home rule)."""
    from hivemind import extraction
    gold = json.load(open(os.path.join(HERE, 'gold-extraction-v2.json')))
    out = collections.Counter(); rows = []
    for art in gold['articles']:
        if art['day'] > UNTIL or art['input_id'] not in hand:
            continue
        h = hand[art['input_id']]
        for s in art['statements']:
            spans = [s['span']] + s['also']
            def hit(e):
                q = extraction.normalise(e['quote'])
                return any(extraction.normalise(sp) in q or (len(q) >= 20 and q in extraction.normalise(sp)) for sp in spans)
            kept = [e for e in h['evidence'] if hit(e)]; unpl = [e for e in h.get('unplaced', []) if hit(e)]
            if kept and set(l for e in kept for l in e['links']) & set(s['primary_home']):
                cell = 'kept_right'
            elif kept:
                cell = 'kept_wrong_link'
            elif unpl:
                cell = 'unplaced'
            else:
                cell = 'not_written_or_dropped'
            out[cell] += 1; rows.append((s['id'], s['weight'], cell))
    return dict(out), rows


results = {}
for name, path in RUNS.items():
    f, hand = facts(name, path)
    results[name] = f
keys = ['items', 'days', 'cost (day lines, $)', 'statements kept (placed)', 'statements with no home (v36b: kept aside; v37: dropped, D209)', 'statements dropped for another reason', 'items with no placed evidence',
        'theses opened', 'match outcomes of candidates', 'extraction sends / items (re-sends)', 'links total', 'links to the two revenue sinks', 'links to theme theses', 'judgements of theme theses', 'sinks: pieces / cited by own judgements',
        'judge requests (week): count / median input tokens']
print('| measure | ' + ' | '.join(RUNS) + ' |\n|---|' + '---|' * len(RUNS))
for k in keys:
    print(f'| {k} | ' + ' | '.join(str(results[n][k]) for n in RUNS) + ' |')
for n in RUNS:
    print(f'\n{n} questions:'); [print('  ', q) for q in results[n]['questions']]
