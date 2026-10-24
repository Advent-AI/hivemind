"""Probe DeepSeek's Search and Fetch APIs (api-docs.deepseek.com/guides/search) on a few samples and print what
they return: how many results per day-bounded query, their dates and sites, whether `content` is the article text
or a summary, and whether Fetch reaches pages our own fetcher could not. The key is read from the owner-only
credentials file, never passed on the command line. Raw responses are saved to the scratchpad directory given as
the first argument. Nothing here writes into the corpus.
"""
import json
import os
import sys
import time
import urllib.request

SEARCH = 'https://api.deepseek.com/v1/tools/search'
FETCH = 'https://api.deepseek.com/v1/tools/fetch'
CREDENTIALS = os.path.expanduser('~/.config/tn-hivemind/credentials.json')


def key():
    return json.load(open(CREDENTIALS))['DEEPSEEK_API_KEY']


def call(url, payload, api_key):
    request = urllib.request.Request(url, data=json.dumps(payload).encode(), method='POST',
                                     headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'})
    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, json.loads(response.read().decode('utf-8', 'ignore')), round(time.time() - started, 1)
    except urllib.error.HTTPError as error:
        return error.code, {'error': error.read().decode('utf-8', 'ignore')[:500]}, round(time.time() - started, 1)


def describe_search(name, payload, data):
    results = data.get('results') or data.get('data') or []
    if isinstance(data, dict) and not results:
        print(f'  [{name}] no results field; keys: {list(data)[:8]}; body: {json.dumps(data)[:300]}')
        return
    print(f'  [{name}] {len(results)} results; top-level keys {sorted(data.keys())}')
    for r in results[:8]:
        content = r.get('content') or ''
        print(f'    {str(r.get("date"))[:10]} | {r.get("site_name") or ""[:18]:18s} | auth {r.get("authority")} | rank {r.get("rerank_score")} | '
              f'content {len(content):6d} chars | summary {len(r.get("summary") or ""):4d} | {str(r.get("title"))[:70]}')
        print(f'      {r.get("url")[:110]}')
    dates = sorted(str(r.get('date'))[:10] for r in results)
    print(f'    date range {dates[0] if dates else "-"} .. {dates[-1] if dates else "-"}; with content: {sum(1 for r in results if r.get("content"))}')


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    api_key = key()
    samples = [
        ('nvda-earnings-day', {'query': 'nvidia after:2026-08-26 before:2026-08-28', 'count': 50, 'need_content': True}),
        ('nvda-quiet-day', {'query': 'nvidia after:2026-09-14 before:2026-09-15', 'count': 50, 'need_content': False}),
        ('export-controls', {'query': 'nvidia H200 China export after:2026-08-17 before:2026-08-21', 'count': 30, 'need_content': True}),
        ('server-price-hike', {'query': 'nvidia AI server price increase 15% after:2026-08-21 before:2026-08-24', 'count': 20, 'need_content': True}),
        ('site-reuters', {'query': 'nvidia site:reuters.com after:2026-08-01 before:2026-08-31', 'count': 30, 'need_content': True}),
        ('fed-fomc', {'query': 'FOMC statement federal funds rate after:2026-09-15 before:2026-09-18', 'count': 20, 'need_content': False}),
    ]
    for name, payload in samples:
        status, data, seconds = call(SEARCH, payload, api_key)
        json.dump({'payload': payload, 'status': status, 'seconds': seconds, 'data': data}, open(os.path.join(out, f'search-{name}.json'), 'w'), ensure_ascii=False, indent=1)
        print(f'SEARCH {name}: status {status}, {seconds}s')
        if status == 200:
            describe_search(name, payload, data)
        else:
            print('  ', data)
        time.sleep(0.5)
    fetches = [
        ('cnbc-open', 'https://www.cnbc.com/2026/08/27/nvidia-earnings-stock-reaction.html'),
        ('benzinga-blocked-for-us', 'https://www.benzinga.com/markets/tech/26/07/60686864/nvidia-openai-data-center-financing-michael-burry'),
        ('bloomberg-paywall', 'https://www.bloomberg.com/news/articles/2026-08-22/nvidia-customers-notified-about-ai-related-price-hikes-above-15'),
        ('reuters-401-for-us', 'https://www.reuters.com/technology/nvidia-h200-chips-reach-china-small-shipments-ft-reports-2026-08-18/'),
        ('sec-10q', 'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm'),
        ('nvidia-newsroom', 'https://nvidianews.nvidia.com/news/nvidia-announces-a-150-billion-share-repurchase-authorization-increase'),
    ]
    for name, url in fetches:
        status, data, seconds = call(FETCH, {'url': url}, api_key)
        json.dump({'url': url, 'status': status, 'seconds': seconds, 'data': data}, open(os.path.join(out, f'fetch-{name}.json'), 'w'), ensure_ascii=False, indent=1)
        content = (data.get('content') or '') if isinstance(data, dict) else ''
        print(f'FETCH {name}: status {status}, {seconds}s, title {str(data.get("title") if isinstance(data, dict) else "")[:60]!r}, content {len(content)} chars')
        if content:
            print('   head:', content[:240].replace('\n', ' '))
        elif isinstance(data, dict):
            print('   body:', json.dumps(data)[:300])
        time.sleep(0.5)


if __name__ == '__main__':
    main()
