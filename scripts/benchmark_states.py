"""The per-state benchmark of the matching step (log row 41): for each state of the two-layer design, both arms against the
golds, with the retrieval stage measured apart, a threshold sweep from the archived Jev answers (robustness), and cost and
time per stage. Read-only. Writes a Markdown report.

Usage: python3 scripts/benchmark_states.py --out poc/reports/2026-10-25-benchmark/benchmark.md
       [--arm control=poc/data/english-groups4-2026-10-25 --arm jev=poc/data/english-jev2-2026-10-25]
       [--week-gold …json] [--seed-gold …json] [--oracle …summary.md] [--title …]
Two arms, in order: the generative-matching arm first, the Jev arm second (the threshold sweep reads the second arm's archive).
Each arm's label names its section in the golds.
"""
import argparse, collections, json, pathlib, sqlite3, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind.model import PRICES  # noqa: E402  (the published rates' one owner)
DEFAULT_ARMS = ['control=poc/data/english-groups4-2026-10-25', 'jev=poc/data/english-jev2-2026-10-25']
ARMS = {}
WEEK_GOLD = 'poc/eval/gold/week-benchmark-2026-10-25.json'
SEED_GOLD = 'poc/eval/gold/evidence-decisions-seed-2026-10-25.json'
ORACLE = 'poc/reports/2026-10-25-recall-oracle/summary.md'


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def final_candidate_decisions(conn, window_from=None):
    """input|cid -> (checked outcome as written, target view id, candidate card) from the final first-pass record of each input.
    The outcome scored is what the ledger did after the code checks: a view created (succession when a successions row names
    it, else new), or a merge the checks accepted (the raw answer with no view created)."""
    last = {}
    in_window = None
    if window_from:
        in_window = {r[0] for r in conn.execute('select distinct input_id from processing_steps where publication_day >= ?', (window_from,))}
    for r in conn.execute('select input_id, decisions_json from match_records where call_no in (1,2) order by id'):
        if in_window is None or r['input_id'] in in_window:
            last[r['input_id']] = r['decisions_json']
    successors = {r['view_id']: r['succeeds'] for r in conn.execute('select view_id, succeeds from successions')}
    out = {}
    for inp, dj in last.items():
        d = json.loads(dj or '{}')
        if not d.get('candidates'):
            continue
        hand = {c['id']: c for c in json.loads(conn.execute('select handover_json from handovers where input_id=?', (inp,)).fetchone()['handover_json'])['candidates']}
        written = conn.execute("select reason from processing_steps where input_id=? and step='written' order by id desc limit 1", (inp,)).fetchone()
        new_views = json.loads(written['reason']).get('new', {}) if written else {}
        for x in d['candidates']:
            if x['id'] not in hand:
                continue
            if x['id'] in new_views:
                view_id = new_views[x['id']]
                outcome, target = ('succession', successors[view_id]) if view_id in successors else ('new', '')
            elif x['outcome'] == 'merge':
                outcome, target = 'merge', x.get('target_view_id') or ''
            else:
                outcome, target = 'skip', ''
            out[f"{inp}|{x['id']}"] = (outcome, target, hand[x['id']])
    return out


def candidate_layer(conn, gold_arm, label, window_from=None):
    decisions = final_candidate_decisions(conn, window_from)
    views = {r['view_id']: r['looks_at'] for r in conn.execute('select view_id, looks_at from views')}
    counts = collections.Counter()
    errors = []
    for key, (outcome, target, card) in decisions.items():
        g = gold_arm.get(key)
        if g is None:
            gold_outcome = 'new'          # by the rule: no same-measure thesis of the object existed
        elif g['gold'] == 'either':
            counts['either'] += 1
            continue
        else:
            gold_outcome = g['gold']
        if outcome == 'skip':                 # code's rule: the object is not on the research list; not a judge decision
            counts['skipped_by_code'] += 1
            continue
        if outcome == gold_outcome and (gold_outcome == 'new' or (g and g.get('target_text', '') in views.get(target, ''))):
            counts[('right', gold_outcome)] += 1
        else:
            counts[('wrong', gold_outcome)] += 1
            errors.append(f"- {label} {key[-40:]}: gold {gold_outcome} → {outcome} {target} ({card['looks_at'][:50]})")
    return counts, errors


def membership_layer(conn, gold_arm):
    stored = collections.defaultdict(set)
    for r in conn.execute('select view_id, group_id from thesis_group_members'):
        stored[r['view_id']].add(r['group_id'])
    gold_arm = {m: g for m, g in gold_arm.items() if not m.startswith('_')}          # '_notes' and the like are not matters
    group_of_matter = {m: set(g.get('stored_groups', [])) for m, g in gold_arm.items() if m != 'own_matters'}
    required_hit = required_n = forbidden_hit = 0
    details = []
    forbidden_theses = set()
    for matter, g in gold_arm.items():
        if matter == 'own_matters':
            continue
        groups = group_of_matter[matter]
        for v in g['required']:
            required_n += 1
            if groups and stored.get(v, set()) & groups:
                required_hit += 1
            else:
                details.append(f"- missed required: {v} in {matter}" + ('' if groups else ' (no group for this matter in the ledger)'))
        for v in g['forbidden']:
            hit = stored.get(v, set()) & groups
            # a group that stands for several matters (the fused g1 of both ledgers) is credited for any of them and is not a
            # forbidden admission for its other matters; the fusion itself is reported as F1, not counted per member
            fused_ok = any(v in gold_arm[m2]['required'] + gold_arm[m2].get('optional', []) for m2 in group_of_matter if m2 != matter and group_of_matter[m2] & hit)
            if hit and not fused_ok:
                forbidden_hit += 1
                details.append(f"- forbidden admitted: {v} into {matter} via {sorted(hit)}")
                forbidden_theses.add(v)
    total_memberships = sum(len(s) for s in stored.values())
    return required_hit, required_n, len(forbidden_theses), total_memberships, details


def stage_costs(archive_path, since=None, version=None):
    """Calls, seconds and cost per stage from the archive's tokens at the published rates (never the stored cost_usd, which carries
    the price table of its day); `version` restricts to one configuration's own calls (an archive copied from another run holds its rows)."""
    conn = ro(archive_path)
    out = {}
    clauses = ([f"created_at >= '{since}'"] if since else []) + ([f"config_version = '{version}'"] if version else [])
    where = ('where ' + ' and '.join(clauses)) if clauses else ''
    for r in conn.execute(f'select purpose, model, count(*) n, sum(input_tokens) i, sum(output_tokens) o, sum(seconds) s from model_calls {where} group by purpose, model'):
        p = PRICES[r['model']]                     # an unpriced model stops the report
        out[f"{r['purpose']} {r['model']}"] = {'calls': r['n'], 'seconds': round(r['s'] or 0), 'cost': round((r['i'] or 0) / 1e6 * p[0] + (r['o'] or 0) / 1e6 * p[1], 4)}
    return out


def threshold_sweep(archive_path, thresholds=(0.4, 0.5, 0.6, 0.7)):
    """From the archived Jev answers of the match calls: how many piece decisions and candidate 'same' calls change with the threshold."""
    conn = ro(archive_path)
    repeats = {t: 0 for t in thresholds}
    replaces = {t: 0 for t in thresholds}
    same = {t: 0 for t in thresholds}
    pieces = cands = 0
    for r in conn.execute("select answer_json from model_calls where model='jev-1.14.0' and purpose='match' and answer_json is not null"):
        answers = json.loads(r['answer_json'])
        piece_qs = [a for q, a in answers.items() if q.startswith('piece__')]
        rel_qs = [a for q, a in answers.items() if q.startswith('rel__')]
        if piece_qs:
            pieces += 1
            for t in thresholds:
                if any(a['choice'] == 'same_statement' and a['probabilities']['same_statement'] >= t for a in piece_qs):
                    repeats[t] += 1
                elif any(a['choice'] == 'supersedes' and a['probabilities']['supersedes'] >= t for a in piece_qs):
                    replaces[t] += 1
        if rel_qs:
            cands += 1
            for t in thresholds:
                if any(a['choice'] == 'same_quantity_or_event' and a['probabilities']['same_quantity_or_event'] >= t for a in rel_qs):
                    same[t] += 1
    return pieces, cands, repeats, replaces, same


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--arm', action='append', help='label=path, exactly two, generative arm first')
    ap.add_argument('--week-gold', default=WEEK_GOLD)
    ap.add_argument('--seed-gold', action='append', help='a gold file for both arms, or label=path per arm (ids differ between extractions)')
    ap.add_argument('--oracle', default=ORACLE)
    ap.add_argument('--title', default='Matching benchmark by state (seed + week 2026-07-24..31; log row 41)')
    ap.add_argument('--note', default='Arms: control = the generative matching call (poc-v21); jev = Jev matching (poc-v22, the engine as run that day).')
    ap.add_argument('--version', action='append', default=[], help='label=config_version: count only that configuration\'s own calls in the cost table')
    ap.add_argument('--window-from', help='score only candidates of inputs published on or after this day (a later window of the same ledgers)')
    ap.add_argument('--since', action='append', default=[], help='label=created_at: count only calls created at or after this time in the cost table')
    ap.add_argument('--evidence-key', default='evidence_week', help='the gold section holding the window\'s evidence samples')
    ap.add_argument('--no-seed', action='store_true', help='skip the seed evidence gold (a window after the seed)')
    args = ap.parse_args()
    for spec in args.arm or DEFAULT_ARMS:
        label, path = spec.split('=', 1)
        ARMS[label] = path
    if len(ARMS) != 2:
        sys.exit('exactly two arms')
    A, B = list(ARMS)
    gold = json.loads((ROOT / args.week_gold).read_text())
    md = [f'# {args.title}', '',
          args.note + ' Golds: ' + ', '.join(f'`{pathlib.Path(x).name}`' for x in (args.week_gold, args.seed_gold and args.seed_gold[0] or SEED_GOLD)) + '.', '']
    # ---- layer 1: candidates
    md += ['## Layer 1: the candidate thesis against the library', '', f'| state | {A} right/n | {B} right/n |', '|---|---:|---:|']
    conns = {arm: ro(ROOT / path / 'views.sqlite') for arm, path in ARMS.items()}
    per = {arm: candidate_layer(conns[arm], gold['candidates'][arm], arm, args.window_from) for arm in ARMS}
    for state in ('merge', 'succession', 'new'):
        row = []
        for arm in ARMS:
            c = per[arm][0]
            r, w = c[('right', state)], c[('wrong', state)]
            row.append(f"{r}/{r + w}")
        md.append(f"| {state} | {row[0]} | {row[1]} |")
    md.append(f"| set aside (either) | {per[A][0]['either']} | {per[B][0]['either']} |")
    md.append(f"| skipped by code (object not on the list) | {per[A][0]['skipped_by_code']} | {per[B][0]['skipped_by_code']} |")
    md += [''] + per[A][1] + per[B][1] + ['']
    # ---- memberships
    md += ['## Layer 1b: group memberships (each arm against its own ledger)', '', f'| measure | {A} | {B} |', '|---|---:|---:|']
    mem = {arm: membership_layer(conns[arm], gold['memberships'][arm]) for arm in ARMS}
    md.append(f"| required members recovered | {mem[A][0]}/{mem[A][1]} | {mem[B][0]}/{mem[B][1]} |")
    md.append(f"| forbidden members admitted | {mem[A][2]} | {mem[B][2]} |")
    md.append(f"| memberships written | {mem[A][3]} | {mem[B][3]} |")
    fused = {}
    for arm in ARMS:
        matters = {m: set(gg.get('stored_groups', [])) for m, gg in gold['memberships'][arm].items() if m != 'own_matters' and not m.startswith('_')}
        fused[arm] = sorted({g for groups in matters.values() for g in groups if sum(1 for other in matters.values() if g in other) > 1})
    md.append(f"| groups holding two matters (F1) | {fused[A]} | {fused[B]} |")
    md += [''] + mem[A][4] + [''] + mem[B][4] + ['']
    # ---- layer 2: evidence, seed gold (scorer) and week samples
    md += ['## Layer 2: evidence against the thesis\'s pieces', '']
    seed_golds = {}
    for spec in args.seed_gold or [SEED_GOLD]:
        if '=' in spec:
            label, path = spec.split('=', 1); seed_golds[label] = path
        else:
            seed_golds[A] = seed_golds[B] = spec
    seed = ''
    if not args.no_seed:
        for arm in (A, B):
            scored = subprocess.run([sys.executable, str(ROOT / 'scripts/score_evidence_gold.py'), '--gold', seed_golds[arm], '--ledger', f"{arm}={ARMS[arm]}"],
                                    capture_output=True, text=True, cwd=ROOT)
            if scored.returncode != 0:                 # never publish a report whose seed section failed
                sys.exit(f'the evidence scorer failed for {arm}:\n{scored.stderr[-2000:]}')
            seed += scored.stdout + '\n'
        md += ['### Seed (golds: ' + ', '.join(f'{a} `{pathlib.Path(g).name}`' for a, g in seed_golds.items()) + ')', '', '```', seed.strip(), '```', '']
    ev = gold[args.evidence_key]
    md += ['### Window samples (all replacements + repeats + new per arm, read from the texts)', '', f'| state | {A} right/wrong/debatable | {B} right/wrong/debatable |', '|---|---|---|']
    for state in ('repeat', 'replace', 'new'):
        c, j = ev[A][state], ev[B][state]
        md.append(f"| {state} | {c['right']}/{c['wrong']}/{c['debatable']} | {j['right']}/{j['wrong']}/{j['debatable']} |")
    md.append('')
    for arm in (A, B):
        for state in ('repeat', 'replace', 'new'):
            reasons = ev[arm][state].get('wrong_reasons')
            if reasons:
                md.append(f"{arm} {state}, why wrong: {reasons}")
    md.append('')
    # ---- retrieval
    md += ['## Retrieval, measured apart', '']
    oracle = (ROOT / args.oracle).read_text().splitlines()[:7] if (ROOT / args.oracle).exists() else ['(oracle not run)']
    md += ['- theses: every open thesis of the item\'s objects is shown and is a legal target; in all six known duplicates the earlier thesis was in the later candidate\'s list.'] + ['- evidence: ' + l.lstrip('- #') for l in oracle if l.strip()] + ['']
    # ---- robustness: threshold sweep
    pieces, cands, repeats, replaces, same = threshold_sweep(ROOT / ARMS[B] / 'archive.sqlite')
    md += ['## Robustness: the same archived Jev answers under other thresholds', '', f"{pieces} evidence calls and {cands} candidate calls in the {B} archive.", '',
           '| threshold | evidence calls deciding repeat | deciding replace | candidate calls with a `same` ≥ t |', '|---:|---:|---:|---:|']
    for t in (0.4, 0.5, 0.6, 0.7):
        md.append(f"| {t} | {repeats[t]} | {replaces[t]} | {same[t]} |")
    md += ['', 'The decisions were taken at 0.5 (pre-set, never tuned). Rows show how many calls would change their first-stage outcome if the threshold moved; the writer\'s and checker\'s rules apply after.', '']
    # ---- cost and time
    md += ['## Cost and time per stage (archives; published rates)', '', f'| stage | {A} | {B} |', '|---|---|---|']
    versions = dict(v.split('=', 1) for v in args.version)
    since = dict(v.split('=', 1) for v in args.since)
    ca = stage_costs(ROOT / ARMS[A] / 'archive.sqlite', since=since.get(A), version=versions.get(A))
    cb = stage_costs(ROOT / ARMS[B] / 'archive.sqlite', since=since.get(B), version=versions.get(B))
    for k in sorted(set(ca) | set(cb)):
        md.append(f"| {k} | {ca.get(k, '—')} | {cb.get(k, '—')} |")
    md += ['', ('Each arm counted on its own configuration\'s calls only (the archives began as copies of an earlier run).' if versions else
                f'The {B} archive began as a copy of an earlier archive, so its gpt-6-luna rows include calls served from the cache; the jev-1.14.0 rows are the engine\'s own.'), '']
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(md) + '\n')
    print('\n'.join(md))


if __name__ == '__main__':
    main()
