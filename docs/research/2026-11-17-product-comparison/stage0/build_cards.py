"""Library export and cards for the comparison's reading (card-spec.md; plan §1.5 F; D672, D673). Both systems write the same store
(views, rungs, judgements, evidence) and send the same judge request, so one reader of both serves every draw.

    python3 build_cards.py <views.sqlite> <archive.sqlite> <items db> <output.json>

Writes, per question the library holds at the end of its run (the cutoff), the card text of card-spec.md: the question, its due day and its
possible answers (each rung's condition, stance labels removed); the latest answer and its reasons; the material the answering request
contained (evidence renumbered per card; matcher notes, ids and the header's focus string removed); the library's other questions in opening
order with their opening days. A question never judged is carded "no answer".
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

RUNG = re.compile(r'rung (\d+) ([^:]*): ')
# D673 form check: the three suffixes the answer step appends to a rung condition (ladder_step.py, `middle_text_suffix`), a closed set
ANNOTATION = re.compile(r'\s*\((?:no reference figure when the question opened|the (?:amount last reported|reference) when the question opened: ".*")\)$', re.S)
ITEM = re.compile(r'^- e\d+ \[([^;\]]*); (.*?); original source (.*?); from (\S+) (\S+)\] ', re.S)   # a speaker may hold ';'
NOTE = re.compile(r'\n    (?:It replaces |Opinion, not verified: )')


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def conditions(view_id, conn):
    """{position: condition} with stance labels and the answer step's reference annotations removed (D673)."""
    return {r['position']: ANNOTATION.sub('', (r['condition'] or r['label'] or '')).strip() for r in
            conn.execute('select position, label, condition from rungs where view_id=? order by position', (view_id,))}


def material(request_json):
    """The evidence items of a judge request (`judging._lines_english`): [{tier, speaker, original, input_id, day, summary, quote}]. The
    evidence section runs from its header to the next bracketed section; an item runs to the next item, so a summary or quote with line
    breaks is kept whole; the matcher notes after the quote are dropped."""
    text = json.loads(request_json)['messages'][-1]['content']
    start = text.find('[Evidence in view under this thesis')
    if start < 0:
        return []
    section = text[start:]
    end = re.search(r'\n\n?\[(?!Not shown)', section[1:])
    section = section[:end.start() + 1] if end else section
    chunks = re.split(r'\n(?=- e\d+ \[)', section)
    stated = int(re.match(r'\[Evidence in view under this thesis, (\d+) items\]', section).group(1))
    if len(chunks) - 1 != stated:
        raise ValueError(f'the request states {stated} evidence items and the card read {len(chunks) - 1}')
    items = []
    for chunk in chunks[1:]:
        m = ITEM.match(chunk)
        if not m:
            raise ValueError(f'an evidence item the card cannot read: {chunk[:120]!r}')
        rest = chunk[m.end():]
        rest = NOTE.split(rest)[0]
        summary, _, quote = rest.partition('\n    Quote: ')
        items.append({'tier': m.group(1).strip(), 'speaker': m.group(2).strip(), 'original': m.group(3).strip(), 'input_id': m.group(4),
                      'day': m.group(5), 'summary': summary.strip(), 'quote': quote.strip()})
    return items


def section(text, header):
    """The body of one bracketed section of a judge request, from its header line to the next blank-line section, or ''."""
    start = text.find(header)
    if start < 0:
        return ''
    body = text[start:].split('\n', 1)[1] if '\n' in text[start:] else ''
    return re.split(r'\n\n(?:\[|Answer per the JSON schema)', body, maxsplit=1)[0]


def entries(body):
    """The '- ' entries of a section, each kept whole across line breaks."""
    return [e[2:] for e in re.split(r'\n(?=- )', body) if e.startswith('- ')]


def context(request_json, conn):
    """What the answering request gave besides its evidence items (`judging._lines_english`), blinded as the card is: thesis ids removed,
    each rung shown by its condition (D673). {hidden, previous, depends_on, themes}."""
    text = json.loads(request_json)['messages'][-1]['content']
    hidden = re.search(r'\[Not shown: (\d+) more pieces in force', text)
    previous = re.search(r'\[Previous conclusion, for comparison only\] rung (\d+); reasons: (.*?)(?:\n\nAnswer per the JSON schema|$)', text, re.S)
    out = {'hidden': int(hidden.group(1)) if hidden else 0, 'previous': None, 'depends_on': [], 'themes': []}
    for e in entries(section(text, '[Current conclusions of the theses it depends on]')):
        m = re.match(r'(v\d+) \(([^;]*); ([^)]*)\) (.*): now rung (\S+) .*?; reasons: (.*)$', e, re.S)
        if m:
            answer = conditions(m.group(1), conn).get(int(m.group(5))) if m.group(5).isdigit() else 'not judged yet'
            out['depends_on'].append({'flag': m.group(2), 'direction': m.group(3), 'question': m.group(4), 'answer': answer, 'reasons': m.group(6).strip()})
        else:
            out['depends_on'].append({'flag': 'not yet created', 'direction': '', 'question': re.sub(r'^the (\S+) thesis on chain v\d+', r'the \1 question of a chain', e).strip(),
                                      'answer': None, 'reasons': ''})
    for e in entries(section(text, '[Themes in force, ')):
        m = re.match(r'(v\d+) \([^,]*, due (\S+)\) (.*): now rung (\d+) .*?; judged (\S+?)(; updated since this thesis was last judged)?; reasons: (.*)$', e, re.S)
        if not m:
            raise ValueError(f'a theme entry the card cannot read: {e[:120]!r}')
        rungs = conditions(m.group(1), conn)
        out['themes'].append({'question': m.group(3), 'due': m.group(2), 'rung': int(m.group(4)), 'answer': rungs.get(int(m.group(4))),
                              'possible_answers': [rungs[p] for p in sorted(rungs)], 'judged': m.group(5), 'updated': bool(m.group(6)),
                              'reasons': m.group(7).strip()})
    if previous:
        out['previous'] = {'rung': int(previous.group(1)), 'reasons': previous.group(2).strip()}
    return out


def library(views_path, archive_path, items_path):
    conn, archive, items = ro(views_path), ro(archive_path), ro(items_path)
    day_of = lambda input_id: (items.execute('select publication_day from items where input_id=?', (input_id,)).fetchone() or [None])[0]
    publisher_of = lambda input_id: (items.execute('select publisher from items where input_id=?', (input_id,)).fetchone() or [None])[0]
    views = list(conn.execute('select view_id, question, due_day, created_seq, created_from_input from views order by created_seq'))
    out = []
    for v in views:
        latest = conn.execute('select rung, reasons, request_sha256, seq from judgements where view_id=? order by seq desc limit 1',
                              (v['view_id'],)).fetchone()
        rungs = conditions(v['view_id'], conn)
        bounded = conn.execute('select count(*) from rungs where view_id=? and (lo is not null or hi is not null)', (v['view_id'],)).fetchone()[0]
        entry = {'question_id': v['view_id'], 'question': v['question'], 'due': v['due_day'], 'opened': day_of(v['created_from_input']),
                 'opened_from': v['created_from_input'], 'type': 'figure' if bounded else 'yes/no',
                 'possible_answers': [rungs[p] for p in sorted(rungs)], 'answer': None, 'answer_index': None, 'reasons': None, 'material': []}
        if latest is not None:
            entry['answer'] = rungs.get(latest['rung'])
            entry['answer_index'] = sorted(rungs).index(latest['rung'])      # the stored rung's place in possible_answers
            entry['reasons'] = latest['reasons']
            row = archive.execute('select request_json from model_calls where request_sha256=? limit 1', (latest['request_sha256'],)).fetchone()
            if row is None:
                raise SystemExit(f"{v['view_id']}: the latest judgement's request is not in the archive")
            entry['material'] = [dict(item, publisher=publisher_of(item['input_id'])) for item in material(row['request_json'])]
            entry['context'] = context(row['request_json'], conn)
            if entry['context']['previous']:
                entry['context']['previous']['answer'] = rungs.get(entry['context']['previous']['rung'])
        out.append(entry)
    return out


def card_text(entry, lib):
    lines = [f"Question: {entry['question']}", f"Opened: {entry['opened']}", f"Due: {entry['due']}", 'Possible answers (numbered as the reasons cite them):']
    lines += [f'{k}. {c}' for k, c in enumerate(entry['possible_answers'], 1)]
    if entry['answer'] is None:
        lines += ['', 'Latest answer at the cutoff: no answer']
    else:
        lines += ['', f"Latest answer at the cutoff: {entry['answer']}", f"Reason given: {entry['reasons']}", '',
                  f"Material that answer was given ({len(entry['material'])} items, by day):"]
        for k, item in enumerate(sorted(entry['material'], key=lambda m: m['day']), 1):
            lines.append(f"{k}. ({item['tier']}; publisher {item['publisher']}; speaker {item['speaker']}; original source {item['original']}; "
                         f"published {item['day']}) {item['summary']}")
            if item['quote']:
                lines.append(f"   Quote: {item['quote']}")
        ctx = entry.get('context') or {}
        if ctx.get('hidden'):
            lines.append(f"Not shown to the answer: {ctx['hidden']} more items in force, read in earlier answers; the previous answer carries them.")
        if ctx.get('depends_on'):
            lines += ['', 'Answers of the questions it depends on, as the answer was given them:']
            for d in ctx['depends_on']:
                lines.append(f"- ({d['flag']}; {d['direction']}) {d['question']}: answered {d['answer'] or 'not yet'}; reason: {d['reasons']}"
                             if d['answer'] else f"- {d['question']} ({d['flag']})")
        if ctx.get('themes'):
            lines += ['', 'Themes in force, as the answer was given them:']
            for t in ctx['themes']:
                lines.append(f"- {t['question']} (due {t['due']}): answered {t['rung']}. {t['answer']} on {t['judged']}"
                             + ('; updated since this question was last answered' if t['updated'] else '') + f"; reason: {t['reasons']}")
                lines.append('  Its possible answers: ' + ' '.join(f'{k}. {c}' for k, c in enumerate(t['possible_answers'], 1)))
        previous = ctx.get('previous')
        lines += ['', f"Previous answer, given for comparison: {previous['rung']}. {previous['answer']}; reason: {previous['reasons']}" if previous
                  else 'Previous answer: none (this was the first answer).']
    lines += ['', "The library's questions in opening order (this card's question marked):"]
    lines += [f"- opened {e['opened']}: {e['question']}" + ('   <- this question' if e['question_id'] == entry['question_id'] else '') for e in lib]
    return '\n'.join(lines)


def main(views_path, archive_path, items_path, out_path):
    lib = library(views_path, archive_path, items_path)
    cards = [{'question_id': e['question_id'], 'answered': e['answer'] is not None, 'text': card_text(e, lib)} for e in lib]
    Path(out_path).write_text(json.dumps({'library': lib, 'cards': cards}, indent=1, ensure_ascii=False) + '\n')
    print(f'{len(lib)} questions, {sum(c["answered"] for c in cards)} answered; material items {sum(len(e["material"]) for e in lib)}')


if __name__ == '__main__':
    main(*sys.argv[1:5])
