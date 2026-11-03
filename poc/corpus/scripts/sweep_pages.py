"""Sweep every remaining line of the fed articles in a cleaned database and census what still looks like junk.

Reports, over all fed, non-copy article pages in the window (dispatch merges copies, which are never read): the share of characters in lines matching a broad junk keyword list
(a census, wider than the removal rule: it includes words that also occur in prose), the share in unpunctuated short
lines, runs of such lines, the most frequent remaining lines across pages, and the keyword counts with examples.

Usage: python3 poc/corpus/scripts/sweep_pages.py --db poc/data/items-nvda-2026-07-01-10-27.sqlite --from 2026-07-01 --until 2026-10-27
"""
import argparse
import collections
import re
import sqlite3

END = re.compile(r'[.!?:"”’)\]]$')
KEYWORDS = re.compile(r"(sign up|subscribe|newsletter|privacy policy|cookie|all rights reserved|getty images|read more|most read|most popular"
                      r"|trending|the motley fool has|stock advisor|advertisement|sponsored|click here|follow us|share this|leave a comment"
                      r"|terms of (?:service|use)|©|copyright|image credit|photo:|photo by|credit:|you may also like|more from|watch now"
                      r"|download the app|log in|sign in|free trial|editor's picks|top stories|latest news|breaking news|min read|hours? ago)", re.I)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', required=True); parser.add_argument('--from', dest='from_day', required=True); parser.add_argument('--until', required=True)
    args = parser.parse_args()
    conn = sqlite3.connect(f'file:{args.db}?mode=ro', uri=True); conn.row_factory = sqlite3.Row
    rows = conn.execute("select input_id, publisher, text from items where feed=1 and document_format='article' and (copy_of is null or copy_of in ('', 'None')) and publication_day between ? and ?", (args.from_day, args.until)).fetchall()
    line_pages = collections.Counter(); pages_with = collections.Counter(); examples = collections.defaultdict(list)
    total_lines = total_chars = key_lines = key_chars = short_lines = short_chars = runs = run_lines = 0
    for r in rows:
        lines = r['text'].split('\n'); total_lines += len(lines); total_chars += sum(map(len, lines))
        for line in set(lines):
            line_pages[line] += 1
        run = 0
        for line in lines + ['END.']:
            m = KEYWORDS.search(line)
            if m:
                key_lines += 1; key_chars += len(line); k = m.group(1).lower(); pages_with[k] += 1
                if len(examples[k]) < 2: examples[k].append(line[:100])
            short = len(line) <= 110 and not END.search(line) and not line.startswith('By ')
            if short:
                short_lines += 1; short_chars += len(line); run += 1
            else:
                if run >= 3: runs += 1; run_lines += run
                run = 0
    print(f'fed articles {len(rows):,}; lines {total_lines:,}; chars {total_chars:,}')
    print(f'lines with a junk keyword (broad census): {key_lines:,} = {key_chars / total_chars:.1%} of chars')
    print(f'unpunctuated lines of at most 110 chars: {short_lines:,} = {short_chars / total_chars:.1%} of chars; runs of 3+: {runs:,} ({run_lines:,} lines)')
    print('most frequent remaining lines (pages):')
    for line, n in line_pages.most_common(20):
        print(f'  {n:5} | {line[:110]}')
    print('keyword census (pages, examples):')
    for k, n in pages_with.most_common(30):
        print(f'  {n:5} {k:20} | ' + ' || '.join(examples[k]))


if __name__ == '__main__':
    main()
