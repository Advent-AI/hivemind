"""Census of event questions whose "happened" outcome names a periodic report that comes out after the question's due day
($0; council round 10). Every stored written answer of the answer-choice step, by population. It classes text by patterns and
judges nothing: each flagged case is to be read by hand.

  python3 due_day_census.py
"""
import collections
import json
import re
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind/poc/data')
POPULATIONS = {
    "Alex's 44 topics (fourth Stage A)": [ROOT / 'clean-ladder-stage-a-2026-11-10/run-4'],
    'July, three runs': [ROOT / f'clean-e2e-full-2026-11-13/c{n}/ladder' for n in (1, 2, 3)],
    'fresh week 09-22, empty start': [ROOT / 'clean-lean-week-2026-11-14/week-r2/c1/ladder'],
    'week 10-06, empty start': [ROOT / 'clean-second-week-2026-11-15/week-continued/c1/ladder'],
    'fortnight 09-22..10-05, library kept': [ROOT / 'clean-carried-run-2026-11-16/c1/ladder'],
}
REPORT = re.compile(r'10-K|10-Q|annual report|quarterly (results|report|filing)|fourth-quarter|fiscal-year results|full-year results|earnings (release|report|call)|results for', re.I)
ANNOUNCEMENT = re.compile(r'announc|press release|statement|confirm|disclos(es|ed) (in|through) (a|an) (press|announcement)|says|said|reports? that', re.I)


def outcomes(folder):
    for send in sorted(folder.glob('send-*')):
        for line in (send / 'outcomes.jsonl').read_text().splitlines():
            row = json.loads(line)
            yield send.name, row


def main():
    for name, folders in POPULATIONS.items():
        classes = collections.Counter()
        topics = collections.defaultdict(set)
        examples = []
        events = 0
        for folder in folders:
            for send, row in outcomes(folder):
                ladder = (row.get('answer') or {}).get('ladder')
                if row.get('status') != 'ladder' or not ladder or not ladder.get('event'):
                    continue
                events += 1
                happened = ladder['event'].get('happened') or ''
                topic = f"{folder.parent.name}/{row['case']}"
                if REPORT.search(happened):
                    kind = 'report named, with an announcement also accepted' if ANNOUNCEMENT.search(happened) else 'report named, nothing else accepted'
                    if ladder.get('due_day_basis') == 'period_end':
                        kind += ', due day = period end'
                else:
                    kind = 'no periodic report named'
                classes[kind] += 1
                topics[kind].add(topic)
                if 'nothing else accepted' in kind and 'period end' in kind and len(examples) < 4:
                    examples.append((topic, send, ladder['due_day'], happened[:200]))
        print(f'\n## {name}: {events} written event answers')
        for kind, count in sorted(classes.items()):
            print(f'   {kind}: {count} answers, {len(topics[kind])} topics')
        for example in examples:
            print('      e.g.', example)


if __name__ == '__main__':
    main()
