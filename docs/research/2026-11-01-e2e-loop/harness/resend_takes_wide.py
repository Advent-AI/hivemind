"""Cheapest proof of D259 (the takes line widened to the evidence that bears on a question): re-send every stored placement request of one
run once with the four takes-line clauses replaced by the ones `placement.takes()` now writes (checked byte for byte against the code on
every view of the run), and count, against the stored answers, per gold class (core, supporting, optional, not-kept, unlisted) the
statements that gain a home, lose every home, move or stay; the gold matters that gain or lose a filed statement; and where the links land
(the sink share on the total and segment revenue questions). One draw, one send: the size of a mechanism, not a difference between arms.

    python3 resend_takes_wide.py <run folder> <config json> [--dry]
"""
import collections
import json
import re
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'docs/research/2026-10-31-reference-context'), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402
from hivemind import config, model, placement  # noqa: E402
from hivemind.views import store  # noqa: E402

SENDERS = 8
SINKS = ('v1', 'v2')     # FY2027 total revenue and Data Center revenue: the company-wide figures D207 found absorbing links
SUBS = [
    (", and the direct drivers of that figure stated with a size",
     ", and what makes that figure more or less likely: the demand, supply, competition and pricing behind it"),
    ("deadlines of this process, and any statement of whether and how much the permitted or restricted activity is actually happening: ",
     "deadlines of this process, its enforcement and evasion, any statement of whether and how much the permitted or restricted activity is "
     "actually happening, and the affected parties' own plans and statements about it: "),
    ("design or configuration changes, confirmations and denials of this event, and named customers' statements about receiving it: ",
     "design or configuration changes, variants and stopgaps of this event, confirmations and denials, and named customers' statements about receiving it: "),
    ("of this obligation or deal, and its steps, confirmations and denials: ",
     "of this obligation or deal, its steps, confirmations and denials, and the counterparties' own plans, financing and demand that bear on it: "),
]
QUESTION_LINE = re.compile(r'^  - (v\d+) \(', re.M)


def old_takes(view):
    """The takes line as the code wrote it before D259 (placement.py at D254), for the equivalence check."""
    key = view.get('key') or {}
    measure, scope = key.get('measure') or '', key.get('scope') or view.get('looks_at') or view.get('object_id')
    tail = f"; statements about {placement.matter(view)} belong here under any of those names" if placement.matter(view) else ''
    if measure == 'policy_event':
        return (f"takes: the decisions, drafts, approvals, denials and deadlines of this process, and any statement of whether and how much "
                f"the permitted or restricted activity is actually happening: {scope}{tail}")
    if measure == 'event':
        if key.get('event_type') in ('launch', 'shipment', 'deployment'):
            return (f"takes: steps, dates, delays, cancellations, design or configuration changes, confirmations and denials of this event, "
                    f"and named customers' statements about receiving it: {scope}{tail}")
        return f"takes: the terms, amounts, counterparties, agreements and approvals of this obligation or deal, and its steps, confirmations and denials: {scope}{tail}"
    population = ", including estimates for another population or wording of the same aggregate" if view.get('kind') == 'theme' else ''
    measure_name = f"{measure} " if measure and measure != 'other' else ''
    return (f"takes: {measure_name}figures, guidance, estimates and revisions for {scope} over {key.get('period_start')}..{key.get('period_end')}{population}, "
            f"and the direct drivers of that figure stated with a size{tail}")


def edit(text):
    for old, new in SUBS:
        text = text.replace(old, new)
    return text


def check_equivalence(views_path):
    """Every view of the run: the edited old line must be the line the code writes now."""
    conn = sqlite3.connect(f'file:{views_path}?mode=ro', uri=True); conn.row_factory = sqlite3.Row
    n = 0
    for row in conn.execute('select view_id from views order by created_seq'):
        v = store.view(conn, row['view_id'])
        v = dict(v, key=store.view_key(conn, v['view_id']) or {}, groups=[{'name': g['name'], 'scope': g['scope'], 'aliases': g.get('aliases') or []} for g in store.groups_of_view(conn, v['view_id'])])
        new, edited = placement.takes(v), edit(old_takes(v))
        if new != edited:
            raise SystemExit(f'{v["view_id"]}: the harness edit differs from the code:\n  code   {new}\n  edited {edited}')
        n += 1
    return n


def gold_class(article, statement):
    items = article['items']
    for weight in ('core', 'supporting'):
        if any(sr.sg.same_matter(i, statement) for i in items if i['weight'] == weight):
            return weight
    if any(sr.sg.same_matter(i, statement) for i in items if i['weight'] == 'optional') or any(sr.sg.same(n['span'], statement['quote']) for n in article['not_kept'] if n['weight'] == 'optional'):
        return 'optional'
    if any(sr.sg.same(n['span'], statement['quote']) for n in article['not_kept'] if n['weight'] == 'not_kept'):
        return 'not_kept'
    return 'unlisted'


def main():
    run, cfg = sys.argv[1], config.load(sys.argv[2])
    dry = '--dry' in sys.argv
    print(f'takes-line equivalence: {check_equivalence(f"{run}/views.sqlite")} views, the edited old line is the line the code writes now')
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    rows = archive.execute("select call_id, request_json, answer_json, input_tokens, output_tokens from model_calls where purpose='place' order by call_id").fetchall()
    titles = {}
    for a in sr.articles:
        needle = json.dumps(a['title'], ensure_ascii=False)[1:-1]
        hit = archive.execute("select call_id from model_calls where purpose='place' and request_json like ? order by call_id desc limit 1", (f'%{needle}%',)).fetchone()
        if hit:
            titles[hit[0]] = a
    extracted = {}
    for a in titles.values():
        r = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {a["input_id"]},%',)).fetchone()
        extracted[a['input_id']] = {e['id']: e for e in (json.loads(r[0]) if r and r[0] else {}).get('evidence', [])}
    in_tokens = sum(r[3] or 0 for r in rows); out_tokens = sum(r[4] or 0 for r in rows)
    print(f'{len(rows)} stored placement requests ({len(titles)} of gold articles); one send each ≈ ${in_tokens * 0.10 / 1e6 + out_tokens * 0.50 / 1e6:.2f} at list price '
          f'({in_tokens:,} in, {out_tokens:,} out tokens stored)', flush=True)
    jobs = []
    for call_id, request_json, answer_json, _, _ in rows:
        body = json.loads(request_json)
        user = body['messages'][-1]['content']
        edited = edit(user)
        if edited == user:
            print(f'  call {call_id}: no takes line edited (request unchanged)')
        body['messages'][-1]['content'] = edited
        allowed = set(QUESTION_LINE.findall(user))
        stored = {p['id']: [l for l in p['links'] if l in allowed] for p in json.loads(answer_json or '{}').get('placements', [])}
        jobs.append((call_id, body, allowed, stored))
    if dry:
        print(jobs[0][1]['messages'][-1]['content'][:3000]); return

    def send(body, allowed):
        content = model.openai_transport(cfg.provider, body)['choices'][0]['message']['content']
        return {p['id']: [l for l in p['links'] if l in allowed] for p in json.loads(content).get('placements', [])}

    with ThreadPoolExecutor(SENDERS) as pool:
        futures = [(call_id, stored, pool.submit(send, body, allowed)) for call_id, body, allowed, stored in jobs]
        results = [(call_id, stored, f.result()) for call_id, stored, f in futures]

    change_of = lambda old, new: 'unchanged' if set(old) == set(new) else ('loses every home' if old and not new else ('gains a home' if not old and new else 'moves'))
    table = collections.Counter(); links_before = collections.Counter(); links_after = collections.Counter()
    filed_before = filed_after = 0; gained, lost = [], []
    matters = {'core': [0, 0], 'supporting': [0, 0]}
    for call_id, stored, new in results:
        for sid, old in stored.items():
            now = new.get(sid, [])
            filed_before += bool(old); filed_after += bool(now)
            links_before.update(old); links_after.update(now)
        a = titles.get(call_id)
        if not a:
            continue
        by_id = extracted.get(a['input_id'], {})
        for sid, old in stored.items():
            if sid not in by_id:
                continue
            cls, now = gold_class(a, by_id[sid]), new.get(sid, [])
            change = change_of(old, now)
            table[(cls, change)] += 1
            if change == 'gains a home':
                gained.append((cls, a['publication_day'], by_id[sid].get('one_line', '')[:110], now))
            elif change == 'loses every home':
                lost.append((cls, a['publication_day'], by_id[sid].get('one_line', '')[:110], old))
        for weight in matters:
            for item in (i for i in a['items'] if i['weight'] == weight):
                expressed = [sid for sid in stored if sid in by_id and sr.sg.same_matter(item, by_id[sid])]
                if not expressed:
                    continue
                matters[weight][0] += any(stored[sid] for sid in expressed)
                matters[weight][1] += any(new.get(sid) for sid in expressed)
    print(f'\nstatements filed (all {len(rows)} requests): {filed_before} -> {filed_after}; links {sum(links_before.values())} -> {sum(links_after.values())}; '
          f'sink share (links on {"+".join(SINKS)}): {sum(links_before[s] for s in SINKS) / max(1, sum(links_before.values())):.1%} -> '
          f'{sum(links_after[s] for s in SINKS) / max(1, sum(links_after.values())):.1%}')
    print('\nlinks per question, stored -> re-sent (top 15 after):')
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    questions = {r[0]: r[1] for r in views.execute('select view_id, question from views')}
    for vid, n in links_after.most_common(15):
        print(f'  {vid:>4} {links_before[vid]:>4} -> {n:<4} {questions.get(vid, "?")[:80]}')
    print(f'\ngold articles, statements by gold class x change (stored answer -> one re-send):')
    print(f'{"class":<12}{"unchanged":>11}{"gains home":>12}{"loses home":>12}{"moves":>8}')
    for cls in ('core', 'supporting', 'optional', 'not_kept', 'unlisted'):
        print(f'{cls:<12}{table[(cls, "unchanged")]:>11}{table[(cls, "gains a home")]:>12}{table[(cls, "loses every home")]:>12}{table[(cls, "moves")]:>8}')
    print(f'\ngold matters with an extracted statement, filed under at least one question, stored -> re-sent: '
          f'core {matters["core"][0]} -> {matters["core"][1]}; supporting {matters["supporting"][0]} -> {matters["supporting"][1]}')
    print('\nstatements that gain a home (class | day | one_line | links):')
    for cls, day, line, links in sorted(gained):
        print(f'  {cls:<11}| {day} | {line} | {links}')
    print('\nstatements that lose every home:')
    for cls, day, line, links in sorted(lost):
        print(f'  {cls:<11}| {day} | {line} | was {links}')


if __name__ == '__main__':
    main()
