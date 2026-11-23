"""Deck 1 marked by the council (PROTOCOL.md): two closed reader sessions a card, a debate on every differing field (at most two
rounds), the council's marks in the page's own format, ready for the unchanged `tally_deck.py`. No API spend: Codex and the Claude
command line run on the operator's subscriptions.

  python3 council_mark.py build                 # cards.json from deck-1.html (code only)
  python3 council_mark.py mark                  # round 0: both readers, every card
  python3 council_mark.py debate <round>        # round 1 or 2: both readers, every card still differing
  python3 council_mark.py merge                 # council-marks.json in the page's format, and splits.json
"""
import concurrent.futures
import html
import json
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
DECK = HERE.parent / 'deck-1.html'
BRIEF = (HERE / 'brief.md').read_text()
FAMILIES = ('codex', 'claude')
AT_ONCE = 6
CODEX = ['codex', 'exec', '--skip-git-repo-check', '--ephemeral', '--json', '-s', 'read-only', '-m', 'gpt-6.1-terra',
         '-c', 'model_reasoning_effort=high', '-c', 'features.memories=false', '-c', 'memories.use_memories=false',
         '-c', 'memories.generate_memories=false']
CLAUDE = ['claude', '-p', '--output-format', 'stream-json', '--verbose', '--no-session-persistence', '--setting-sources', '',
          '--strict-mcp-config', '--tools', '', '--disable-slash-commands', '--model', 'claude-opus-5-5']
BLOCK = {'p', 'div', 'li', 'h2', 'h3', 'h4', 'blockquote', 'pre', 'summary', 'ol', 'ul', 'section', 'br'}


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in BLOCK:
            self.parts.append('\n')
        if tag == 'li':
            self.parts.append('- ')
        if tag == 'blockquote':
            self.parts.append('  > ')

    def handle_endtag(self, tag):
        if tag in BLOCK:
            self.parts.append('\n')

    def handle_data(self, data):
        self.parts.append(data)


def to_text(fragment):
    parser = Text()
    parser.feed(fragment)
    return re.sub(r'\n{3,}', '\n\n', ''.join(parser.parts)).strip()


def build():
    page = DECK.read_text()
    cards = {}
    for match in re.finditer(r'<section class="card" id="card-(\d+)" data-card="\d+">(.*?)</section>', page, re.S):
        number, body = match.group(1), match.group(2)
        body = re.sub(r'<div class="marks">.*?</div></div>', '', body, flags=re.S)          # the mark buttons are not content
        body = re.sub(r'<div class="choice">.*?</div>', '', body, flags=re.S)
        linked = sorted(set(re.findall(r'href="#(src-\d+)"', match.group(2))), key=lambda s: int(s.split('-')[1]))
        articles = []
        for anchor in linked:
            found = re.search(rf'<section class="article" id="{anchor}">(.*?)</section>', page, re.S)
            articles.append({'anchor': anchor, 'text': to_text(found.group(1)) if found else '(not found)'})
        facts = len(re.findall(r'name="c\d+-fact(\d+)-bears"', match.group(2))) // 3
        cards[number] = {'card': int(number), 'kind': 'matter' if 'The library holds no question on it' in body else 'question',
                         'facts': facts, 'text': to_text(body), 'articles': articles}
    assert len(cards) == 19, len(cards)
    (HERE / 'cards.json').write_text(json.dumps(cards, indent=1, ensure_ascii=False) + '\n')
    print({n: (c['kind'], c['facts'], len(c['text']), len(c['articles'])) for n, c in cards.items()})


def card_prompt(card):
    articles = '\n\n'.join(f'## Article {a["anchor"]}\n{a["text"]}' for a in card['articles'])
    return f'{BRIEF}\n\n# The card (card {card["card"]})\n\n{card["text"]}\n\n# The linked articles\n\n{articles}\n'


def run(family, prompt):
    """One closed session; returns (answer text, void reason or None)."""
    with tempfile.TemporaryDirectory(prefix='deck-reader-') as empty:
        command = CODEX + ['-C', empty, '-'] if family == 'codex' else CLAUDE
        result = subprocess.run(command, input=prompt, text=True, capture_output=True, cwd=empty, timeout=1800)
    events = [json.loads(line) for line in result.stdout.splitlines() if line.strip().startswith('{')]
    if family == 'codex':
        started = False
        for e in events:
            item = e.get('item', {})
            if e.get('type') == 'turn.started':
                started = True
            kind = item.get('type')
            if not kind or kind in ('agent_message', 'reasoning'):
                continue
            if kind == 'error' and not started and 'is deprecated' in item.get('message', ''):
                continue                                   # a configuration notice printed before the turn starts, not an action
            return None, f'a {kind} item in the log'
        items = [e.get('item', {}) for e in events]
        texts = [i.get('text', '') for i in items if i.get('type') == 'agent_message']
        answer = texts[-1] if texts else None
    else:
        for e in events:
            if e.get('type') == 'system' and e.get('subtype') == 'init' and (e.get('tools') or e.get('mcp_servers')):
                return None, 'tools or MCP servers loaded'
            if e.get('type') == 'system' and e.get('subtype') not in ('init', 'thinking_tokens'):
                return None, f"system event {e.get('subtype')}"
            content = (e.get('message') or {}).get('content')
            if isinstance(content, list) and any(c.get('type') == 'tool_use' for c in content):
                return None, 'a tool use'
        results = [e.get('result') for e in events if e.get('type') == 'result']
        answer = results[-1] if results else None
    if result.returncode != 0 or not answer:
        return None, f'exit {result.returncode} or no answer'
    return answer, None


def parse(answer):
    start = answer.find('{')
    depth = 0
    for index in range(start, len(answer)):
        depth += {'{': 1, '}': -1}.get(answer[index], 0)
        if depth == 0:
            return json.loads(answer[start:index + 1])
    raise ValueError('no object')


def valid(row, card):
    allowed = ('yes', 'no', 'cannot tell')
    if row.get('card') != card['card'] or row.get('worth') not in allowed:
        return False
    if card['kind'] == 'question' and row.get('supported') not in allowed:
        return False
    facts = row.get('facts') or []
    if len(facts) != card['facts']:
        return False
    return all(f.get('bears') in allowed and f.get('effect') in ('the answer', 'only the confidence', 'neither', 'cannot tell') for f in facts)


def fields(row, card):
    out = {'worth': row['worth']}
    if card['kind'] == 'question':
        out['supported'] = row['supported']
    for f in row.get('facts') or []:
        out[f'fact{f["fact"]}-bears'] = f['bears']
        out[f'fact{f["fact"]}-effect'] = f['effect']
    return out


def mark_one(family, card, prompt, label):
    for attempt in (1, 2):
        answer, void = run(family, prompt)
        record = {'family': family, 'card': card['card'], 'label': label, 'attempt': attempt, 'void': void, 'answer': answer}
        with open(HERE / 'launches.jsonl', 'a') as log:
            log.write(json.dumps(record, ensure_ascii=False) + '\n')
        if void:
            continue
        try:
            row = parse(answer)
        except (ValueError, json.JSONDecodeError):
            continue
        if valid(row, card):
            return row
    return None


def mark():
    cards = json.loads((HERE / 'cards.json').read_text())
    out = HERE / 'round-0.json'
    if out.exists():
        raise SystemExit('round 0 exists')
    done = {}
    if (HERE / 'launches.jsonl').exists():                 # resume: a valid round-0 answer already recorded is reused, not re-asked
        for line in (HERE / 'launches.jsonl').read_text().splitlines():
            record = json.loads(line)
            if record['label'] == 'round-0' and not record['void'] and record['answer']:
                try:
                    row = parse(record['answer'])
                except (ValueError, json.JSONDecodeError):
                    continue
                if valid(row, cards[str(record['card'])]):
                    done[(record['family'], record['card'])] = row
    jobs = [(family, card) for card in cards.values() for family in FAMILIES if (family, card['card']) not in done]
    rows = {}
    for (family, number), row in done.items():
        rows.setdefault(str(number), {})[family] = row
    print(f'reused {len(done)} valid answers; {len(jobs)} to ask', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=AT_ONCE) as pool:
        for (family, card), row in zip(jobs, pool.map(lambda job: mark_one(job[0], job[1], card_prompt(job[1]), 'round-0'), jobs)):
            rows.setdefault(str(card['card']), {})[family] = row
            print(f"card {card['card']} {family}: {'ok' if row else 'UNRESOLVED'}", flush=True)
    out.write_text(json.dumps(rows, indent=1, ensure_ascii=False) + '\n')


def differing(cards, rows):
    out = {}
    for number, pair in rows.items():
        if not all(pair.get(f) for f in FAMILIES):
            continue
        a, b = (fields(pair[f], cards[number]) for f in FAMILIES)
        diff = sorted(k for k in a if a[k] != b.get(k))
        if diff:
            out[number] = diff
    return out


def debate_prompt(card, family, rows, diff):
    other = 'claude' if family == 'codex' else 'codex'
    mine, theirs = rows[family], rows[other]
    return (card_prompt(card) + '\n# A second reading\n\nAnother analyst marked this card independently and differs from you on: '
            + ', '.join(diff) + '.\n\nYour marks: ' + json.dumps(fields(mine, card), ensure_ascii=False) + '\nYour reason: ' + mine.get('why', '')
            + '\n\nThe other analyst\'s marks: ' + json.dumps(fields(theirs, card), ensure_ascii=False) + '\nTheir reason: ' + theirs.get('why', '')
            + '\n\nRead the card and its articles again. For every field, keep your mark or change it, judged on the material alone; the other '
              'analyst can be wrong. Return the full JSON object in the shape asked above, with `why` saying for each disputed field why you '
              'kept or changed it.')


def debate(round_number):
    cards = json.loads((HERE / 'cards.json').read_text())
    previous = json.loads((HERE / f'round-{round_number - 1}.json').read_text())
    out = HERE / f'round-{round_number}.json'
    if out.exists():
        raise SystemExit(f'round {round_number} exists')
    diff = differing(cards, previous)
    print(f'round {round_number}: {len(diff)} cards differ: {diff}')
    rows = {number: dict(pair) for number, pair in previous.items()}
    jobs = [(family, number) for number in diff for family in FAMILIES]
    with concurrent.futures.ThreadPoolExecutor(max_workers=AT_ONCE) as pool:
        results = pool.map(lambda job: mark_one(job[0], cards[job[1]], debate_prompt(cards[job[1]], job[0], previous[job[1]], diff[job[1]]),
                                                f'round-{round_number}'), jobs)
        for (family, number), row in zip(jobs, results):
            if row:
                rows[number][family] = row
            print(f'card {number} {family}: {"ok" if row else "kept previous (no valid answer)"}', flush=True)
    out.write_text(json.dumps(rows, indent=1, ensure_ascii=False) + '\n')


def merge():
    cards = json.loads((HERE / 'cards.json').read_text())
    last = max(int(p.stem.split('-')[1]) for p in HERE.glob('round-*.json'))
    rows = json.loads((HERE / f'round-{last}.json').read_text())
    marks, splits = {}, {}
    for number, card in cards.items():
        pair = rows.get(number, {})
        if not all(pair.get(f) for f in FAMILIES):
            splits[number] = {'unresolved': [f for f in FAMILIES if not pair.get(f)]}
            continue
        a, b = (fields(pair[f], card) for f in FAMILIES)
        for key in a:
            if a[key] == b.get(key):
                marks[f'c{number}-{key}'] = a[key]
            else:
                marks[f'c{number}-{key}'] = 'cannot tell'
                splits.setdefault(number, {})[key] = {'codex': a[key], 'claude': b[key]}
        marks[f'c{number}-why'] = f"codex: {pair['codex'].get('why', '')} | claude: {pair['claude'].get('why', '')}"
    (HERE / 'council-marks.json').write_text(json.dumps({'deck': 'deck-1', 'marks': marks, 'opened': {}, 'times': {}, 'started': None,
                                                          'last': None, 'by': f'council, rounds 0 to {last}'}, indent=1, ensure_ascii=False) + '\n')
    (HERE / 'splits.json').write_text(json.dumps(splits, indent=1, ensure_ascii=False) + '\n')
    print(f'merged from round {last}: {len(splits)} cards with a split or unresolved field: {splits}')


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command == 'build':
        build()
    elif command == 'mark':
        mark()
    elif command == 'debate':
        debate(int(sys.argv[2]))
    elif command == 'merge':
        merge()
    else:
        sys.exit(__doc__)
