"""D1 of the loop's ruler (README.md): the gold's must_open and may_open questions (golden-v5, the questions part, the frozen ruler's piece 2)
against the questions a finished run's ledger holds: a gold question counts as opened when a view's question and focus share enough words
with its gist (score_ref.same_question, the same test the 2026-10-31 arms used). Prints, per run folder, must_open and may_open covered,
how many of those are covered by a seed against by an article-opened question, and the article-opened questions with their creator
item, so duplicates can be read by a person. $0, read-only, finished folders only.

    python3 question_recall.py <run folder> [<run folder> ...]
"""
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'docs/research/2026-10-31-reference-context'), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402


def gold_questions():
    out = []
    for a in sr.articles:
        for kind in ('must_open', 'may_open'):
            for gq in a.get('questions', {}).get(kind, []):
                out.append((kind, a['input_id'], a.get('title', '')[:60], gq['gist']))
    return out


def main():
    gold = gold_questions()
    for run in sys.argv[1:]:
        views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); views.row_factory = sqlite3.Row
        rows = [dict(r) for r in views.execute('select view_id, kind, object_id, looks_at, question, created_seq, created_from_input from views order by created_seq')]
        covered = {'must_open': [0, 0, 0], 'may_open': [0, 0, 0]}        # [any, by a seed, by an article-opened question]
        misses = {'must_open': [], 'may_open': []}
        for kind, iid, title, gist in gold:
            hits = [v for v in rows if sr.same_question(gist, v['question'] + ' ' + (v['looks_at'] or ''))]
            if hits:
                covered[kind][0] += 1
                covered[kind][1] += any(v['created_seq'] == 0 for v in hits)
                covered[kind][2] += any(v['created_seq'] > 0 for v in hits)
            else:
                misses[kind].append((iid, title, gist))
        total = {k: sum(1 for g in gold if g[0] == k) for k in covered}
        opened = [v for v in rows if v['created_seq'] > 0]
        print(f'\n== {run}: views {len(rows)} (seeds {len(rows) - len(opened)}, article-opened {len(opened)})')
        for kind in ('must_open', 'may_open'):
            c = covered[kind]
            print(f'   {kind}: covered {c[0]}/{total[kind]} (by a seed {c[1]}, by an article-opened question {c[2]})')
        for iid, title, gist in misses['must_open']:
            print(f'   must_open missed: {gist[:100]} | {title}')
        for v in opened:
            print(f"   opened {v['view_id']} ({v['kind']} {v['object_id']}, seq {v['created_seq']}, by {v['created_from_input'][:30]}): {v['question'][:100]}")


if __name__ == '__main__':
    main()
