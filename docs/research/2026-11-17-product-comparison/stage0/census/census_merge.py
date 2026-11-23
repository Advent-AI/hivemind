"""The blind matter census after the batch reading (plan §1.3 items 3–7; D668). Every session is closed (census_readers.run).

    python3 census_merge.py merge        # each family merges its own 11 batch lists into one, flagging company figures (D505's list)
    python3 census_merge.py reconcile    # a reconciler of each family pairs the two families' matters that are one bet
    python3 census_merge.py third        # a third reader of each family reads each one-family matter with its articles: worth a question?
    python3 census_merge.py freeze       # matters.json: both-listed matters, and one-family matters both third readers accept; N
    python3 census_merge.py dedup        # both families group the entries that are one bet (D248)
    python3 census_merge.py adjudicate   # pairs only one family grouped, and pairs a reviewer named, read blind against their articles
    python3 census_merge.py final        # matters.json: agreed groups plus adjudicated one-bet pairs; one canonical question each; N

A pair is "listed by both" only when both reconcilers name it. A one-family matter joins only when both third readers say yes. The company
figure flag is set when both families' marks say yes; a split is listed. N < 20 is "too small" and goes to Alex before any paid send.
"""
import concurrent.futures
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import census_readers  # noqa: E402

FAMILIES = census_readers.FAMILIES
D505 = '营收、毛利率的指引、市场预期、实际业绩 (revenue, gross-margin guidance, market expectations, reported results)'

MERGE = """# Blind reader: merge your own matter lists into one (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Below are the questions and matters you listed, batch by batch, from {count} news
articles of 2026-09-07 to 09-20 (article numbers are global). Merge them into one list across all batches:
- one matter = one underlying bet, whichever articles raise it;
- another year of a figure is another matter;
- two entries are one matter only when the same outcome would settle both and their answers cannot move apart.

For each merged matter also mark `company_figure`: true when the matter is about NVIDIA's own reported financials or guidance, by this list:
{d505}; false otherwise.

Write one JSON object per line, and nothing else:
{{"matter": "<new short key>", "name": "<one line>", "example_question": "<the question, with its period or check date>",
  "merged_from": ["<batch>:<old key>", ...], "articles": [n, ...], "first_day": "YYYY-MM-DD", "company_figure": true|false}}

## Your lists

{lists}
"""

RECONCILE = """# Reconcile two lists of matters (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Two readers listed, apart, the big matters raised by the same news articles of 2026-09-07
to 09-20. Pair every matter of list X with the matter of list Y that is the same underlying bet, if any: the same outcome would settle both
and their answers cannot move apart; another year of a figure is another matter. A matter pairs with at most one; leave it unpaired when none
is the same bet.

Write one JSON object per line, and nothing else: {{"x": "<key in X>", "y": "<key in Y or null>"}} for every matter of X, then
{{"x": null, "y": "<key>"}} for every matter of Y left unpaired.

## List X

{x}

## List Y

{y}
"""

THIRD = """# Third reader: is this a matter worth a question of its own? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. One reader listed the matter below from these articles; another did not. Read the
articles in full and the signed standard's §3 and §4, then answer.

A question worth tracking on its own is a big matter (it can change NVIDIA's revenue, profit, cash, credit risk or competitive position, or it
is a quantity or decision in the world that many companies depend on), with an outcome a dated public release, filing or official decision
can settle. Small matters, background, a stock-price or valuation view, and anything no public material can settle are not.

Also mark `company_figure`: true when the matter is about NVIDIA's own reported financials or guidance ({d505}).

Write one JSON object and nothing else: {{"worth": true|false, "company_figure": true|false, "why": "<= 40 words"}}

## The matter

{matter}

## The signed standard, §3 and §4

{standard}

## The articles

{articles}
"""


def json_lines(text):
    rows = []
    for line in (text or '').splitlines():
        line = line.strip().rstrip(',')
        if line.startswith('{'):
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def batch_lists(family):
    parts = []
    for path in sorted((HERE / 'answers').glob(f'{family}-batch-*.txt')):
        batch = path.stem.split('-', 1)[1]
        rows = json_lines(path.read_text())
        questions = [r for r in rows if r.get('question')]
        matters = [r for r in rows if 'name' in r and 'articles' in r]
        parts.append(f'### {batch}\n' + '\n'.join(json.dumps(r, ensure_ascii=False) for r in questions + matters))
    return parts


def closed(family, prompt, check):
    for attempt in (1, 2):
        answer, void = census_readers.run(family, prompt)
        if answer and not void:
            problem = check(answer)
            if not problem:
                return answer, None
            void = problem
    return None, void


def merge():
    numbering = json.loads((HERE / 'numbering.json').read_text())
    for family in FAMILIES:
        out = HERE / 'merged' / f'{family}.jsonl'
        if out.exists():
            continue
        prompt = MERGE.format(count=len(numbering), d505=D505, lists='\n\n'.join(batch_lists(family)))
        answer, void = closed(family, prompt, lambda a: None if json_lines(a) else 'no JSON lines')
        if void:
            raise SystemExit(f'{family} merge void twice: {void}')
        out.parent.mkdir(exist_ok=True)
        out.write_text(answer)
        print(family, 'merged:', len(json_lines(answer)), 'matters')


def reconcile():
    lists = {family: json_lines((HERE / 'merged' / f'{family}.jsonl').read_text()) for family in FAMILIES}
    show = lambda rows: '\n'.join(json.dumps({k: r.get(k) for k in ('matter', 'name', 'example_question', 'articles')}, ensure_ascii=False) for r in rows)
    prompt = RECONCILE.format(x=show(lists['codex']), y=show(lists['claude']))
    keys_x = {r['matter'] for r in lists['codex']}
    keys_y = {r['matter'] for r in lists['claude']}

    def check(answer):
        rows = json_lines(answer)
        named_x = {r.get('x') for r in rows if r.get('x')}
        return None if keys_x <= named_x else f'{len(keys_x - named_x)} matters of X not answered'
    for family in FAMILIES:
        out = HERE / 'reconciled' / f'{family}.jsonl'
        if out.exists():
            continue
        answer, void = closed(family, prompt, check)
        if void:
            raise SystemExit(f'{family} reconciliation void twice: {void}')
        out.parent.mkdir(exist_ok=True)
        out.write_text(answer)
        pairs = [r for r in json_lines(answer) if r.get('x') and r.get('y') in keys_y]
        print(family, 'reconciler paired', len(pairs))


def pair_sets():
    found = []
    for family in FAMILIES:
        rows = json_lines((HERE / 'reconciled' / f'{family}.jsonl').read_text())
        found.append({(r['x'], r['y']) for r in rows if r.get('x') and r.get('y')})
    return found


def pairs_agreed():
    found = pair_sets()
    return found[0] & found[1]


def pairs_half():
    """Pairs one reconciler names and the other does not, whose two matters are in no agreed pair: each goes to the third readers as
    one matter, so the same bet is never counted twice."""
    found = pair_sets()
    agreed = found[0] & found[1]
    used_x, used_y = {x for x, _ in agreed}, {y for _, y in agreed}
    half = sorted((found[0] | found[1]) - agreed)
    chosen, seen_x, seen_y = [], set(), set()
    for x, y in half:
        if x in used_x or y in used_y or x in seen_x or y in seen_y:
            continue
        chosen.append((x, y))
        seen_x.add(x)
        seen_y.add(y)
    return chosen


def third():
    lists = {family: {r['matter']: r for r in json_lines((HERE / 'merged' / f'{family}.jsonl').read_text())} for family in FAMILIES}
    agreed, half = pairs_agreed(), pairs_half()
    paired = {'codex': {x for x, _ in list(agreed) + half}, 'claude': {y for _, y in list(agreed) + half}}
    numbering = json.loads((HERE / 'numbering.json').read_text())
    by_number = {}
    for path in sorted((HERE / 'batches').glob('batch-*.json')):
        for row in json.loads(path.read_text()):
            by_number[row['article']] = row
    standard = census_readers.standard_sections()
    jobs = []
    for family in FAMILIES:
        for key, matter in lists[family].items():
            if key in paired[family]:
                continue
            for reader in FAMILIES:
                out = HERE / 'third' / f'{family}--{key}--{reader}.json'
                if not out.exists():
                    jobs.append((family, key, matter, reader, out))
    for x, y in half:                                       # one matter of two entries the reconcilers split on
        a, b = lists['codex'][x], lists['claude'][y]
        joined = dict(a, name=f"{a.get('name')} / {b.get('name')}", articles=sorted(set(a.get('articles', [])) | set(b.get('articles', []))))
        for reader in FAMILIES:
            out = HERE / 'third' / f'pair--{x}|{y}--{reader}.json'
            if not out.exists():
                jobs.append(('pair', f'{x}|{y}', joined, reader, out))

    def one(job):
        family, key, matter, reader, out = job
        numbers = [int(n) for n in matter.get('articles', []) if str(n).isdigit() and int(n) in by_number][:12]
        articles = '\n\n'.join(f"### Article {n} · {by_number[n]['day']} · {by_number[n]['publisher']}\n{by_number[n]['title']}\n\n{by_number[n]['text']}"
                               for n in numbers)
        shown = {k: matter.get(k) for k in ('name', 'example_question')}
        prompt = THIRD.format(matter=json.dumps(shown, ensure_ascii=False), standard=standard, articles=articles, d505=D505)

        def check(answer):
            rows = json_lines(answer)
            return None if rows and isinstance(rows[-1].get('worth'), bool) else 'no worth mark'
        answer, void = closed(reader, prompt, check)
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps({'family': family, 'matter': key, 'reader': reader, 'void': void,
                                   'mark': json_lines(answer)[-1] if answer else None}, ensure_ascii=False) + '\n')
        return family, key, reader, void
    print(len(jobs), 'third-reader sessions')
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for family, key, reader, void in pool.map(one, jobs):
            print(family, key, reader, 'VOID ' + void if void else 'marked', flush=True)


def freeze():
    lists = {family: {r['matter']: r for r in json_lines((HERE / 'merged' / f'{family}.jsonl').read_text())} for family in FAMILIES}
    matters, splits = [], []
    for x, y in sorted(pairs_agreed()):
        a, b = lists['codex'][x], lists['claude'][y]
        flag = (a.get('company_figure') is True) and (b.get('company_figure') is True)
        if a.get('company_figure') != b.get('company_figure'):
            splits.append({'matter': f'{x}|{y}', 'company_figure': {'codex': a.get('company_figure'), 'claude': b.get('company_figure')}})
        matters.append({'key': f'{x}|{y}', 'listed_by': 'both', 'name': a.get('name'), 'name_other': b.get('name'),
                        'example_question': a.get('example_question'), 'articles': sorted(set(a.get('articles', [])) | set(b.get('articles', []))),
                        'first_day': min([d for d in (a.get('first_day'), b.get('first_day')) if d], default=None), 'company_figure': flag})
    third_marks = {}
    for path in (HERE / 'third').glob('*.json'):
        row = json.loads(path.read_text())
        third_marks.setdefault((row['family'], row['matter']), {})[row['reader']] = row['mark'] or {}
    for (family, key), marks in sorted(third_marks.items()):
        if all(marks.get(r, {}).get('worth') is True for r in FAMILIES):
            if family == 'pair':
                x, y = key.split('|', 1)
                a, b = lists['codex'][x], lists['claude'][y]
                m = dict(a, name=f"{a.get('name')} / {b.get('name')}", articles=sorted(set(a.get('articles', [])) | set(b.get('articles', []))))
            else:
                m = lists[family][key]
            flags = [marks[r].get('company_figure') for r in FAMILIES]
            if len(set(flags)) > 1:
                splits.append({'matter': key, 'company_figure': dict(zip(FAMILIES, flags))})
            matters.append({'key': key, 'listed_by': family, 'name': m.get('name'), 'example_question': m.get('example_question'),
                            'articles': m.get('articles', []), 'first_day': m.get('first_day'), 'company_figure': all(f is True for f in flags)})
    doc = {'frozen': 'stage 0, before any system output', 'kept_articles_sha256': hashlib.sha256((HERE.parent / 'kept-articles.json').read_bytes()).hexdigest(),
           'N': len(matters), 'company_figure_subgroup': sum(m['company_figure'] for m in matters), 'matters': matters, 'flag_splits': splits}
    text = json.dumps(doc, indent=1, ensure_ascii=False) + '\n'
    (HERE / 'matters.json').write_text(text)
    (HERE / 'matters.json.sha256').write_text(hashlib.sha256(text.encode()).hexdigest() + '  matters.json\n')
    print(f"N = {doc['N']} (both-listed {sum(m['listed_by'] == 'both' for m in matters)}, one-family accepted "
          f"{sum(m['listed_by'] != 'both' for m in matters)}); company-figure subgroup {doc['company_figure_subgroup']}; flag splits {len(splits)}")
    if doc['N'] < 20:
        print('TOO SMALL: N < 20. Return to Alex before any paid send (D667, D668).')


DEDUP = """# Group the entries that are one underlying bet (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Below is a numbered list of matters two readers listed from news of 2026-09-07 to
09-20. Some entries are the same bet written differently. Group them by the signed standard's rule (D248):
- wordings, deadlines, milestones and periods of one bet are one question;
- another year of a figure is another matter;
- two entries stay apart only when their answers can move apart and an analyst would bet on each separately.

Write one JSON object per line, and nothing else: {{"group": [entry numbers that are one bet], "why": "<= 25 words"}} for every group of two or
more entries. Entries you do not name stand alone.

## The entries

{entries}
"""


def dedup():
    entries = json.loads((HERE / 'matters-entries.json').read_text())['matters']
    listing = '\n'.join(f"{i}. {m['name']} | e.g. {m.get('example_question') or ''}" for i, m in enumerate(entries, 1))
    prompt = DEDUP.format(entries=listing)
    edges = {}
    for family in FAMILIES:
        out = HERE / 'dedup' / f'{family}.jsonl'
        if not out.exists():
            answer, void = closed(family, prompt, lambda a: None if json_lines(a) or a.strip() else 'empty')
            if void:
                raise SystemExit(f'{family} dedup void twice: {void}')
            out.parent.mkdir(exist_ok=True)
            out.write_text(answer)
        pairs = set()
        for row in json_lines(out.read_text()):
            members = sorted({int(n) for n in row.get('group', []) if str(n).isdigit() and 1 <= int(n) <= len(entries)})
            pairs |= {(a, b) for a in members for b in members if a < b}
        edges[family] = pairs
    agreed, either = edges['codex'] & edges['claude'], edges['codex'] | edges['claude']

    def components(pairs):
        parent = list(range(len(entries) + 1))
        def root(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i
        for a, b in pairs:
            parent[root(a)] = root(b)
        groups = {}
        for i in range(1, len(entries) + 1):
            groups.setdefault(root(i), []).append(i)
        return sorted(groups.values())
    final_groups, agreed_groups = components(either), components(agreed)
    matters = []
    for group in final_groups:
        members = [entries[i - 1] for i in group]
        flags = {m['company_figure'] for m in members}
        matters.append({'entries': group, 'names': [m['name'] for m in members], 'listed_by': sorted({m['listed_by'] for m in members}),
                        'articles': sorted({a for m in members for a in m.get('articles', [])}, key=lambda a: int(a) if str(a).isdigit() else 0),
                        'first_day': min([m['first_day'] for m in members if m.get('first_day')], default=None),
                        'company_figure': flags == {True}, 'company_figure_mixed': len(flags) > 1,
                        'merged_by': 'both' if all((a, b) in agreed for a in group for b in group if a < b) else ('one reader' if len(group) > 1 else '')})
    doc = {'frozen': 'stage 0, before any system output', 'entries_sha256': hashlib.sha256((HERE / 'matters-entries.json').read_bytes()).hexdigest(),
           'rule': 'entries grouped by either family are one matter (no matter counted twice); the count under agreed groups only is reported',
           'N': len(matters), 'N_agreed_groups_only': len(agreed_groups), 'company_figure_subgroup': sum(m['company_figure'] for m in matters),
           'matters': matters}
    text = json.dumps(doc, indent=1, ensure_ascii=False) + '\n'
    (HERE / 'matters-final.json').write_text(text)
    (HERE / 'matters-final.json.sha256').write_text(hashlib.sha256(text.encode()).hexdigest() + '  matters-final.json\n')
    print(f"entries {len(entries)} -> N = {doc['N']} (agreed groups only: {doc['N_agreed_groups_only']}); company-figure {doc['company_figure_subgroup']}")
    if doc['N'] < 20:
        print('TOO SMALL: N < 20. Return to Alex before any paid send (D667, D668).')


D248_RULE = """D248, the signed one-bet rule: two questions are one when the same outcome settles both; they are kept apart only when their answers can
move apart and an analyst would bet on each separately. Wordings of one plan whose final check is the same number are one question; a
single deal under a plan already opened by amount merges into it. One event with several deadlines is one question (a later deadline is its
evidence). Another year of a figure is another matter."""

ADJUDICATE = """# Are these two entries one bet? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Two entries were listed from news of 2026-09-07 to 09-20. Read the rule, both entries
and their articles, then decide.

{rule}

Write one JSON object and nothing else: {{"one_bet": true|false, "why": "<= 40 words"}}

## Entry 1

{a}

## Entry 2

{b}

## The articles

{articles}
"""
REVIEWER_PAIRS = [(2, 26), (3, 27), (12, 37)]      # named by the council's check (dedup-check-codex.md), read blind like the rest


def entry_edges():
    edges = {}
    n = len(json.loads((HERE / 'matters-entries.json').read_text())['matters'])
    for family in FAMILIES:
        pairs = set()
        for row in json_lines((HERE / 'dedup' / f'{family}.jsonl').read_text()):
            members = sorted({int(x) for x in row.get('group', []) if str(x).isdigit() and 1 <= int(x) <= n})
            pairs |= {(a, b) for a in members for b in members if a < b}
        edges[family] = pairs
    return edges


def adjudicate():
    entries = json.loads((HERE / 'matters-entries.json').read_text())['matters']
    edges = entry_edges()
    agreed = edges['codex'] & edges['claude']
    candidates = sorted(((edges['codex'] | edges['claude']) - agreed) | set(REVIEWER_PAIRS))
    by_number = {}
    for path in sorted((HERE / 'batches').glob('batch-*.json')):
        for row in json.loads(path.read_text()):
            by_number[row['article']] = row
    jobs = []
    for a, b in candidates:
        for reader in FAMILIES:
            out = HERE / 'adjudicated' / f'{a}-{b}--{reader}.json'
            if not out.exists():
                jobs.append((a, b, reader, out))

    def one(job):
        a, b, reader, out = job
        show = lambda m: json.dumps({'name': m.get('name'), 'question': m.get('example_question')}, ensure_ascii=False)
        numbers = []
        for m in (entries[a - 1], entries[b - 1]):
            numbers += [int(x) for x in m.get('articles', []) if str(x).isdigit() and int(x) in by_number][:4]
        numbers = sorted(set(numbers))
        articles = '\n\n'.join(f"### Article {n} · {by_number[n]['day']} · {by_number[n]['publisher']}\n{by_number[n]['title']}\n\n{by_number[n]['text']}"
                                for n in numbers)
        prompt = ADJUDICATE.format(rule=D248_RULE, a=show(entries[a - 1]), b=show(entries[b - 1]), articles=articles)
        answer, void = closed(reader, prompt, lambda t: None if json_lines(t) and isinstance(json_lines(t)[-1].get('one_bet'), bool) else 'no mark')
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps({'pair': [a, b], 'reader': reader, 'void': void, 'mark': json_lines(answer)[-1] if answer else None},
                                  ensure_ascii=False) + '\n')
        return a, b, reader, void
    print(len(candidates), 'pairs,', len(jobs), 'sessions')
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for a, b, reader, void in pool.map(one, jobs):
            print(a, b, reader, 'VOID ' + void if void else 'marked', flush=True)


def final():
    entries = json.loads((HERE / 'matters-entries.json').read_text())['matters']
    edges = entry_edges()
    agreed = edges['codex'] & edges['claude']
    marks = {}
    for path in (HERE / 'adjudicated').glob('*.json'):
        row = json.loads(path.read_text())
        marks.setdefault(tuple(row['pair']), {})[row['reader']] = (row['mark'] or {}).get('one_bet')
    adjudicated = {pair for pair, m in marks.items() if all(m.get(r) is True for r in FAMILIES)}
    split = {pair: m for pair, m in marks.items() if len({m.get(r) for r in FAMILIES}) > 1}
    parent = list(range(len(entries) + 1))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for a, b in agreed | adjudicated:
        parent[root(a)] = root(b)
    groups = {}
    for i in range(1, len(entries) + 1):
        groups.setdefault(root(i), []).append(i)
    matters = []
    for group in sorted(groups.values()):
        members = [entries[i - 1] for i in group]
        canonical = sorted(members, key=lambda m: (m['listed_by'] != 'both', m.get('first_day') or '9999'))[0]
        flags = {m['company_figure'] for m in members}
        matters.append({'matter': f'M{len(matters) + 1:02d}', 'question': canonical.get('example_question'), 'name': canonical.get('name'),
                        'entries': group, 'entry_names': [m['name'] for m in members], 'listed_by': sorted({m['listed_by'] for m in members}),
                        'articles': sorted({int(a) for m in members for a in m.get('articles', []) if str(a).isdigit()}),
                        'first_day': min([m['first_day'] for m in members if m.get('first_day')], default=None),
                        'company_figure': flags == {True}, 'company_figure_mixed': len(flags) > 1})
    doc = {'frozen': 'stage 0, before any system output (D671)', 'entries_sha256': hashlib.sha256((HERE / 'matters-entries.json').read_bytes()).hexdigest(),
           'rule': 'one matter per group of entries joined by a grouping both families made or a pair both blind adjudicators read as one bet (D248)',
           'N': len(matters), 'company_figure_subgroup': sum(m['company_figure'] for m in matters),
           'adjudicated_one_bet': sorted(map(list, adjudicated)), 'adjudication_splits': {f'{a}-{b}': m for (a, b), m in sorted(split.items())},
           'matters': matters}
    text = json.dumps(doc, indent=1, ensure_ascii=False) + '\n'
    (HERE / 'matters.json').write_text(text)
    (HERE / 'matters.json.sha256').write_text(hashlib.sha256(text.encode()).hexdigest() + '  matters.json\n')
    print(f"entries {len(entries)} -> N = {doc['N']}; company-figure {doc['company_figure_subgroup']}; adjudicated one-bet {sorted(adjudicated)}; splits {sorted(split)}")
    if doc['N'] < 20:
        print('TOO SMALL: N < 20. Return to Alex before any paid send (D667, D668).')


if __name__ == '__main__':
    {'merge': merge, 'reconcile': reconcile, 'third': third, 'freeze': freeze, 'dedup': dedup, 'adjudicate': adjudicate, 'final': final}[sys.argv[1]]()
