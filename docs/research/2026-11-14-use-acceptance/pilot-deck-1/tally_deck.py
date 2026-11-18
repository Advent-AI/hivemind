"""Deck 1's tally ($0): Alex's marks (the JSON the page's last box holds, saved to a file) against the sealed key.

  python3 tally_deck.py <marks.json> <the deck's key folder outside the repository>

Prints every mark beside the card's kind; his marks on the three repeats beside their originals; whether the two wrong
answers were rejected and the confirmed supported controls accepted; his marks beside each model family's stored marks on
the same cards; his completeness answers beside the census; the time and what he opened. It judges nothing.
"""
import collections
import json
import sys
from pathlib import Path

TEAMS = ('codex', 'claude')


def family_mark(stored, field):
    """A model family's stored mark mapped to Alex's scale: question worth (worth → yes; trivia, duplicate → no) and answer
    support (SUPPORTED → yes; UNSUPPORTED → no; INSUFFICIENT, UNSURE → cannot tell)."""
    if not stored:
        return None
    if field == 'worth':
        verdict = (stored.get('question') or {}).get('verdict')
        return {'worth': 'yes', 'trivia': 'no', 'duplicate': 'no'}.get(verdict, verdict)
    verdict = (stored.get('answer') or {}).get('verdict')
    return {'SUPPORTED': 'yes', 'UNSUPPORTED': 'no'}.get(verdict, 'cannot tell' if verdict else None)


def main(marks_path, keys):
    marks = json.loads(Path(marks_path).read_text())
    key = json.loads((Path(keys) / 'deck-1-key.json').read_text())
    given = marks['marks']
    mark = lambda number, field: given.get(f'c{number}-{field}')
    cards = key['cards']
    print(f"cards marked: {sum(1 for n in cards if mark(n, 'worth'))} of {len(cards)}")
    if marks.get('started') and marks.get('last'):
        print(f"time from first to last mark: {(marks['last'] - marks['started']) / 60000:.0f} min")
    for number, record in cards.items():
        label = record['kind'] + (f" (repeat of {record['repeat_of']})" if record.get('repeat') else '')
        what = record.get('view') or record.get('matter')
        opened = {k.split(':')[1]: v for k, v in marks.get('opened', {}).items() if k.split(':')[0] == number}
        print(f"{number:>2} {label:<36} {record.get('system', ''):<3} {what:<4} worth={mark(number, 'worth')} supported={mark(number, 'supported')}"
              f" opened={opened or '-'} why={mark(number, 'why') or ''}")
    print('\nREPEATS (his consistency on identical cards):')
    for number, record in cards.items():
        if record.get('repeat'):
            original = str(record['repeat_of'])
            same = all(mark(number, f) == mark(original, f) for f in ('worth', 'supported'))
            print(f"  card {original} and {number}: {'same' if same else 'DIFFERENT'} "
                  f"({mark(original, 'worth')}/{mark(original, 'supported')} against {mark(number, 'worth')}/{mark(number, 'supported')})")
    print('\nCONTROLS:')
    for number, record in cards.items():
        if record['kind'] == 'planted wrong answer':
            print(f"  wrong answer ({record['plant']}), card {number}: supported={mark(number, 'supported')} (rejected if 'no')")
        if record.get('separate_reader') and not record.get('repeat'):
            print(f"  separately read as {record['separate_reader']}, card {number}: supported={mark(number, 'supported')}")
        if record['kind'] == 'no question':
            print(f"  matter {record['matter']} (no question in one system), card {number}: should hold a question={mark(number, 'worth')}")
    print('\nAGREEMENT WITH EACH MODEL FAMILY (cards both marked; repeats left out):')
    for field in ('worth', 'supported'):
        for team in TEAMS:
            pairs = [(mark(n, field), family_mark(r.get('stored_marks', {}).get(team), field)) for n, r in cards.items()
                     if not r.get('repeat') and r.get('stored_marks')]
            pairs = [(a, b) for a, b in pairs if a and b]
            agree = sum(1 for a, b in pairs if a == b)
            print(f"  {field:<9} {team:<6} agree {agree} of {len(pairs)}; differ on {[(a, b) for a, b in pairs if a != b]}")
    print('\nCOMPLETENESS SHEETS:')
    for number, record in cards.items():
        for fact in record.get('sheet', []):
            index = fact['fact']
            print(f"  card {number} fact {index} ({fact['role']}, {fact['statements']}): bears={mark(number, f'fact{index}-bears')}, "
                  f"would change={mark(number, f'fact{index}-effect')}")
    print('\nHIS REASONS FOR A "no", BY CARD KIND:')
    reasons = collections.defaultdict(list)
    for number, record in cards.items():
        if 'no' in (mark(number, 'worth'), mark(number, 'supported')) and mark(number, 'why'):
            reasons[record['kind']].append(f"card {number}: {mark(number, 'why')}")
    for kind, lines in reasons.items():
        print(f'  {kind}:')
        for line in lines:
            print(f'    {line}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
