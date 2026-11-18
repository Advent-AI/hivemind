"""The census of the class, step 2 ($0; CLASS-CENSUS-DESIGN.md): the candidates by code, and the packets for the fresh pair. Read-only on a
finished run.

Reads both first-reader families' answers over the six parts (refusing a part unless every statement has exactly one line holding all
seven question keys, and no unknown statement), sets them against the links the system made, and writes: `class-candidates.json`, every (statement, question) a reader lists where the statement is not
linked to that question, with who listed it, the statement's own links, whether its article was read before the question opened, and
its same-claim group (a lead for grouping repeats, nothing more); the instrument's own check (of the links the system made, which each
family also lists); and, for each question with candidates, packets of at most fifteen for a fresh reader: the whole text of the
question's last judgement request with each candidate's summary, quote and whole article.

  python3 class_candidates.py <run folder of the clean draw>
"""
import collections
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')
PACKET = 15


def objects(path):
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"statement"', position)
        if start == -1:
            return out
        row, position = decoder.raw_decode(text, start)
        out.append(row)


def main():
    run = Path(sys.argv[1])
    views = sqlite3.connect(f"file:{run / 'judge/draw-c1/views.sqlite'}?mode=ro", uri=True)
    archive = sqlite3.connect(f"file:{run / 'judge/draw-c1/archive.sqlite'}?mode=ro", uri=True)
    parts = int((HERE / 'parts.txt').read_text())
    statements = {}
    for number in range(1, parts + 1):
        for row in json.loads((HERE / f'statements-part{number}.json').read_text()):
            statements[row['statement']] = dict(row, part=number)
    questions = {q['question']: q for q in json.loads((HERE / 'questions.json').read_text())}
    listed = {family: collections.defaultdict(dict) for family in FAMILIES}      # family -> statement -> question -> how
    for family in FAMILIES:
        for number in range(1, parts + 1):
            answered = objects(HERE / f'{family}-class-part{number}.jsonl')
            expected = [s for s, row in statements.items() if row['part'] == number]
            seen = collections.Counter(row['statement'] for row in answered)
            problems = ([f'no line: {s}' for s in expected if seen[s] == 0][:4] + [f'more than one line: {s}' for s in expected if seen[s] > 1][:4]
                        + [f'unknown statement: {s}' for s in seen if s not in expected][:4]
                        + [f"{row['statement']} lacks a question key" for row in answered if any(view not in row for view in questions)][:4])
            if problems:
                raise SystemExit(f'{family} part {number} is not read as asked ({problems}): run it again')
            for row in answered:
                for view in questions:
                    if row[view]:
                        listed[family][row['statement']][view] = row[view]
    linked = collections.defaultdict(set)
    for evidence_id, view_id in views.execute('select evidence_id, view_id from evidence_links'):
        linked[evidence_id].add(view_id)
    opened = {view_id: created_seq for view_id, created_seq in views.execute('select view_id, created_seq from views')}
    read_at = {evidence_id: created_seq for evidence_id, created_seq in views.execute('select evidence_id, created_seq from evidence')}
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for old, new in views.execute('select old_evidence_id, new_evidence_id from same_claims'):
        parent[find(old)] = find(new)
    trace = sqlite3.connect(f"file:{run / 'step1/trace.sqlite'}?mode=ro", uri=True)

    def article(sequence):
        request = json.loads(trace.execute('select request from trace where sequence = ?', (sequence,)).fetchone()[0])
        payload, _ = json.JSONDecoder().raw_decode(request['messages'][1]['content'])
        item = payload['source_item']
        return {'article': sequence, 'publication_date': item.get('publication_date'), 'publisher': item.get('publisher'), 'title': item.get('title'), 'text': item.get('text')}
    last_request = {}
    for view_id, call_id in views.execute('select view_id, call_id from judgements order by seq, judgement_id'):
        last_request[view_id] = json.loads(archive.execute('select request_json from model_calls where call_id = ?', (call_id,)).fetchone()[0])['messages'][-1]['content']

    print('THE INSTRUMENT: of the links the system made, the share each first-reader family also lists')
    total = {family: 0 for family in FAMILIES}
    for view in sorted(questions):
        made = [s for s in statements if view in linked[s]]
        also = {family: sum(1 for s in made if view in listed[family][s]) for family in FAMILIES}
        both = sum(1 for s in made if all(view in listed[family][s] for family in FAMILIES))
        for family in FAMILIES:
            total[family] += also[family]
        print(f"  {view}: {len(made)} links; also listed by codex {also['codex']}, claude {also['claude']}, both {both}")
    made_all = sum(len(v) for v in linked.values())
    print(f"  all: {made_all} links; codex lists {total['codex']} ({total['codex'] / made_all:.0%}), claude {total['claude']} ({total['claude'] / made_all:.0%})")

    candidates = []
    for statement, row in statements.items():
        for view in questions:
            who = [family for family in FAMILIES if view in listed[family][statement]]
            if who and view not in linked[statement]:
                candidates.append({'candidate': f'{view}:{statement}', 'question': view, 'statement': statement, 'listed_by': 'both' if len(who) == 2 else who[0],
                                   'how': {family: listed[family][statement].get(view) for family in FAMILIES},
                                   'linked_to': sorted(linked[statement]), 'read_before_the_question_opened': read_at[statement] < opened[view],
                                   'article_place': read_at[statement], 'claim_group': find(statement),
                                   'summary': row['summary'], 'quote': row['quote'], 'said_by': row['said_by'], 'article_day': row['article_day']})
    (HERE / 'class-candidates.json').write_text(json.dumps(candidates, ensure_ascii=False, indent=1))
    print('\nCANDIDATES: listed for a question by a first reader, not linked to it')
    for view in sorted(questions):
        mine = [c for c in candidates if c['question'] == view]
        by = collections.Counter(c['listed_by'] for c in mine)
        print(f"  {view}: {len(mine)} (both {by['both']}, codex only {by['codex']}, claude only {by['claude']}); distinct claim groups {len({c['claim_group'] for c in mine})}; "
              f"read before the question opened {sum(c['read_before_the_question_opened'] for c in mine)}; linked to another question {sum(bool(c['linked_to']) for c in mine)}")
        packets = [mine[start:start + PACKET] for start in range(0, len(mine), PACKET)]
        for number, chosen in enumerate(packets, 1):
            needed = sorted({c['article_place'] for c in chosen})
            (HERE / f'class-settle-{view}-{number}.json').write_text(json.dumps({
                'question': questions[view], 'what_the_judge_was_shown': last_request[view], 'articles': [article(n) for n in needed],
                'items': [{'item': c['candidate'], 'article': c['article_place'], 'article_day': c['article_day'], 'said_by': c['said_by'], 'summary': c['summary'],
                           'quote': c['quote']} for c in chosen]}, ensure_ascii=False, indent=1))
            (HERE / f'brief-class-settle-{view}-{number}.md').write_text(f'''# Blind reader: would this further statement bear on the judgement? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/delivery-class/class-settle-{view}-{number}.json`.
Open no other file in that folder or anywhere else, and use nothing you know from elsewhere.

The packet holds one research `question` (what it asks, what settles it, its possible answers), `what_the_judge_was_shown` (the whole
text a judge received when it last judged the question: the question, its possible answers and every piece of evidence under it),
the `articles` the items came from (number, date, publisher, title, text) and {len(chosen)} `items`: statements a system stored from the
same week's news (its article, who said it, a one-line summary and the quote) that the judge was NOT shown under this question. A
statement may hold several facts: judge the one fact in it that bears most on this question, and name it.

Think as a hedge-fund analyst. Read all of what the judge was shown first. Then for each item decide:
- `fact`: at most 15 words naming the one fact in the statement you are judging;
- `in_article`: yes when the article states that fact with the source, the period and the qualification the summary gives it; no
  when the article says something else (say what);
- `already_shown`: yes when what the judge was shown already states this same fact (the same event, or the same figure for the same
  thing and period), in any wording, including the same underlying claim repeated by another outlet; no when the judge has no
  statement of it, or when this is a different source's own figure or a detail the judge lacks;
- `bears`: yes when, added to what the judge was shown, this fact can change the question's answer or how likely an answer is: it
  is the question's own event or figure, or a fact an analyst would reason onward from to the answer. No when it is background that
  would leave the judgement where it is. Say which answer it makes more or less likely and why, or why it does not bear. A
  judgement already on one answer can still become more or less likely to hold.
Judge `already_shown` and `bears` separately: a fact can be not shown and still not bear.

Write one JSON object per line and nothing else, with no code fence, one line per item ({len(chosen)} lines):
{{"item": "{view}:e000", "fact": "...", "in_article": "yes", "already_shown": "no", "bears": "yes", "why": "<= 30 words>"}}
''')
        print(f'      packets for the fresh pair: {len(packets)}')
    (HERE / 'settle-packets.json').write_text(json.dumps({view: len([c for c in candidates if c['question'] == view][::PACKET]) for view in sorted(questions)}))
    by = collections.Counter(c['listed_by'] for c in candidates)
    print(f"\n{len(candidates)} candidates: both {by['both']}, codex only {by['codex']}, claude only {by['claude']}")


if __name__ == '__main__':
    main()
