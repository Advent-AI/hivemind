"""Measure the evidence retriever's recall@k separately from the judge (log row 39). For a sample of the week's evidence decisions
whose top-k list was cut while the thesis held more pieces in force, ask Jev once about EVERY piece in force under that thesis
(an offline oracle, never the production path) and record whether the strongest `same_statement` lies outside the list the
retriever showed. A hit outside the list is a candidate recall miss, to be read by hand. Read-only on the ledger; its own archive.

Usage: python3 scripts/recall_oracle.py --ledger poc/data/english-jev2-2026-10-25 --out poc/reports/2026-10-25-recall-oracle [--sample 120] [--cap-usd 0.10]
"""
import argparse, json, pathlib, random, sqlite3, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, jev, model  # noqa: E402
from hivemind.views import jev_matching, matching  # noqa: E402



def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ledger', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--sample', type=int, default=120); ap.add_argument('--cap-usd', type=float, default=0.10)
    ap.add_argument('--from-day', default='2026-07-24')
    args = ap.parse_args()
    out = ROOT / args.out; out.mkdir(parents=True, exist_ok=True)
    conn = ro(ROOT / args.ledger / 'views.sqlite')
    cfg = config.load(str(ROOT / 'poc/config/poc-v22.json'))
    archive = model.Archive(str(out / 'archive.sqlite'))
    replaced_at = {r['old_evidence_id']: r['seq'] for r in conn.execute('select old_evidence_id, seq from replacements')}
    handovers = {r['input_id']: {e['id']: e for e in json.loads(r['handover_json'])['evidence']} for r in conn.execute('select input_id, handover_json from handovers')}
    week = {r['input_id'] for r in conn.execute("select distinct input_id from processing_steps where publication_day >= ?", (args.from_day,))}
    cases = []
    for r in conn.execute('select seq, input_id, shown_json, decisions_json from match_records where call_no in (1,2) order by id'):
        if r['input_id'] not in week:
            continue
        shown = json.loads(r['shown_json'])['evidence']
        decided = {(d['id'], d['view_id']): d for d in json.loads(r['decisions_json'] or '{}').get('evidence', [])}
        for key, listed in shown.items():
            eid, view = key.split('|')
            in_force = []
            for x in conn.execute('select evidence_id from evidence_links where view_id=? and seq<? order by id', (view, r['seq'])):
                if replaced_at.get(x['evidence_id'], 10 ** 9) >= r['seq'] and x['evidence_id'] not in in_force:
                    in_force.append(x['evidence_id'])
            if len(in_force) > len(listed) and (eid, view) in decided and eid in handovers.get(r['input_id'], {}):
                cases.append({'seq': r['seq'], 'input_id': r['input_id'], 'eid': eid, 'view': view, 'listed': listed, 'in_force': in_force,
                              'decision': decided[(eid, view)]})
    random.seed(11)
    sample = random.sample(cases, min(args.sample, len(cases)))
    print(f'{len(cases)} truncated decisions in the week; sampling {len(sample)}')
    spent, results = 0.0, []
    for n, c in enumerate(sample, 1):
        e = handovers[c['input_id']][c['eid']]
        said_day = e.get('original_day') or c['input_id']
        state = jev_matching.piece_state(e, said_day)
        questions = {f'piece__{c["view"]}__{x}': jev_matching.piece_question(matching.describe_evidence(conn, x, english=True)) for x in c['in_force'][:200]}
        if spent > args.cap_usd:
            print('cap reached'); break
        answer = jev.ask(archive, cfg, cfg.matching, state, questions, 'recall_oracle')
        spent += answer.cost_usd
        scored = []
        for x in c['in_force'][:200]:
            a = answer.data[f'piece__{c["view"]}__{x}']
            scored.append((a['probabilities']['same_statement'], a['probabilities']['supersedes'], a['choice'], x))
        inside_best = max((s for s in scored if s[3] in c['listed']), default=(0, 0, '', ''))
        outside_best = max((s for s in scored if s[3] not in c['listed']), default=(0, 0, '', ''))
        results.append({**{k: c[k] for k in ('seq', 'input_id', 'eid', 'view', 'listed')}, 'in_force_n': len(c['in_force']), 'decision': c['decision']['outcome'],
                        'decision_target': c['decision'].get('target_evidence_id'), 'incoming': e['one_line'],
                        'best_inside': {'p_same': inside_best[0], 'p_supersedes': inside_best[1], 'choice': inside_best[2], 'id': inside_best[3]},
                        'best_outside': {'p_same': outside_best[0], 'p_supersedes': outside_best[1], 'choice': outside_best[2], 'id': outside_best[3]},
                        'outside_text': conn.execute('select one_line from evidence where evidence_id=?', (outside_best[3],)).fetchone()[0] if outside_best[3] else ''})
        if n % 20 == 0:
            print(f'  {n} done, ${spent:.4f}')
    (out / 'results.json').write_text(json.dumps(results, indent=1, ensure_ascii=False) + '\n')
    miss = [r for r in results if r['best_outside']['choice'] == 'same_statement' and r['best_outside']['p_same'] >= 0.5 and not (r['best_inside']['choice'] == 'same_statement' and r['best_inside']['p_same'] >= 0.5)]
    both = [r for r in results if r['best_outside']['choice'] == 'same_statement' and r['best_outside']['p_same'] >= 0.5 and r['best_inside']['choice'] == 'same_statement' and r['best_inside']['p_same'] >= 0.5]
    with_repeat = [r for r in results if (r['best_outside']['choice'] == 'same_statement' and r['best_outside']['p_same'] >= 0.5) or (r['best_inside']['choice'] == 'same_statement' and r['best_inside']['p_same'] >= 0.5)]
    lines = [f'# Evidence retriever recall@k, oracle over every piece in force ({len(results)} sampled truncated decisions of {len(cases)}; ${spent:.4f})', '',
             f'- decisions where the oracle finds a same-statement piece anywhere: {len(with_repeat)}',
             f'- of which the strongest lies only OUTSIDE the shown top-{len(results[0]["listed"]) if results else 10} (candidate recall misses, to read): **{len(miss)}**',
             f'- inside and outside both ≥ 0.5: {len(both)}',
             f'- recall@k estimate on decisions with a true repeat (before reading the misses): {(len(with_repeat) - len(miss))}/{len(with_repeat)}', '', '## Candidate misses']
    for r in miss:
        lines.append(f"- {r['input_id'][-30:]} {r['eid']}→{r['view']} ({r['in_force_n']} in force, decided {r['decision']} {r['decision_target'] or ''})\n    IN: {r['incoming'][:110]}\n    OUTSIDE {r['best_outside']['id']} p_same {r['best_outside']['p_same']}: {r['outside_text'][:110]}\n    best inside: {r['best_inside']['id']} {r['best_inside']['choice']} {r['best_inside']['p_same']}")
    (out / 'summary.md').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines[:7]))


if __name__ == '__main__':
    main()
