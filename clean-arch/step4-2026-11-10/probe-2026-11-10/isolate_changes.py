"""Which of the second request's changes turned a declined topic into a written question? (AGENTS §7.3: one lever an arm.)

Each arm is the request as FIRST sent with exactly one of the four changes applied, sent on the one topic that changed
(u2/clean-10), three times. The first request declined it 4 of 4; the second request, with all four changes, 0 of 4.

  python3 clean-arch/step4-2026-11-10/probe-2026-11-10/isolate_changes.py
"""
import concurrent.futures
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
sys.path[:0] = [str(REPOSITORY / 'src'), str(REPOSITORY / 'clean-arch' / 'e2e-2026-11-09')]
from hivemind import config, model  # noqa: E402
import budget  # noqa: E402

SENDS_AN_ARM = 3
SETTING = config.Setting(name='clean_ladder_probe', model='gpt-6-luna', prompt_version='ladder-isolation', reasoning_effort='medium',
                         max_output_tokens=16000)
# arm -> (text to change, replacements); each replacement is the exact edit made between the first and the second request
ARMS = {
    'A the reference is copied exactly': {
        'system': [("a consensus, the company's guidance, the stated plan or deadline, in the item's own words, with its value when the item states it as a number;",
                    "a consensus, the company's guidance, the stated plan or deadline. Its words are copied from the item exactly, as one unbroken passage: not reworded, not reordered, and not taken from the topic. It carries its value when the item states it as a number;")],
        'schema': [("The item's own words stating what the market expects: a consensus, the company's guidance, the stated plan or deadline.",
                    "One unbroken passage copied from the item exactly, stating what the market expects: a consensus, the company's guidance, the stated plan or deadline. Not reworded, not reordered, not the topic's wording.")]},
    'B the question stands on its own': {
        'system': [("For a figure, the question names the period it covers or the day it is measured at, and the material that settles it.",
                    "For a figure, the question names the period it covers or the day it is measured at, and the material that settles it. The question is read later by a judge who has only the question, the ladder and new evidence, never this item or the topic: it must stand on its own, naming the thing asked, any company relevant to that question, and any amount it includes in full, and never say \"this item\".")],
        'schema': [("For a figure it names the period covered or the day measured at, and the material that settles it.",
                    "For a figure it names the period covered or the day measured at, and the material that settles it. It stands on its own for a reader who never sees this item.")]},
    "C a theme's states carry names": {
        'system': [("For a company each state carries one of the labels Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish, each used once, meaning good or bad for the business, with the Neutral state's condition saying what it is neutral against: the outcome the market expects when the item states one, otherwise the baseline you compare with; for a theme each carries a short name of the state, each name different.",
                    "A theme's states are never labelled bullish or bearish: each carries a short name of the state itself, each name different. A company's states each carry one of the labels Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish, each used once, meaning good or bad for the business, with the Neutral state's condition saying what it is neutral against: the outcome the market expects when the item states one, otherwise the baseline you compare with.")],
        'schema': [("For a theme: a short name of the state.", "For a theme: a short name of the state itself, never one of those five labels.")]},
    'D the closing check reads the three back': {
        'closing': [("Check that a reference's value is the number its words state",
                     "Check that the question can be understood without this item, that a theme's states carry names and not bullish or bearish labels, and that a reference's words are copied from the item exactly. Check that a reference's value is the number its words state")]},
}


def main():
    output_path = HERE / 'isolation-clean-10.json'
    if output_path.exists():
        raise SystemExit(f'{output_path} exists')
    first = {'system': (HERE / 'sent-system.txt').read_text(), 'closing': (HERE / 'sent-closing.txt').read_text().strip(),
             'schema': (HERE / 'sent-schema.json').read_text()}
    sent = next(entry['request'] for entry in json.loads((HERE / 'requests-sent.json').read_text()) if entry['case'] == 'u2/clean-10')
    payload_text = sent['messages'][1]['content'].rsplit('\n\n', 1)[0]
    jobs = []
    for arm, edits in ARMS.items():
        texts = dict(first)
        for part, replacements in edits.items():
            for old, new in replacements:
                if texts[part].count(old) != 1:
                    raise SystemExit(f'{arm}: the text to change occurs {texts[part].count(old)} times in the {part}')
                texts[part] = texts[part].replace(old, new)
        request = model.build_request(SETTING, texts['system'], payload_text + '\n\n' + texts['closing'], json.loads(texts['schema']),
                                      'clean_ladder', 'openai')
        jobs.extend((arm, number, request) for number in range(1, SENDS_AN_ARM + 1))
    limit = budget.Budget(0.20)

    def send(job):
        arm, number, request = job
        answer = json.loads(limit.send('openai', request)['choices'][0]['message']['content'])
        ladder = answer.get('ladder')
        shape = 'declined' if answer.get('no_ladder') else next(name for name in ('yes_no', 'states', 'figure') if ladder.get(name))
        return {'arm': arm, 'send': number, 'shape': shape, 'answer': answer}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    output_path.write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    for arm in ARMS:
        shapes = [result['shape'] for result in results if result['arm'] == arm]
        print(f"{arm:<44} | declined {shapes.count('declined')} of {len(shapes)} | {shapes}")
    print(f'spent ${limit.spent_usd:.4f}')


if __name__ == '__main__':
    main()
