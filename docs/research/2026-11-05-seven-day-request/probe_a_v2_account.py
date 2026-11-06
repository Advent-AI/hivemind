"""The model's own account of three empty version-2 answers: the stored request and its answer are continued with one question.
A self-report is a lead, not proof of cause."""
import json, sqlite3, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model

OUT = ROOT / 'poc/data/a-v2-variants-2026-11-05'
ASK = {1246: 'The article reports that management preliminarily expects NVIDIA CPU revenue to more than double in fiscal 2028.',
       1269: "The article reports Amazon Web Services' revenue and growth.",
       1238: 'The article discusses the U.S. CPI inflation rate for 2026.'}

def main():
    cfg = config.load(str(ROOT / 'poc/config/poc-split-v2.json'))
    archive = sqlite3.connect(str(OUT / 'built-1.sqlite'))
    results = []
    for seq, fact in ASK.items():
        row = next(r for r in archive.execute('select request_json, answer_json from model_calls') if fact.split()[0] and str(seq) and json.loads(r[0])['messages'][-1]['content'].find(_marker(seq)) >= 0)
        request = json.loads(row[0])
        request['messages'] = request['messages'] + [{'role': 'assistant', 'content': row[1]},
            {'role': 'user', 'content': fact + ' You proposed no new question about it. Quote the exact sentence of your instructions or the existing question (by id) that led you not to propose one, and say whether, on reflection, it should have been proposed.'}]
        request.pop('response_format', None)
        response = model.openai_transport(cfg.provider, request)
        text = response['choices'][0]['message']['content']
        results.append({'seq': seq, 'account': text})
        print('==', seq); print(text[:1500])
    (OUT / 'accounts.json').write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')

def _marker(seq):
    return {1246: 'gnews:d77b4275dcd0a713692fe3ba', 1269: '[Article] id ', 1238: '[Article] id '}[seq] if seq == 1246 else MARKERS[seq]

RUN = ROOT / 'poc/data/split-fresh-seven-day-matching-v4-2026-11-05'
MARKERS = {s: json.loads((RUN / 'items' / str(s) / 'b-request.json').read_text())['messages'][-1]['content'].split('[Item] id ')[1].split(',')[0] for s in (1269, 1238)}

if __name__ == '__main__':
    main()
