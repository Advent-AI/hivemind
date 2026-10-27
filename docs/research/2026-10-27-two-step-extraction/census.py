"""The numbers in design.md §2 and §5, over the cleaned NVDA window (D256): pages, paragraphs, mandatory paragraphs under
the reading rule (a digit, a month name or 120+ characters), reading chunks of READ_CHUNK mandatory paragraphs, sentence
counts with the abbreviation guard, sentences broken across lines, and the output-token estimate per chunk.
Run: python3 census.py [items db]"""
import re
import sqlite3
import sys

READ_CHUNK = 40
TOKENS_PER_STATEMENT, TOKENS_PER_SKIP, REASONING = 80, 15, 1000
MONTH = re.compile(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b')
SPLIT = re.compile(r'(?<=[.!?])\s+(?=[“"A-Z])')
ABBREVIATION = re.compile(r'\b(U\.S|U\.K|Inc|Corp|Co|Ltd|Mr|Mrs|Ms|Dr|Jr|Sr|vs|e\.g|i\.e|No|St|Fig|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.$')
END = re.compile(r'[.!?:"”’)\]]$')


def mandatory(paragraph):
    return bool(re.search(r'\d', paragraph) or MONTH.search(paragraph) or len(paragraph) >= 120)


def sentences(paragraph):
    merged = []
    for part in SPLIT.split(paragraph):
        if merged and ABBREVIATION.search(merged[-1]):
            merged[-1] += ' ' + part
        else:
            merged.append(part)
    return merged


def quantiles(values):
    values = sorted(values)
    n = len(values)
    return f'median {values[n // 2]} p90 {values[int(n * .9)]} p99 {values[int(n * .99)]} max {values[-1]}'


def main(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    rows = conn.execute("select text, category, max_output_tokens from items join (select 'T7' c, 8000 max_output_tokens union select 'T8', 8000 union select 'T6', 12000 union select 'T1', 16000 union select 'T2', 16000 union select 'T3', 12000 union select 'T4', 16000 union select 'T10', 12000 union select 'T11', 12000) caps on caps.c = items.category "
                        "where feed=1 and (copy_of is null or copy_of in ('', 'None')) and object_identifiers like '%\"NVDA\"%' and publication_day between '2026-07-01' and '2026-10-27'").fetchall()
    chars, paragraphs, mandatories, chunks, over_cap_single, breaks_pages = [], [], [], [], 0, 0
    naive = guarded = 0
    for text, category, cap in rows:
        lines = [line for line in text.split('\n') if line.strip()]
        m = sum(1 for line in lines if mandatory(line))
        chars.append(len(text)); paragraphs.append(len(lines)); mandatories.append(m)
        chunks.append(max(1, -(-m // READ_CHUNK)))
        over_cap_single += m * TOKENS_PER_STATEMENT + REASONING > cap          # one call for the whole page
        for line in lines:
            parts = SPLIT.split(line); naive += len(parts); guarded += len(sentences(line))
        breaks_pages += any(len(a) >= 60 and not END.search(a) and b[:1].islower() for a, b in zip(lines, lines[1:]))
    print(f'fed NVDA items (non-copy) {len(rows)}')
    print(f'characters      {quantiles(chars)}')
    print(f'paragraphs      {quantiles(paragraphs)}')
    print(f'mandatory       {quantiles(mandatories)}')
    print(f'reading chunks of {READ_CHUNK}: {quantiles(chunks)}; items needing more than one chunk: {sum(1 for c in chunks if c > 1)}')
    print(f'items whose single-call reading estimate ({TOKENS_PER_STATEMENT}/statement + {REASONING} reasoning) exceeds the category cap: {over_cap_single}')
    print(f'chunk estimate at one statement per mandatory line: {READ_CHUNK * TOKENS_PER_STATEMENT + REASONING} tokens, under every cap (8,000 at T7/T8)')
    print(f'sentences: naive split {naive:,}; with the abbreviation guard {guarded:,}')
    print(f'pages with a sentence broken across lines (heuristic): {breaks_pages} ({breaks_pages / len(rows):.1%})')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite')
