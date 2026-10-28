"""What the placer rejects that the in-call linking kept: the poc-v35 week's placed pieces (255, stored in its handovers) sent to the
placer with the theses shown at their turn; the share placed again, and the rejected ones listed for reading. Pool of 8; scratch archive."""
import json, sqlite3, sys, os, collections, random, concurrent.futures
random.seed(9)
TITLE = '--title' in sys.argv
NARROW = '--narrow' in sys.argv
DRIVERS = json.load(open(os.path.join(os.path.dirname(__file__), 'drivers-seed.json'))) if '--drivers' in sys.argv else []
HINTS = True if '--hints' in sys.argv else ('events' if '--event-hints' in sys.argv else False)
ALIASES = '--no-aliases' not in sys.argv
ROOT='/Users/lchingen/hivemind-extraction-quality-2026-10-28'; sys.path.insert(0, ROOT+'/src')
from hivemind import config, model, placement
from hivemind.views import store
V35='/Users/lchingen/hivemind/poc/data/english-v35-nvda-2w-2026-10-28'
cfg=config.load(ROOT+'/poc/config/poc-v36.json')
c=sqlite3.connect(f'file:{V35}/views.sqlite?mode=ro', uri=True); c.row_factory=sqlite3.Row
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
archive=model.Archive(os.path.join(os.path.dirname(__file__), 'results', 'archive-placer-over-v35' + ('-hints' if HINTS is True else '-eventhints' if HINTS else '') + ('-aliases' if ALIASES else '') + ('-title' if TITLE else '') + ('-narrow' if NARROW else '') + ('-drivers' if DRIVERS else '') + '.sqlite'))
cutoff=c.execute("select max(sequence_no) from processing_steps where publication_day<=?", ('2026-07-07',)).fetchone()[0]
jobs=[]
for r in c.execute("select input_id, seq, handover_json from handovers where seq<=? order by seq", (cutoff,)):
    h=json.loads(r['handover_json'])
    if not h['evidence']: continue
    shown=[dict(store.view(c, x['view_id']), key=store.view_key(c, x['view_id']) or {}, groups=[{'name': g['name'], 'scope': g['scope'], 'aliases': g.get('aliases') or []} for g in store.groups_of_view(c, x['view_id'])]) for x in c.execute("select view_id from views where created_seq<? order by created_seq", (r['seq'],)) if store.is_open(c, x['view_id'])]
    item=dict(t.execute('select publisher, publication_day, title from items where input_id=?', (r['input_id'],)).fetchone()) if TITLE else None
    jobs.append((r['input_id'], h['evidence'], shown + DRIVERS, item))
def send(job):
    iid, statements, shown, item = job
    if HINTS or not ALIASES:
        raise SystemExit('the hints and no-aliases arms are retired with those options of placement.py (routing-analysis.md §8)')
    placed, unplaced, answer = placement.place(archive, cfg, statements, shown, item=item, prompt=('placement-narrow-v1' if NARROW else 'placement-v1'))
    return iid, statements, placed, unplaced, answer.cost_usd
tot=kept=0; rejected=[]; cost=0; results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for iid, statements, placed, unplaced, cst in pool.map(send, jobs):
        results.append((iid, statements, placed, unplaced, cst))
        tot+=len(statements); kept+=len(placed); cost+=cst
        rejected += [(iid, e) for e in unplaced]
print(f'items {len(jobs)}: v35 placed pieces {tot}; the placer places {kept} ({kept/tot:.0%}) and rejects {len(rejected)}; cost ${cost:.3f}')
if DRIVERS:
    import collections as _c; land=_c.defaultdict(list)
    for iid, statements, placed, unplaced, cst in results:
        for e in placed:
            for l in e['links']:
                if l.startswith('d'): land[l].append(e['one_line'][:110])
    for d in sorted(land): print(f'\n{d}: {len(land[d])} pieces'); [print('   -', x) for x in land[d][:10]]
print('\ndecisive cases:'); [print(f"  {'REJECTED' if (iid,e) in rejected else 'placed  '} {e['one_line'][:110]}") for iid, e in [(j[0], e) for j in jobs for e in j[1]] if any(w in e['one_line'] for w in ('Rubin Ultra','roadmap','NVL576','Oberon','Sharon AI plans','revenue-sharing','Goldman','Alphabet is renting'))]
print('\n20 random rejected pieces (in-call links shown):')
for iid, e in random.sample(rejected, min(20, len(rejected))):
    print(f"- [{e['tier']}] in-call {e['links']} who='{(e.get('original_who') or '')[:28]}' | {e['one_line'][:150]}")
