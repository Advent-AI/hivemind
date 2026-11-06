"""The blind reader's packet ($0): the cases of packet.json without Claude's labels, the gold weight or the gold's standard line; with the
source paragraph, the gold span and meaning, the gold's question entries for the article, the dropped statements as written, the questions
the same answer proposed, and the exact question block and links rule the stored request showed. Quote refusals (code-decided) are left out."""
import hashlib, json, sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCH = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-06-architecture-benchmark')
GOLD = '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-{}.json'
packet, labels = json.load(open(HERE / 'packet.json')), json.load(open(HERE / 'labels-claude.json'))
archives = {('window', d): BENCH / f'runs/control-v108-{d}/archive.sqlite' for d in ('d1', 'd2', 'd3')}
archives.update({('test', d): BENCH / f'runs/test-control-{d}/archive.sqlite' for d in ('d1', 'd2', 'd3')})
traces = {s: {m['matter']: m for m in json.load(open(BENCH / f'results/traces-{s}-control.json'))} for s in ('window', 'test')}
golds = {s: {a['input_id']: a for a in json.load(open(GOLD.format(s)))['articles']} for s in ('dev', 'test')}
blocks, cases, links_rule = {}, [], None
for n, e in enumerate(packet):
    if labels[str(n)][0] == 'Q':
        continue
    draws = []
    for d, dr in sorted(e['draws'].items()):
        call_id = traces[e['set']][e['matter']]['draws'][d]['raw']['extract'][0]['call_id']
        con = sqlite3.connect(f"file:{archives[(e['set'], d)]}?mode=ro", uri=True)
        request = json.loads(con.execute('select request_json from model_calls where call_id = ?', (call_id,)).fetchone()[0])
        user = request['messages'][-1]['content']
        start = user.index('[Open questions'); end = user.index('\n[', start + 5)
        block = user[start:end].split('\n', 1)[1]
        block_id = 'Q' + hashlib.sha256(block.encode()).hexdigest()[:8]
        blocks[block_id] = block
        if links_rule is None:
            links_rule = request['response_format']['json_schema']['schema']['properties']['evidence']['items']['properties']['links']['description']
        draws.append({'draw': d, 'questions_shown': block_id, 'day': user[start:].split('\n', 1)[0],
                      'dropped_statements': [{k: s[k] for k in ('quote', 'one_line', 'original_who', 'tier', 'links')} for s in dr['statements']],
                      'questions_this_answer_proposed': [c.get('question') for c in dr['candidates']]})
    article = golds['dev' if e['set'] == 'window' else 'test'][e['article']['id']]
    cases.append({'case': f'K{n:02d}', 'article_title': e['article']['title'], 'published': e['article']['day'],
                  'source_paragraph': e['article']['source_paragraph'], 'gold_span': e['span'], 'gold_meaning': e['meaning'],
                  'gold_question_entries_for_this_article': article['questions'], 'draws': draws})
json.dump({'links_rule_as_the_model_reads_it': links_rule, 'question_blocks': blocks, 'cases': cases},
          open(HERE / 'reader-packet.json', 'w'), ensure_ascii=False, indent=1)
print(len(cases), 'cases;', len(blocks), 'question blocks')
