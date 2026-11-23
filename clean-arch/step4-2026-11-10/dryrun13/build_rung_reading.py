"""Thirteenth practice reading ($0): can a reader who sees only an event's rungs, as the judge will, place a fully stated set
of facts in the rung the design means? Asked by the council before the three-outcome request is sent (council `iz`): several
applicants of whom one withdraws; a withdrawal after which the event can still happen; a prohibition that is lifted.

The four ladders are the by-hand answers of `stage_a/three_outcomes_by_hand.py` as the view writer writes them. The scenarios
and the rung each is meant to fall in are written here before any reader answers; the key is written to a path outside this
folder. The reading passes when the two readers place every scenario alike; a scenario they place differently, or both place
against the key, shows wording to change.

The first reading (`packet.json`, `reader-brief.md`, twenty scenarios) was made when code's sentence in the second rung read
"…any other decision against the event of rung 1 as a whole, or a formal abandonment or withdrawal of it as a whole, stands on
<due day>": both readers placed all twenty as the key. The sentence then gained "taken after <the article's day>", for a bar
already in place when the question opened; the second reading (`packet-2.json`) is on that sentence, with three scenarios
added for such a bar.

  python3 clean-arch/step4-2026-11-10/dryrun13/build_rung_reading.py <key path> 2
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(STEP / 'ladder'), str(STEP / 'stage_a')]
import ladder_step  # noqa: E402
import three_outcomes_by_hand  # noqa: E402
from hivemind import universe  # noqa: E402

SCENARIOS = {
    'u1/clean-11': [
        ('Alibaba received an official approval in October 2026 for a limited quantity; ByteDance was refused in November.', 1),
        ('ByteDance withdrew its request in September 2026. The requests of Alibaba and DeepSeek are still under review on the due day. No firm has been approved.', 3),
        ('In November 2026 the authorities refused every request and announced that no H200 imports will be approved. Nothing has changed since.', 2),
        ('In December 2026 every firm withdrew its request after a rule required domestic chips. No request is left, and no firm was approved.', 2),
        ('Alibaba received an official approval in October 2026. The approval was revoked in December 2026.', 1),
        ('There has been no official announcement of any kind. Press reports say requests were filed in July 2026. No firm has been approved.', 3),
        ('The restriction on H200 imports that China had in place before July 2026 is unchanged on the due day. There has been no new decision, and no firm has been approved.', 3),
    ],
    'u3/clean-12': [
        ('A licensing rule for AI-chip shipments to third countries was published in the Federal Register in November 2026, and further firms were added to the entity list in December.', 1),
        ('A proposed rule was withdrawn in October 2026. Another proposed rule, issued in December, is open for comment on the due day. No restriction has been adopted.', 3),
        ('In November 2026 the Commerce Department announced that it will not go beyond the May guidance and withdrew its only proposal. Nothing has changed since.', 2),
        ('A binding licensing rule was adopted in September 2026 and rescinded on 2027-01-15.', 1),
        ('There has been no proposal and no announcement. The May 2026 guidance is as it was.', 3),
        ('Export restrictions adopted in 2025, before the May 2026 guidance, are still in force. Nothing has been adopted or announced since the guidance.', 3),
    ],
    'u3/clean-5': [
        ('Beijing prohibited purchases in August 2026 and lifted the prohibition in December. No sale has been shown by the due day.', 3),
        ('Beijing prohibited purchases in August 2026. The prohibition is in force on the due day; a review of it was announced in January 2027. No sale has been made.', 2),
        ("Nvidia's Form 10-Q published in November 2026 discloses revenue from H200 sales to a Chinese customer.", 1),
        ('Beijing announced in September 2026 that purchases are permitted. No sale has been disclosed or shown by the due day.', 3),
        ('The bar on purchases that Beijing had in place in June 2026 has simply continued. There has been no new decision of any kind, and no sale.', 3),
    ],
    'acc/clean-2': [
        ('The acquisition closed in June 2027 at a renegotiated price of $11.0 billion.', 1),
        ('The merger agreement expired in January 2028 and both companies confirmed that they will not go on with the deal.', 2),
        ('A US regulator sued to block the deal in 2027. The case is still in court on the due day. The deal has not closed, and neither company has ended it.', 3),
        ('A court blocked the deal in December 2027. Nvidia has appealed, and the appeal is pending on the due day.', 2),
        ('The deal has not closed. Neither company has announced anything except that the latest date for closing was moved to September 2028.', 3),
    ],
}


def main():
    key_path, version = Path(sys.argv[1]), sys.argv[2]
    if key_path.resolve().is_relative_to(HERE.resolve()):
        raise SystemExit('the key must not sit in the readers\' folder')
    cases = {case['case']: case for case in json.loads((STEP / 'stage_a' / 'cases.json').read_text())}
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    packet, key, number = [], {}, 0
    for case_name, scenarios in SCENARIOS.items():
        hand_answer = three_outcomes_by_hand.BY_HAND[case_name][0]
        view = ladder_step.write_view(ladder_step.parse_exactly(json.dumps(hand_answer))['ladder'], None, thesis=cases[case_name]['thesis'],
                                      article_day=cases[case_name]['item']['publication_date'], company='NVDA', research_list=research_list)
        entry = {'question': view['question'], 'due_day': view['due_day'],
                 'rungs': [f"rung {position} {rung['label']}: {rung['condition']}" for position, rung in enumerate(view['rungs'], start=1)],
                 'facts_on_the_due_day': []}
        for facts, rung in scenarios:
            number += 1
            entry['facts_on_the_due_day'].append({'scenario': number, 'facts': facts})
            key[str(number)] = rung
        packet.append(entry)
    (HERE / f'packet-{version}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    key_path.write_text(json.dumps(key, indent=1) + '\n')
    (HERE / f'reader-brief-{version}.md').write_text(f'''# A reading of rungs (read-only)

You are an independent reader. Do not edit files, run model calls or start runs. Open only this brief and `packet-{version}.json` in this
folder; open and list nothing else, in the repository or anywhere else.

`packet-{version}.json` holds four questions about events. Each has a `due_day` and its `rungs`, exactly as a later judge is shown them:
"rung N label: condition". For each question there is a list `facts_on_the_due_day`: each entry states, as known and complete,
what is true on the due day.

For every scenario, say which rung holds, reading only the rung texts and the facts given. Add nothing you know from elsewhere.
Exactly one rung is meant to hold; if you find that none does, or that two do, say so instead of choosing.

Return one JSON object per scenario, one per line, in scenario order, and nothing else:
`{{"scenario": 7, "rung": 3, "why": "one sentence naming the words of the rung that decide it"}}`; use `"rung": "none"` or
`"rung": "two"` when that is what you find.
''')
    print(f'{len(packet)} ladders, {number} scenarios; key at {key_path}')


if __name__ == '__main__':
    main()
