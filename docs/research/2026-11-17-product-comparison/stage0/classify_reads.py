"""Which of the scored window's articles were read (D669): every location the exposure census found is classed, and an article is kept
only when none of its locations is a read.

Not a read, and only these:
1. **corpus storage:** the rows of any SQLite table named `items` (the corpus schema), anywhere, tar members included;
2. **pool lists:** a file named `manifest.json` or `selection.json`, or a Step 1 trace's `run` table (the manifest a run was given);
3. **code-only corpus census output:** a data file (.json, .jsonl, .txt, .csv, .log) outside any archive, whose own folder holds at least one
   Python script, none of which calls a model, and holds no reader material (a `.stream`, `.html` or `.md` file, a `packet*` or `round*`
   file, a `codex*` or `claude*` file, or a subfolder named packets, verdicts, readers or review*).

Everything else is a read, including a file in a folder with no script to show what produced it.

Also a read: an article whose own text a reader was shown without its id, so the census cannot see it (READER_SHOWN, each with the session
that showed it; found by the council check of 2026-11-17 and confirmed by searching the session for the article's text).

    python3 classify_reads.py <census.json> <output folder>
"""
import collections
import datetime
import hashlib
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

WINDOW = ('2026-09-07', '2026-09-20')
SOURCE = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
MODEL_CALL = re.compile(r'model\.call|openai_transport|LiveTransport|codex exec|claude -p|model_caller|build_request|anthropic|/v1/chat')
DATA_FILE = ('.json', '.jsonl', '.txt', '.csv', '.log')
READER_FILE = re.compile(r'(\.stream$|\.html$|\.md$|^packet|^round|^codex|^claude)')
READER_DIR = re.compile(r'^(packets|verdicts|readers|review.*)$')
_folders = {}
READER_SHOWN = {      # D670: shown to the source-loss council's reader as text without an id (poc/data/clean-step1-source-loss-council-2026-11-07)
    'nvblog:ai-infra-summit-vera-rubin-dsx-energy-efficiencies-tokens-per-watt-ai-factories': 'round1.jsonl',
    'gnews:53741d7b758d3017c47200d7': 'round1.jsonl',
    'gnews:76e0f9b1225dc3897236406e': 'round3.jsonl',
    'gnews:e65a31b1f0133480705d099e': 'round3.jsonl',
}


def folder_is_code_only(folder):
    """A folder with at least one script, none calling a model, and no reader material."""
    if folder in _folders:
        return _folders[folder]
    result = False
    if os.path.isdir(folder):
        names = os.listdir(folder)
        scripts = [n for n in names if n.endswith('.py') and os.path.isfile(os.path.join(folder, n))]
        reader = any(READER_FILE.search(n) for n in names) or any(READER_DIR.match(n) and os.path.isdir(os.path.join(folder, n)) for n in names)
        calls = False
        for name in scripts:
            try:
                if MODEL_CALL.search(Path(folder, name).read_text(errors='ignore')):
                    calls = True
                    break
            except OSError:
                calls = True
        result = bool(scripts) and not calls and not reader
    _folders[folder] = result
    return result


def classify(location):
    """'storage', 'pool', 'code-only' or 'read'."""
    inner = location.split('!')[-1]
    in_archive = '!' in location
    if '::' in inner:
        table = inner.rsplit('::', 1)[1]
        if table == 'items':
            return 'storage'
        if table == 'run':
            return 'pool'
        return 'read'
    name = inner.rsplit('/', 1)[-1]
    if name in ('manifest.json', 'selection.json'):
        return 'pool'
    if not in_archive and name.endswith(DATA_FILE) and folder_is_code_only(os.path.dirname(location)):
        return 'code-only'
    return 'read'


def main(census_path, out_dir):
    census = json.loads(Path(census_path).read_text())
    conn = sqlite3.connect(f'file:{SOURCE}?mode=ro', uri=True)
    day = dict(conn.execute('select input_id, publication_day from items where publication_day between ? and ?', WINDOW))
    window_ids = set(census['kept_ids']) | set(census['hits'])
    window_ids = {a for a in window_ids if a in day}
    kept, reads_by_location, not_reads = [], collections.Counter(), collections.Counter()
    for article in sorted(window_ids):
        classes = [(location, classify(location)) for location in census['hits'].get(article, [])]
        if article in READER_SHOWN:
            classes.append((f'reader shown without id: {READER_SHOWN[article]}', 'read'))
        if not any(c == 'read' for _, c in classes):
            kept.append(article)
        for location, c in classes:
            folder = location.split('::')[0]
            (reads_by_location if c == 'read' else not_reads)[(c, folder)] += 1
    week = lambda d: str(datetime.date.fromisoformat(d) - datetime.timedelta(days=datetime.date.fromisoformat(d).weekday()))
    by_week = collections.Counter(week(day[a]) for a in kept)
    population = collections.Counter(week(day[a]) for a in window_ids)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    report = {'rule': __doc__.split('\n\n')[1], 'window': WINDOW, 'census_sha256': hashlib.sha256(Path(census_path).read_bytes()).hexdigest(),
              'population': len(window_ids), 'population_by_week': dict(sorted(population.items())), 'kept': len(kept),
              'kept_by_week': dict(sorted(by_week.items())), 'kept_ids': kept,
              'not_read_locations': [{'class': c, 'location': f, 'articles': n} for (c, f), n in not_reads.most_common()],
              'read_locations': [{'location': f, 'articles': n} for (c, f), n in reads_by_location.most_common()]}
    text = json.dumps(report, indent=1, ensure_ascii=False) + '\n'
    (out / 'reads.json').write_text(text)
    print(json.dumps({k: report[k] for k in ('population', 'population_by_week', 'kept', 'kept_by_week')}, indent=1))
    print('not-read locations by class:', collections.Counter(r['class'] for r in report['not_read_locations']))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
