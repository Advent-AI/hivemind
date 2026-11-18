"""Deck 1: a pilot of Alex's own product-level review (D560), built at $0 from the stored fresh-week comparison. The selection
rule and seed are in DESIGN.md, written before this draw. No model is called; every store is opened read-only.

  python3 build_deck.py <the week's key folder> <a new key folder outside the repository>

Writes deck-1.html beside this file, and the sealed key (which card is which, the controls, the model families' stored marks).
"""
import html
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'clean-arch/step4-2026-11-10/stage_b'))
import stored_judgements  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
USE = HERE.parent
WEEK = USE / 'week'
CLASS = USE / 'delivery-class'
RUN = ROOT / 'poc/data/clean-lean-week-2026-11-14'
FOLDERS = {'old': RUN / 'week/p1/prod', 'new': RUN / 'week-r2/c1/judge/draw-c1'}
DRAW = {'old': 'p1', 'new': 'c1'}
ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
SEED = 20261115
TEAMS = ('codex', 'claude')
SHEET_VIEWS = ('v2', 'v3', 'v7')
NEW_PLANT, OLD_PLANTS = 1, (22, 24)
MATTERS = {'M01': ('fiscal 2027', 'revenue'), 'M04': ('commitments',)}


def objects(path, opener='{"'):
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find(opener, position)
        if start == -1:
            return out
        try:
            row, position = decoder.raw_decode(text, start)
            out.append(row)
        except json.JSONDecodeError:
            position = start + 1


def read_only(path):
    connection = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def yes(value):
    return str(value).strip().lower().startswith('yes')


class Sources:
    """Every article a card points to, stored once and shown in the page's appendix."""

    def __init__(self):
        self.items = read_only(ITEMS)
        self.order = []

    def anchor(self, input_id):
        if input_id not in self.order:
            self.order.append(input_id)
        return f'src-{self.order.index(input_id) + 1}'

    def row(self, input_id):
        return self.items.execute('select title, publisher, publication_day, text from items where input_id = ?', (input_id,)).fetchone()


def answer_card(system, entry, packet, stores, sources):
    """One answer as the reading showed it: the stored question and answer choices, the answer of the reading item, its cited statements."""
    store = stores[system]
    view = store.execute('select view_id, object_id, kind, question, due_day from views where view_id = ?', (entry['view'],)).fetchone()
    rungs = [dict(row) for row in store.execute('select position, label, condition from rungs where view_id = ? order by position', (entry['view'],))]
    item = next(row for row in packet if row['item'] == entry['item'])
    answer = item['answer']
    day = store.execute('select publication_day from judgements where call_id = ?', (entry['call_id'],)).fetchone()
    if day is None:
        raise SystemExit(f'{system} {entry["view"]} item {entry["item"]}: no judgement of call {entry["call_id"]} in the store: refused')
    cited = []
    for evidence_id in answer.get('cites', []):
        row = store.execute('select one_line, quote, original_who, original_day, tier from evidence where evidence_id = ?', (evidence_id,)).fetchone()
        if row is None:
            raise SystemExit(f'{system} {entry["view"]} item {entry["item"]}: cited statement {evidence_id} is not in the store: refused')
        source = store.execute('select input_id, publication_day from evidence_sources where evidence_id = ? order by seq limit 1', (evidence_id,)).fetchone()
        cited.append({'id': evidence_id, **dict(row), 'article': sources.anchor(source['input_id']) if source else None,
                      'article_day': source['publication_day'] if source else None})
    return {'kind': 'answer', 'question': view['question'], 'about': f"{view['object_id']} ({'the company' if view['kind'] == 'asset' else 'a theme'})",
            'due': view['due_day'], 'answer_day': day['publication_day'] if day else None, 'rungs': rungs, 'rung': answer['rung'],
            'reasons': answer.get('reasons') or '', 'expects': answer.get('implied_outcome') or '', 'cited': cited, 'request': item['request']}


def matter_card(matter, sample_ids, sources):
    excerpts = []
    for place in matter['articles']:
        input_id = sample_ids[place - 1]
        row = sources.row(input_id)
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', row['text']) if all(word in s.lower() for word in MATTERS[matter['matter']])]
        excerpts.append({'article': sources.anchor(input_id), 'title': row['title'], 'publisher': row['publisher'], 'day': row['publication_day'],
                         'sentences': sentences[:2]})
    return {'kind': 'matter', 'matter': matter['name'], 'example': matter['example_question'], 'excerpts': excerpts}


def sheet(view, rng, stores, sources):
    """The confirmed kept-but-undelivered fact of one question and one checked negative control, shuffled."""
    candidates = [c for c in json.loads((CLASS / 'class-candidates.json').read_text()) if c['question'] == view]
    packets = json.loads((CLASS / 'settle-packets.json').read_text())
    marks = {team: {} for team in TEAMS}
    for team in TEAMS:
        for number in range(1, packets[view] + 1):
            for row in objects(CLASS / f'{team}-class-settle-{view}-{number}.jsonl', '{"item"'):
                marks[team][row['item']] = row
    confirmed = []
    for candidate in candidates:
        pair = [marks[team][candidate['candidate']] for team in TEAMS]
        if all(yes(m.get('in_article')) and not yes(m.get('already_shown')) and yes(m.get('bears')) for m in pair):
            confirmed.append(candidate)
    # The negative control: a kept statement both first readers of the census, reading every statement against all seven
    # questions, left empty for this question while naming it for another one (so it is a substantive fact), not linked to
    # this question and not one of its candidates.
    first = {team: {} for team in TEAMS}
    for team in TEAMS:
        for path in sorted(CLASS.glob(f'{team}-class-part*.jsonl')):
            for row in objects(path, '{"statement"'):
                first[team][row['statement']] = row
    linked = {row[0] for row in stores['new'].execute('select evidence_id from evidence_links where view_id = ?', (view,))}
    listed = {c['statement'] for c in candidates}
    negative = sorted(statement for statement in first['codex'] if statement in first['claude']
                      and all(not first[team][statement].get(view) for team in TEAMS)
                      and any(first[team][statement].get(other) for team in TEAMS for other in packets if other != view)
                      and statement not in linked and statement not in listed)
    if not confirmed or not negative:
        raise SystemExit(f'{view}: no confirmed fact or no negative control ({len(confirmed)}, {len(negative)}): refused')
    negative = [{'candidate': f'{view}:{statement}', 'statement': statement} for statement in negative]
    merges = [m for m in json.loads((CLASS / 'class-merges.json').read_text()) if m['question'] == view]
    groups = {}
    for candidate in confirmed:
        merged = next((index for index, m in enumerate(merges) if candidate['candidate'] in m['members']), candidate['candidate'])
        groups.setdefault(merged, []).append(candidate)
    facts = [{'role': 'confirmed', 'members': group} for group in groups.values()]
    facts.append({'role': 'negative control', 'members': [rng.choice(sorted(negative, key=lambda c: c['candidate']))]})
    rng.shuffle(facts)
    store = stores['new']
    out = []
    for fact in facts:
        lead = fact['members'][-1]
        row = store.execute('select one_line, quote, original_who, original_day from evidence where evidence_id = ?', (lead['statement'],)).fetchone()
        source = store.execute('select input_id, publication_day from evidence_sources where evidence_id = ? order by seq limit 1', (lead['statement'],)).fetchone()
        out.append({'role': fact['role'], 'statements': [c['statement'] for c in fact['members']], 'text': row['one_line'], 'quote': row['quote'],
                    'who': row['original_who'], 'day': row['original_day'], 'article': sources.anchor(source['input_id']),
                    'article_day': source['publication_day'], 'reports': len(fact['members'])})
    return out


def escape(text):
    return html.escape(str(text if text is not None else ''))


def render_card(number, total, card, sources):
    parts = [f'<section class="card" id="card-{number}" data-card="{number}"><h2>Card {number} of {total}</h2>']
    if card['kind'] == 'matter':
        parts.append('<p class="tag">A matter in that week\'s articles. The library holds no question on it.</p>')
        parts.append(f'<h3>{escape(card["matter"])}</h3>')
        parts.append(f'<p class="small">A question a reader wrote for it (not the system\'s): <em>{escape(card["example"])}</em></p><h4>Where it appears</h4><ul>')
        for excerpt in card['excerpts']:
            found = ''.join(f'<blockquote>{escape(s)}</blockquote>' for s in excerpt['sentences']) or '<p class="small">(no sentence found by keyword: open the article)</p>'
            parts.append(f'<li><a href="#{excerpt["article"]}" class="src">{escape(excerpt["title"])}</a> <span class="small">({escape(excerpt["publisher"])}, {escape(excerpt["day"])})</span>{found}</li>')
        parts.append('</ul>')
        parts.append(marks_block(number, 'Should the library hold a question on this?', None))
    else:
        parts.append(f'<h3>{escape(card["question"])}</h3><p class="small">About {escape(card["about"])} · due {escape(card["due"])} · answer as of {escape(card["answer_day"])}</p>')
        parts.append('<h4>Answer choices</h4><ol class="rungs">')
        for rung in card['rungs']:
            chosen = ' class="chosen"' if rung['position'] == card['rung'] else ''
            mark = ' <strong>← the present answer</strong>' if rung['position'] == card['rung'] else ''
            condition = f': {escape(rung["condition"])}' if rung['condition'] and rung['condition'] != rung['label'] else ''
            parts.append(f'<li{chosen}>{escape(rung["label"])}{condition}{mark}</li>')
        parts.append('</ol>')
        parts.append(f'<h4>Its reasons</h4><p>{escape(card["reasons"])}</p>')
        if card['expects']:
            parts.append(f'<p class="small">What it expects: {escape(card["expects"])}</p>')
        parts.append(f'<h4>The {len(card["cited"])} statements it cites</h4><ul class="cited">')
        for statement in card['cited']:
            link = f' · <a href="#{statement["article"]}" class="src">article</a>' if statement['article'] else ''
            who = ' · '.join(escape(x) for x in (statement['original_who'], statement['original_day'] or statement['article_day']) if x)
            parts.append(f'<li><span class="sid">{escape(statement["id"])}</span> {escape(statement["one_line"])} <span class="small">({who}{link})</span>'
                         f'<details class="track" data-what="passage"><summary>passage</summary><blockquote>{escape(statement["quote"])}</blockquote></details></li>')
        parts.append('</ul>')
        parts.append(f'<details class="track" data-what="request"><summary>Everything the answer step was shown (the complete request, {len(card["request"]):,} characters)</summary><pre>{escape(card["request"])}</pre></details>')
        if card.get('sheet'):
            parts.append('<div class="sheet"><h4>Completeness sheet: facts the system kept that week and did not show to this answer</h4>')
            for index, fact in enumerate(card['sheet'], 1):
                reports = f' (reported by {fact["reports"]} articles)' if fact['reports'] > 1 else ''
                who = ' · '.join(escape(x) for x in (fact['who'], fact['day'] or fact['article_day']) if x)
                parts.append(f'<div class="fact"><p><strong>Fact {index}.</strong> {escape(fact["text"])}{reports} <span class="small">({who} · <a href="#{fact["article"]}" class="src">article</a>)</span></p>'
                             f'<details class="track" data-what="passage"><summary>passage</summary><blockquote>{escape(fact["quote"])}</blockquote></details>'
                             + choice(number, f'fact{index}-bears', 'Does it bear on this question?', ('yes', 'no', 'cannot tell'))
                             + choice(number, f'fact{index}-effect', 'It would change:', ('the answer', 'only the confidence', 'neither', 'cannot tell')) + '</div>')
            parts.append('</div>')
        parts.append(marks_block(number, 'Is this a question worth tracking for this company?', 'Is the present answer supported by what is shown?'))
    parts.append('</section>')
    return '\n'.join(parts)


def choice(number, name, label, options):
    buttons = ''.join(f'<label><input type="radio" name="c{number}-{name}" value="{escape(option)}"> {escape(option)}</label>' for option in options)
    return f'<div class="choice"><span class="q">{escape(label)}</span>{buttons}</div>'


def marks_block(number, first, second):
    block = '<div class="marks">' + choice(number, 'worth', first, ('yes', 'no', 'cannot tell'))
    if second:
        block += choice(number, 'supported', second, ('yes', 'no', 'cannot tell'))
    return block + f'<div class="choice"><span class="q">A few words why (optional):</span><input type="text" name="c{number}-why" class="why"></div></div>'


PAGE = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Deck 1</title><style>
body{font:16px/1.5 -apple-system,system-ui,sans-serif;max-width:860px;margin:0 auto;padding:16px;color:#111;background:#fafafa}
.card{background:#fff;border:1px solid #ddd;border-radius:8px;padding:16px 20px;margin:22px 0}
h1{font-size:22px}h2{font-size:14px;color:#666;margin:0 0 6px;text-transform:uppercase;letter-spacing:.04em}h3{font-size:19px;margin:6px 0}h4{font-size:14px;margin:16px 0 4px;color:#333}
.small{font-size:13px;color:#666}.tag{font-size:13px;color:#8a4b00;margin:0}.sid{font:12px ui-monospace,monospace;color:#888}
ol.rungs li{margin:2px 0}ol.rungs li.chosen{background:#fff3c4;border-radius:4px;padding:2px 6px}
ul.cited li{margin:8px 0}blockquote{margin:6px 0;padding:6px 10px;border-left:3px solid #ccc;color:#333;font-size:14px;background:#f6f6f6}
details summary{cursor:pointer;color:#0645ad;font-size:13px}pre{white-space:pre-wrap;font:12px/1.45 ui-monospace,monospace;background:#f6f6f6;padding:10px;border-radius:6px}
.marks,.sheet{border-top:1px solid #eee;margin-top:14px;padding-top:10px}.sheet{background:#f3f8ff;border:1px solid #cfe0f5;border-radius:6px;padding:10px 12px}
.choice{margin:6px 0}.choice .q{display:inline-block;min-width:300px;font-weight:600;font-size:14px}.choice label{margin-right:14px;font-size:14px}
.why{width:60%;padding:4px 6px;font-size:14px}.fact{margin:10px 0;padding-top:6px;border-top:1px dashed #cfe0f5}
#bar{position:sticky;top:0;background:#111;color:#fff;padding:8px 12px;border-radius:6px;font-size:14px;z-index:5}
#out{width:100%;height:150px;font:12px ui-monospace,monospace}button{font-size:14px;padding:6px 12px}
.article{background:#fff;border:1px solid #ddd;border-radius:8px;padding:12px 16px;margin:14px 0}
</style></head><body>
<h1>Deck 1: nineteen cards from one week of the product's output</h1>
<p>Each card is one question a research library held at the end of the week of 22 to 28 September 2026, with the answer it gave and what
the answer rests on. Two cards show a matter with no question. For each card, mark the two lines at its foot; a few words help but are
optional. Three cards carry a blue sheet with one or two more lines per fact. Open a passage, the complete request or an article whenever you
want to: that is normal reading. Nothing here says which system wrote a card, and some cards are controls. About half an hour.
Your marks are kept in this browser as you go; when you finish, copy the box at the very end and paste it back.</p>
<div id="bar">0 of __TOTAL__ cards marked · 0 min</div>
__CARDS__
<section class="card"><h2>When you finish</h2><p>Copy everything in this box and paste it into the chat.</p>
<textarea id="out" readonly></textarea><p><button id="copy">Copy</button> <span id="copied" class="small"></span></p></section>
<h1>Appendix: the articles</h1>
__ARTICLES__
<script>
const KEY='deck-1-marks-v1', TOTAL=__TOTAL__;
let state=JSON.parse(localStorage.getItem(KEY)||'{"marks":{},"opened":{},"times":{},"started":null}');
function save(){localStorage.setItem(KEY,JSON.stringify(state));render();}
function touch(card){const now=Date.now();if(!state.started)state.started=now;state.last=now;const t=state.times[card]||(state.times[card]={first:now,last:now});t.last=now;}
function render(){const done=new Set();for(const k in state.marks){const m=k.match(/^c(\\d+)-worth$/);if(m&&state.marks[k])done.add(m[1]);}
 const minutes=state.started?Math.round(((state.last||Date.now())-state.started)/60000):0;
 document.getElementById('bar').textContent=done.size+' of '+TOTAL+' cards marked · '+minutes+' min';
 document.getElementById('out').value=JSON.stringify({deck:'deck-1',marks:state.marks,opened:state.opened,times:state.times,started:state.started,last:state.last});}
document.querySelectorAll('input[type=radio]').forEach(e=>{if(state.marks[e.name]===e.value)e.checked=true;
 e.addEventListener('change',()=>{state.marks[e.name]=e.value;touch(e.name.match(/^c(\\d+)/)[1]);save();});});
document.querySelectorAll('input.why').forEach(e=>{if(state.marks[e.name])e.value=state.marks[e.name];
 e.addEventListener('input',()=>{state.marks[e.name]=e.value;touch(e.name.match(/^c(\\d+)/)[1]);save();});});
document.querySelectorAll('details.track').forEach(e=>e.addEventListener('toggle',()=>{if(!e.open)return;const card=e.closest('.card').dataset.card;
 const k=card+':'+e.dataset.what;state.opened[k]=(state.opened[k]||0)+1;touch(card);save();}));
document.querySelectorAll('a.src').forEach(e=>e.addEventListener('click',()=>{const c=e.closest('.card');if(!c)return;const k=c.dataset.card+':article';
 state.opened[k]=(state.opened[k]||0)+1;touch(c.dataset.card);save();}));
document.getElementById('copy').addEventListener('click',()=>{const o=document.getElementById('out');o.select();document.execCommand('copy');
 document.getElementById('copied').textContent='copied';});
render();
</script></body></html>'''


def main(week_keys, deck_keys):
    week_keys, deck_keys = Path(week_keys), Path(deck_keys)
    deck_keys.mkdir(parents=True, exist_ok=False)
    rng = random.Random(SEED)
    key_a = json.loads((week_keys / 'week-key-A2.json').read_text())
    key_b = json.loads((week_keys / 'week-key-B.json').read_text())
    packet = json.loads((WEEK / 'packet-B.json').read_text())
    stores = {system: read_only(folder / 'views.sqlite') for system, folder in FOLDERS.items()}
    for connection in stores.values():                      # it maps a view to its topic by id (clean-<view number>)
        stored_judgements.refuse_split_store(connection, 'build_deck')
    sources = Sources()
    quality = {team: {row['id']: row for row in objects(WEEK / f'{team}-A2.jsonl') if row.get('part') == 2} for team in TEAMS}
    support = {team: {row['item']: row for row in objects(WEEK / f'{team}-B.jsonl', '{"item"')} for team in TEAMS}
    confirmation = {row['candidate']: row for row in objects(WEEK / 'control-confirmation.jsonl', '{"candidate"')}
    blind = {system: {entry['own_id']: entry['system_id'] for entry in key_a[DRAW[system]]} for system in DRAW}
    system_of = {draw: system for system, draw in DRAW.items()}
    real = {system: {entry['view']: entry for entry in key_b if entry['draw'] == DRAW[system] and not entry.get('planted')} for system in DRAW}
    planted = {entry['item']: entry for entry in key_b if entry.get('planted')}

    def stored_marks(system, entry):
        own = entry['view'] if system == 'old' else f"clean-{entry['view'][1:]}"
        out = {}
        for team in TEAMS:
            worth = quality[team].get(blind[system].get(own, ''))
            answer = support[team].get(entry['item'])
            out[team] = {'question': worth and {k: worth.get(k) for k in ('verdict', 'duplicate_of', 'why')},
                         'answer': answer and {k: answer.get(k) for k in ('verdict', 'why')}}
        return out

    old_plant = planted[rng.choice(OLD_PLANTS)]
    new_views = [view for view in sorted(real['new'], key=lambda v: int(v[1:])) if view != planted[NEW_PLANT]['view']]
    if len(new_views) != 6 or not set(SHEET_VIEWS) <= set(new_views):
        raise SystemExit(f'the new system\'s six real answers are not as the rule says: {new_views}: refused')
    old_pool = [view for view in sorted(real['old'], key=lambda v: int(v[1:])) if view != old_plant['view']]
    confirmed_old = [view for view in old_pool if real['old'][view].get('candidate')
                     and confirmation.get(real['old'][view]['candidate'], {}).get('verdict') == 'SUPPORTED']
    control = rng.choice(confirmed_old)
    old_views = [control] + rng.sample([view for view in old_pool if view != control], 5)
    distinct = []
    for system, views in (('new', new_views), ('old', old_views)):
        for view in views:
            entry = real[system][view]
            card = answer_card(system, entry, packet, stores, sources)
            confirmed = entry.get('candidate') and confirmation.get(entry['candidate'], {}).get('verdict')
            distinct.append((card, {'kind': 'real answer', 'system': system, 'view': view, 'item': entry['item'], 'separate_reader': confirmed or None,
                                    'stored_marks': stored_marks(system, entry)}))
    for entry in (planted[NEW_PLANT], old_plant):
        system = system_of[entry['draw']]
        distinct.append((answer_card(system, entry, packet, stores, sources),
                         {'kind': 'planted wrong answer', 'system': system, 'view': entry['view'], 'item': entry['item'], 'plant': entry['planted'],
                          'stored_marks': {team: {'answer': support[team].get(entry['item']) and {k: support[team][entry['item']].get(k) for k in ('verdict', 'why')}} for team in TEAMS}}))
    sample_ids = json.loads((WEEK / 'sample-ids.json').read_text())
    matters = {m['matter']: m for m in json.loads((WEEK / 'matters-A2.json').read_text())}
    matter_marks = {team: [row for row in objects(WEEK / f'{team}-A2.jsonl') if row.get('part') == 1] for team in TEAMS}
    label_of = {key_a['labels'][draw]: system for system, draw in DRAW.items()}
    for name in MATTERS:
        missed_by = sorted({label_of[row['system']] for team in TEAMS for row in matter_marks[team] if row['matter'] == name and row['status'] == 'missed'
                            and all(any(other['matter'] == name and other['system'] == row['system'] and other['status'] == 'missed' for other in matter_marks[t]) for t in TEAMS)})
        if len(missed_by) != 1:
            raise SystemExit(f'{name}: not missed by exactly one system for both families ({missed_by}): refused')
        distinct.append((matter_card(matters[name], sample_ids, sources), {'kind': 'no question', 'matter': name, 'missed_by': missed_by[0]}))
    distinct = [(card, dict(record, uid=index)) for index, (card, record) in enumerate(distinct)]
    rng.shuffle(distinct)
    head, tail = distinct[:10], distinct[10:]
    repeats = rng.sample([pair for pair in head if pair[1]['kind'] == 'real answer'
                          and not (pair[1]['system'] == 'new' and pair[1]['view'] in SHEET_VIEWS)], 3)
    tail = tail + [(pair[0], dict(pair[1], repeat=True)) for pair in repeats]
    rng.shuffle(tail)
    order = head + tail
    key = {'seed': SEED, 'built_from': {system: str(folder) for system, folder in FOLDERS.items()}, 'cards': {}}
    for number, (card, record) in enumerate(order, 1):
        if record.get('repeat'):
            record = dict(record, repeat_of=next(n for n, (c, r) in enumerate(order, 1) if r['uid'] == record['uid'] and not r.get('repeat')))
        if record['kind'] == 'real answer' and record['system'] == 'new' and record['view'] in SHEET_VIEWS and not record.get('repeat'):
            card = dict(card, sheet=sheet(record['view'], rng, stores, sources))
            record = dict(record, sheet=[{'fact': index, 'role': fact['role'], 'statements': fact['statements']} for index, fact in enumerate(card['sheet'], 1)])
            order[number - 1] = (card, record)
        key['cards'][str(number)] = record
    total = len(order)
    cards = '\n'.join(render_card(number, total, card, sources) for number, (card, _) in enumerate(order, 1))
    articles = []
    for index, input_id in enumerate(sources.order, 1):
        row = sources.row(input_id)
        articles.append(f'<section class="article" id="src-{index}"><h3>{escape(row["title"])}</h3><p class="small">{escape(row["publisher"])} · {escape(row["publication_day"])}</p>'
                        f'<details><summary>the stored text ({len(row["text"]):,} characters)</summary><pre>{escape(row["text"])}</pre></details></section>')
    page = PAGE.replace('__CARDS__', cards).replace('__ARTICLES__', '\n'.join(articles)).replace('__TOTAL__', str(total))
    (HERE / 'deck-1.html').write_text(page)
    (deck_keys / 'deck-1-key.json').write_text(json.dumps(key, indent=1, ensure_ascii=False) + '\n')
    kinds = [record['kind'] + (' (repeat)' if record.get('repeat') else '') for _, record in order]
    print(f'deck-1.html: {total} cards, {len(sources.order)} articles, {len(page):,} characters; key written outside the repository')
    print('kinds in order:', kinds)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
