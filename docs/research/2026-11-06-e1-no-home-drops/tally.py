"""The final classes ($0): a class stands where Claude's labels and the blind reader's agree; a disagreement is DISPUTED; quote refusals are
decided by code. LINK cases are split into the question's own quantity in another period or quarter, or a variant of a tracked product
('fence'), and indirect relations."""
import collections, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
packet, mine = json.load(open(HERE / 'packet.json')), json.load(open(HERE / 'labels-claude.json'))
text = (HERE / 'reader-answer.json').read_text()
reader = {int(a['case'][1:]): a for a in json.loads(text[text.index('['):text.rindex(']') + 1])}
NAMES = {'A': 'LINK', 'B': 'OPEN', 'C': 'NONE', 'Q': 'QUOTE'}
FENCE = {1, 2, 5, 9, 18, 27, 39, 54, 23, 29, 30, 31}


def final(n):
    m = NAMES[mine[str(n)][0]]
    if m == 'QUOTE':
        return 'QUOTE (code)'
    if m != reader[n]['class']:
        return 'DISPUTED'
    return ('LINK fence' if n in FENCE else 'LINK indirect') if m == 'LINK' else m


table = collections.defaultdict(collections.Counter)
for n, e in enumerate(packet):
    t = table[final(n)]
    t['matters'] += 1; t['core'] += e['weight'] == 'core'; t[e['set']] += len(e['draws'])
print(f"{'class':<15}{'matters':>8}{'core':>6}{'window draws':>14}{'test draws':>12}")
for c in ['LINK fence', 'LINK indirect', 'DISPUTED', 'OPEN', 'NONE', 'QUOTE (code)']:
    t = table[c]; print(f"{c:<15}{t['matters']:>8}{t['core']:>6}{t['window']:>14}{t['test']:>12}")
print('agreement on the 54 read cases:', sum(NAMES[mine[str(n)][0]] == reader[n]['class'] for n in reader), 'of', len(reader))
json.dump({str(n): final(n) for n in range(len(packet))}, open(HERE / 'final_labels.json', 'w'), indent=1)
