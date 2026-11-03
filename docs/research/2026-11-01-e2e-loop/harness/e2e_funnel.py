"""The whole pipeline as one funnel, from stored end-to-end run folders ($0): per stage, what went in, what came out, what the
gold says about it, and what the stage cost. Three run folders per arm; every number is the mean over draws with the draws beside it.
The gold part reuses e2e_compare.py's classification (one research matter in one article; score_gold.same_matter); the stages the
gold does not cover (matching, judging) are counted, not judged, and the table says so.

    python3 harness/e2e_funnel.py default=poc/data/e2e-v69-dev14-2026-10-31,poc/data/e2e-v69-dev14-d2,poc/data/e2e-v69-dev14-d3 \
                          best=poc/data/e2e-v83-seed-d1,poc/data/e2e-v83-seed-d2,poc/data/e2e-v83-seed-d3
"""
import collections
import json
import sqlite3
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REFERENCE_CONTEXT = ROOT / 'docs/research/2026-10-31-reference-context'
sys.path[:0] = [str(REFERENCE_CONTEXT), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402
from hivemind import model  # noqa: E402

UNLISTED_NOISE_SHARE = 0.27          # e2e_compare.py: two blind readers on 60 gold-unlisted statements, 16 of 60 not kept
FIRST = 'This is the first judgement.'


def gold_side(views, archive):
    """e2e_compare.measure, kept in step: every gold core/supporting matter of a processed article by what happened to it."""
    replaced = {r[0] for r in views.execute('select old_evidence_id from replacements')}
    repeats = {r[0] for r in views.execute('select new_evidence_id from same_claims')}

    def answer(iid):
        r = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {iid},%',)).fetchone()
        return json.loads(r[0]) if r and r[0] else {}

    def gold_class(a, e):
        if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] in ('core', 'supporting')):
            return 'core/supp'
        if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] == 'optional') or any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'optional'):
            return 'optional'
        if any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'not_kept'):
            return 'not_kept'
        return 'unlisted'

    pieces, matters, processed, gold_counts = collections.Counter(), collections.Counter(), 0, collections.Counter()
    for a in sr.articles:
        iid = a['input_id']
        stored = [dict(r) for r in views.execute('select evidence_id, quote, one_line from evidence where created_from_input=?', (iid,))]
        h = views.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (iid,)).fetchone()
        if not h and not stored:
            continue
        processed += 1
        by_id = {e['id']: e for e in answer(iid).get('evidence', [])}
        dropped_ids = {e for e, _ in json.loads(h['handover_json']).get('dropped', [])} if h else set()
        dropped = [by_id[e] for e in dropped_ids if e in by_id]
        shown = [s for s in stored if s['evidence_id'] not in replaced]
        for s in shown:
            pieces[('reaches', gold_class(a, s))] += 1
        for e in dropped:
            pieces[('dropped', gold_class(a, e))] += 1
        for it in a['items']:
            if it['weight'] not in ('core', 'supporting'):
                continue
            gold_counts[it['weight']] += 1
            if any(sr.sg.same_matter(it, s) for s in shown if s['evidence_id'] not in repeats):
                state = 'reaches'
            elif any(sr.sg.same_matter(it, s) for s in shown):
                state = 'reaches as repeat'
            elif any(sr.sg.same_matter(it, e) for e in dropped):
                state = 'dropped at placement'
            elif any(sr.sg.same_matter(it, e) for e in by_id.values()):
                state = 'extracted, lost later'
            else:
                state = 'not extracted'
            matters[(it['weight'], state)] += 1
    return pieces, matters, processed, gold_counts


def measure(run):
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); views.row_factory = sqlite3.Row
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    q1 = lambda sql, *a: views.execute(sql, a).fetchone()[0]
    r = {}
    # 0 input
    r['0 days'] = q1('select count(*) from days_completed')
    r['0 items processed'] = q1("select count(distinct input_id) from processing_steps where step='extracted'")
    pieces, matters, processed, gold_counts = gold_side(views, archive)
    r['0 of them gold articles'] = processed
    r['0 gold core matters'] = gold_counts['core']
    r['0 gold supporting matters'] = gold_counts['supporting']
    # 1 extraction
    written = sum(len(json.loads(a).get('evidence', [])) for (a,) in archive.execute("select answer_json from model_calls where purpose='extract' and answer_json is not null"))
    hand = [json.loads(h) for (h,) in views.execute('select handover_json from handovers')]
    filed = sum(len(h.get('evidence', [])) for h in hand)
    dropped_no_home = sum(len(h.get('dropped', [])) for h in hand)
    r['1 statements the model wrote'] = written
    r['1 lost between the answer and the handover'] = written - filed - dropped_no_home
    r['1 statements per item'] = round(written / max(1, r['0 items processed']), 2)
    r['1 gold core extracted'] = gold_counts['core'] - matters[('core', 'not extracted')]
    r['1 gold core not extracted'] = matters[('core', 'not extracted')]
    r['1 gold supporting not extracted'] = matters[('supporting', 'not extracted')]
    # the extraction's own noise, before placement (an extraction arm's regression guard): gold not-kept and unlisted statements it wrote
    r['1 gold not-kept statements written (gold articles)'] = pieces[('reaches', 'not_kept')] + pieces[('dropped', 'not_kept')]
    r['1 unlisted statements written (gold articles)'] = pieces[('reaches', 'unlisted')] + pieces[('dropped', 'unlisted')]
    one_lines = [len(e.get('one_line') or '') for (a,) in archive.execute("select answer_json from model_calls where purpose='extract' and answer_json is not null")
                 for e in json.loads(a).get('evidence', [])]
    r['1 one_line characters, mean'] = round(sum(one_lines) / max(1, len(one_lines)), 1)
    # 2 placement
    r['2 statements dropped, no home'] = dropped_no_home
    r['2 share of written statements dropped'] = round(dropped_no_home / max(1, written), 2)
    r['2 statements filed (evidence rows)'] = q1('select count(*) from evidence')
    r['2 links written'] = q1('select count(*) from evidence_links')
    r['2 links per filed statement'] = round(r['2 links written'] / max(1, r['2 statements filed (evidence rows)']), 2)
    r['2 gold core dropped at placement'] = matters[('core', 'dropped at placement')]
    r['2 gold supporting dropped at placement'] = matters[('supporting', 'dropped at placement')]
    r['2 gold core reaching (incl. repeats)'] = matters[('core', 'reaches')] + matters[('core', 'reaches as repeat')]
    r['2 gold supporting reaching (incl. repeats)'] = matters[('supporting', 'reaches')] + matters[('supporting', 'reaches as repeat')]
    reaching = sum(v for (p, g), v in pieces.items() if p == 'reaches')
    r['2 pieces reaching judgement (gold articles)'] = reaching
    r['2 of them noise (est.)'] = round(pieces[('reaches', 'not_kept')] + UNLISTED_NOISE_SHARE * pieces[('reaches', 'unlisted')], 1)
    # 3 questions
    r['3 questions from seeds'] = q1("select count(*) from views where created_from_input like 'seed:%'")
    r['3 questions opened by articles'] = q1("select count(*) from views where created_from_input not like 'seed:%'")
    r['3 of them theme questions'] = q1("select count(*) from views where created_from_input not like 'seed:%' and kind='theme'")
    r['3 open at the end'] = q1('select count(*) from views v where (select open from view_switches s where s.view_id=v.view_id order by id desc limit 1)=1')
    # 4 matching
    outcomes = collections.Counter()
    for (d,) in views.execute('select decisions_json from match_records'):
        for c in json.loads(d).get('candidates', []):
            outcomes[c.get('outcome', '?')] += 1
    r['4 candidates judged by matching'] = sum(outcomes.values())
    for k, v in sorted(outcomes.items()):
        r[f'4   outcome {k}'] = v
    r['4 collision-judge calls (LLM)'] = archive.execute("select count(*) from model_calls where purpose='match' and model!='jev-1.14.0'").fetchone()[0]
    r['4 repeats recorded (same_claims)'] = q1('select count(*) from same_claims')
    r['4 successions / replacements'] = f"{q1('select count(*) from successions')} / {q1('select count(*) from replacements')}"
    # 5 judging
    r['5 judgements'] = q1('select count(*) from judgements')
    r['5 questions judged at least once'] = q1('select count(distinct view_id) from judgements')
    later = q1('select count(*) from judgements where why_changed != ?', FIRST)
    r['5 later judgements the judge marked changed'] = f"{q1('select count(*) from judgements where why_changed != ? and changed=1', FIRST)} of {later}"
    paths = collections.defaultdict(list)                       # the rung path per question, in judgement order: the moves and the reversals a reader would see
    for view_id, rung in views.execute('select view_id, rung from judgements order by view_id, judgement_id'):
        paths[view_id].append(rung)
    moved = sum(1 for p in paths.values() for i in range(1, len(p)) if p[i] != p[i - 1])
    reversed_ = sum(1 for p in paths.values() for i in range(2, len(p)) if p[i] != p[i - 1] and p[i] == p[i - 2])
    r['5 later judgements that moved the rung / moved back'] = f'{moved} / {reversed_} of {later}'
    rungs = collections.Counter(x for (x,) in views.execute('select rung from judgements'))
    r['5 rung distribution 1/2/3'] = '/'.join(str(rungs.get(k, 0)) for k in (1, 2, 3))
    r['5 cited pieces per judgement'] = round(statistics.mean(len(json.loads(c)) for (c,) in views.execute('select cited_evidence_json from judgements')), 2) if r['5 judgements'] else 0
    jt = archive.execute("select round(avg(input_tokens)), max(input_tokens) from model_calls where purpose='judge'").fetchone()
    r['5 judge request tokens mean / max'] = f'{int(jt[0] or 0)} / {jt[1] or 0}'
    # 6 state at the end
    r['6 questions with no evidence filed'] = q1('select count(*) from views v where not exists (select 1 from evidence_links l where l.view_id=v.view_id)')
    r['6 questions never judged'] = q1('select count(*) from views v where not exists (select 1 from judgements j where j.view_id=v.view_id)')
    # cost
    cost = collections.defaultdict(float); secs = collections.defaultdict(float)
    for purpose, mdl, i, o, s in archive.execute('select purpose, model, sum(input_tokens), sum(output_tokens), sum(seconds) from model_calls group by purpose, model'):
        pin, pout = model.PRICES.get(mdl, (0, 0))
        cost[purpose] += (i or 0) / 1e6 * pin + (o or 0) / 1e6 * pout
        secs[purpose] += s or 0
    for p in ('extract', 'place', 'match', 'judge'):
        r[f'$ {p} (list price)'] = round(cost[p], 2)
    r['$ total (list price)'] = round(sum(cost.values()), 2)
    r['$ per item'] = round(sum(cost.values()) / max(1, r['0 items processed']), 4)
    r['time model seconds, total'] = int(sum(secs.values()))
    return r


def main(args):
    arms = {}
    for arg in args:
        name, paths = arg.split('=', 1)
        arms[name] = [measure(str(ROOT / p) if not p.startswith('/') else p) for p in paths.split(',')]
    keys = []                                     # the union of the rows, in first-seen order (an outcome one arm never produced is 0 there)
    for runs in arms.values():
        for r in runs:
            keys += [k for k in r if k not in keys]
    print(f'{"":<46}' + ''.join(f'{name:>30}' for name in arms))
    for k in keys:
        cells = []
        for name, runs in arms.items():
            vals = [r.get(k, 0) for r in runs]
            if all(isinstance(v, (int, float)) for v in vals):
                cells.append(f'{statistics.mean(vals):>8.1f} {str(vals):>20}')
            else:
                cells.append(' | '.join(str(v) for v in vals))
        print(f'{k:<46}' + ''.join(f'{c:>30}' for c in cells))
    print('\nmeasured against the gold: stages 1–3 (one matter in one article, score_gold.same_matter; noise = gold not-kept + 27% of unlisted).'
          '\ncounted only, no gold on this window: matching outcomes, judgements, rungs, costs. Link precision and question duplicates come from the 2026-10-31 blind reads.')


if __name__ == '__main__':
    main(sys.argv[1:])
