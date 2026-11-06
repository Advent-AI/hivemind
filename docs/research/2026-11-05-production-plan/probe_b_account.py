"""The evidence call's own account of three filings the census found too broad or too narrow: the stored B request and answer of the
confirmation run continued with one question each. A self-report is a lead to the instruction, not proof."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model

RUN = ROOT / 'poc/data/split-v2-confirm-first100-2026-11-05'
OUT = ROOT / 'poc/data/b-filing-account-2026-11-05'
ASK = {1211: ('Within the data center book, hyperscale customers contributed', 'v10'),
       1246: ('Management continues to see around $20 billion in total server CPU demand', 'v7'),
       1210: ('Kress revealed that the company will be spending $279 billion on supply commitments', None)}

def main():
    OUT.mkdir(exist_ok=False)
    cfg = config.load(str(ROOT / 'poc/config/poc-split-v2.json'))
    for seq, (fragment, other) in ASK.items():
        request = json.loads((RUN / 'items' / str(seq) / 'b-request.json').read_text())
        answer = json.loads((RUN / 'items' / str(seq) / 'b-answer.json').read_text())
        piece = next(e for e in answer['evidence'] if fragment in e['quote'])
        question = (f'You filed the statement "{piece["quote"][:160]}…" under {piece["links"]}. ' +
                    (f'Question {other} was also open. Quote the exact sentence of your instructions, or the takes line, that led you to file it where you did rather than under {other}, and say on reflection where it belongs.'
                     if other else 'Quote the exact sentence of your instructions, or the takes line, that led you to file the whole total under that question, and say on reflection whether the whole figure answers it.'))
        follow = dict(request); follow.pop('response_format')
        follow['messages'] = request['messages'] + [{'role': 'assistant', 'content': json.dumps(answer, ensure_ascii=False)}, {'role': 'user', 'content': question}]
        response = model.openai_transport(cfg.provider, follow)
        text = response['choices'][0]['message']['content']
        (OUT / f'{seq}.json').write_text(json.dumps({'question': question, 'response': response}, ensure_ascii=False))
        print('==', seq, piece['links']); print(text[:1300])

if __name__ == '__main__':
    main()
