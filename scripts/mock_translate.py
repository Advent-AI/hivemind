"""Translate the mock's data (poc/mock/data.json, written by the pipeline in Chinese) into English for the
front-end mock, with gpt-6-luna through the same archived model call as the pipeline (a repeated run costs $0).

Enumerations are mapped, not translated (tiers, view kinds, object ladder labels, judgement pushes). Everything
else that the page shows is translated in batches: view questions and what they look at, ladder conditions,
evidence one-liners and event times, each judgement's reasons and why-changed. Quotes, speakers, titles and dates
stay as stored (quotes are the source's own words, almost all English). The Chinese ladder conditions are kept
as `condition_zh` because the page reads the rung thresholds from them.

Usage: python3 scripts/mock_translate.py [--dry] [--limit N]   → poc/mock/data.en.json
"""
import argparse
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, model  # noqa: E402

TIERS = {'发生的事': 'Fact', '当事人说的': 'Party statement', '第三方看法': 'Third-party view', '传闻': 'Rumour'}
KINDS = {'对象观点': 'Company view', '主题观点': 'Theme view'}
OBJECT_LABELS = {'强烈看多': 'Strongly bullish', '看多': 'Bullish', '中性': 'Neutral', '看空': 'Bearish', '强烈看空': 'Strongly bearish', '是': 'Yes', '否': 'No'}
PUSHES = {'推向第一格': 'pushes toward rung 1', '推向最后一格': 'pushes toward rung 5', '不推': 'no push', '定格': 'settles the rung'}
SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['items'],
          'properties': {'items': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['k', 'en'],
                                                             'properties': {'k': {'type': 'string'}, 'en': {'type': 'string'}}}}}}
SYSTEM = ('You translate short Chinese texts from an equity-research system into concise, natural financial English. '
          'Keep every number, unit, ticker, company and product name, fiscal label (FY2027, Q1, H2) and date exactly as given. '
          'Write 第 N 格 as "rung N" and 梯子 as "ladder"; 观点 is "view", 证据 is "evidence", 发生的事 is "a fact", 当事人说的 is "a party statement", '
          '第三方看法 is "a third-party view", 传闻 is "a rumour". Translate questions as questions. Return one English text per key, every key, nothing else.')
BATCH_CHARS = 5000


def collect(data):
    """Every distinct string the page shows, keyed by a stable id -> the original text."""
    todo = collections.OrderedDict()

    def add(key, text):
        if text and text.strip():
            todo[key] = text
    for v in data['views']:
        add(f'v:{v["view_id"]}:q', v['question'])
        add(f'v:{v["view_id"]}:l', v['looks_at'])
        for r in v['rungs']:
            add(f'v:{v["view_id"]}:c{r["position"]}', r['condition'])
            if r['label'] not in OBJECT_LABELS:
                add(f'v:{v["view_id"]}:r{r["position"]}', r['label'])
        for n, j in enumerate(v['judgements']):
            add(f'j:{v["view_id"]}:{n}:why', j['why_changed'])
            add(f'j:{v["view_id"]}:{n}:reasons', j['reasons'])
        for e in v['evidence']:
            add(f'e:{e["id"]}:line', e['one_line'])
            add(f'e:{e["id"]}:time', e['event_time'])
    return todo


def batches(todo, done):
    batch, size = [], 0
    for key, text in todo.items():
        if key in done:
            continue
        if batch and size + len(text) > BATCH_CHARS:
            yield batch
            batch, size = [], 0
        batch.append((key, text))
        size += len(text)
    if batch:
        yield batch


CJK = re.compile(r'[一-鿿]')
MONTHS = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def polish(text):
    """Money and dates the model copied in Chinese units ("300亿美元", "2026年8月26日") written the English way; a
    literal "3500 hundred million" becomes "$350 billion"."""
    def yi_to_dollars(match):
        n = float(match.group(1).replace(',', ''))
        return f'${n / 10:g} billion'
    text = re.sub(r'(\d[\d,.]*)\s*万亿美元', lambda m: f'${float(m.group(1).replace(",", "")):g} trillion', text)
    text = re.sub(r'(\d[\d,.]*)\s*亿美元', yi_to_dollars, text)
    text = re.sub(r'\$?(\d[\d,.]*)\s*hundred million(?: U\.S\. dollars| dollars)?', yi_to_dollars, text)
    text = re.sub(r'(\d[\d,.]*)\s*万亿', lambda m: f'{float(m.group(1).replace(",", "")):g} trillion', text)
    text = re.sub(r'(\d[\d,.]*)\s*亿', lambda m: f'{float(m.group(1).replace(",", "")) / 10:g} billion', text)
    text = re.sub(r'(\d[\d,.]*)\s*美元', r'$\1', text)
    text = re.sub(r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日', lambda m: f'{MONTHS[int(m.group(2))]} {int(m.group(3))}, {m.group(1)}', text)
    text = re.sub(r'(\d{4})\s*年\s*(\d{1,2})\s*月', lambda m: f'{MONTHS[int(m.group(2))]} {m.group(1)}', text)
    text = re.sub(r'(\d{1,2})\s*月\s*(\d{1,2})\s*日', lambda m: f'{MONTHS[int(m.group(1))]} {int(m.group(2))}', text)
    text = re.sub(r'(\d{4})\s*年', r'\1', text)
    text = re.sub(r'第\s*([一二三四1-4])\s*季度?', lambda m: 'Q' + str('一二三四'.find(m.group(1)) + 1 if m.group(1) in '一二三四' else m.group(1)), text)
    text = re.sub(r'(\d[\d,.]*)\s*%\s*', r'\1% ', text)
    return re.sub(r'\s{2,}', ' ', text).strip()


FIX_SYSTEM = SYSTEM + ' The output must contain no Chinese characters at all: write money as $X billion or $X trillion (1亿 = $0.1 billion), dates as "Aug 26, 2026", quarters as Q1..Q4.'


def apply(data, done):
    done = {k: polish(v) for k, v in done.items()}
    out = json.loads(json.dumps(data))
    for v in out['views']:
        v['question'] = done.get(f'v:{v["view_id"]}:q', v['question'])
        v['looks_at'] = done.get(f'v:{v["view_id"]}:l', v['looks_at'])
        v['kind'] = KINDS.get(v['kind'], v['kind'])
        for r in v['rungs']:
            r['condition_zh'] = r['condition']
            r['condition'] = done.get(f'v:{v["view_id"]}:c{r["position"]}', r['condition'])
            r['label'] = OBJECT_LABELS.get(r['label'], done.get(f'v:{v["view_id"]}:r{r["position"]}', r['label']))
        for n, j in enumerate(v['judgements']):
            j['why_changed'] = done.get(f'j:{v["view_id"]}:{n}:why', j['why_changed'])
            j['reasons'] = done.get(f'j:{v["view_id"]}:{n}:reasons', j['reasons'])
            for p in j['pushes']:
                p['push'] = PUSHES.get(p['push'], p['push'])
        for e in v['evidence']:
            e['one_line'] = done.get(f'e:{e["id"]}:line', e['one_line'])
            e['event_time'] = done.get(f'e:{e["id"]}:time', e['event_time'])
            e['tier'] = TIERS.get(e['tier'], e['tier'])
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default=os.path.join(ROOT, 'poc', 'mock', 'data.json'))
    parser.add_argument('--out', default=os.path.join(ROOT, 'poc', 'mock', 'data.en.json'))
    parser.add_argument('--cache', default=os.path.join(ROOT, 'poc', 'mock', 'translations.json'), help='key -> English, kept between runs')
    parser.add_argument('--config', default=os.path.join(ROOT, 'poc', 'config', 'poc-v2.json'))
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'archive.sqlite'))
    parser.add_argument('--dry', action='store_true')
    parser.add_argument('--limit', type=int, default=0, help='stop after N batches')
    parser.add_argument('--shard', default='', help='k/n: this process takes every n-th batch starting at k and writes its own cache file')
    args = parser.parse_args()
    with open(args.data, encoding='utf-8') as handle:
        data = json.load(handle)
    todo = collect(data)
    # every cache file in the folder counts (one per shard), so a merge is just reading them all
    done = {}
    for path in sorted(glob.glob(os.path.join(os.path.dirname(args.cache), 'translations*.json'))):
        done.update(json.load(open(path, encoding='utf-8')))
    shard_k, shard_n = (int(x) for x in args.shard.split('/')) if args.shard else (0, 1)
    if args.shard:
        args.cache = args.cache.replace('.json', f'.shard-{shard_k}.json')
    own = json.load(open(args.cache, encoding='utf-8')) if os.path.exists(args.cache) else {}
    pushes = collections.Counter(p['push'] for v in data['views'] for j in v['judgements'] for p in j['pushes'])
    unknown_pushes = [p for p in pushes if p not in PUSHES]
    print(f'{len(todo)} strings, {sum(len(t) for t in todo.values()):,} chars; cached {sum(1 for k in todo if k in done)}; pushes {dict(pushes)}'
          + (f'; UNMAPPED pushes {unknown_pushes}' if unknown_pushes else ''))
    if args.dry:
        return
    cfg = config.load(args.config)
    setting = config.Setting(name='translate', model='gpt-6-luna', prompt_version='translate-v1', temperature=0.2, reasoning_effort='low', max_output_tokens=16000)
    archive = model.Archive(args.archive)
    cost = 0.0
    for n, batch in enumerate(batches(todo, done), 1):
        if args.limit and n > args.limit:
            break
        if (n - 1) % shard_n != shard_k:
            continue
        user = 'Translate each item. Keys:\n' + json.dumps([{'k': k, 'zh': t} for k, t in batch], ensure_ascii=False)
        answer = model.call(archive, cfg, setting, SYSTEM, user, SCHEMA, 'translation', 'translate')
        cost += answer.cost_usd
        got = {item['k']: item['en'] for item in answer.data['items']}
        missing = [k for k, _ in batch if k not in got]
        for k, en in got.items():
            if k in todo:
                done[k] = en
                own[k] = en
        with open(args.cache, 'w', encoding='utf-8') as handle:
            json.dump(own, handle, ensure_ascii=False, indent=0)
        print(f'batch {n}: {len(batch)} strings, {len(got)} back, {len(missing)} missing, ${answer.cost_usd:.3f}{" (cached)" if answer.cached else ""}', flush=True)
    # second pass: anything still carrying Chinese after the polish goes back with the stricter instruction
    if not args.shard and not args.limit:
        leftover = [(k, todo[k]) for k in todo if k in done and CJK.search(polish(done[k]))]
        print(f'fix pass: {len(leftover)} strings still carry Chinese after polishing')
        for n, batch in enumerate([leftover[i:i + 40] for i in range(0, len(leftover), 40)], 1):
            user = 'Translate each item. Keys:\n' + json.dumps([{'k': k, 'zh': t} for k, t in batch], ensure_ascii=False)
            answer = model.call(archive, cfg, setting, FIX_SYSTEM, user, SCHEMA, 'translation', 'translate')
            cost += answer.cost_usd
            for item in answer.data['items']:
                if item['k'] in todo and not CJK.search(polish(item['en'])):
                    done[item['k']] = item['en']; own[item['k']] = item['en']
            with open(args.cache, 'w', encoding='utf-8') as handle:
                json.dump(own, handle, ensure_ascii=False, indent=0)
            print(f'fix batch {n}: {len(batch)} strings, ${answer.cost_usd:.3f}{" (cached)" if answer.cached else ""}', flush=True)
    still = [k for k in todo if k not in done]
    out = apply(data, done)
    print('strings with Chinese left in the English data:', sum(1 for k in todo if k in done and CJK.search(polish(done[k]))))
    with open(args.out, 'w', encoding='utf-8') as handle:
        json.dump(out, handle, ensure_ascii=False, indent=0)
    print(f'written {args.out}; untranslated {len(still)}; this run ${cost:.2f}')


if __name__ == '__main__':
    main()
