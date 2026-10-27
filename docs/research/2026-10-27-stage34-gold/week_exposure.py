"""D204 acceptance: what the stored-repeat rule exposes the judge to, measured on a week ledger. For every judgement of the week:
the pieces shown (judging-v5 view rule), how many of them belong to a same-claim pair whose other member is also shown, and whether
the judgement cited both members (the double-count the label must prevent). Also the ledger counts the acceptance names.
Run: python3 week_exposure.py <week ledger views.sqlite> [<comparison ledger views.sqlite>]"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind.views import judging, store  # noqa: E402


def counts(path):
    conn = store.open_read_only(path)
    q = lambda sql: conn.execute(sql).fetchone()[0]
    has = lambda t: bool(conn.execute("select 1 from sqlite_master where type='table' and name=?", (t,)).fetchone())
    out = {'views': q('select count(*) from views'), 'evidence': q('select count(*) from evidence'), 'links': q('select count(*) from evidence_links'),
           'sources': q('select count(*) from evidence_sources'), 'judgements': q('select count(*) from judgements'),
           'replacements': q('select count(*) from replacements'), 'revisions': q('select count(*) from revisions') if has('revisions') else None,
           'same_claims': q('select count(*) from same_claims') if has('same_claims') else None,
           'late_statements': q('select count(*) from late_statements')}
    return conn, out


def exposure(conn):
    """Replays the view rule at each judgement: shown pieces, pairs both shown, pairs both cited."""
    if not conn.execute("select 1 from sqlite_master where type='table' and name='same_claims'").fetchone():
        return None
    pairs = [(r['old_evidence_id'], r['new_evidence_id']) for r in conn.execute('select old_evidence_id, new_evidence_id from same_claims')]
    partner = {}
    for a, b in pairs:
        partner.setdefault(a, set()).add(b); partner.setdefault(b, set()).add(a)
    judged = conn.execute('select judgement_id, view_id, seq, cited_evidence_json from judgements order by judgement_id').fetchall()
    both_shown = both_cited = shown_total = judgements_with_pair = 0
    for j in judged:
        # pieces linked to the view before this judgement, under the v5 view rule as of the final ledger (the rule reads recent judgements;
        # at acceptance this approximates the request the judge saw; the exact request bytes are in the archive)
        shown, _ = judging.evidence_in_view(conn, j['view_id'], 'judging-v5')
        shown_ids = {p['evidence_id'] for p in shown if store.evidence(conn, p['evidence_id'])['created_seq'] <= j['seq']}
        shown_total += len(shown_ids)
        pairs_here = {frozenset((a, b)) for a in shown_ids for b in partner.get(a, ()) if b in shown_ids}
        if pairs_here:
            judgements_with_pair += 1
        both_shown += len(pairs_here)
        cited = set(json.loads(j['cited_evidence_json'] or '[]'))
        both_cited += sum(1 for p in pairs_here if p <= cited)
    return {'judgements': len(judged), 'pieces shown (sum)': shown_total, 'same-claim pairs both shown (sum)': both_shown,
            'judgements with a pair in view': judgements_with_pair, 'pairs with both members cited': both_cited}


if __name__ == '__main__':
    conn, c = counts(sys.argv[1])
    print('week ledger:', json.dumps(c))
    print('exposure:', json.dumps(exposure(conn)))
    if len(sys.argv) > 2:
        _, c2 = counts(sys.argv[2])
        print('comparison ledger:', json.dumps(c2))
