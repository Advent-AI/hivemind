"""The model's own account of chosen probe-4 answers (AGENTS §1): rebuild the request the probe sent (probe_unfiled.build and the
json_mode_call form), add the stored answer as the assistant turn (re-serialised from the parsed answer: the raw text was not kept), and
ask one free-text question. It locates a reason; it does not prove a fix.

Usage: probe4_account.py <records.json> <output.json> [--send]"""
import concurrent.futures, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import probe_unfiled  # noqa: E402
from hivemind import model  # noqa: E402

TAIL = (' Quote the instruction or instructions in this request that led you there, and name the two statements in the request you set '
        'aside in making that choice. Answer in at most 150 words.')
QUESTIONS = [
    ('d1-62', 'c1', [1, 2, 3], lambda r: [t for t in r['new_theses']][:1],
     lambda t: f'You proposed the new thesis "{t["description"]}" instead of linking its statements to the open theses clean-11 or clean-18. Why is it a separate thesis?'),
    ('empty-62', 'c1', [1, 2, 3], lambda r: [t for t in r['new_theses'] if 'supply' in t['description'].lower()][:1],
     lambda t: f'You proposed the new thesis "{t["description"]}". Why is it a separate thesis rather than evidence for another thesis?'),
    ('d1-57', 'c1', [1, 2, 3], lambda r: [ev for ev in r['kept'] if ev.get('condition') and 'cash' in ev['condition']['measure'].lower()][:1],
     lambda ev: f'You kept this statement as a condition: "{ev["summary"]}". Why keep it rather than leave it out?'),
    ('d1-40', 'c1', [1, 2, 3], lambda r: [ev for ev in r['kept'] if ev.get('condition') and 'margin' in ev['condition']['measure'].lower()][:1],
     lambda ev: f'You kept this statement as a condition with links {[l["target_id"] for l in ev["links"]]}: "{ev["summary"]}". Why did you link it, or not link it, to the open thesis clean-11?'),
]


def main():
    records = json.loads(Path(sys.argv[1]).read_text())
    cases = {c['case']: c for c in json.loads((HERE / 'cases.json').read_text())}
    jobs = []
    for case, arm, draws, pick, ask in QUESTIONS:
        system, user, schema, _ = probe_unfiled.build(cases[case], arm)
        for r in records:
            if r['case'] != case or r['arm'] != arm or r['draw'] not in draws or 'kept' not in r:
                continue
            for target in pick(r):
                request = {'model': probe_unfiled.SETTING.model, 'max_tokens': 4000, 'reasoning_effort': probe_unfiled.SETTING.reasoning_effort,
                           'messages': [{'role': 'system', 'content': system + '\n\nReturn only one JSON object that conforms to this JSON Schema:\n' + json.dumps(schema)},
                                        {'role': 'user', 'content': user},
                                        {'role': 'assistant', 'content': json.dumps(r['answer'], ensure_ascii=False)},
                                        {'role': 'user', 'content': ask(target) + TAIL}]}
                jobs.append(({'case': case, 'arm': arm, 'draw': r['draw'], 'question': ask(target)}, request))
    chars = sum(len(json.dumps(j[1])) for j in jobs)
    price = model.PRICES[probe_unfiled.SETTING.model]
    print(f'{len(jobs)} questions; about ${chars / 4 / 1e6 * price[0] + len(jobs) * 1500 / 1e6 * price[1]:.3f}')
    if '--send' not in sys.argv:
        return
    def send(job):
        meta, request = job
        try:
            response = model.openai_transport('deepseek', request)
            return dict(meta, reply=response['choices'][0]['message']['content'])
        except Exception as error:
            return dict(meta, error=f'{type(error).__name__}: {error}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        replies = list(pool.map(send, jobs))
    Path(sys.argv[2]).write_text(json.dumps(replies, ensure_ascii=False, indent=1))
    print(f'{len(replies)} replies, {sum("error" in r for r in replies)} errors')


if __name__ == '__main__':
    main()
