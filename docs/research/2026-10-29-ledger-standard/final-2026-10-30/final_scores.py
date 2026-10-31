"""Code counts for the final comparison: every version's three draws on the development gold (118) and the test gold (30),
read against the signed pass line (page §9.2). Code counts structure only; meaning is the blind reader's (build_packets.py).
Per version: core matters kept in every draw, supporting matters kept in at least two draws, not-kept entries kept
(of those judged), statements the gold does not hold (per article, median), questions, statements the code dropped,
unusable answers and tokens. Differences against the first version named carry a paired bootstrap interval over articles (seed fixed).

The gold must have been made for the page's version: its evidence part (standard_version) is checked against the page's
<meta name="standard-version"> when this module is imported, and every script that imports it refuses a gold made for another
version (D244, D250). Questions are scored only when the gold's opening part (questions_standard_version) was made for the page's
version too. A not-kept entry counts as kept in a draw only when a statement matching its span is not itself a matter the gold keeps
or allows (core, supporting or optional, by score_gold.same_matter, or an optional span): not-kept words riding inside the quote of a
kept matter are one record of that matter (D250 item 5).

Questions: a gold must-open or may-open question counts as raised when a question of the same opens_as shares at least
QUESTION_SHARE of the gold gist's words (checked on the blind reader's 63 must-open verdicts: 60 agree, 3 counted by code
only); questions that match no listed one are counted and listed for reading.

    python3 final_scores.py PREFIX v29 v42 ...      (PREFIX is the run's tag prefix, e.g. G or H; the first version is the control)
"""
import collections
import json
import re
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402

QUESTION_SHARE = 0.2
PREFIX = 'G'
GOLDS = {'dev': HERE.parent / 'golden-v5/golden-v5-dev.json', 'test': HERE.parent / 'golden-v5/golden-v5-test.json'}   # D250; the v3 and v4 files stay as the record
PAGE = HERE.parents[2] / 'prd/05-extraction-standard.html'


def page_version():
    return int(re.search(r'<meta name="standard-version" content="(\d+)">', PAGE.read_text()).group(1))


def check_golds():
    """Refuse a gold whose evidence part was made for another version of the page; return whether its opening part matches too."""
    version, questions_match = page_version(), {}
    for name, path in GOLDS.items():
        gold = json.loads(Path(path).read_text())
        if gold.get('standard_version') != version:
            raise SystemExit(f'refused: {path} was made for standard version {gold.get("standard_version")}, the page is version {version}; '
                             're-derive the gold first')
        questions_match[name] = gold.get('questions_standard_version', gold.get('standard_version')) == version
    return questions_match


QUESTIONS_SCORED = check_golds()


def matches(gold_question, question):
    g = sg.words(gold_question['gist']) - sg.STOP
    q = sg.words(question['question'] + ' ' + (question.get('looks_at') or '')) - sg.STOP
    return question.get('opens_as') == gold_question.get('opens_as') and bool(g) and len(g & q) >= QUESTION_SHARE * len(g)


def per_article(version, articles):
    """For each article: core/supporting matters and their hits per draw, not-kept entries kept per draw, extras, questions."""
    runs = [sg.answers(f'{PREFIX}-{version}-d{d}') for d in (1, 2, 3)]
    out = {}
    for a in articles:
        iid = a['input_id']
        sifted = [sg.kept(r.get(iid), iid) for r in runs]
        row = {'unusable': sum(s is None for s in sifted), 'core': [], 'supp': [], 'nk_total': 0, 'nk_hits': [], 'extra': [], 'stmts': [],
               'questions': [], 'dropped': [], 'must_open': [], 'unlisted': []}
        listed = a.get('questions', {}).get('must_open', []) + a.get('questions', {}).get('may_open', [])
        row['must_open'] = [[bool(s) and any(matches(gq, q) for q in s['candidates']) for s in sifted] for gq in a.get('questions', {}).get('must_open', [])]
        row['unlisted'] = [[q['question'] for q in s['candidates'] if not any(matches(gq, q) for gq in listed)] if s else [] for s in sifted]
        for it in a['items']:
            hits = [bool(s) and any(sg.same_matter(it, e) for e in s['evidence']) for s in sifted]
            if it['weight'] == 'core':
                row['core'].append(hits)
            elif it['weight'] == 'supporting':
                row['supp'].append(hits)
        nks = [n for n in a['not_kept'] if n['weight'] == 'not_kept']
        row['nk_total'] = len(nks)
        kept_gold = [it for it in a['items'] if it['weight'] in ('core', 'supporting', 'optional')]
        optional_spans = [n['span'] for n in a['not_kept'] if n['weight'] == 'optional']

        def carried(statement):
            return any(sg.same_matter(it, statement) for it in kept_gold) or any(sg.same(span, statement['quote']) for span in optional_spans)
        for s in sifted:
            if not s:
                row['nk_hits'].append(0); row['extra'].append(0); row['stmts'].append(0); row['questions'].append(0); row['dropped'].append(0)
                continue
            row['nk_hits'].append(sum(any(sg.same(n['span'], e['quote']) and not carried(e) for e in s['evidence']) for n in nks))
            ex = 0
            for e in s['evidence']:
                if any(sg.same_matter(it, e) for it in a['items']) or any(sg.same(n['span'], e['quote']) for n in a['not_kept']):
                    continue
                ex += 1
            row['extra'].append(ex)
            row['stmts'].append(len(s['evidence']))
            row['questions'].append(len(s['candidates']))
            row['dropped'].append(sum(1 for d in s['dropped'] if str(d[0]).startswith('e')))
        out[iid] = row
    return out


def totals(rows):
    core = [h for r in rows.values() for h in r['core']]
    supp = [h for r in rows.values() for h in r['supp']]
    nk_total = sum(r['nk_total'] for r in rows.values())
    return {
        'core every draw': sum(all(h) for h in core), 'core total': len(core), 'core never': sum(not any(h) for h in core),
        'core per draw': [sum(h[d] for h in core) for d in range(3)],
        'supporting >=2 draws': sum(sum(h) >= 2 for h in supp), 'supporting total': len(supp), 'supporting never': sum(not any(h) for h in supp),
        'supporting per draw': [sum(h[d] for h in supp) for d in range(3)],
        'not-kept kept per draw': [sum(r['nk_hits'][d] for r in rows.values()) for d in range(3)], 'not-kept judged': nk_total,
        'extra per draw': [sum(r['extra'][d] for r in rows.values()) for d in range(3)],
        'extra per article median': statistics.median(statistics.mean(r['extra']) for r in rows.values()),
        'statements per draw': [sum(r['stmts'][d] for r in rows.values()) for d in range(3)],
        'questions per draw': [sum(r['questions'][d] for r in rows.values()) for d in range(3)],
        'dropped by code per draw': [sum(r['dropped'][d] for r in rows.values()) for d in range(3)],
        'unusable answers': sum(r['unusable'] for r in rows.values()),
        'must-open raised every draw': sum(all(h) for r in rows.values() for h in r['must_open']),
        'must-open total': sum(len(r['must_open']) for r in rows.values()),
        'must-open raised per draw': [sum(h[d] for r in rows.values() for h in r['must_open']) for d in range(3)],
        'unlisted questions per draw': [sum(len(r['unlisted'][d]) for r in rows.values()) for d in range(3)],
    }


def metric(r, name):
    if name == 'core every draw':
        return sum(all(h) for h in r['core'])
    if name == 'supporting >=2 draws':
        return sum(sum(h) >= 2 for h in r['supp'])
    if name == 'not-kept kept (mean of draws)':
        return statistics.mean(r['nk_hits'])
    if name == 'extra (mean of draws)':
        return statistics.mean(r['extra'])


def paired(rows_a, rows_b, name, n=4000):
    ids = sorted(rows_a)
    diffs = [metric(rows_a[i], name) - metric(rows_b[i], name) for i in ids]
    rng = random.Random(20261030)
    boots = sorted(sum(rng.choice(diffs) for _ in ids) for _ in range(n))
    return round(sum(diffs), 1), (round(boots[int(0.025 * n)], 1), round(boots[int(0.975 * n)], 1))


def tokens(version, ids):
    tin = tout = 0
    for d in (1, 2, 3):
        db = sg.sqlite3.connect(f'file:{sg.LOOP / f"{PREFIX}-{version}-d{d}" / "answers.sqlite"}?mode=ro', uri=True)
        for i, a, b in db.execute('select input_id, input_tokens, output_tokens from answers'):
            if i in ids:
                tin += a or 0; tout += b or 0
    return tin, tout


def main():
    global PREFIX
    PREFIX, versions = sys.argv[1], sys.argv[2:]
    control = versions[0]          # the first version named is the control every other one is compared with
    print(f'standard version {page_version()}; gold sha256 ' + ', '.join(f'{n} {sg.sha(p)[:8]}' for n, p in GOLDS.items()))
    report = {}
    for name, path in GOLDS.items():
        articles = json.load(open(path))['articles']
        ids = {a['input_id'] for a in articles}
        rows = {v: per_article(v, articles) for v in versions}
        report[name] = {v: totals(rows[v]) for v in versions}
        for v in versions:
            tin, tout = tokens(v, ids)
            report[name][v]['tokens in/out (3 draws)'] = [tin, tout]
            if v != control:
                report[name][v][f'minus {control} (sum over articles, 95% paired bootstrap)'] = {
                    m: paired(rows[v], rows[control], m) for m in ('core every draw', 'supporting >=2 draws', 'not-kept kept (mean of draws)', 'extra (mean of draws)')}
        (HERE / f'per-article-{PREFIX}-{name}.json').write_text(json.dumps(rows, indent=0) + '\n')
    (HERE / f'final-scores-{PREFIX}.json').write_text(json.dumps(report, indent=1) + '\n')
    for name in GOLDS:
        print(f'===== {name}')
        for v in versions:
            t = report[name][v]
            print(f"{v}: core every {t['core every draw']}/{t['core total']} never {t['core never']} per-draw {t['core per draw']} | supp>=2 {t['supporting >=2 draws']}/{t['supporting total']} never {t['supporting never']} | "
                  f"not-kept {t['not-kept kept per draw']}/{t['not-kept judged']} | extra {t['extra per draw']} med/art {t['extra per article median']:.2f} | stmts {t['statements per draw']} | "
                  + (f"q {t['questions per draw']} must-open every {t['must-open raised every draw']}/{t['must-open total']} per-draw {t['must-open raised per draw']} unlisted {t['unlisted questions per draw']} | "
                     if QUESTIONS_SCORED[name] else f"q {t['questions per draw']} (not scored: the gold's opening part is not made for this version) | ")
                  + f"dropped {t['dropped by code per draw']} | unusable {t['unusable answers']} | tok {t['tokens in/out (3 draws)']}")
            if v != control:
                print(f'      vs {control}:', t[f'minus {control} (sum over articles, 95% paired bootstrap)'])


if __name__ == '__main__':
    main()
