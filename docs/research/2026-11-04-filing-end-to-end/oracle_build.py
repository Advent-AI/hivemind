"""Build the requests of the complete-evidence test (oracle-design.md, D361), sending nothing: the gold's cited passages for v10, v12 and v16
as constructed evidence pieces (each quote an exact span of its article, written as start and end anchors below and checked), formatted by the
production judging code at the window end of the frozen v108 draw 1. v16's request is its last stored judging request, rebuilt and refused unless
it has the stored archive key, with the pieces inserted in its evidence block; v10 and v12 were never judged in production (no evidence), so theirs
are constructed with `judging._lines_english` from the draw's ledger (question, ladder, dependencies, themes in force) and labelled constructed.

usage: python3 oracle_build.py <out.json>        (prints every request in full for reading)
"""
import json
import re
import sqlite3
import sys

ROOT = '/Users/lchingen/hivemind'
HERE = f'{ROOT}/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = [f'{ROOT}/src', HERE]
import measure_filing as mf  # noqa: E402
from hivemind import config, model  # noqa: E402
from hivemind.views import judging, store  # noqa: E402

RUN = f'{ROOT}/poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
ITEMS_DB = f'{ROOT}/poc/data/items-nvda-2026-07-01-10-27.sqlite'
PACKET = f'{ROOT}/docs/research/2026-11-01-e2e-loop/judgement-gold/packet-v1.json'
QUESTIONS = {
    'v10': ['i163', 'i084', 'i153', 'i281', 'i302', 'i295', 'i217', 'i142'],
    'v12': ['i131', 'i007', 'i006', 'i001', 'i285', 'i120', 'i301', 'i052', 'i145', 'i295'],
    'v16': ['i234', 'i139', 'i155', 'i228', 'i300', 'i138'],
}
SPANS = {   # item → the quote spans, each (start anchor, end anchor[, 'author']) in its article; the first span holds the gold passage; 'author'
            # marks a context span in the article's own voice, recorded as the publisher's view rather than the item's speaker
    'i163': [('Micron’s GAAP gross margin was 84.6 percent', 'compared with Nvidia’s roughly 66 percent.')],
    'i084': [('Net income totaled $58.3 billion', 'its gross margin was 74.9% during Q1.')],
    'i153': [('Management guided Q2 FY27 revenue', 'non-GAAP gross margin holding at 75%.')],
    'i281': [('Additionally, Nvidia issued another optimistic outlook', 'due to ongoing U.S. export restrictions.')],
    'i302': [('In its most recent quarter (ended April 26)', '(up 211% year over year).')],
    'i295': [('The meetings were upbeat, as expected', 'the $100 bn per quarter mark.')],
    'i217': [('As a share of the bill of materials', 'fell from roughly 63 percent to 51 percent.'),
             ('Morgan Stanley puts memory content per rack at about $2 million', 'virtually absent from earlier systems.')],
    'i142': [('Most strikingly, Micron is now forecasting', 'above the peak gross margins NVIDIA ever achieved.')],
    'i131': [('During the first quarter, NVIDIA generated $50.3 billion', 'up from $62.6 billion in the previous quarter.'),
             ('During the quarter, the company repurchased', 'paid $243 million in dividends.')],
    'i007': [('NVIDIA invested $5B into Intel', 'DGX Rubin NVL8 AI systems.')],
    'i006': [('According to a regulatory filing submitted by NVIDIA in May', 'rights to purchase their shares.')],
    'i001': [('NVIDIA also joins as a new investor in Verkada', 'at the end of last year.')],
    'i285': [('Gradium has extended its seed financing to $100 million', 'San Francisco Bay Area office.')],
    'i120': [('The first is SharonAI’s 72MW AI factory in Australia.', 'over the six year period.'),
             ('Nvidia’s backstop program is only getting started', 'is only getting started', 'author')],
    'i301': [("There's a reason the company was comfortable", 'from $0.01 to $0.25.')],
    'i052': [('Nvidia earlier this month said it was aiming to raise debt', 'refinancing of existing debt.')],
    'i145': [('Alongside the demo, the two companies announced', 'from the local community.”'),
             ('Note the verb. Exploring.', 'has no timeline attached.', 'author')],
    'i234': [('Broadcom ( NASDAQ:AVGO ) benefits through custom ASICs.', 'Q3 guided to $16.0 billion.')],
    'i139': [('Broadcom guided Q3 AI semiconductor revenue to $16.0 billion', 'more than 200% year over year.')],
    'i155': [('Amazon has disclosed Trainium is now a multi-billion-dollar business', 'multi-billion-dollar business')],
    'i228': [('OpenAI introduced its first inference chip', 'developing its own AI chips.')],
    'i300': [('However, Broadcom is also making custom AI chips', 'late this year and into next.')],
    'i138': [('NVIDIA still owns roughly 81% of the AI chip market', 'versus 16% for AI accelerators.')],
}
FIRST_ID = 9001
QUOTE_SHOWN = 400                     # `_lines_english` prints a quote's first 400 characters
SENTENCE_END = re.compile(r'(?<=[.!?])["”]?\s+(?=[A-Z“"])')


def span(text, start, end):
    i = text.find(start)
    if i < 0:
        raise SystemExit(f'start anchor not in the article: {start!r}')
    j = text.find(end, i)
    if j < 0:
        raise SystemExit(f'end anchor not after the start: {end!r}')
    return text[i:j + len(end)]


def passage_sentences(quote, passage):
    """The sentences of the quote that the gold passage covers, in full (a passage of two sentences gives both)."""
    start = quote.find(passage)
    end = start + len(passage)
    bounds = [0] + [m.end() for m in SENTENCE_END.finditer(quote)] + [len(quote)]
    chosen = [quote[a:b].strip() for a, b in zip(bounds, bounds[1:]) if a < end and b > start]
    return ' '.join(chosen)


def pieces_for(item_ids, items, articles, publishers):
    """The constructed pieces for one question, one per quote span, in order of publication day then the list order. The original day is left
    blank (production leaves it blank unless the statement's own date is known, 393 of 554 pieces in this draw); no period note is added (a period
    the article does not state would be the gold's reading)."""
    pieces = []
    for item_id in sorted(item_ids, key=lambda i: (items[i]['day'], item_ids.index(i))):
        item = items[item_id]
        meaning = item['meaning'] if isinstance(item['meaning'], dict) else {}
        text = articles[item['input_id']]
        for n, (start, end, *voice) in enumerate(SPANS[item_id]):
            quote = ' '.join(span(text, start, end).split())
            if len(quote) > QUOTE_SHOWN:
                raise SystemExit(f'{item_id} span {n} is {len(quote)} characters; split it')
            if n == 0 and ' '.join(item['passage'].split()) not in quote:
                raise SystemExit(f'{item_id}: the first span does not hold the gold passage')
            one_line = passage_sentences(quote, ' '.join(item['passage'].split())) if n == 0 else quote   # a context span carries its fact whole
            author = f"{publishers[item['input_id']]} (the article's author)"
            pieces.append({'evidence_id': f'e{FIRST_ID + len(pieces)}', 'tier': 'third_party_view' if voice else item['tier'],
                           'speaker': author if voice else item['who'], 'original_who': author if voice else (meaning.get('who') or item['who']),
                           'original_day': '',
                           'sources': [{'input_id': item['input_id'], 'publication_day': item['day']}],
                           'one_line': one_line, 'quote': quote, 'item': item_id, 'span': n})
    return pieces


def evidence_lines(conn, view_id, pieces):
    built = judging._lines_english(conn, view_id, store.view(conn, view_id), store.rungs_of(conn, view_id), pieces, [], None)
    start = next(i for i, line in enumerate(built) if line.startswith('[Evidence in view under this thesis')) + 1
    lines = []
    for line in built[start:]:
        if line.startswith('\n['):
            break
        lines.append(line)
    return lines


def synthetic_check(conn, view_id, user, cite):
    data = {'rung': 1, 'reasons': 'synthetic', 'cites': [cite], 'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': 'synthetic',
            'theme_pushes': []}
    data.update({field: 'synthetic' for field in judging.STANCE_FIELDS})
    return judging.check_answer(conn, view_id, data, request_text=user)


def main():
    out = sys.argv[1]
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    schema = judging.schema_for(cfg.rejudging.prompt_version)
    items = {i['id']: i for i in json.load(open(PACKET))['items']}
    db = sqlite3.connect(f'file:{ITEMS_DB}?mode=ro', uri=True)
    articles = {i['input_id']: db.execute('select text from items where input_id=?', (i['input_id'],)).fetchone()[0] for i in items.values()}
    publishers = {i['input_id']: db.execute('select publisher from items where input_id=?', (i['input_id'],)).fetchone()[0] for i in items.values()}
    conn = sqlite3.connect(f'file:{RUN}/views.sqlite?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    archive = sqlite3.connect(f'file:{RUN}/archive.sqlite?mode=ro', uri=True)
    with open(config.prompt_path(cfg.rejudging.prompt_version + '.txt'), encoding='utf-8') as handle:
        judging_system = handle.read()
    requests = {}
    # v16: the last stored judging request, rebuilt and checked, with the pieces the stored request does not already carry
    sha, rung, seq = conn.execute("select request_sha256, rung, seq from judgements where view_id='v16' order by seq desc limit 1").fetchone()
    stored = json.loads(archive.execute('select request_json from model_calls where request_sha256=?', (sha,)).fetchone()[0])
    system = next(m['content'] for m in stored['messages'] if m['role'] == 'system')
    user = next(m['content'] for m in stored['messages'] if m['role'] == 'user')
    if model.request_identity(model.build_request(cfg.rejudging, system, user, schema, 'judgement', cfg.provider))[1] != sha:
        raise SystemExit('v16: the rebuilt request is not the stored one; refusing')
    stored_quotes = re.findall(r'^    Quote: (.*)$', user, re.M)
    shown_ids = judging.evidence_shown_in(user)
    v16_pieces = [p for p in pieces_for(QUESTIONS['v16'], items, articles, publishers)
                  if not any(mf.overlaps(q, items[p['item']]['passage']) for q in stored_quotes)]
    assert not shown_ids & {p['evidence_id'] for p in v16_pieces}, 'constructed ids collide with stored ones'
    # The evidence block in arrival order (production lists pieces by when they were linked): the stored pieces and the constructed ones merged
    # by publication day. The stale previous conclusion (rung 1, reasoned on a ledger without these facts) is replaced by the first-judgement line,
    # since a judge that had received these facts on their own days would not carry it.
    header = re.search(r'\[Evidence in view under this thesis, (\d+) items\]\n', user)
    block_end = user.index('\n\n[', header.end())
    stored_chunks = re.split(r'\n(?=- e\d+ \[)', user[header.end():block_end])
    day = lambda chunk: re.search(r'from \S+ (\d{4}-\d{2}-\d{2})\]', chunk).group(1)
    chunks = sorted([(day(c), 0, i, c) for i, c in enumerate(stored_chunks)] + [(day(c), 1, i, c) for i, c in enumerate(evidence_lines(conn, 'v16', v16_pieces))])
    block = f'[Evidence in view under this thesis, {len(chunks)} items]\n' + '\n'.join(c for *_, c in chunks)
    with_pieces = user[:header.start()] + block + user[block_end:]
    with_pieces, replaced = re.subn(r'\[Previous conclusion, for comparison only\][^\n]*', '[Previous conclusion] none: this is the first judgement, so changed must be true.', with_pieces)
    assert replaced == 1 and int(header.group(1)) == len(stored_chunks), 'the stored request does not have the expected shape'
    requests['v16 as stored'] = {'view_id': 'v16', 'system': system, 'user': user, 'constructed': False, 'stored_rung': rung, 'stored_seq': seq, 'pieces': []}
    requests['v16 with evidence'] = {'view_id': 'v16', 'system': system, 'user': with_pieces, 'constructed': True, 'pieces': v16_pieces}
    # The second control: the stored request with only the stale conclusion replaced, no new evidence, so a move can be credited to the evidence.
    first_only, replaced_again = re.subn(r'\[Previous conclusion, for comparison only\][^\n]*', '[Previous conclusion] none: this is the first judgement, so changed must be true.', user)
    assert replaced_again == 1
    requests['v16 first judgement, stored evidence'] = {'view_id': 'v16', 'system': system, 'user': first_only, 'constructed': True, 'pieces': []}
    # v10, v12: constructed at the window end from the draw's ledger, in the production format
    for view_id in ('v10', 'v12'):
        if store.evidence_in_force(conn, view_id) or store.current_state(conn, view_id):
            raise SystemExit(f'{view_id} has evidence or a judgement in the draw; the design assumed neither')
        pieces = pieces_for(QUESTIONS[view_id], items, articles, publishers)
        lines = judging._lines_english(conn, view_id, store.view(conn, view_id), store.rungs_of(conn, view_id), pieces,
                                       store.dependencies_of(conn, view_id), None, judging.themes_in_force(conn, view_id))
        requests[f'{view_id} with evidence'] = {'view_id': view_id, 'system': judging_system, 'user': '\n'.join(lines), 'constructed': True, 'pieces': pieces}
    for arm, r in requests.items():
        body = model.build_request(cfg.rejudging, r['system'], r['user'], schema, 'judgement', cfg.provider)
        r['request_sha256'] = model.request_identity(body)[1]
        r['characters'] = len(r['system']) + len(r['user'])
        cite = r['pieces'][0]['evidence_id'] if r['pieces'] else sorted(judging.evidence_shown_in(r['user']))[0]
        r['synthetic_check'] = synthetic_check(conn, r['view_id'], r['user'], cite)
        r['system_is_judging_v7'] = r['system'] == judging_system
        print(f'\n{"=" * 30} {arm}: {r["characters"]} characters, {len(r["pieces"])} constructed pieces, system is judging-v7: '
              f'{r["system_is_judging_v7"]}, synthetic answer check: {r["synthetic_check"] or "passes"}')
        print(r['user'] if arm not in ('v16 as stored', 'v16 first judgement, stored evidence') else r['user'][:600] + ' […]')
    json.dump(requests, open(out, 'w'), indent=1, ensure_ascii=False)
    print(f'\nsaved {out}')


if __name__ == '__main__':
    main()
