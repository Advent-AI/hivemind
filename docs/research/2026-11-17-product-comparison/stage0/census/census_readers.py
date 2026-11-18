"""The blind matter census, batch reading (plan §1.3 items 1–2; D668, D670). Every kept article of 2026-09-07..09-20 is read by two reader
families apart (Codex, memories off; Claude, closed command line), in batches of about 40 articles in publication order, each in a fresh
closed session with the articles and the signed standard's §3 and §4 inline. The brief is week reading A1's
(`docs/research/2026-11-14-use-acceptance/week/brief-A1.md`), its words unchanged except that the material is given inline.

    python3 census_readers.py build          # the batches and prompts, hashed
    python3 census_readers.py read           # every (family, batch) not yet answered; resumable; void sessions retried once

Writes batches/, prompts/, answers/<family>-batch-NN.txt and launches.jsonl. A session is void when a tool, an MCP server or a system event
other than the closed ones appears (the Deck 1 rule), or when the answer does not account for every article of its batch.
"""
import concurrent.futures
import datetime
import hashlib
import html
import json
import re
import sqlite3
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/lchingen/hivemind')
SOURCE = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
KEPT = HERE.parent / 'kept-articles.json'
STANDARD = ROOT / 'docs/prd/05-extraction-standard.html'
FAMILIES = ('codex', 'claude')
CODEX = ['codex', 'exec', '--skip-git-repo-check', '--ephemeral', '--json', '-s', 'read-only', '-m', 'gpt-6.1-terra',
         '-c', 'model_reasoning_effort=high', '-c', 'features.memories=false', '-c', 'memories.use_memories=false',
         '-c', 'memories.generate_memories=false']
CLAUDE = ['claude', '-p', '--output-format', 'stream-json', '--verbose', '--no-session-persistence', '--setting-sources', '',
          '--strict-mcp-config', '--tools', '', '--disable-slash-commands', '--model', 'claude-opus-5-5']
WEEK_SIZES = {'2026-09-07': 5, '2026-09-14': 6}             # batches per week: about 35 and about 40 articles each
LOCK = threading.Lock()

BRIEF = """# Blind reader, matter census batch {batch} of {batches}: which big questions do these articles raise? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Read ONLY the material below: {count} articles (numbers {first} to {last},
{first_day} to {last_day}, in publication order) and the signed standard's §3 (the opening reasons and "问题怎么写") and §4 (the opening
tests: the answer can change a position; a date and public material can settle it; no question already asks the same). You have no other
material: system answers and reference answers exist and you must not see them.

Read every article in full, first paragraph to last. For each article, list every question worth tracking on its own that it raises: a big
matter (it can change NVIDIA's revenue, profit, cash, credit risk or competitive position, or it is a quantity or decision in the world that
many companies depend on), with an outcome a dated public release, filing or official decision can settle. Small matters, background, a
repeat of what an earlier article already raised (list it again only under the same matter key), a stock-price or valuation view, and anything
no public material can settle are not questions. Most articles raise none or one; say "none" when none qualifies.

Then merge: one matter = one underlying bet, whichever articles raise it; another year of a figure is another matter; two questions are one
matter only when the same outcome would settle both and their answers cannot move apart.

Write one JSON object per line, and nothing else:
- per question: {{"article": n, "matter": "<short key>", "question": "<the question, with its period or check date>", "quote": "<= 40 words from
  the article>", "reason": "<the §3 reason and why it is big, <= 30 words>", "settled_by": "<the public material and when>"}}
- per article with none: {{"article": n, "matter": null}}
- finally, per matter: {{"matter": "<key>", "name": "<one line>", "articles": [n, ...]}}

## The signed standard, §3 and §4

{standard}

## The articles

{articles}
"""


def text_of(fragment):
    fragment = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', fragment, flags=re.S)
    fragment = re.sub(r'<br\s*/?>|</(p|li|h[1-6]|tr|div)>', '\n', fragment)
    return re.sub(r'\n{3,}', '\n\n', html.unescape(re.sub(r'<[^>]+>', '', fragment))).strip()


def standard_sections():
    """§3 and §4 of the signed standard, as text (from the heading of §3 to the heading of §5)."""
    page = STANDARD.read_text()
    start = re.search(r'<h2[^>]*>\s*(<[^>]+>\s*)*3\s*(<[^>]+>\s*)*问题的五类', page)
    end = re.search(r'<h2[^>]*>\s*(<[^>]+>\s*)*5\s*(<[^>]+>\s*)*证据标准', page)
    if not start or not end or end.start() <= start.start():
        raise SystemExit('could not find §3 and §5 in the standard page')
    return text_of(page[start.start():end.start()])


def build():
    kept = json.loads(KEPT.read_text())
    conn = sqlite3.connect(f'file:{SOURCE}?mode=ro', uri=True)
    rows = []
    for article in kept['kept_ids']:
        day, published, publisher, title, text = conn.execute(
            'select publication_day, published_at, publisher, title, text from items where input_id=?', (article,)).fetchone()
        rows.append({'id': article, 'day': day, 'published_at': published or '', 'publisher': publisher or '', 'title': title or '', 'text': text})
    rows.sort(key=lambda r: (r['day'], r['published_at'], r['id']))
    for number, row in enumerate(rows, 1):
        row['article'] = number
    standard = standard_sections()
    (HERE / 'batches').mkdir(exist_ok=True)
    (HERE / 'prompts').mkdir(exist_ok=True)
    batches, number = [], 0
    for week, parts in WEEK_SIZES.items():
        members = [r for r in rows if str(datetime.date.fromisoformat(r['day']) - datetime.timedelta(
            days=datetime.date.fromisoformat(r['day']).weekday())) == week]
        size = -(-len(members) // parts)
        for start in range(0, len(members), size):
            batches.append(members[start:start + size])
    hashes = {}
    for index, batch in enumerate(batches, 1):
        name = f'batch-{index:02d}'
        (HERE / 'batches' / f'{name}.json').write_text(json.dumps(batch, indent=1, ensure_ascii=False) + '\n')
        articles = '\n\n'.join(f"### Article {r['article']} · {r['day']} · {r['publisher']}\n{r['title']}\n\n{r['text']}" for r in batch)
        prompt = BRIEF.format(batch=index, batches=len(batches), count=len(batch), first=batch[0]['article'], last=batch[-1]['article'],
                              first_day=batch[0]['day'], last_day=batch[-1]['day'], standard=standard, articles=articles)
        (HERE / 'prompts' / f'{name}.md').write_text(prompt)
        hashes[name] = hashlib.sha256(prompt.encode()).hexdigest()
    (HERE / 'numbering.json').write_text(json.dumps({r['article']: r['id'] for r in rows}, indent=1) + '\n')
    (HERE / 'prompts.sha256').write_text(''.join(f'{h}  prompts/{n}.md\n' for n, h in hashes.items()))
    print(f'{len(rows)} articles in {len(batches)} batches: {[len(b) for b in batches]}; standard §3–§4 {len(standard)} characters')


def run(family, prompt):
    """One closed session; returns (answer text, void reason or None). The Deck 1 rule (council_mark.run)."""
    with tempfile.TemporaryDirectory(prefix='census-reader-') as empty:
        command = CODEX + ['-C', empty, '-'] if family == 'codex' else CLAUDE
        result = subprocess.run(command, input=prompt, text=True, capture_output=True, cwd=empty, timeout=3600)
    events = [json.loads(line) for line in result.stdout.splitlines() if line.strip().startswith('{')]
    if family == 'codex':
        started = False
        for event in events:
            item = event.get('item', {})
            if event.get('type') == 'turn.started':
                started = True
            kind = item.get('type')
            if not kind or kind in ('agent_message', 'reasoning'):
                continue
            if kind == 'error' and not started and 'is deprecated' in item.get('message', ''):
                continue
            return None, f'a {kind} item in the log'
        texts = [e.get('item', {}).get('text', '') for e in events if e.get('item', {}).get('type') == 'agent_message']
        answer = texts[-1] if texts else None
    else:
        for event in events:
            if event.get('type') == 'system' and event.get('subtype') == 'init' and (event.get('tools') or event.get('mcp_servers')):
                return None, 'tools or MCP servers loaded'
            if event.get('type') == 'system' and event.get('subtype') not in ('init', 'thinking_tokens'):
                return None, f"system event {event.get('subtype')}"
            content = (event.get('message') or {}).get('content')
            if isinstance(content, list) and any(c.get('type') == 'tool_use' for c in content):
                return None, 'a tool use'
        results = [e.get('result') for e in events if e.get('type') == 'result']
        answer = results[-1] if results else None
    if result.returncode != 0 or not answer:
        return None, f'exit {result.returncode} or no answer'
    return answer, None


def accounted(answer, batch):
    """The batch's article numbers the answer does not account for (a question or a 'none' line)."""
    seen = set()
    for line in answer.splitlines():
        line = line.strip().strip(',')
        if not line.startswith('{'):
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if 'article' in row:
            try:
                seen.add(int(row['article']))
            except (TypeError, ValueError):
                pass
    return sorted({r['article'] for r in batch} - seen)


def read_one(family, name):
    batch = json.loads((HERE / 'batches' / f'{name}.json').read_text())
    prompt = (HERE / 'prompts' / f'{name}.md').read_text()
    for attempt in (1, 2):
        answer, void = run(family, prompt)
        missing = accounted(answer, batch) if answer else None
        if answer and missing:
            void = f'{len(missing)} articles not accounted for: {missing[:10]}'
        record = {'family': family, 'batch': name, 'attempt': attempt, 'void': void,
                  'at': datetime.datetime.now().isoformat(timespec='seconds')}
        with LOCK:
            with open(HERE / 'launches.jsonl', 'a') as log:
                log.write(json.dumps(record) + '\n')
        if not void:
            (HERE / 'answers').mkdir(exist_ok=True)
            (HERE / 'answers' / f'{family}-{name}.txt').write_text(answer)
            return name, family, None
    return name, family, void


def read():
    names = sorted(p.stem for p in (HERE / 'batches').glob('batch-*.json'))
    jobs = [(family, name) for name in names for family in FAMILIES if not (HERE / 'answers' / f'{family}-{name}.txt').exists()]
    print(f'{len(jobs)} sessions to run')
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for name, family, void in pool.map(lambda job: read_one(*job), jobs):
            print(f'{family} {name}: {"VOID after two attempts: " + void if void else "answered"}', flush=True)


if __name__ == '__main__':
    {'build': build, 'read': read}[sys.argv[1]]()
