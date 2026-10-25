"""Compare two ledgers built from the same items under two configurations (log row 34: the generative matching call vs
Jev): library counts, decisions by kind, evidence consolidation, groups, dependencies, cost and time per stage, and
decision-level agreement on every item whose extraction handover is identical in both. Read-only.

Usage: python3 scripts/compare_ledgers.py --a poc/data/english-groups4-2026-10-25 --b poc/data/english-jev-2026-10-25 [--label-a control --label-b jev]
"""
import argparse, collections, json, pathlib, sqlite3, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind.views import store  # noqa: E402
PRICES = {'gpt-6-luna': (0.10, 0.50), 'jev-1.14.0': (0.042, 0.0)}


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def library(conn):
    out = {}
    q = lambda sql: conn.execute(sql).fetchone()[0]
    out['theses'] = q('select count(*) from views')
    out['open theses'] = len(store.open_views(conn))
    out['successions'] = q('select count(*) from successions')
    out['dependencies'] = q('select count(*) from dependencies')
    out['evidence stored'] = q('select count(*) from evidence')
    out['evidence links'] = q('select count(*) from evidence_links')
    out['evidence sources'] = q('select count(*) from evidence_sources')
    out['replacements'] = q('select count(*) from replacements')
    out['late statements'] = q('select count(*) from late_statements')
    out['groups'] = q('select count(*) from thesis_groups') if conn.execute("select count(*) from sqlite_master where name='thesis_groups'").fetchone()[0] else 0
    out['memberships'] = q('select count(*) from thesis_group_members') if out['groups'] is not None and conn.execute("select count(*) from sqlite_master where name='thesis_group_members'").fetchone()[0] else 0
    out['judgements'] = q('select count(*) from judgements')
    out['items failed'] = q("select count(distinct input_id) from processing_steps where result='failed'")
    quotes = collections.Counter(' '.join((r[0] or '').split()) for r in conn.execute('select quote from evidence'))
    out['exact-quote duplicate groups'] = sum(1 for v in quotes.values() if v > 1)
    return out


def decisions(conn):
    cand, ev = collections.Counter(), collections.Counter()
    retries = 0
    for r in conn.execute('select call_no, decisions_json, checks_json from match_records'):
        d = json.loads(r['decisions_json'] or '{}')
        retries += r['call_no'] in (2, 4)
        for x in d.get('candidates', []):
            cand[x.get('outcome')] += 1
        for x in d.get('evidence', []):
            ev[x.get('outcome')] += 1
    return cand, ev, retries


def stages(archive):
    out = {}
    for r in archive.execute('select purpose, model, count(*) n, sum(input_tokens) i, sum(output_tokens) o, sum(seconds) s, sum(cost_usd) c from model_calls group by purpose, model'):
        price = PRICES.get(r['model'], (0.0, 0.0))
        out[(r['purpose'], r['model'])] = {'calls': r['n'], 'input_tokens': r['i'] or 0, 'output_tokens': r['o'] or 0, 'seconds': round(r['s'] or 0, 1),
                                           'cost_published': round((r['i'] or 0) / 1e6 * price[0] + (r['o'] or 0) / 1e6 * price[1], 4)}
    return out


def handovers(conn):
    return {r['input_id']: (r['handover_json'], r['seq']) for r in conn.execute('select input_id, handover_json, seq from handovers')}


def written_outcomes(conn):
    """Per input: candidate id -> written destination (view id), from match records' final decisions after checks."""
    out = {}
    for r in conn.execute('select input_id, call_no, decisions_json, checks_json from match_records order by id'):
        d = json.loads(r['decisions_json'] or '{}')
        if r['call_no'] in (1, 2):
            out.setdefault(r['input_id'], {'candidates': {}, 'evidence': {}})
            for x in d.get('candidates', []):
                out[r['input_id']]['candidates'][x['id']] = (x['outcome'], x.get('target_view_id') or '')
            for x in d.get('evidence', []):
                out[r['input_id']]['evidence'][(x['id'], x['view_id'])] = (x['outcome'], x.get('target_evidence_id') or '')
    return out


def read_diffs(va, vb, label_a, label_b, limit):
    """Print every decision where the two ledgers differ on an identical handover, with the incoming piece, both targets'
    texts and both reasons, so each can be judged from the text (AGENTS §1: read the case, not the count)."""
    def recs(c, input_id):
        out = {'candidates': {}, 'evidence': {}}
        for r in c.execute('select call_no, decisions_json from match_records where input_id=? order by id', (input_id,)):
            d = json.loads(r['decisions_json'] or '{}')
            if r['call_no'] in (1, 2):
                for x in d.get('candidates', []):
                    out['candidates'][x['id']] = x
                for x in d.get('evidence', []):
                    out['evidence'][(x['id'], x['view_id'])] = x
        return out

    def ev_text(c, eid):
        e = c.execute('select one_line, quote, speaker, original_day from evidence where evidence_id=?', (eid,)).fetchone()
        return f"[{e['speaker']} {e['original_day']}] {e['one_line']} | {e['quote'][:150]}" if e else '(none)'
    ha, hb = handovers(va), handovers(vb)
    printed = 0
    for i in ha:
        if i not in hb or ha[i][0] != hb[i][0]:
            continue
        hand = json.loads(ha[i][0])
        pieces = {e['id']: e for e in hand['evidence']}
        cands = {c['id']: c for c in hand['candidates']}
        ra, rb = recs(va, i), recs(vb, i)
        for cid, xa in ra['candidates'].items():
            xb = rb['candidates'].get(cid)
            if xb and xa['outcome'] != xb['outcome']:
                c = cands[cid]
                print(f"\n### {i} candidate {cid}: {c['looks_at']} | {c.get('measure')} {c.get('scope')} {c.get('period_start')}..{c.get('period_end')}")
                print(f"  {label_a}: {xa['outcome']} -> {xa['target_view_id']} ({xa['reason'][:160]})\n  {label_b}: {xb['outcome']} -> {xb['target_view_id']} ({xb['reason'][:220]})")
                printed += 1
        for key, xa in ra['evidence'].items():
            xb = rb['evidence'].get(key)
            if xb and xa['outcome'] != xb['outcome']:
                e = pieces[key[0]]
                print(f"\n### {i.split(':')[-1]} {key}: INCOMING [{e['speaker']} {e['original_day']}] {e['one_line']} | {e['quote'][:170]}")
                print(f"  {label_a}: {xa['outcome']} {xa['target_evidence_id'] or ''} -> {ev_text(va, xa['target_evidence_id']) if xa['target_evidence_id'] else ''}\n     {xa['reason'][:170]}")
                print(f"  {label_b}: {xb['outcome']} {xb['target_evidence_id'] or ''} -> {ev_text(vb, xb['target_evidence_id']) if xb['target_evidence_id'] else ''}\n     {xb['reason'][:220]}")
                printed += 1
        if printed >= limit:
            break
    print(f"\n{printed} differences printed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--a', required=True); ap.add_argument('--b', required=True)
    ap.add_argument('--label-a', default='control'); ap.add_argument('--label-b', default='jev')
    ap.add_argument('--read-diffs', type=int, default=0, help='print up to N differing decisions with their texts')
    args = ap.parse_args()
    A, B = ROOT / args.a, ROOT / args.b
    va, vb = ro(A / 'views.sqlite'), ro(B / 'views.sqlite')
    aa, ab = ro(A / 'archive.sqlite'), ro(B / 'archive.sqlite')
    la, lb = library(va), library(vb)
    print(f'| measure | {args.label_a} | {args.label_b} |\n|---|---:|---:|')
    for k in la:
        print(f'| {k} | {la[k]} | {lb[k]} |')
    ca, ea, ra = decisions(va); cb, eb, rb = decisions(vb)
    print(f'\n| decisions (raw, incl. retries) | {args.label_a} | {args.label_b} |\n|---|---|---|')
    print(f'| candidates | {dict(ca)} | {dict(cb)} |\n| evidence | {dict(ea)} | {dict(eb)} |\n| matching retries | {ra} | {rb} |')
    sa, sb = stages(aa), stages(ab)
    print(f'\n| stage (archive) | {args.label_a} | {args.label_b} |\n|---|---|---|')
    for key in sorted(set(sa) | set(sb)):
        print(f'| {key[0]} {key[1]} | {sa.get(key, "—")} | {sb.get(key, "—")} |')
    # decision-level agreement on identical handovers
    ha, hb = handovers(va), handovers(vb)
    same = [i for i in ha if i in hb and ha[i][0] == hb[i][0]]
    wa, wb = written_outcomes(va), written_outcomes(vb)
    agree_c = total_c = agree_e = total_e = 0
    diffs = []
    for i in same:
        for cid, oa in wa.get(i, {}).get('candidates', {}).items():
            ob = wb.get(i, {}).get('candidates', {}).get(cid)
            if ob is None:
                continue
            total_c += 1
            if oa[0] == ob[0]:
                agree_c += 1
            else:
                diffs.append(f'- {i} candidate {cid}: {args.label_a} {oa} vs {args.label_b} {ob}')
        for key, oa in wa.get(i, {}).get('evidence', {}).items():
            ob = wb.get(i, {}).get('evidence', {}).get(key)
            if ob is None:
                continue
            total_e += 1
            if oa[0] == ob[0]:
                agree_e += 1
            else:
                diffs.append(f'- {i} evidence {key}: {args.label_a} {oa} vs {args.label_b} {ob}')
    print(f'\nItems with byte-identical extraction handovers: {len(same)} of {len(ha)} / {len(hb)}; candidate decisions agree {agree_c}/{total_c}; evidence decisions agree {agree_e}/{total_e}')
    print('\n'.join(diffs[:80]))
    # thesis lists side by side
    ta = {(r['object_id'], r['looks_at']) for r in va.execute('select object_id, looks_at from views')}
    tb = {(r['object_id'], r['looks_at']) for r in vb.execute('select object_id, looks_at from views')}
    print(f'\nTheses only in {args.label_a} ({len(ta - tb)}):\n' + '\n'.join(f'- {o} | {l}' for o, l in sorted(ta - tb)))
    print(f'\nTheses only in {args.label_b} ({len(tb - ta)}):\n' + '\n'.join(f'- {o} | {l}' for o, l in sorted(tb - ta)))
    if args.read_diffs:
        read_diffs(va, vb, args.label_a, args.label_b, args.read_diffs)
    if lb['groups']:
        print(f'\nGroups in {args.label_b}:')
        for g in vb.execute('select group_id, name from thesis_groups'):
            members = [r[0] for r in vb.execute('select view_id from thesis_group_members where group_id=? order by seq', (g['group_id'],))]
            print(f'- {g["group_id"]} {g["name"]}: {members}')


if __name__ == '__main__':
    main()
