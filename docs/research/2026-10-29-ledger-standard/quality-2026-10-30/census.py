"""Field census over what production keeps from role-v51's answers (run P, three draws, 148 articles), at no cost:
dates, numbers in the summary line absent from the quote, tiers, duplicates within one answer, statement and question counts
per article, draw-to-draw agreement, and code drops by reason.

    python3 census.py
"""
import collections
import json
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402

DRAWS = ['P-v51-d1', 'P-v51-d2', 'P-v51-d3']


def numbers(text):
    """Number tokens as written (1.5, 40,000 -> 40000, 82%) for a containment check; years are kept."""
    return {n.replace(',', '') for n in re.findall(r'\d[\d,]*\.?\d*', text or '') if n.strip(',.')}


def main():
    dev = json.load(open(HERE.parent / 'golden-v3/golden-v3-signed.json'))['articles']
    test = json.load(open(HERE.parent / 'test-set/golden-test-signed.json'))['articles']
    gold = {a['input_id']: a for a in dev + test}
    runs = {tag: sg.answers(tag) for tag in DRAWS}
    c = collections.Counter()
    per_article = collections.defaultdict(list)
    q_per_article = collections.defaultdict(list)
    drop_reasons = collections.Counter()
    examples = collections.defaultdict(list)
    agree = []
    for iid, a in gold.items():
        pub = a.get('publication_day')
        quotes_by_draw = []
        for tag in DRAWS:
            s = sg.kept(runs[tag].get(iid), iid)
            if s is None:
                c['unusable'] += 1
                continue
            per_article[iid].append(len(s['evidence']))
            q_per_article[iid].append(len(s['candidates']))
            for d in s['dropped']:
                drop_reasons[str(d[1])[:70] if len(d) > 1 else '?'] += 1
            seen = []
            for e in s['evidence']:
                c['statements'] += 1
                day = e.get('original_day') or ''
                if not day or day.lower() in ('unknown', 'null', 'none'):
                    c['day unknown'] += 1
                elif day == pub:
                    c['day = publication day'] += 1
                elif day > (pub or ''):
                    c['day after publication'] += 1
                    examples['day after publication'].append((iid, e['quote'][:90], day, pub))
                else:
                    c['day before publication'] += 1
                c[f'tier {e.get("tier")}'] += 1
                extra = numbers(e['one_line']) - numbers(e['quote'])
                extra = {n for n in extra if not re.fullmatch(r'20\d\d', n)}
                if extra:
                    c['one_line has a number not in the quote (years ignored)'] += 1
                    examples['number not in quote'].append((iid, e['quote'][:110], e['one_line'][:110], sorted(extra)))
                w = sg.words(e['quote'])
                if any(len(w & x) >= 0.8 * min(len(w), len(x)) for x in seen if w and x):
                    c['near-duplicate quote within one answer'] += 1
                    examples['duplicate'].append((iid, e['quote'][:100]))
                seen.append(w)
            quotes_by_draw.append({sg.norm(e['quote']) for e in s['evidence']})
        if len(quotes_by_draw) == 3:
            union = set().union(*quotes_by_draw)
            if union:
                inter = set.intersection(*quotes_by_draw)
                agree.append(len(inter) / len(union))
    counts = [statistics.mean(v) for v in per_article.values()]
    out = {
        'articles': len(gold), 'draws': len(DRAWS),
        'counts': dict(c),
        'statements per article (mean over draws): median, p90, max': [statistics.median(counts), sorted(counts)[int(0.9 * len(counts))], max(counts)],
        'articles with 0 statements in every draw': sum(1 for v in per_article.values() if max(v) == 0),
        'articles with statements in some draws and 0 in others': sum(1 for v in per_article.values() if max(v) > 0 and min(v) == 0),
        'articles with a question in some draw': sum(1 for v in q_per_article.values() if max(v) > 0),
        'articles whose question count differs across draws': sum(1 for v in q_per_article.values() if len(set(v)) > 1),
        'same quotes in all three draws / quotes in any draw (median over articles with any)': statistics.median(agree),
        'mean of that share': statistics.mean(agree),
        'drop reasons': drop_reasons.most_common(12),
    }
    (HERE / 'census.json').write_text(json.dumps({'summary': out, 'examples': {k: v[:40] for k, v in examples.items()}}, ensure_ascii=False, indent=1) + '\n')
    print(json.dumps(out, ensure_ascii=False, indent=1))
    for k, v in examples.items():
        print('##', k, len(v))
        for x in v[:12]:
            print('  ', x)


if __name__ == '__main__':
    main()
