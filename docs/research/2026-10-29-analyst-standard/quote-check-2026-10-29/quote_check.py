"""The quote check's refusals in the six stored draws (haiku-week/sifted.json), and a repair rule for the harmless ones. $0: no model call.

census:  every evidence record the production sift dropped with 'quote not in item' (extraction.sift, the quote check), its closest
         passage in the item text, its class (closed set CLASSES, read by hand: LABELS) and the reference cells it alone carried
         (structure-v2.json state 'refused').
rule:    repair_quote(quote, text). A quote that today's check accepts is returned unchanged. Otherwise it is accepted only when its
         words are the words of one passage of the text, in order, with at most one run of the passage's words left out inside one
         sentence; the stored quote becomes that passage, cut verbatim from the text. Everything else stays refused.
replay:  every stored evidence record of every draw through repair_quote; the repaired answers through the unchanged production
         sift (extraction.sift_with_groups, version 22, keep_unlinked, as haiku_week.py runs it), compared with a control re-run of
         the stored answers; reference cells before and after (score_week.py's matching, re-implemented and checked against
         structure-v2.json).

Run: python3 quote_check.py  (writes census.json and replay.json beside this file, prints the tables).
"""
import collections
import difflib
import json
from pathlib import Path
import re
import sqlite3
import sys

sys.dont_write_bytecode = True
ROOT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import extraction, universe  # noqa: E402

HERE = Path(__file__).resolve().parent
STANDARD = HERE.parent
SIFTED = STANDARD / 'haiku-week' / 'sifted.json'
STRUCTURE = STANDARD / 'structure-v2.json'
REFERENCES = [STANDARD / 'reference-week-v2.json', STANDARD / 'reference-holdout-v2.json']
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
DRAWS = ['luna-1', 'luna-2', 'luna-3', 'haiku-1', 'haiku-2', 'haiku-3']
REFUSAL = 'quote not in item'

# ---------------------------------------------------------------------------------------------------------------------------
# The rule.
#
# A token is what the comparison reads: a footnote marker "[3]" (read and then discarded), a number with its sign, currency sign,
# inner separators and percent sign ("-5%", "$329", "2.4", "30,000"), a word with its inner apostrophes, dots, slashes,
# ampersands and hyphens ("nvidia's", "u.s", "aa/aa2", "current-generation"), or a lone $ € £ ¥ %. Quotation marks, other
# punctuation and spaces between tokens are not compared. Tokens are compared in lower case after extraction.GLYPHS (curly
# quotes and dashes made plain), the same folding today's normalise() applies.
TOKEN = re.compile(r"\[\d{1,3}\]|[-+−]?[$€£¥]?\d+(?:[.,:/]\d+)*%?|[^\W_]+(?:['./&-][^\W_]+)*|[$€£¥%]")
FOOTNOTE = re.compile(r'\[\d{1,3}\]$')
# A sentence ends in a left-out run when the run's raw text holds a line break or a . ! ? … (closing quote or bracket allowed)
# followed by a space. Abbreviations ("U.S. data") read as an end too, which only refuses more.
SENTENCE_END = re.compile(r"[.!?…][\"')\]”’]*\s|\n")
# The stored passage runs from the first matched token to the last, widened over an opening quotation mark or bracket directly
# before it and a sentence end with closing quotation marks or brackets directly after it, so that 'is intact."' stays whole.
OPENING = re.compile(r"[\"'(\[“‘]+$")
CLOSING = re.compile(r"[.!?]?[\"')\]”’]*")


def passage(text, start, end):
    """text[start:end] widened over attached opening and closing marks (OPENING, CLOSING)."""
    before = OPENING.search(text[max(0, start - 3):start])
    if before:
        start -= len(before.group(0))
    return text[start:end + len(CLOSING.match(text, end).group(0))]


def tokens(text):
    """The comparison tokens of a text with their character spans in it: [(token, start, end)]. Offsets index the text as given,
    because GLYPHS maps one character to one character and lower case is applied per token."""
    plain = text.translate(extraction.GLYPHS)
    return [(m.group(0).lower(), m.start(), m.end()) for m in TOKEN.finditer(plain) if not FOOTNOTE.match(m.group(0))]


def _runs(needle, hay):
    """Start indexes in hay (a token list) where needle occurs contiguously."""
    n = len(needle)
    first = needle[0]
    return [i for i in range(len(hay) - n + 1) if hay[i] == first and hay[i:i + n] == needle]


def repair_quote(quote, text, text_tokens=None, one_sentence=True, shorter_than_quote=True):
    """(verdict, stored_quote, detail). verdict is 'exact' (today's check accepts; quote unchanged), 'typographic' (the quote's
    tokens equal one passage's tokens), 'elided' (they equal a passage's tokens with one run left out inside one sentence) or
    'refused'. For 'typographic' and 'elided' the stored quote is the passage cut from the text, first token to last token.
    The left-out run must lie inside one sentence (one_sentence) and hold fewer tokens than the quote (shorter_than_quote); the
    two switches exist only so the replay can show what each bound decides."""
    normal = extraction.normalise(quote)
    if len(normal) < 8:
        return 'refused', None, 'shorter than 8 characters (today\'s rule)'
    if normal in extraction.normalise(text):
        return 'exact', quote, ''
    spans = text_tokens if text_tokens is not None else tokens(text)
    hay = [t for t, _, _ in spans]
    need = [t for t, _, _ in tokens(quote)]
    if not need:
        return 'refused', None, 'no tokens'
    found = _runs(need, hay)
    if found:
        i = found[0]
        return 'typographic', passage(text, spans[i][1], spans[i + len(need) - 1][2]), ''
    best = None
    for k in range(1, len(need)):
        head, tail = need[:k], need[k:]
        for j in _runs(tail, hay):
            # the nearest head ending before tail with at least one token left out, the left-out run inside one sentence
            for end in range(j - 1, k - 1, -1):          # end: index after head's last token; tokens end..j-1 are left out
                if shorter_than_quote and j - end >= len(need):
                    break
                if one_sentence and SENTENCE_END.search(text[spans[end - 1][2]:spans[j][1]]):
                    break
                if hay[end - k:end] == head:
                    left_out = j - end
                    if best is None or left_out < best[0]:
                        best = (left_out, end - k, j + len(tail) - 1, end, j)
                    break
    if best is None:
        return 'refused', None, 'no passage holds the quote\'s words in order with at most one left-out run inside a sentence'
    left_out, first, last, gap_start, gap_end = best
    return 'elided', passage(text, spans[first][1], spans[last][2]), text[spans[gap_start][1]:spans[gap_end - 1][2]]


# ---------------------------------------------------------------------------------------------------------------------------
# The census classes (closed set), and the hand reading of every refused record: class, whether the quote means what the
# source passage means, and what differs. Read 2026-10-29 against the item texts.
CLASSES = {
    'A typographic': 'the quote\'s words equal one passage\'s words; only quotation marks, other punctuation, spacing or a footnote marker differ',
    'B elided': 'the quote is one passage with one run of whole words left out; nothing added or changed',
    'C added': 'the quote is one passage with words added; nothing left out or changed',
    'D substituted': 'one word or short phrase of the passage replaced by other words',
    'E joined or paraphrased': 'words from separate places joined, or the statement reworded beyond one replacement',
    'F not in the body': 'the quote is the item title (the body is another page) or empty',
}
LABELS = {
    'luna-1|gnews:022516991251df7f1af4d7cb|e4': ('D substituted', 'same', '"This post covers" -> "The post covers"'),
    'luna-1|gnews:085b1e1a1543437edb9756d6|e33': ('C added', 'same', '"In mid-2026" -> "In this mid-2026"'),
    'luna-1|gnews:085b1e1a1543437edb9756d6|e7': ('D substituted', 'same', '"Nvidia\'s backstop program" -> "the Nvidia backstop program"'),
    'luna-1|gnews:784c556d2e58ed09dd8aa7fc|e6': ('D substituted', 'changed', '"His research" (Craig Singleton) -> "Its research"; the one_line keeps Singleton'),
    'luna-1|gnews:9f430c6ce2e8d551fe1f063a|e7': ('A typographic', 'same', 'footnote marker "[3]" left out'),
    'luna-1|gnews:b680fbe2c3e9228eba33a0b4|e3': ('D substituted', 'changed', '"the reactor, which was then turned up" -> "the company then turned up"; the one_line keeps the reactor'),
    'luna-1|gnews:c75f16a6d64cc27fc28fb571|e1': ('B elided', 'same', '"with a short statement" left out'),
    'luna-1|gnews:cfa20b22ec2a161c6fd85d8e|e1': ('F not in the body', 'n/a', 'the item title; the body is an unrelated news listing (reference: input defect)'),
    'luna-1|gnews:e26afcac61813d4e7af1b802|e2': ('B elided', 'same', '"poured cold water on Tuesday\'s rebound in chip stocks" left out (a comma added)'),
    'luna-2|gnews:07610e55de6cc86b2b508b1d|e6': ('C added', 'same', '"NVIDIA" added before "NemoClaw"'),
    'luna-2|gnews:085b1e1a1543437edb9756d6|e9': ('D substituted', 'same', '"In the backstop program" -> "In this backstop program"'),
    'luna-2|gnews:26325b9e051efe16db34f758|e1': ('B elided', 'same', '", a leader in AI-powered physical security and operations," left out'),
    'luna-2|gnews:26325b9e051efe16db34f758|e3': ('A typographic', 'same', 'an opening quotation mark added before "With" (the source opens it two sentences earlier)'),
    'luna-2|gnews:cfa20b22ec2a161c6fd85d8e|e1': ('F not in the body', 'n/a', 'the item title; the body is an unrelated news listing'),
    'luna-2|gnews:d4c5dc540392f8df39aee250|e6': ('D substituted', 'same', '"the company\'s" -> "Nvidia\'s"'),
    'luna-3|gnews:07610e55de6cc86b2b508b1d|e7': ('C added', 'same', '"NVIDIA" added before "NemoClaw"'),
    'luna-3|gnews:2a41a34c16f5280b624481fb|e1': ('B elided', 'same', '", which builds some of the most coveted AI chips in the world," left out'),
    'luna-3|gnews:3faf8050f6d3b8ddee1d18c2|e2': ('B elided', 'same', '"NVIDIA GeForce" left out'),
    'luna-3|gnews:68a3ed21f77b935d9fa7ec5e|e6': ('D substituted', 'same', '"The chipmaker" -> "Nvidia"'),
    'luna-3|gnews:784c556d2e58ed09dd8aa7fc|e35': ('D substituted', 'same', '"the company sued" -> "Hesai sued"'),
    'luna-3|gnews:784c556d2e58ed09dd8aa7fc|e36': ('D substituted', 'changed', '"Huawei challenged ... lost both cases" -> "Hesai challenged ..."; wrong company (the one_line says Huawei)'),
    'luna-3|gnews:784c556d2e58ed09dd8aa7fc|e5': ('F not in the body', 'n/a', 'empty quote; the one_line paraphrases Huang\'s "every single car, every single truck will be autonomous"'),
    'luna-3|gnews:9f430c6ce2e8d551fe1f063a|e1': ('B elided', 'same', '", the Hangzhou-based AI startup behind ... language models," left out'),
    'luna-3|gnews:c75f16a6d64cc27fc28fb571|e10': ('B elided', 'same', '"with a short statement" left out'),
    'luna-3|gnews:cfa20b22ec2a161c6fd85d8e|e1': ('F not in the body', 'n/a', 'the item title; the body is an unrelated news listing'),
    'luna-3|gnews:d4c5dc540392f8df39aee250|e7': ('D substituted', 'same', '"the company\'s" -> "Nvidia\'s"'),
    'haiku-1|gnews:085b1e1a1543437edb9756d6|e14': ('E joined or paraphrased', 'changed', 'two places joined with "...", "program" added, "its" -> "Nvidia\'s"'),
    'haiku-1|gnews:2957e5c79a365952140c8cce|e13': ('E joined or paraphrased', 'changed', '"Reuters previously reported that the company was preparing" -> "DeepSeek later reportedly raised"; the one_line keeps "preparing"'),
    'haiku-1|gnews:4d1b1ca014068fb532f116b3|e7': ('A typographic', 'same', 'the quotation marks around "close to about $50 billion in the future," left out'),
    'haiku-1|gnews:b680fbe2c3e9228eba33a0b4|e6': ('D substituted', 'same', '"the delay or cancellation" -> "have been delay or cancellation"'),
    'haiku-1|gnews:c1658c3cc3b216fa2b0eaa54|e1': ('D substituted', 'same', '"who said" -> "he said"'),
    'haiku-1|gnews:cfa20b22ec2a161c6fd85d8e|e1': ('F not in the body', 'n/a', 'the item title; the body is an unrelated news listing'),
    'haiku-2|gnews:1eeceeb212a2c82c2e75e806|e2': ('B elided', 'same', 'first name "Alan" left out'),
    'haiku-2|gnews:c1658c3cc3b216fa2b0eaa54|e1': ('D substituted', 'changed', '"the company is working" -> "he is working"; the actor moves from Valve to Griffais (the one_line keeps Valve)'),
    'haiku-2|gnews:cfa20b22ec2a161c6fd85d8e|e1': ('F not in the body', 'n/a', 'the item title; the body is an unrelated news listing'),
    'haiku-3|gnews:2f953a56cd06571ab0afc348|e1': ('B elided', 'same', '"has led here for years and" left out'),
    'haiku-3|gnews:af6e4910e877d5682a773d4b|e6': ('B elided', 'same', '"shifted to a multi-model strategy and" left out'),
    'haiku-3|gnews:cfa20b22ec2a161c6fd85d8e|e1': ('F not in the body', 'n/a', 'the item title; the body is an unrelated news listing'),
}
# The rule's verdict each class is expected to get: A and B accepted, every other class refused.
EXPECTED = {'A typographic': 'typographic', 'B elided': 'elided'}


# Positive controls on made-up text: what the rule must accept and refuse, including the residual risk it accepts on purpose
# (a left-out "not" is accepted; the stored quote then carries the "not", the model's other fields may not).
CONTROL_TEXT = ('Nvidia will not ship the H20 to China this year. Unlike Hesai, Huawei challenged both rulings in court. '
                'Revenue fell -5% to $329 million [2] . The company, based in Santa Clara, said demand was "strong" in July.')
CONTROLS = [
    ('Nvidia will not ship the H20 to China this year.', 'exact'),
    ('Revenue fell -5% to $329 million.', 'typographic'),                      # footnote marker left out
    ('the company, based in Santa Clara, said demand was strong in July', 'typographic'),   # quotation marks left out
    ('The company said demand was "strong" in July.', 'elided'),              # appositive left out
    ('Nvidia will ship the H20 to China this year.', 'elided'),               # "not" left out: accepted, repaired with "not"
    ('Hesai challenged both rulings in court.', 'elided'),                    # a name earlier in the sentence: accepted, repaired
    ('Revenue fell 5% to $329 million.', 'refused'),                          # sign dropped
    ('Revenue fell -5% to €329 million.', 'refused'),                         # currency changed
    ('Huawei challenged both rulings in court and lost.', 'refused'),         # word added
    ('Nvidia will not ship the H20 to Asia this year.', 'refused'),           # word substituted
    ('Nvidia will not ship the H20 to Huawei.', 'refused'),                  # the left-out run crosses a sentence end
    ('The company in July.', 'refused'),                                      # the left-out run is longer than the quote
    ('in July', 'refused'),                                                   # shorter than 8 characters
]


def run_controls(**switches):
    """Each control's verdict, and for repaired ones the stored quote; fails on the first wrong verdict."""
    out = []
    for quote, expected in CONTROLS:
        verdict, stored, _ = repair_quote(quote, CONTROL_TEXT, None, **switches)
        assert verdict == expected, (quote, expected, verdict, stored)
        if stored is not None:
            assert stored in CONTROL_TEXT and extraction.normalise(stored) in extraction.normalise(CONTROL_TEXT)
        out.append((quote, verdict, stored))
    return out


def mutants():
    """The controls under the rule with one bound switched off: each mutant must fail a control."""
    caught = {}
    for name, switches in (('without one_sentence', {'one_sentence': False}), ('without shorter_than_quote', {'shorter_than_quote': False})):
        try:
            run_controls(**switches)
            caught[name] = 'NOT CAUGHT'
        except AssertionError as error:
            caught[name] = f'caught by control {error.args[0][0]!r} ({error.args[0][2]})'
    return caught


def closest_passage(quote, text, spans):
    """The text passage best aligned with the quote's tokens (for the census only): (raw passage, token differences)."""
    need = [t for t, _, _ in tokens(quote)]
    hay = [t for t, _, _ in spans]
    if not need:
        return None, []
    a, b, size = difflib.SequenceMatcher(None, need, hay, autojunk=False).find_longest_match(0, len(need), 0, len(hay))
    if size == 0:
        return None, []
    lo, hi = max(0, b - a - 30), min(len(hay), b + (len(need) - a) + 30)
    blocks = [x for x in difflib.SequenceMatcher(None, need, hay[lo:hi], autojunk=False).get_matching_blocks() if x.size]
    start, stop = lo + blocks[0].b, lo + blocks[-1].b + blocks[-1].size
    if sum(x.size for x in blocks) * 2 < len(need):
        return None, []
    passage = hay[start:stop]
    diffs = [f'{tag}: quote[{" ".join(need[i1:i2])}] source[{" ".join(passage[j1:j2])}]'
             for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, need, passage, autojunk=False).get_opcodes() if tag != 'equal']
    return text[spans[start][1]:spans[stop - 1][2]], diffs


def matches(quote, item):
    """score_week.py's matching of a record to a reference item, unchanged."""
    q = extraction.normalise(quote)
    return any(s in q or (len(q) >= 30 and q in s)
               for s in [extraction.normalise(x) for x in [item['span']] + list(item.get('also', []))])


def load_item(db, input_id):
    item = dict(db.execute('select * from items where input_id=?', (input_id,)).fetchone())
    item['object_identifiers'] = json.loads(item['object_identifiers'])
    return item


def structure(answers, kept, refs):
    """{(input_id, item_id, draw): state} as score_week.py computes it, for the given answers {draw: {input_id: evidence}} and
    kept ids {draw: {input_id: set}}."""
    out = {}
    for draw in DRAWS:
        for input_id, art in refs.items():
            evidence = answers[draw].get(input_id, [])
            keep = kept[draw].get(input_id, set())
            for item in art.get('statements', []) + [dict(x, weight='exclude') for x in art.get('exclude', [])]:
                hits = [e for e in evidence if matches(e['quote'], item)]
                out[(input_id, item['id'], draw)] = 'kept' if any(e['id'] in keep for e in hits) else ('refused' if hits else 'omitted')
    return out


def main():
    controls = run_controls()
    caught = mutants()
    assert all(v != 'NOT CAUGHT' for v in caught.values()), caught
    sifted = json.loads(SIFTED.read_text())
    db = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    refs, weight = {}, {}
    for path in REFERENCES:
        for art in json.loads(path.read_text())['articles']:
            refs[art['input_id']] = art
            for item in art.get('statements', []):
                weight[(art['input_id'], item['id'])] = item['weight']
            for item in art.get('exclude', []):
                weight[(art['input_id'], item['id'])] = 'exclude'
    items, spans_of = {}, {}

    def item_of(input_id):
        if input_id not in items:
            items[input_id] = load_item(db, input_id)
            spans_of[input_id] = tokens(items[input_id]['text'])
        return items[input_id]

    # 1. replay every record through today's check and the rule; control re-run of the production sift; repaired re-run
    rows = []
    before_ev, after_ev, before_kept, after_kept = ({d: {} for d in DRAWS} for _ in range(4))
    sift_checks = collections.Counter()
    changed_kept = []
    for draw in DRAWS:
        for input_id, record in sifted[draw].items():
            if record['sift'] is None:
                sift_checks['answers without a sift (failed or schema)'] += 1
                continue
            item = item_of(input_id)
            text = item['text']
            answer = record['answer']
            evidence = extraction.flatten_account(answer)['evidence']
            dropped_quote = {i for i, reason in record['sift']['dropped'] if reason == REFUSAL}
            repaired_evidence = []
            for e in evidence:
                verdict, stored, detail = repair_quote(e['quote'], text, spans_of[input_id])
                today = 'refused' if e['id'] in dropped_quote else 'accepted'
                assert (verdict == 'exact') == (today == 'accepted'), (draw, input_id, e['id'], verdict, today)
                if verdict == 'exact':
                    assert stored == e['quote']
                rows.append({'draw': draw, 'input_id': input_id, 'id': e['id'], 'today': today, 'verdict': verdict,
                             'quote': e['quote'], 'stored_quote': stored, 'left_out': detail if verdict == 'elided' else '',
                             'one_line': e.get('one_line')})
                repaired_evidence.append(dict(e, quote=stored) if verdict in ('typographic', 'elided') else e)
            assert 'paragraphs' not in answer, 'flattened answers would need the repair written back per paragraph'
            control = extraction.sift_with_groups(answer, item, text, set(), uni, english=True, shown_group_ids=(), version='22', keep_unlinked=True)
            stored_sift = record['sift']
            same = json.loads(json.dumps([control[0], control[1], [list(x) for x in control[2]], control[3]], ensure_ascii=False)) == \
                [stored_sift['evidence'], stored_sift['candidates'], stored_sift['dropped'], stored_sift['new_groups']]
            sift_checks['control re-run equals stored sift' if same else 'control re-run DIFFERS from stored sift'] += 1
            repaired = extraction.sift_with_groups(dict(answer, evidence=repaired_evidence), item, text, set(), uni, english=True,
                                                   shown_group_ids=(), version='22', keep_unlinked=True)
            old_kept = {e['id']: e for e in control[0]}
            new_kept = {e['id']: e for e in repaired[0]}
            for i, e in old_kept.items():
                if new_kept.get(i) != e:
                    changed_kept.append((draw, input_id, i))
            for i, reason in repaired[2]:
                if reason == REFUSAL:
                    sift_checks['repaired re-run: quote refusals'] += 1
            old_c = {c['id']: c for c in control[1]}
            new_c = {c['id']: c for c in repaired[1]}
            for cid in set(old_c) | set(new_c):
                if old_c.get(cid) != new_c.get(cid):
                    sift_checks[f'candidate changed ({"new" if cid not in old_c else "lost" if cid not in new_c else "edited"})'] += 1
            merges_before = sum(1 for _, r in control[2] if r.startswith('same quote as'))
            merges_after = sum(1 for _, r in repaired[2] if r.startswith('same quote as'))
            sift_checks['same-quote merges added by the repair'] += merges_after - merges_before
            before_ev[draw][input_id] = evidence
            after_ev[draw][input_id] = repaired_evidence
            before_kept[draw][input_id] = set(old_kept)
            after_kept[draw][input_id] = set(new_kept)
            for r in rows:
                if r['draw'] == draw and r['input_id'] == input_id and r['verdict'] in ('typographic', 'elided'):
                    r['kept_after_repair'] = r['id'] in new_kept
                    r['production_check_accepts_stored'] = extraction.normalise(r['stored_quote']) in extraction.normalise(text)

    # 2. census of today's refusals
    refused = [r for r in rows if r['today'] == 'refused']
    keys = {f"{r['draw']}|{r['input_id']}|{r['id']}" for r in refused}
    assert keys == set(LABELS), ('labels do not cover the refusals', keys ^ set(LABELS))
    structure_v2 = json.loads(STRUCTURE.read_text())['per_item']
    only_carrier = collections.defaultdict(list)
    for key, cells in structure_v2.items():
        input_id, item_id = key.split('|')
        for draw, cell in cells.items():
            if cell['state'] == 'refused':
                for rec in cell['records']:
                    only_carrier[f'{draw}|{input_id}|{rec["id"]}'].append((item_id, weight[(input_id, item_id)]))
    assert set(only_carrier) <= keys, 'a refused cell rests on a record dropped for another reason'
    census = []
    for r in refused:
        key = f"{r['draw']}|{r['input_id']}|{r['id']}"
        cls, meaning, note = LABELS[key]
        passage, diffs = closest_passage(r['quote'], items[r['input_id']]['text'], spans_of[r['input_id']])
        census.append(dict(r, key=key, cls=cls, meaning=meaning, note=note, closest_passage=passage, token_differences=diffs,
                           only_carrier_of=only_carrier.get(key, [])))
    disagreements = [(c['key'], c['cls'], c['verdict']) for c in census if c['verdict'] != EXPECTED.get(c['cls'], 'refused')]
    variants = {}
    for one_sentence in (False, True):
        for shorter in (False, True):
            name = f'one_sentence={one_sentence} shorter_than_quote={shorter}'
            accepted = collections.Counter()
            for c in census:
                verdict = repair_quote(c['quote'], items[c['input_id']]['text'], spans_of[c['input_id']], one_sentence, shorter)[0]
                if verdict != 'refused':
                    accepted[c['cls']] += 1
            variants[name] = dict(accepted)
    sizes = []
    for c in census:
        if c['verdict'] == 'elided' or c['cls'] == 'B elided':
            unbounded = repair_quote(c['quote'], items[c['input_id']]['text'], spans_of[c['input_id']], False, False)
            sizes.append((c['key'], c['cls'], len(tokens(c['quote'])), len(tokens(unbounded[2])) if unbounded[0] == 'elided' else None))

    # 3. reference cells before and after
    before = structure(before_ev, before_kept, refs)
    after = structure(after_ev, after_kept, refs)
    control_ok = all(structure_v2[f'{a}|{b}'][d]['state'] == s for (a, b, d), s in before.items())
    moves = collections.Counter((weight[(a, b)], before[(a, b, d)], after[(a, b, d)]) for (a, b, d) in before if before[(a, b, d)] != after[(a, b, d)])

    # 4. write and print
    (HERE / 'census.json').write_text(json.dumps({'classes': CLASSES, 'records': census}, ensure_ascii=False, indent=1) + '\n')
    newly = [r for r in rows if r['verdict'] in ('typographic', 'elided')]
    for r in newly:
        r['hand'] = LABELS[f"{r['draw']}|{r['input_id']}|{r['id']}"]
    per_draw = {d: {'records': sum(1 for r in rows if r['draw'] == d),
                    'refused_today': sum(1 for r in rows if r['draw'] == d and r['today'] == 'refused'),
                    'refused_after': sum(1 for r in rows if r['draw'] == d and r['verdict'] == 'refused')} for d in DRAWS}
    (HERE / 'replay.json').write_text(json.dumps({
        'controls': controls, 'mutants': caught, 'per_draw': per_draw, 'newly_accepted': newly, 'rule_variants': variants, 'left_out_sizes': sizes, 'class_disagreements': disagreements, 'sift_checks': dict(sift_checks), 'previously_kept_changed': changed_kept,
        'structure_control_matches_structure_v2': control_ok,
        'cell_moves': [{'weight': w, 'before': b, 'after': a, 'cells': n} for (w, b, a), n in sorted(moves.items())],
    }, ensure_ascii=False, indent=1) + '\n')

    print(f'CONTROLS: {len(controls)} judged, all as expected')
    for quote, verdict, stored in controls:
        print(f'  {verdict:11} {quote}' + (f'  ->  {stored}' if stored and stored != quote else ''))
    print('  mutants:', caught)
    print('CENSUS: refused records by class and model')
    table = collections.Counter((c['cls'], c['draw'].split('-')[0]) for c in census)
    for cls in CLASSES:
        print(f'  {cls:26} luna {table[(cls, "luna")]:2}  haiku {table[(cls, "haiku")]:2}  total {table[(cls, "luna")] + table[(cls, "haiku")]:2}')
    print(f'  {"all":26} luna {sum(v for (c, m), v in table.items() if m == "luna"):2}  haiku {sum(v for (c, m), v in table.items() if m == "haiku"):2}  total {len(census)}')
    meaning = collections.Counter((c['cls'], c['meaning']) for c in census)
    print('  meaning by class:', {f'{k[0][:1]} {k[1]}': v for k, v in sorted(meaning.items())})
    print('\nRULE VARIANTS: refused records accepted, by class:')
    for name, acc in variants.items():
        print(f'  {name:45} {acc}')
    print('  quote tokens vs left-out tokens (unbounded elision search):')
    for key, cls, kept_n, left_n in sizes:
        print(f'    {cls:14} quote {kept_n:3} left out {left_n}  {key}')
    print('  rule verdict vs hand class (A typographic, B elided, rest refused) disagreements:', disagreements or 'none')
    print('\nONLY CARRIER of a reference item (structure-v2 state refused):')
    for c in census:
        for item_id, w in c['only_carrier_of']:
            print(f"  {c['draw']:8} {c['input_id']} {c['id']:4} {item_id:8} {w:10} {c['cls']:24} -> {c['verdict']}")
    print('\nREPLAY per draw (records, refused today -> refused under the rule):')
    for d, v in per_draw.items():
        print(f"  {d:8} {v['records']:4}  {v['refused_today']:2} -> {v['refused_after']:2}")
    print('  sift checks:', dict(sift_checks))
    print('  previously kept records changed:', changed_kept or 'none')
    print('  structure control equals structure-v2.json:', control_ok)
    print('  reference cell moves:', [(w, b, a, n) for (w, b, a), n in sorted(moves.items())] or 'none')
    print('\nNEWLY ACCEPTED (verdict, hand class/meaning, kept after the production sift):')
    for r in newly:
        print(f"- {r['draw']} {r['input_id']} {r['id']} [{r['verdict']}; {r['hand'][0]}; meaning {r['hand'][1]}; kept {r.get('kept_after_repair')}; "
              f"production check accepts stored quote {r.get('production_check_accepts_stored')}]")
        print(f"    quote : {r['quote']}")
        print(f"    stored: {r['stored_quote']}")
        if r['left_out']:
            print(f"    left out: {r['left_out']}")


if __name__ == '__main__':
    main()
