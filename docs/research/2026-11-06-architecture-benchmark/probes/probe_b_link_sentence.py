"""Cents proof of the mechanism (AGENTS §1.4): the split's evidence call (B) is told in its system prompt "When no supplied question is connected,
leave links empty; do not create a question.", while its links field carries the adopted fallback (D273, D361; plan decision 2): an unconnected
statement that moves the demand, supply, competition or pricing behind the company's results goes to the company-wide revenue question of its
period. The stored B requests of window draw 1, for every item holding a helpful gold matter the split missed and the control reached, are sent as
stored and with that one sentence changed to defer to the field; two sends each. Each answer is put through the split's source check, then counted
against the gold of its article (D372: helpful reached, not-kept written, extras) and by where its links go.

    PYTHONPATH=src python3 probe_b_link_sentence.py <out.json>"""
import concurrent.futures
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'src'))
import hivemind.model  # noqa: E402,F401
from hivemind import config, model, split, testdb  # noqa: E402
sys.path.insert(1, '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard')
import score_gold as sg  # noqa: E402

OLD = 'When no supplied question is connected, leave links empty; do not create a question.'
NEW = "When no supplied question is connected, apply the links field's rule; do not create a question."
GOLD = '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json'
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
SENDS = 2


def main():
    cfg = config.load(str(ROOT / 'poc/config/poc-split-v3.json'))
    gold = {a['input_id']: a for a in json.load(open(GOLD))['articles']}
    lost = json.load(open(HERE.parent / 'results/differential-window.json'))['split_lost']
    input_ids = sorted({k.rsplit('#', 1)[0] for k in lost})
    archive = sqlite3.connect(f'file:{HERE.parent}/runs/split-v3-d1/archive.sqlite?mode=ro', uri=True)
    items = testdb.open_db(ITEMS)
    stored = [(json.loads(r)) for (r,) in archive.execute("select request_json from model_calls where purpose='split_b'")]
    texts = {i: testdb.item_of(items.execute('select * from items where input_id=?', (i,)).fetchone())['text'] for i in input_ids}
    jobs = []
    for input_id in input_ids:
        request = next((r for r in stored if f'id {input_id},' in r['messages'][-1]['content']), None)
        if request is None:
            print('no stored B request for', input_id)
            continue
        assert request['messages'][0]['content'].count(OLD) == 1
        for arm, sentence in (('stored', OLD), ('deferred', NEW)):
            changed = json.loads(json.dumps(request))
            changed['messages'][0]['content'] = changed['messages'][0]['content'].replace(OLD, sentence)
            for send in range(SENDS):
                jobs.append((input_id, arm, send, changed))

    def run(job):
        input_id, arm, send, request = job
        response = model.openai_transport(cfg.provider, request)
        answer = json.loads(response['choices'][0]['message']['content'])
        text = texts[input_id]
        kept = [dict(e, quote=split.source_quote(e['quote'], text, ['NVIDIA'])) for e in answer['evidence']]
        kept = [e for e in kept if e['quote'] and e['links']]
        a = gold[input_id]
        helpful = [i for i, it in enumerate(a['items']) if it['weight'] in ('core', 'supporting') and any(sg.same_matter(it, e) for e in kept)]
        lost_here = [int(k.rsplit('#', 1)[1]) for k in lost if k.rsplit('#', 1)[0] == input_id]
        not_kept = sum(1 for n in a['not_kept'] if n['weight'] == 'not_kept' and any(sg.same(n['span'], e['quote']) for e in kept))
        extras = sum(1 for e in kept if not any(sg.same_matter(it, e) for it in a['items']) and not any(sg.same(n['span'], e['quote']) for n in a['not_kept']))
        links = [l for e in kept for l in e['links']]
        return {'input_id': input_id, 'arm': arm, 'send': send, 'filed': len(kept), 'helpful': len(helpful), 'lost_recovered': len(set(helpful) & set(lost_here)),
                'lost_total': len(lost_here), 'not_kept': not_kept, 'extras': extras, 'links': links, 'usage': response.get('usage')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(run, jobs))
    json.dump(results, open(sys.argv[1], 'w'), indent=1)
    for arm in ('stored', 'deferred'):
        rows = [r for r in results if r['arm'] == arm]
        for send in range(SENDS):
            s = [r for r in rows if r['send'] == send]
            v1 = sum(r['links'].count('v1') for r in s)
            print(f"{arm:9} send {send + 1}: items {len(s)}, filed {sum(r['filed'] for r in s)}, helpful {sum(r['helpful'] for r in s)}, "
                  f"lost recovered {sum(r['lost_recovered'] for r in s)}/{sum(r['lost_total'] for r in s)}, not-kept {sum(r['not_kept'] for r in s)}, "
                  f"extras {sum(r['extras'] for r in s)}, links to v1 {v1}")


if __name__ == '__main__':
    main()
