"""Bounds on the exposure claim for the week of 2026-10-06..12 ($0; council round 9 of the cold thread).

1. The source-page work that `exposure_census.py` set aside: every file of those five folders that holds one of the week's article
   ids is classed here as a code-only record (page copies, cleaner replays, counts) or as something a model or a reader was given
   (a model trace, a readers' packet, a review page, a council transcript). An article of the second class that is not already
   among the seen-before articles is added as a flagged article.
2. The same article under another id: every article of the database whose stored content hash, normalised text or normalised title
   equals one of the week's, under a different id; then whether that other id appears in an earlier run, probe, packet or transcript.

  python3 exposure_bounds.py
"""
import collections
import hashlib
import json
import mmap
import re
import sqlite3
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).parent
ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
WEEK = '2026-10-06..2026-10-12'
CODE_ONLY = ('page-source-candidate-v3.sqlite', 'page-source-candidate-v4.sqlite', 'manifest.json', 'page-budget-records.jsonl', 'candidates.jsonl', 'extractor-results.jsonl',
             'html-v2-corpus.jsonl', 'lineage.jsonl', 'observations.json', 'dom-observations.jsonl', 'census.json', 'sentence-body-probe.json', 'symbol-tail-corpus.jsonl',
             'symbol-tail-two-sites-corpus.jsonl', 'check_observation.py', 'design.md')
SEARCHED = ['poc/data', 'clean-arch', 'docs/research']


def normalised(text):
    return re.sub(r'\s+', ' ', (text or '').strip().lower())


def main():
    census = json.loads((HERE / 'exposure-census.json').read_text())['weeks'][WEEK]
    summary = json.loads((HERE / 'exposure-summary.json').read_text())
    source_work = tuple(summary['source_page_work_not_counted'])
    manifest = json.loads((HERE / 'manifest-2026-10-06-10-12.json').read_text())['item_ids']
    seen_before = set(json.loads((HERE / 'exposed-2026-10-06-10-12.json').read_text())['seen_before'])

    # 1. the set-aside folders, file by file
    shown, code_only_files, shown_files = collections.defaultdict(list), collections.Counter(), collections.Counter()
    for article, paths in census['sent_articles'].items():
        for path in paths:
            if not path.startswith(source_work):
                continue
            if Path(path).name in CODE_ONLY:
                code_only_files[path] += 1
            else:
                shown_files[path] += 1
                shown[article].append(path)
    flagged = {article: paths for article, paths in shown.items() if article not in seen_before}
    trace = sqlite3.connect(f"file:{ROOT / 'poc/data/clean-step1-full-page-diagnostic-2026-11-07/trace.sqlite'}?mode=ro", uri=True)
    requests = ' '.join(row[0] or '' for row in trace.execute('select request from attempt'))
    in_full_page_trace = [article for article in manifest if article in requests]

    # 2. the same article under another id
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    by_hash, by_text, by_title = collections.defaultdict(set), collections.defaultdict(set), collections.defaultdict(set)
    week_rows = {}
    for input_id, content_hash, title, text in items.execute('select input_id, content_sha256, title, text from items'):
        text_key = hashlib.sha256(normalised(text).encode()).hexdigest() if (text or '').strip() else None
        title_key = normalised(title) if len(normalised(title)) >= 25 else None
        if content_hash:
            by_hash[content_hash].add(input_id)
        if text_key:
            by_text[text_key].add(input_id)
        if title_key:
            by_title[title_key].add(input_id)
        if input_id in set(manifest):
            week_rows[input_id] = (content_hash, text_key, title_key)
    twins = {}
    for article, (content_hash, text_key, title_key) in week_rows.items():
        others = {}
        for label, index, key in (('same stored content hash', by_hash, content_hash), ('same text', by_text, text_key), ('same title', by_title, title_key)):
            for other in (index.get(key, set()) if key else set()) - {article}:
                others.setdefault(other, []).append(label)
        if others:
            twins[article] = others
    other_ids = sorted({other for others in twins.values() for other in others})
    wanted = {other.encode() for other in other_ids}
    prefixes = sorted({other.split(':', 1)[0] for other in other_ids}) or ['gnews']
    shape = re.compile(b'(?:' + b'|'.join(re.escape(prefix.encode()) for prefix in prefixes) + rb'):[0-9A-Za-z_\-\.]{6,120}')
    found = collections.defaultdict(set)
    not_a_send = ('poc/data/items-', '.page.sqlite', 'docs/research/2026-11-14-use-acceptance/second-week/', 'fresh-week-manifest.json', 'docs/research/2026-11-14-use-acceptance/fresh-articles-2026-09-22-10-05')
    for folder in SEARCHED:
        for path in (ROOT / folder).rglob('*'):
            relative = str(path.relative_to(ROOT))
            if not path.is_file() or path.is_symlink() or path.stat().st_size == 0 or any(mark in relative for mark in not_a_send):
                continue
            if relative.startswith(source_work) and path.name in CODE_ONLY:
                continue
            with open(path, 'rb') as handle, mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as data:
                for match in shape.finditer(data):
                    if match.group(0) in wanted:
                        found[match.group(0).decode()].add(relative)
    twin_exposed = {}
    for article, others in twins.items():
        hits = {other: {'why': labels, 'seen_in': sorted(found[other])[:6]} for other, labels in others.items() if found[other]}
        if hits and article not in seen_before:
            twin_exposed[article] = hits
    out = {'week': WEEK, 'articles': len(manifest), 'seen_before': len(seen_before),
           'set_aside_files_code_only': dict(code_only_files), 'set_aside_files_given_to_a_model_or_reader': dict(shown_files),
           'in_the_full_page_diagnostic_model_trace': in_full_page_trace,
           'flagged_shown_in_source_page_review': flagged,
           'articles_with_a_twin_under_another_id': len(twins), 'twin_ids': len(other_ids),
           'flagged_twin_seen_before': twin_exposed}
    (HERE / 'exposure-bounds.json').write_text(json.dumps(out, indent=1) + '\n')
    print(f"week {WEEK}: {len(manifest)} articles; seen before {len(seen_before)}")
    print(f"set-aside files holding a week id: code-only {len(code_only_files)}, given to a model or reader {len(shown_files)}: {dict(shown_files)}")
    print(f"in the full-page diagnostic's model requests: {len(in_full_page_trace)}")
    print(f"flagged, shown in a source-page review and not already seen-before: {len(flagged)}")
    print(f"articles with a twin under another id: {len(twins)} ({len(other_ids)} other ids); of the not-seen-before articles, with a twin in an earlier run, probe, packet or transcript: {len(twin_exposed)}")
    for article, hits in list(twin_exposed.items())[:8]:
        print('   ', article, json.dumps(hits)[:260])


if __name__ == '__main__':
    main()
