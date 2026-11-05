"""Fix 1 of D362, at no cost: every quote the production check refuses, replayed through a candidate rule that maps a same-sentence rewrite back
to its source sentence. Nothing is sent and nothing in the package changes; the rule lives here until Alex decides.

Candidate rule (same-sentence rewrite): a refused quote carrying at least one number and three content words (words outside the repair's harmless
set) stands for one source sentence when every one of its content tokens occurs in that sentence (as often as in the quote); when the sentence names
two or more parties, every number of the quote must be attributed to the same party in the quote as in the sentence (the nearest party named before
it: a possessive word, or a capitalised word that is not an acronym or a harmless word). The stored quote is then that sentence, verbatim.

Population: the raw evidence quotes of answers.json and answers-links.json (today's two re-send batches) and of the three frozen v108 draws' stored
extraction answers. A quote is refused exactly as `extraction.sift` refuses it: its normalised form is not in the normalised item text and
`extraction.repair_quote` finds no passage.

usage: python3 quote_rewrite_census.py > quote-rewrite-census.txt
"""
import collections
import json
import re
import sqlite3
import sys

ROOT = '/Users/lchingen/hivemind'
HERE = f'{ROOT}/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = [f'{ROOT}/src', HERE]
import measure_filing as mf  # noqa: E402
from hivemind import extraction  # noqa: E402

ITEMS_DB = f'{ROOT}/poc/data/items-nvda-2026-07-01-10-27.sqlite'
DRAWS = [f'{ROOT}/poc/data/e2e-r9-frozen-v108-2026-11-03/d{n}' for n in (1, 2, 3)]
NUMBER = re.compile(r'[-+−]?[$€£¥]?\d')
SENTENCE = re.compile(r'[^.!?\n]*(?:[.!?](?=\s|$)|\n|$)')
WORD = re.compile(r"[A-Za-z][A-Za-z.&'’-]*")


def refused(quote, text, body):
    q = extraction.normalise(quote)
    if len(q) >= 8 and q in body:
        return False
    repaired = extraction.repair_quote(quote, text)
    return repaired is None or extraction.normalise(repaired) not in body


def sentences(text):
    """Source sentences with their exact text (a sentence ends at . ! ? before a space, at a line break, or at the end)."""
    out, start = [], 0
    for m in re.finditer(r'(?<=[.!?])["”’)]*\s+|\n+', text):
        if m.start() > start:
            out.append(text[start:m.start()].strip())
        start = m.end()
    if start < len(text):
        out.append(text[start:].strip())
    return [s for s in out if s]


def parties(text):
    """(position, party) for each word that names a party: a possessive, or a capitalised word that is not an acronym or a harmless word."""
    found = []
    for n, m in enumerate(WORD.finditer(text.translate(extraction.GLYPHS))):
        word = m.group(0)
        bare = re.sub(r"'s$", '', word)
        possessive = word.endswith("'s")
        capitalised = n > 0 and bare[:1].isupper() and not bare.isupper() and bare.lower() not in extraction.HARMLESS_TOKENS   # not the opening word
        if possessive or capitalised:
            found.append((m.start(), bare.lower()))
    return found


def party_before(text, position):
    named = [p for at, p in parties(text) if at < position]
    return named[-1] if named else None


def number_positions(text, number):
    plain = text.translate(extraction.GLYPHS).lower()
    return [m.start() for m in re.finditer(re.escape(number), plain)]


def same_sentence_rewrite(quote, text):
    """The source sentence a refused quote rewrites, or None (the candidate rule above)."""
    tokens = [t for t, _, _ in extraction._quote_tokens(quote)]
    content = [t for t in tokens if t not in extraction.HARMLESS_TOKENS]
    numbers = [t for t in content if NUMBER.match(t)]
    if not numbers or len(content) - len(numbers) < 3:
        return None
    need = collections.Counter(content)
    for sentence in sentences(text):
        have = collections.Counter(t for t, _, _ in extraction._quote_tokens(sentence))
        if any(have[t] < n for t, n in need.items()):
            continue
        if len({p for _, p in parties(sentence)}) >= 2:
            ok = True
            for number in numbers:
                in_quote = [party_before(quote, at) for at in number_positions(quote, number)]
                in_source = {party_before(sentence, at) for at in number_positions(sentence, number)}
                if not in_quote or any(p is None or p not in in_source for p in in_quote):
                    ok = False
            if not ok:
                continue
        return sentence
    return None


def stored_answers():
    """(origin, input_id, raw evidence item) for every raw evidence item of the two answer files and the three frozen draws."""
    for name in ('answers.json', 'answers-links.json'):
        for input_id, per in json.load(open(f'{HERE}/{name}')).items():
            for arm, sends in per.items():
                for n, r in enumerate(sends):
                    for e in r['raw']:
                        yield f'{name}:{arm}:{n}', input_id, e
    for draw in DRAWS:
        archive = sqlite3.connect(f'file:{draw}/archive.sqlite?mode=ro', uri=True)
        for request_json, answer_json in archive.execute("select request_json, answer_json from model_calls where purpose='extract' and answer_json is not null"):
            found = re.search(r'\[Item\] id (\S+?), category ', json.loads(request_json)['messages'][1]['content'])
            if not found:
                continue
            for e in json.loads(answer_json).get('evidence', []):
                yield f'{draw.rsplit("/", 1)[1]}', found.group(1), e


def main():
    db = sqlite3.connect(f'file:{ITEMS_DB}?mode=ro', uri=True)
    texts = {}
    items, pairs, cited_for, articles, by_passage = mf.load_gold()
    gold_items = collections.defaultdict(list)
    for item_id, item in items.items():
        gold_items[item['input_id']].append(item_id)
    counts = collections.Counter()
    accepted = []
    for origin, input_id, e in stored_answers():
        if input_id not in texts:
            row = db.execute('select text from items where input_id=?', (input_id,)).fetchone()
            texts[input_id] = (row[0] or '', extraction.normalise(row[0] or '')) if row else None
        if texts[input_id] is None:
            continue
        text, body = texts[input_id]
        counts['quotes'] += 1
        if not refused(e['quote'], text, body):
            continue
        counts['refused'] += 1
        sentence = same_sentence_rewrite(e['quote'], text)
        if sentence is None:
            continue
        counts['accepted by the candidate rule'] += 1
        gold = [i for i in gold_items[input_id] if mf.overlaps(sentence, items[i]['passage'])]
        counts['of which carry a gold item'] += bool(gold)
        accepted.append((origin, input_id, e, sentence, gold))
    print(dict(counts))
    for origin, input_id, e, sentence, gold in accepted:
        print(f'\n[{origin}] {input_id} links {e.get("links")} gold {gold}\n  quote:    {e["quote"][:220]}\n  one_line: {e.get("one_line", "")[:220]}\n  sentence: {sentence[:300]}')


if __name__ == '__main__':
    main()
