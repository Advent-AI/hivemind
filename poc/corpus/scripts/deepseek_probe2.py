"""Second DeepSeek probe: recall with lang:en and different phrasings, a major-outlet site list, and whether the
search `content` field and the Fetch Markdown are the article text (compared with our own fetch of the same page).
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from deepseek_probe import SEARCH, FETCH, key, call, describe_search  # noqa: E402
from common import fetch, decode, page_text  # noqa: E402


def overlap(a, b):
    """Share of 12-word shingles of a that also appear in b: 1.0 means a is contained in b."""
    def shingles(text):
        words = re.findall(r'\w+', text.lower())
        return {' '.join(words[i:i + 12]) for i in range(max(0, len(words) - 11))}
    sa, sb = shingles(a), shingles(b)
    return round(len(sa & sb) / max(1, len(sa)), 2), len(sa), len(sb)


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    api_key = key()
    samples = [
        ('plain-lang-en', {'query': 'nvidia lang:en after:2026-08-26 before:2026-08-28', 'count': 50, 'need_content': False}),
        ('earnings-lang-en', {'query': 'nvidia earnings lang:en after:2026-08-26 before:2026-08-28', 'count': 50, 'need_content': False}),
        ('stock-quiet-day', {'query': 'nvidia stock lang:en after:2026-09-14 before:2026-09-15', 'count': 50, 'need_content': False}),
        ('majors-site-list', {'query': 'nvidia site:reuters.com OR site:cnbc.com OR site:wsj.com OR site:bloomberg.com OR site:ft.com after:2026-08-26 before:2026-08-28', 'count': 50, 'need_content': False}),
        ('ori-question', {'query': 'nvidia Q2 results data center revenue lang:en after:2026-08-26 before:2026-08-28', 'count': 50, 'need_content': False, 'ori_question': 'What did Nvidia report for its second quarter and how did the stock react?'}),
        ('theme-capex', {'query': 'Microsoft capital expenditures AI data centers lang:en after:2026-07-29 before:2026-07-31', 'count': 30, 'need_content': True}),
        ('tsmc-monthly', {'query': 'TSMC monthly revenue lang:en after:2026-08-10 before:2026-08-12', 'count': 30, 'need_content': True}),
    ]
    for name, payload in samples:
        status, data, seconds = call(SEARCH, payload, api_key)
        json.dump({'payload': payload, 'status': status, 'seconds': seconds, 'data': data}, open(os.path.join(out, f'search2-{name}.json'), 'w'), ensure_ascii=False, indent=1)
        print(f'SEARCH {name}: status {status}, {seconds}s')
        if status == 200:
            describe_search(name, payload, data)
        else:
            print('  ', data)
        time.sleep(0.4)
    # fidelity: compare DeepSeek content with our own fetch of the same page
    checks = []
    data = json.load(open(os.path.join(out, 'search2-theme-capex.json')))['data']
    for r in (data.get('results') or [])[:6]:
        if r.get('content') and len(r['content']) > 1500:
            checks.append(('search-content', r['url'], r['content']))
    data = json.load(open(os.path.join(out, 'search2-tsmc-monthly.json')))['data']
    for r in (data.get('results') or [])[:6]:
        if r.get('content') and len(r['content']) > 1500:
            checks.append(('search-content', r['url'], r['content']))
    for kind, url, theirs in checks[:5]:
        status, _, body = fetch(url, timeout=30, retries=0)
        ours = page_text(decode(body)) if status == 200 and body else ''
        share, n_theirs, n_ours = overlap(theirs, ours) if ours else ('-', 0, 0)
        print(f'FIDELITY {kind}: our fetch status {status}, ours {len(ours)} chars, theirs {len(theirs)} chars, '
              f'theirs-in-ours {share} ({n_theirs} shingles) | {url[:90]}')
    # fetch fidelity on a page we hold: the newsroom release
    status, data, seconds = call(FETCH, {'url': 'https://nvidianews.nvidia.com/news/nvidia-announces-a-150-billion-share-repurchase-authorization-increase'}, api_key)
    theirs = (data.get('content') or '').replace('\\', '') if isinstance(data, dict) else ''
    path = None
    for name in os.listdir('/Users/lchingen/hivemind/poc/corpus/raw/nvidianews'):
        if 'share-repurchase' in name and name.endswith('.full.txt'):
            path = os.path.join('/Users/lchingen/hivemind/poc/corpus/raw/nvidianews', name)
    ours = open(path, encoding='utf-8').read() if path else ''
    print(f'FIDELITY fetch newsroom: theirs {len(theirs)} chars, ours {len(ours)} chars, theirs-in-ours {overlap(theirs, ours)[0] if ours else "-"}, ours-in-theirs {overlap(ours, theirs)[0] if ours else "-"}')


if __name__ == '__main__':
    main()
