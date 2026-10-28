"""The placement experiment (results.md §"根因"): the statements the control sends wrote (results/archive-control-s{1,2,3}.sqlite,
production bytes) are filed by a separate call that sees only the statements and the open questions (the theme theses included,
as under A), each question with a code-written 'takes' line from its key. Two rules:
  same   - the link rule of role-v18 as it stands (a customer's, supplier's or competitor's statement is read for the company's
           demand, pricing and margin questions): isolates the placer from the rule
  narrow - one home, the narrowest question that names the matter; a company-wide figure question takes only its own figures,
           guidance and management statements: Alex's hypothesis on the two sinks
Scored on the frozen gold with ab_gold's cells, the placer's links in place of the extraction's; plus the links to the two sinks.
  python3 place_gold.py send same|narrow     (three draws: the statements of control s1, s2, s3)
  python3 place_gold.py report
"""
import collections, json, os, sqlite3, sys, types
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ab_gold                                               # noqa: E402  (snapshot connections, context, gold, overlap)
from hivemind import extraction, model                      # noqa: E402
RES = os.path.join(HERE, 'results')
SINKS = {'v2', 'v10'}
SETTING = types.SimpleNamespace(model='gpt-6-luna', prompt_version='placement-v1', temperature=0.2, reasoning_effort='medium', max_output_tokens=6000)
ROLE = ("You are a senior hedge-fund analyst filing statements into a library of open questions about NVIDIA and its world. For each "
        "statement, return the ids of the questions it is filed under, or an empty list. Read each question's 'takes' line: it says what "
        "that question collects. A statement filed under no question is a valid answer, not a failure: never file a statement under a "
        "question it does not bear on because no better question exists.\n")
RULES = {
 'same': ("A statement bears on a question when its figure or fact changes what that question's answer will be: a customer's order of "
          "18,000 Blackwell chips bears on the data center revenue question; a CPU server order bears on the stand-alone CPU revenue "
          "question; a renewal price for older GPUs bears on the gross margin question; an expert's view on political dependence bears on "
          "none. A customer's, supplier's or competitor's statement is read for the company's demand, pricing and margin questions. A "
          "rumour bears on a question exactly as a confirmed statement does. File it under every question it bears on."),
 'narrow': ("File each statement under the narrowest question that names its matter, and under that one only; never add a broader "
            "question beside it. A company-wide figure question (total revenue, segment revenue, gross margin, operating margin, profit, "
            "capex) takes only the company's own reported figures, guidance, estimates of that figure and management's statements about "
            "it. News about a customer, supplier, competitor, product, policy or deal is filed under the question that names that matter "
            "(an event, a policy process, a theme), or under none when no question names it. A rumour is filed exactly as a confirmed "
            "statement is."),
}
RULES['same2'] = RULES['same']
RULES['same3'] = RULES['same']
RULES['same4'] = RULES['same']
RULES['same5'] = RULES['same']
RULES['same6'] = RULES['same']
RULES['narrow2'] = RULES['narrow']
RULES['drivers'] = RULES['narrow']    # E2 arm: narrow2 with the six seeded driver questions (drivers-seed.json) shown; scored against gold v2's primary_home    # arm 7: the narrow rule (one home, company-wide figures take only their own numbers) with the title line and the group names      # arm 6: same4 plus the item's title line (publisher, day, title) at the top of the request      # arm 5: same4 plus the extraction's first opinion shown for event and policy questions only      # arm 4: production build_request, takes lines carry the research group's names and scope; aggregates admit other populations      # arm 3: production placement.build_request (same2 takes) with the extraction's own links shown as a first opinion      # arm 2: the same rule; only the 'takes' lines change (policy processes take facts of the permitted activity; obligations take the counterparty's terms)
SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['placements'],
          'properties': {'placements': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['id', 'links'],
                                                                     'properties': {'id': {'type': 'string'}, 'links': {'type': 'array', 'items': {'type': 'string'}}}}}}}


def takes(vw, rule='same'):
    k = ab_gold.store.view_key(ab_gold.v, vw['view_id']) or {}
    m = k.get('measure') or ''
    if m == 'policy_event':
        if rule == 'same2':
            return f"takes: the decisions, drafts, approvals, denials and deadlines of this process, and any statement of whether and how much the permitted or restricted activity is actually happening: {k.get('scope') or vw['looks_at']}"
        return f"takes: decisions, drafts, approvals, denials, deadlines and official statements of this process: {k.get('scope') or vw['looks_at']}"
    if m == 'event':
        if rule == 'same2' and k.get('event_type') in ('launch', 'shipment', 'deployment'):
            return f"takes: steps, dates, delays, confirmations and denials of this event, and named customers' statements about receiving it: {k.get('scope') or vw['looks_at']}"
        if rule == 'same2':
            return f"takes: the terms, amounts, counterparties, agreements and approvals of this obligation or deal, and its steps, confirmations and denials: {k.get('scope') or vw['looks_at']}"
        return f"takes: steps, dates, delays, confirmations and denials of this event: {k.get('scope') or vw['looks_at']} ({k.get('event_type')})"
    tail = ", and the direct drivers of that figure stated with a size" if rule in ('same', 'same2') else ", by the company, its management or named analysts"
    return f"takes: {m or 'the figure'} figures, guidance, estimates and revisions for {k.get('scope') or vw['object_id']} over {k.get('period_start')}..{k.get('period_end')}{tail}"


def request(statements, shown, rule):
    lines = [f"  - {v['view_id']} ({v['object_id']}, due {v['due_day']}): {v['question']}\n      {takes(v, rule)}" for v in shown]
    user = ('[Open questions]\n' + '\n'.join(lines) + '\n\n[Statements]\n' +
            '\n'.join(f"  - {e['id']} [{e.get('tier')}] who: {e.get('original_who') or e.get('speaker') or ''} | {e.get('one_line')} | quote: {e.get('quote')[:240]}" for e in statements) +
            '\n\nReturn one placement per statement id, in order.')
    return ROLE + RULES[rule], user


def raw_statements(draw, item_id):
    a = sqlite3.connect(f'file:{RES}/archive-control-s{draw}.sqlite?mode=ro', uri=True)
    row = a.execute("select answer_json from model_calls where purpose='extract' and request_json like ? and request_sha256 not like '%:%' order by call_id desc limit 1", (f'%[Item] id {item_id},%',)).fetchone()
    return json.loads(row[0]).get('evidence', []) if row else None


def score(art, statements, placed, shown):
    """ab_gold's cells with the placer's links; 'unplaced' replaces written_dropped (the design under test keeps the statement)."""
    allowed = {v['view_id'] for v in shown}
    links = {p['id']: [l for l in p['links'] if l in allowed] for p in placed}
    cells, matched = {}, set()
    for s in art['statements']:
        spans = [s['span']] + s['also']
        hits = [e for e in statements if any(ab_gold.overlap(e['quote'], sp) for sp in spans)]
        matched.update(e['id'] for e in hits)
        got = sorted({l for e in hits for l in links.get(e['id'], [])})
        wanted = s.get('primary_home', s['bears_on_with_themes'])
        if not hits:
            cell = 'not_written'
        elif got and set(got) & set(wanted):
            cell = 'kept_right'
        elif got:
            cell = 'kept_wrong_link'
        else:
            cell = 'unplaced'
        cells[s['id']] = {'cell': cell, 'weight': s['weight'], 'links': got, 'wanted': wanted, 'split': max(0, len(hits) - 1)}
    extra = [{'id': e['id'], 'links': links.get(e['id'], []), 'one_line': e['one_line'][:140]} for e in statements if e['id'] not in matched and links.get(e['id'])]
    sink_links = sum(1 for e in statements for l in links.get(e['id'], []) if l in SINKS)
    in_call_sink = sum(1 for e in statements for l in e.get('links', []) if l in SINKS)
    return {'cells': cells, 'extra_kept': extra, 'raw_pieces': len(statements), 'placed_pieces': sum(1 for e in statements if links.get(e['id'])),
            'sink_links': sink_links, 'in_call_sink_links': in_call_sink, 'links_total': sum(len(x) for x in links.values())}


def run(rule, transport=None):
    arts = ab_gold.load_gold([os.path.join(HERE, 'gold-extraction-v2.json')]) if rule == 'drivers' else ab_gold.load_gold([os.path.join(HERE, 'gold-extraction.json'), os.path.join(HERE, 'gold-extraction-themes.json')])
    import concurrent.futures
    jobs = []
    for draw in (1, 2, 3):
        archive = model.Archive(os.path.join(RES, f'archive-place-{rule}-s{draw}.sqlite'))
        for art in arts:
            statements = raw_statements(draw, art['input_id'])
            if not statements:
                continue
            item, shown, groups = ab_gold.context(art)            # ledger reads on this thread; only the send runs in the pool
            if rule in ('same3', 'same4', 'same5', 'same6', 'narrow2', 'drivers'):
                from hivemind import placement as production_placement
                from hivemind.views import store as _store
                drivers = json.load(open(os.path.join(HERE, 'drivers-seed.json'))) if rule == 'drivers' else []
                shown_g = [dict(v, groups=[{'name': g['name'], 'scope': g['scope'], 'aliases': g.get('aliases') or []} for g in _store.groups_of_view(ab_gold.v, v['view_id'])]) for v in shown['themes']] + drivers
                if rule in ('same3', 'same4', 'same5'):
                    raise SystemExit(f'arm {rule} is retired with the hints/aliases options of placement.py (routing-analysis.md §8); its results stay in results/')
                system, user = ROLE + RULES['narrow' if rule in ('narrow2', 'drivers') else 'same'], production_placement.build_request(statements, shown_g, item=item)
            else:
                system, user = request(statements, shown['themes'], rule)
            jobs.append((draw, art, statements, (shown['themes'] + drivers) if rule in ('same3', 'same4', 'same5', 'same6', 'narrow2', 'drivers') else shown['themes'], archive, system, user))

    def send(job):
        draw, art, statements, shown, archive, system, user = job
        return job, model.call(archive, ab_gold.cfg, SETTING, system, user, SCHEMA, 'placement', 'place', transport=transport)
    out = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:          # AGENTS §9: a harness sends concurrently, a pool of 8
        for (draw, art, statements, shown, _, _, _), answer in pool.map(send, jobs):
            rec = {'arm': f'place-{rule}', 'sample': draw, 'input_id': art['input_id'], 'held_out': art['held_out'], 'cost_usd': answer.cost_usd,
                   **score(art, statements, answer.data['placements'], shown)}
            out.append(rec)
            print(f"{rule} s{draw} {art['input_id'][-12:]}: statements {rec['raw_pieces']} placed {rec['placed_pieces']} cells {dict(collections.Counter(c['cell'] for c in rec['cells'].values()))} sinks {rec['in_call_sink_links']}->{rec['sink_links']} ${answer.cost_usd:.4f}", flush=True)
    json.dump(out, open(os.path.join(RES, f'place-{rule}.json'), 'w'), indent=1, ensure_ascii=False)


def report():
    rows = []
    for name in ('send-control.json', 'place-same.json', 'place-same2.json', 'place-same3.json', 'place-same4.json', 'place-same5.json', 'place-same6.json', 'place-narrow.json', 'place-narrow2.json', 'place-drivers.json'):
        p = os.path.join(RES, name)
        if os.path.exists(p):
            rows += json.load(open(p))
    by = collections.defaultdict(list)
    for r in rows:
        by[(r['arm'], r['sample'])].append(r)
    print('| arm | draw | kept_right | wrong_link | unplaced/dropped | not_written | extra placed | links to v2+v10 | links total |\n|---|---|---|---|---|---|---|---|---|')
    for (arm, sample), rs in sorted(by.items()):
        c = collections.Counter(); core = collections.Counter(); extra = sinks = total = 0
        for r in rs:
            for cell in r['cells'].values():
                c[cell['cell']] += 1
                if cell['weight'] == 'core':
                    core[cell['cell']] += 1
            extra += len(r['extra_kept']); sinks += r.get('sink_links', r.get('in_call_sink_links', 0)); total += r.get('links_total', 0)
        if arm == 'control':                      # the control's in-call links, counted from the same statements the placer arms read
            sinks = sum(sum(1 for e in (raw_statements(sample, r['input_id']) or []) for l in e.get('links', []) if l in SINKS) for r in rs)
            total = sum(sum(len(e.get('links', [])) for e in (raw_statements(sample, r['input_id']) or [])) for r in rs)
        drop = c['unplaced'] + c['written_dropped']
        print(f"| {arm} | {sample} | {c['kept_right']} (core {core['kept_right']}) | {c['kept_wrong_link']} | {drop} | {c['not_written']} | {extra} | {sinks} | {total} |")


if __name__ == '__main__':
    if sys.argv[1] == 'send':
        run(sys.argv[2])
    else:
        report()
