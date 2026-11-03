"""Every candidate decision in a ledger's match records (each input's candidates sit in exactly one record; checked), classed by the mechanism that set its outcome:
merged or succession; opened new with the collision judge calling a peer the same question (blocked later), the same question for
another period, or a distinct question in the same matter; opened new on Jev alone by its strongest label; or nothing to compare."""
import sqlite3, json, sys, re, collections
def census(db):
    conn = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    holding = collections.defaultdict(list)
    for rec in conn.execute('select id, input_id, decisions_json from match_records order by id'):
        if json.loads(rec['decisions_json'] or '{}').get('candidates'):
            holding[rec['input_id']].append(rec)
    if any(len(recs) > 1 for recs in holding.values()):
        raise SystemExit('an input has candidates in more than one match record: decide which one counts before counting')
    classes = collections.Counter()
    examples = collections.defaultdict(list)
    for input_id, (rec,) in holding.items():
        for c in json.loads(rec['decisions_json'] or '{}').get('candidates', []):
            reason = c.get('reason', '')
            outcome = c.get('outcome')
            if outcome in ('merge', 'succession'):
                cls = outcome
            elif 'no list' in reason:
                cls = 'new: nothing listed'
            else:
                judge = reason.split('collision judge: ')[1] if 'collision judge: ' in reason else ''
                verdicts = re.findall(r'(v\d+): (\w+)', judge)
                labels = re.findall(r'(v\d+): (\w+) ([0-9.]+)', reason.split('; groups joined')[0])
                if verdicts:
                    kinds = {k for _, k in verdicts}
                    if 'same_question' in kinds: cls = 'new: judge said same question'
                    elif 'same_question_other_period' in kinds: cls = 'new: judge said other period'
                    elif 'distinct_question_same_matter' in kinds: cls = 'new: judge said distinct, same matter'
                    else: cls = 'new: judge said different'
                else:
                    order = ['same_quantity_or_event', 'same_quantity_other_period', 'part_of', 'same_matter_different_quantity', 'cannot_tell', 'different']
                    best = min((order.index(l) for _, l, _ in labels if l in order), default=len(order) - 1)
                    cls = 'new: Jev alone, strongest ' + order[best]
            classes[cls] += 1
            if len(examples[cls]) < 3:
                examples[cls].append((input_id, reason[:160]))
    return classes, examples, conn.execute('select count(*) from views').fetchone()[0]
for db in sys.argv[1:]:
    classes, examples, views = census(db)
    print('=====', db.split('/data/')[1], 'questions', views, 'candidates', sum(classes.values()))
    for cls, n in sorted(classes.items(), key=lambda kv: -kv[1]):
        print(f'  {n:4d}  {cls}')
