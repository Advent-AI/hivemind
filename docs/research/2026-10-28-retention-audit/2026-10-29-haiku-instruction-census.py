"""Census the stored v38 prompt and selected Haiku outputs without classifying unseen semantic errors."""
import collections
import json
from pathlib import Path
import sqlite3

HERE = Path(__file__).resolve().parent
ARCHIVE = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'
INPUTS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
OUT = HERE / '2026-10-29-haiku-instruction-census.json'


def main():
    db = sqlite3.connect(f'file:{ARCHIVE}?mode=ro', uri=True)
    count = collections.Counter()
    results = []
    for call_id, data in db.execute("select call_id,request_json from model_calls where purpose=?", ('extract',)):
        req = json.loads(data)
        system = next(m['content'] for m in req['messages'] if m['role'] == 'system')
        user = next(m['content'] for m in req['messages'] if m['role'] == 'user')
        evidence = req['response_format']['json_schema']['schema']['properties']['evidence']['items']
        lines = system.splitlines()
        predicates = {
            'singapore_positive_example': any(line.startswith('- A material statement is one of four kinds.') and '"Singapore charged four firms over server exports"' in line for line in lines),
            'take_every_kind_not_selection': '- Go through the item from its first paragraph to its last and take every statement of these kinds; a page with eight such statements yields eight evidence items, not a selection. Stop only at the end of the item.' in lines,
            'no_empty_if_business_content': user.splitlines()[-1].endswith('Return empty arrays only for a page with no business content.'),
            'ask_original_day_without_unknown_rule': any(line.startswith('- Identify the speaker and, for a retelling, the original speaker and statement day.') for line in lines) and not any('original_day' in line and ('unknown' in line.lower() or 'empty' in line.lower()) for line in lines),
            'original_day_required': 'original_day' in evidence['required'],
        }
        count.update(k for k,v in predicates.items() if v)
        results.append({'call_id':call_id,'checks':predicates})
    assert len(results)==98 and all(count[k]==98 for k in ('singapore_positive_example','take_every_kind_not_selection','no_empty_if_business_content','ask_original_day_without_unknown_rule','original_day_required'))
    known = db.execute('select request_json from model_calls where request_sha256=?', ('99dc1c7e9f97d09ba8f9480db32e267c0f57465051f50cccf2e7e190af507007',)).fetchone()
    assert known and 'Singapore charged four firms over server exports' in json.loads(known[0])['messages'][0]['content']
    itemdb=sqlite3.connect(f'file:{INPUTS}?mode=ro',uri=True)
    days={'memory':'gnews:fbce0469dbb5b33e2c34a0f5','amd':'gnews:55b3b854d30ecb73679c2088',
          'singapore':'gnews:1eeceeb212a2c82c2e75e806','policy':'gnews:f9e7da6ddbf890fa64baf922',
          'growth':'gnews:71df54965281684cc500960f'}
    publication={k:itemdb.execute('select publication_day from items where input_id=?',(v,)).fetchone()[0] for k,v in days.items()}
    date_counts=collections.Counter(); samples=[]
    folders=[(HERE/'haiku-luna-multi-2026-10-29', [f'{n}-haiku-{i}.json' for n in ('memory','amd','singapore','policy') for i in (1,2,3)]),
             (HERE/'haiku-extraction-probe-2026-10-29', [f'haiku-{i}.json' for i in (1,2,3)])]
    for folder,names in folders:
        for filename in names:
            d=json.loads((folder/filename).read_text())
            name=filename.split('-')[0] if folder.name.startswith('haiku-luna') else 'growth'
            assert d['completed'] and not d['schema_errors'] and 'sift' in d
            counts=collections.Counter('empty' if not e['original_day'] else 'publication_day' if e['original_day']==publication[name] else 'other' for e in d['sift']['evidence'])
            date_counts.update(counts)
            samples.append({'article':name,'sample':filename,'evidence':len(d['sift']['evidence']),'dates':dict(counts)})
    assert len(samples)==15 and sum(date_counts.values())==89 and date_counts['publication_day']==61
    output={'stored_v38_extract_requests':len(results),'prompt_condition_counts':dict(count),'request_checks':results,
            'selected_haiku_outputs':len(samples),'selected_haiku_evidence':sum(date_counts.values()),'original_day_counts':dict(date_counts),
            'date_note':'Publication-day equality is a route census, not proof it is wrong; review each actual statement and source. Five articles selected by user examples, not a random sample.',
            'samples':samples,'known_control':'historical extraction call 209 checked by exact request digest'}
    with OUT.open('x',encoding='utf-8') as f:
        json.dump(output,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({k:output[k] for k in ('stored_v38_extract_requests','prompt_condition_counts','selected_haiku_outputs','selected_haiku_evidence','original_day_counts','date_note')},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
