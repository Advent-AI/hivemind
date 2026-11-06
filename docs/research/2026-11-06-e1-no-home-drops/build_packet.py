"""E1 reading packet ($0): every helpful gold matter production wrote and then dropped (reader verdict DROPPED_BY_CHECK), with the gold
entry, the source paragraph, the dropped statement as the model wrote it, the answer's candidates, and the open questions the request showed."""
import json, re, sqlite3, collections
from pathlib import Path

BENCH = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-06-architecture-benchmark')
OUT = Path(__file__).resolve().parent
verdicts = json.load(open(OUT / 'dropped-verdicts.json'))
traces = {'window': {m['matter']: m for m in json.load(open(BENCH / 'results/traces-window-control.json'))},
          'test': {m['matter']: m for m in json.load(open(BENCH / 'results/traces-test-control.json'))}}
archives = {('window', d): BENCH / f'runs/control-v108-{d}/archive.sqlite' for d in ('d1', 'd2', 'd3')}
archives.update({('test', d): BENCH / f'runs/test-control-{d}/archive.sqlite' for d in ('d1', 'd2', 'd3')})


def open_questions(set_name, draw, input_id, call_id):
    con = sqlite3.connect(f'file:{archives[(set_name, draw)]}?mode=ro', uri=True)
    row = con.execute('select request_json from model_calls where call_id = ?', (call_id,)).fetchone()
    user = json.loads(row[0])['messages'][-1]['content']
    assert f'[Item] id {input_id},' in user, (set_name, draw, input_id, call_id)
    start = user.index('[Open questions')
    end = user.index('\n[', start + 5)
    block = user[start:end]
    questions = re.findall(r'^  - (v\d+) \(([^,]+), due ([0-9-]+)\): (.*)$', block, re.M)
    return block.splitlines()[0], [(qid, obj, due, text) for qid, obj, due, text in questions]


entries = collections.OrderedDict()
for verdict in verdicts:
    key = (verdict['set'], verdict['matter'])
    trace = traces[verdict['set']][verdict['matter']]
    draw = trace['draws'][verdict['draw']]
    calls = draw['raw'].get('extract') or []
    assert len(calls) == 1, (key, verdict['draw'], len(calls))
    answer = calls[0]['answer']
    ids = re.findall(r'\be(\d+)\b', verdict['reason'])
    statements = [e for e in answer['evidence'] if e['id'] in {f'e{i}' for i in ids}]
    heading, questions = open_questions(verdict['set'], verdict['draw'], trace['article']['id'], calls[0]['call_id'])
    entry = entries.setdefault(key, {'set': verdict['set'], 'matter': verdict['matter'], 'weight': trace['weight'], 'span': trace['span'],
                                     'meaning': trace['meaning'], 'standard_line': trace['standard_line'], 'article': trace['article'],
                                     'draws': {}})
    entry['draws'][verdict['draw']] = {'reader_reason': verdict['reason'], 'statements': statements,
                                       'dropped': draw['handover']['dropped'], 'candidates': answer.get('candidates', []),
                                       'questions_heading': heading, 'questions': questions}
json.dump(list(entries.values()), open(OUT / 'packet.json', 'w'), ensure_ascii=False, indent=1)
print(len(entries), 'matters;', sum(len(e['draws']) for e in entries.values()), 'dropped draws')
print(collections.Counter(e['set'] for e in entries.values()), collections.Counter(e['weight'] for e in entries.values()))
