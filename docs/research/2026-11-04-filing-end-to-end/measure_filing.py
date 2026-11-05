"""The numbers behind predictions-filing.md, per arm, from the answers resend_filing.py saved (or, with --stored, from draw 1's stored answers
through the same production code, as the calibration). Every answer is first passed through production's checks and filing (done in
resend_filing.py); a statement counts only when it would reach the ledger with a link.

  M1  class: each (gold item, question) pair where the judgement gold uses another company's fact for a question other than NVIDIA's two revenue
      questions: the kept statement that best matches the item (shared figures and words, at least MATCH) linked to the question's seed thesis /
      only to v1-v2 / elsewhere / written but no home / not written
  M2  the total-revenue question's intake on the pile articles: statements kept under v1, by the extraction gold's label (not kept, kept and used
      by no question, used only for other questions, used for q01, gold has no span)
  M3  extraction recall on the articles the extraction gold read: its core and supporting matters present (a kept statement matching the span)
  M4  noise: the extraction gold's not-kept spans present
  M5  guards: the gold's q01/q02 items still kept under v1 or v2
  M6  per gold-used item (not per pair): the matching kept statement linked to at least one question the gold uses the item for
  M7  question links on kept statements (to see a metric gamed by linking one statement to many questions)
  P   parking: kept statements under the company-wide revenue questions v1 or v22, every article
  N   per question, links on kept statements whose gold span is not kept, or kept and used by no question
Counts are per send, summed over articles; three sends are shown as their values, never averaged into one.

usage: python3 measure_filing.py <selection.json> <answers.json> [--only <set>] [--examples] | --stored <selection.json>
"""
import collections
import difflib
import json
import re
import sys

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/docs/research/2026-11-04-filing-end-to-end']
import resend_filing as rf
from hivemind import extraction  # noqa: E402

NVIDIA = re.compile(r'nvidia|nvda|jensen|kress|colette', re.I)
FIGURE = re.compile(r'(?<![A-Za-z\d.,])(\d+(?:[.,]\d+)*)(?![A-Za-z]{2,}|\d)')   # a standalone number: not NVL72, GB300, Q2
NAME = re.compile(r'(?<![.!?]\s)(?<!^)\b([A-Z][A-Za-z0-9]+(?:[-][A-Za-z0-9]+)*)')
COMMON_NAMES = {'NVIDIA', 'Nvidia', 'NVDA', 'The', 'This', 'That', 'In', 'On', 'At', 'For', 'And', 'But', 'It', 'Its', 'We', 'Our', 'He', 'She',
                'They', 'A', 'An', 'As', 'By', 'Q1', 'Q2', 'Q3', 'Q4', 'FY2026', 'FY2027', 'FY2028', 'January', 'February', 'March', 'April',
                'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Wall', 'Street', 'CEO', 'CFO', 'AI'}
GENERIC = {'with', 'that', 'this', 'from', 'said', 'says', 'will', 'have', 'were', 'than', 'also', 'into', 'over', 'more', 'about', 'which',
           'their', 'there', 'billion', 'million', 'percent', 'year', 'years', 'quarter', 'company', 'reported', 'according', 'article', 'author',
           'nvidia', 'item', 'gives', 'specified', 'expected', 'expects'}


def figures(text):
    out = set()
    for raw in FIGURE.findall(text or ''):
        value = raw.replace(',', '')
        try:
            number = float(value)
        except ValueError:
            continue
        if number < 10 and '.' not in value or ('.' not in value and len(value) == 4 and 1990 <= number <= 2100):
            continue                     # single digits and years identify nothing
        out.add(number)
    return out


def content(text):
    return {w for w in rf.words(text) if not w[0].isdigit() and w not in GENERIC}


def names(text):
    return {n for n in NAME.findall(text or '') if n not in COMMON_NAMES and not NVIDIA.fullmatch(n)}


def same_fact(statement_text, target_text):
    """(matches, score): a statement states the target fact when it shares one of the target's figures (to the precision either writes)
    and two of its content words, or, for a target with no figure, one of its names other than NVIDIA and three content words."""
    tf, sf = figures(target_text.split(FIGURE_SPLIT)[0]), figures(statement_text)
    shared_figures = sum(1 for t in tf if any(abs(t - x) <= max(0.051, 0.005 * abs(t)) for x in sf))
    shared_words = len(content(target_text) & content(statement_text))
    shared_names = len(names(target_text) & names(statement_text))
    if tf:
        ok = shared_figures >= 1 and shared_words >= 2
    elif names(target_text):
        ok = shared_names >= 1 and shared_words >= 3
    else:
        ok = shared_words >= 4
    return ok, (shared_figures, shared_names, shared_words)


def item_text(item):
    """A gold item's passage and its meaning's 'what' (two items store an empty string as their meaning), with the passage first: same_fact
    takes the figures from the passage alone (the text before FIGURE_SPLIT), never from the paraphrase or its dates."""
    meaning = item['meaning'] if isinstance(item['meaning'], dict) else {}
    return item['passage'] + FIGURE_SPLIT + str(meaning.get('what', ''))


FIGURE_SPLIT = ' \u2016 '          # separates the text figures are read from and the text read only for words and names


def item_who(item):
    return item['who'] + ' ' + (item['meaning'].get('who', '') if isinstance(item['meaning'], dict) else '')


def best(statements, target_text):
    scored = [(same_fact(s['quote'] + ' ' + s['one_line'], target_text), s) for s in statements]
    scored = [(score, s) for (ok, score), s in scored if ok]
    return max(scored, key=lambda x: x[0])[1] if scored else None


def overlaps(quote, passage, run=8):
    """Whether a statement's quote and a gold item's passage are the same source text: both are exact spans of the article (the code checks a
    quote against the item's text; the gold checks its passages), so one contains the other or they share a run of eight consecutive words."""
    q, p = extraction.normalise(quote), extraction.normalise(passage)
    if q in p or p in q:
        return True
    qw, pw = q.split(), p.split()
    return difflib.SequenceMatcher(None, qw, pw, autojunk=False).find_longest_match(0, len(qw), 0, len(pw)).size >= run


def expressing(statements, item):
    """The statements that express a gold item: its best match by `same_fact`, and every statement quoting the item's own passage (a passage
    holding two facts, revenue and margin guidance, is often written as two statements filed under two questions)."""
    found = [s for s in statements if overlaps(s['quote'], item['passage'])]
    top = best(statements, item_text(item))
    if top is not None and not any(s is top for s in found):
        found.append(top)
    return found


def load_gold():
    gold = json.load(open(f'{rf.GOLD}/gold-v1.json'))['entries']
    items = {i['id']: i for i in json.load(open(f'{rf.GOLD}/packet-v1.json'))['items']}
    cited_for = collections.defaultdict(set)
    pairs = []
    for entry in gold:
        if entry['no_view'] or not entry.get('seed_view_id'):
            continue
        cited = set(re.findall(r'\bi\d{3}\b', json.dumps(entry, ensure_ascii=False))) & set(items)   # structured lists and the reasoning text
        for item_id in cited:
            cited_for[item_id].add(entry['question_id'])
            pairs.append((entry['question_id'], entry['seed_view_id'], item_id))
    articles = {a['input_id']: a for part in ('dev', 'test') for a in json.load(open(f'{rf.STANDARD}/golden-v5-{part}.json'))['articles']}
    by_passage = {(i['input_id'], i['passage']): i['id'] for i in items.values()}
    return items, pairs, cited_for, articles, by_passage


def measure_send(input_id, result, sets, gold):
    items, pairs, cited_for, articles, by_passage = gold
    kept = result['kept']
    written = result['kept'] + result['homeless']
    out = collections.Counter()
    notes = []
    for qid, seed, item_id in pairs:
        item = items[item_id]
        if item['input_id'] != input_id:
            continue
        other = not NVIDIA.search(item_who(item))
        target = item_text(item)
        if other and qid not in ('q01', 'q02'):
            hit = best(kept, target)
            if hit:
                links = set(hit['links'])
                outcome = 'narrow home' if seed in links else ('only v1/v2' if links <= {'v1', 'v2'} else 'elsewhere')
            else:
                outcome = 'no home (dropped)' if best(written, target) else 'not written'
            out[f'M1 {outcome}'] += 1
            notes.append((qid, item_id, outcome, hit['one_line'][:90] if hit else '', sorted(hit['links']) if hit else []))
        if qid in ('q01', 'q02'):
            hit = best(kept, target)
            out['M5 guard pairs'] += 1
            out['M5 kept under v1/v2'] += bool(hit and set(hit['links']) & {'v1', 'v2'})
    by_item = collections.defaultdict(set)
    for qid, seed, item_id in pairs:
        if items[item_id]['input_id'] == input_id:
            by_item[item_id].add(seed)
    for item_id, seeds in by_item.items():
        carriers = expressing(kept, items[item_id])
        reached = set().union(*[set(c['links']) for c in carriers]) if carriers else set()
        out['M6 gold-used items'] += 1
        out['M6 reaching a gold question'] += bool(reached & seeds)
        out['M6 homeless'] += bool(not carriers and expressing(result['homeless'], items[item_id]))
        for question in seeds:                       # per question: the gold-used items that reach that very question
            out[f'Q {question} items'] += 1
            out[f'Q {question} reached'] += question in reached
    out['M7 links on kept statements'] += sum(len([l for l in s['links'] if l.startswith('v')]) for s in kept)
    out['P parking: statements under v1 or v22'] += sum(1 for s_ in kept if set(s_['links']) & {'v1', 'v22'})
    article = articles.get(input_id)
    if article:                                       # per question, links on statements the gold does not keep or no question uses
        spans = [('kept' if x.get('weight', 'kept') != 'not_kept' else 'not kept', x['span'], x) for x in article['items'] + article['not_kept']]
        for s_ in kept:
            text = s_['quote'] + ' ' + s_['one_line']
            matched = [(same_fact(text, x[1])[1], x) for x in spans if same_fact(text, x[1])[0]]
            top = max(matched, key=lambda m: m[0])[1] if matched else None
            if not top:
                continue
            unused = top[0] == 'not kept' or not cited_for.get(by_passage.get((input_id, top[1])), set())
            if unused:
                for link in s_['links']:
                    if link.startswith('v'):
                        out[f'N {link} noise links'] += 1
    if input_id in sets.get('pile', []):
        for s in kept:
            if 'v1' not in s['links']:
                continue
            label = 'gold did not read'
            if article:
                spans = [('kept' if x.get('weight', 'kept') != 'not_kept' else 'not kept', x['span'], x) for x in article['items'] + article['not_kept']]
                text = s['quote'] + ' ' + s['one_line']
                matched = [(same_fact(text, x[1])[1], x) for x in spans if same_fact(text, x[1])[0]]
                top = max(matched, key=lambda m: m[0])[1] if matched else None
                if not top:
                    label = 'no gold span'
                elif top[0] == 'not kept':
                    label = 'not kept by the standard'
                else:
                    qs = cited_for.get(by_passage.get((input_id, top[1])), set())
                    label = 'used for q01' if 'q01' in qs else ('used only for other questions' if qs else 'kept, used by no question')
            out[f'M2 v1: {label}'] += 1
    if article:
        for i in article['items']:
            out[f'M3 {i["weight"]} matters'] += 1
            out[f'M3 {i["weight"]} present'] += bool(best(kept, i['span']))
        for n in article['not_kept']:
            label = 'not-kept' if n.get('weight') == 'not_kept' else f'{n.get("weight")} (listed under not_kept)'
            out[f'M4 {label} spans'] += 1
            out[f'M4 {label} present'] += bool(best(kept, n['span']))
    out['code refusals'] += len(result['dropped'])
    out['statements kept'] += len(kept)
    out['statements homeless'] += len(result['homeless'])
    return out, notes


def main():
    gold = load_gold()
    if sys.argv[1] == '--stored':
        selection = json.load(open(sys.argv[2]))
        from hivemind import config, universe
        cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
        uni = universe.load(f'{ROOT}/poc/universe.json')
        items_conn, archive, views = rf.ro(rf.ITEMS), rf.ro(f'{rf.DRAW}/archive.sqlite'), rf.ro(f'{rf.DRAW}/views.sqlite')
        answers = {}
        for input_id, meta in selection['articles'].items():
            item, setting, system, user, schema, shown, parents = rf.rebuild(cfg, items_conn, archive, views, input_id, meta['call_id'], meta['request_sha256'])
            data = json.loads(archive.execute('select answer_json from model_calls where call_id=?', (meta['call_id'],)).fetchone()[0])
            kept, homeless, dropped, candidates = rf.file_like_production(data, item, shown, parents, uni)
            answers[input_id] = {'archived': [{'kept': kept, 'homeless': homeless, 'dropped': dropped}]}
    else:
        selection, answers = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    if '--only' in sys.argv:                          # one article set of the selection (dev, heldout, class, pile, guard)
        keep = set(selection['sets'][sys.argv[sys.argv.index('--only') + 1]])
        answers = {k: v for k, v in answers.items() if k in keep}
    arms = list(dict.fromkeys(arm for per in answers.values() for arm in per))
    sends = max(len(r) for per in answers.values() for r in per.values())
    table, examples = {}, collections.defaultdict(list)
    for arm in arms:
        columns = []
        for n in range(sends):
            total = collections.Counter()
            for input_id, per in answers.items():
                if arm in per and n < len(per[arm]):
                    counts, notes = measure_send(input_id, per[arm][n], selection['sets'], gold)
                    total += counts
                    examples[arm] += [(n, input_id) + note for note in notes]
            columns.append(total)
        table[arm] = columns
    keys = sorted(set().union(*[c for cols in table.values() for c in cols]))
    print(f'{"":42}' + ''.join(f'{arm[:26]:>28}' for arm in arms))
    for key in keys:
        print(f'{key[:42]:42}' + ''.join(f'{" / ".join(str(c[key]) for c in table[arm]):>28}' for arm in arms))
    if '--examples' in sys.argv:
        for arm in arms:
            print(f'\n== {arm}: class pairs not reaching their narrow home (send, article, question, item, outcome, statement, links)')
            for e in examples[arm]:
                if e[4] != 'narrow home':
                    print('  ', e[0], e[2], e[3], e[4], '|', e[5], e[6])


if __name__ == '__main__':
    main()
