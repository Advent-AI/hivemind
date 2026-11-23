"""The census of the class: the tally ($0; CLASS-CENSUS-DESIGN.md version 2, step 4). It joins the fresh pair's marks to the candidates and
sorts each one by the frozen rule:

- confirmed: both fresh readers mark it in the article, not already shown, and bearing;
- dropped: both say it does not bear, or both say it is already shown;
- open: anything else (both pairs of marks are printed).

It refuses a question whose candidates are not all marked by both families. Confirmed candidates that state one fact are counted once
for a question only through `class-merges.json`, a list written by hand after reading (each entry: the question, the member candidates
and the reason); without it every confirmed candidate is printed with its same-claim group as a lead and the count is of statements,
not yet of facts. It judges nothing itself.

  python3 tally_class.py
"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')


def objects(path):
    if not path.exists():
        return []
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"item"', position)
        if start == -1:
            return out
        row, position = decoder.raw_decode(text, start)
        out.append(row)


def yes(value):
    return str(value).strip().lower().startswith('yes')


def main():
    candidates = json.loads((HERE / 'class-candidates.json').read_text())
    packets = json.loads((HERE / 'settle-packets.json').read_text())
    marks = {family: {} for family in FAMILIES}
    for family in FAMILIES:
        for view, count in packets.items():
            for number in range(1, count + 1):
                for row in objects(HERE / f'{family}-class-settle-{view}-{number}.jsonl'):
                    marks[family][row['item']] = row
    missing = {family: [c['candidate'] for c in candidates if c['candidate'] not in marks[family]] for family in FAMILIES}
    if any(missing.values()):
        raise SystemExit(f"candidates without a fresh mark: codex {len(missing['codex'])} {missing['codex'][:5]}, claude {len(missing['claude'])} {missing['claude'][:5]}: refused")
    merges_path = HERE / 'class-merges.json'
    merges = json.loads(merges_path.read_text()) if merges_path.exists() else []
    merged_into = {member: index for index, merge in enumerate(merges) for member in merge['members']}
    sorted_out = collections.defaultdict(lambda: collections.defaultdict(list))
    for candidate in candidates:
        pair = [marks[family][candidate['candidate']] for family in FAMILIES]
        if all(yes(m.get('in_article')) and not yes(m.get('already_shown')) and yes(m.get('bears')) for m in pair):
            state = 'confirmed'
        elif all(not yes(m.get('bears')) for m in pair) or all(yes(m.get('already_shown')) for m in pair):
            state = 'dropped'
        else:
            state = 'open'
        sorted_out[candidate['question']][state].append((candidate, pair))
    totals = collections.Counter()
    kinds = collections.Counter()
    for view in sorted(packets):
        found = sorted_out[view]
        confirmed = found['confirmed']
        groups = collections.OrderedDict()
        for candidate, pair in confirmed:
            key = ('merge', merged_into[candidate['candidate']]) if candidate['candidate'] in merged_into else ('single', candidate['candidate'])
            groups.setdefault(key, []).append((candidate, pair))
        print(f"\n{view}: candidates {sum(len(v) for v in found.values())}; confirmed {len(confirmed)} statements in {len(groups)} {'facts' if merges else 'entries (not yet merged into facts)'}; "
              f"open {len(found['open'])}; dropped {len(found['dropped'])}")
        totals['confirmed statements'] += len(confirmed)
        totals['confirmed facts'] += len(groups)
        totals['open'] += len(found['open'])
        totals['dropped'] += len(found['dropped'])
        for key, members in groups.items():
            first, first_pair = members[0]
            kind = ('the question opened later' if all(c['read_before_the_question_opened'] for c, _ in members)
                    else 'linked to another question' if any(c['linked_to'] for c, _ in members) else 'linked to none')
            kinds[kind] += 1
            reason = f" | merged: {merges[key[1]]['reason']}" if key[0] == 'merge' else ''
            print(f"  FACT ({kind}; {len(members)} statement{'s' if len(members) > 1 else ''}: {', '.join(c['statement'] for c, _ in members)}; listed first by {sorted({c['listed_by'] for c, _ in members})}){reason}")
            print(f"      codex: {first_pair[0].get('fact')} — {str(first_pair[0].get('why'))[:200]}")
            print(f"      claude: {first_pair[1].get('fact')} — {str(first_pair[1].get('why'))[:200]}")
            print(f"      stored: [{first['article_day']}, article {first['article_place']}, claim group {first['claim_group']}, linked to {first['linked_to'] or 'none'}] {first['summary'][:230]}")
        for candidate, pair in found['open']:
            print(f"  OPEN {candidate['candidate']} [{candidate['listed_by']}]: codex in_article={pair[0].get('in_article')} shown={pair[0].get('already_shown')} bears={pair[0].get('bears')} | "
                  f"claude in_article={pair[1].get('in_article')} shown={pair[1].get('already_shown')} bears={pair[1].get('bears')} | {candidate['summary'][:150]}")
    print(f"\nTOTAL: confirmed {totals['confirmed statements']} statements in {totals['confirmed facts']} {'facts' if merges else 'entries'}; open {totals['open']}; dropped {totals['dropped']}; "
          f"confirmed by kind: {dict(kinds)}")


if __name__ == '__main__':
    main()
