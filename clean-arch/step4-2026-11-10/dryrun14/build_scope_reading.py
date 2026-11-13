"""Fourteenth practice reading ($0): does binding the model's own ruled-out sentence to the scope code writes change how a
reader places a decision that was already made before the article?

The second Stage A left one cause in three of the four event ladders both readers failed on R: the model's ruled-out sentence
does not say "after the article's day", and code's sentence carried that scope for every other decision only. The change makes
code's sentence govern the model's too ("…was made after <day> and stands on <due day>").

Six event answers of the second run whose ruled-out sentence has no "after" are shown twice, each as the judge would see it:
with the sentence as it was in that run and with the sentence as it now is. Each carries three sets of facts stated in full: a
decision against the event made before the article and still standing with nothing new since; a new decision against it made
after the article; the event having happened. The order of the twelve ladders is shuffled; a reader sees no thesis and no article.

Fixed before any reader answers:
- with the sentence as it now is, both readers place the earlier decision in the last rung (still open) for all six;
- with the sentence as it was, at least one reader places it in the ruled-out rung for the three ladders both readers failed in
  the second run (u1/clean-11 pass 2, u2/clean-3 passes 1 and 2);
- the new decision is placed in the ruled-out rung and the event in the first rung under both sentences.

  python3 clean-arch/step4-2026-11-10/dryrun14/build_scope_reading.py <key path>
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(STEP / 'ladder')]
import ladder_step  # noqa: E402

RUN = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'run-2'
AS_IT_WAS = ('This rung holds when that, or any other decision against the event of rung 1 as a whole taken after {article_day}, or a formal '
             'abandonment or withdrawal of it as a whole after that day, stands on {due_day}, and only when rung 1 does not.')
FACTS = {       # send: (a decision made before the article and still standing, a new decision after it, the event)
    ('u2/clean-3', 1): ('In March 2026 Chinese regulators formally decided to keep H200 sales barred. That decision is still in force on the due day. Nothing has been decided or announced since, and no sale or shipment has been disclosed.',
                        'In October 2026 Chinese regulators formally decided not to permit H200 sales. That decision is in force on the due day. No sale or shipment has been disclosed.',
                        'In November 2026 China officially permitted H200 sales to mainland China.'),
    ('u2/clean-3', 2): ('In March 2026 China officially decided to continue barring H200 imports. Nothing has been decided or announced since, and NVIDIA has disclosed no H200 sales or shipments to China.',
                        'In October 2026 China formally denied authorization for H200 sales. Nothing has changed since, and no sale has been disclosed.',
                        'In November 2026 China authorized H200 sales in mainland China.'),
    ('u1/clean-11', 2): ('In May 2026 Chinese authorities formally decided against permitting H200 imports into China. That position still stands on the due day. Nothing has been decided since, and no import has been approved.',
                         'In November 2026 Chinese authorities formally decided against permitting H200 imports into China. That position stands on the due day, and no import has been approved.',
                         'In October 2026 Chinese authorities approved imports of Nvidia H200 chips into China.'),
    ('u1/clean-11', 1): ('In May 2026 Chinese authorities formally decided not to approve H200 imports for any Chinese firm. That decision is unchanged on the due day; nothing has been decided since, and no firm has been approved.',
                         'In November 2026 Chinese authorities formally decided not to approve H200 imports for any Chinese firm. No firm has been approved.',
                         'In October 2026 Chinese authorities approved Alibaba to import Nvidia H200 chips, as shown by an official announcement.'),
    ('u2/clean-5', 1): ('In June 2026 NVIDIA decided that Kyber NVL144 would not ship until 2028. Nothing has changed since: NVIDIA has announced nothing new, and no shipment has been made.',
                        'In March 2027 NVIDIA announced that it had decided Kyber NVL144 will not ship until 2028. No shipment has been made.',
                        'In November 2027 NVIDIA disclosed that the Kyber NVL144 rack-scale system, paired with Rubin Ultra, had made its first shipment.'),
    ('u3/clean-12', 3): ('In June 2026 the Commerce Department formally decided against a proposed escalation to a binding export-licensing rule. Nothing has been proposed or decided since, and no restriction beyond the May 2026 guidance has been issued or put into effect.',
                         'In November 2026 the Commerce Department formally withdrew its proposed escalation to a binding export-licensing rule. No restriction beyond the May 2026 guidance has been issued or put into effect.',
                         'In October 2026 the Bureau of Industry and Security put into effect a binding export-licensing rule, beyond its May 2026 guidance, on AI-chip shipments to third countries.'),
}


def main():
    key_path = Path(sys.argv[1])
    if key_path.resolve().is_relative_to(HERE.resolve()):
        raise SystemExit('the key must not sit in the readers\' folder')
    cases = {case['case']: case for case in json.loads((STEP / 'stage_a' / 'cases.json').read_text())}
    outcomes = {(row['case'], row['pass']): row for pass_folder in sorted(RUN.glob('send-*'))
                for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)]}
    entries = []
    for send, (before, after, happened) in FACTS.items():
        ladder = outcomes[send]['answer']['ladder']
        article_day, due_day = cases[send[0]]['item']['publication_date'], ladder['due_day']
        as_it_is = ladder_step.event_rungs(ladder['event'], due_day, article_day)
        ruled_out = ladder['event']['ruled_out'].rstrip()
        as_it_was = [dict(rung) for rung in as_it_is]
        as_it_was[1]['condition'] = f"{ruled_out}{'' if ruled_out.endswith('.') else '.'} " + AS_IT_WAS.format(article_day=article_day, due_day=due_day)
        for sentence, rungs in (('as it was', as_it_was), ('as it is', as_it_is)):
            entries.append({'send': send, 'sentence': sentence, 'question': ladder['question'], 'due_day': due_day,
                            'rungs': [f"rung {position} {rung['label']}: {rung['condition']}" for position, rung in enumerate(rungs, start=1)],
                            'facts': [('an earlier decision still standing', before, 3 if sentence == 'as it is' else None),
                                      ('a new decision', after, 2), ('the event', happened, 1)]})
    random.Random(20261110).shuffle(entries)
    packet, key, number = [], {}, 0
    for entry in entries:
        shown = {'question': entry['question'], 'due_day': entry['due_day'], 'rungs': entry['rungs'], 'facts_on_the_due_day': []}
        facts = list(entry['facts'])
        random.Random(f"{entry['send']}{entry['sentence']}").shuffle(facts)
        for kind, text, rung in facts:
            number += 1
            shown['facts_on_the_due_day'].append({'scenario': number, 'facts': text})
            key[str(number)] = {'send': list(entry['send']), 'sentence': entry['sentence'], 'kind': kind, 'rung': rung}
        packet.append(shown)
    (HERE / 'packet.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    key_path.write_text(json.dumps(key, indent=1) + '\n')
    (HERE / 'reader-brief.md').write_text('''# A reading of rungs (read-only)

You are an independent reader. Do not edit files, run model calls or start runs. Open only this brief and `packet.json` in this
folder; open and list nothing else, in the repository or anywhere else.

`packet.json` holds twelve questions about events. Each has a `due_day` and its `rungs`, exactly as a later judge is shown them:
"rung N label: condition". Some questions resemble one another; read each one's own rungs word by word, for they differ. For
each question there is a list `facts_on_the_due_day`: each entry states, as known and complete, what is true on the due day.

For every scenario, say which rung holds, reading only that question's rung texts and the facts given. Add nothing you know
from elsewhere. Exactly one rung is meant to hold; if you find that none does, or that two do, say so instead of choosing.

Return one JSON object per scenario, one per line, in scenario order, and nothing else:
`{"scenario": 7, "rung": 3, "why": "one sentence naming the words of the rung that decide it"}`; use `"rung": "none"` or
`"rung": "two"` when that is what you find.
''')
    print(f'{len(packet)} ladders, {number} scenarios; key at {key_path}')


if __name__ == '__main__':
    main()
