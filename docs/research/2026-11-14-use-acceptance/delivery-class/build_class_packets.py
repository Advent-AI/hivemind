"""The census of the class, the first readers' packets ($0; CLASS-CENSUS-DESIGN.md, D507). Read-only on a finished run.

Every kept statement of the run (as its judge would see it: the one-line summary, the quote, who said it and when), in the order the
articles were read, cut into parts of about ninety-five. A reader takes one part and the seven questions and says, for each
statement, which questions it bears on. The packets do not say which statements the system linked to which question.

  python3 build_class_packets.py <run folder of the clean draw>
"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = 95


def main():
    run = Path(sys.argv[1])
    views = sqlite3.connect(f"file:{run / 'judge/draw-c1/views.sqlite'}?mode=ro", uri=True)
    statements = [{'statement': evidence_id, 'article_day': day, 'said_by': original_who or speaker, 'reported_by': speaker, 'original_day': original_day,
                   'summary': one_line, 'quote': quote}
                  for evidence_id, one_line, quote, speaker, original_who, original_day, day in views.execute(
                      'select e.evidence_id, e.one_line, e.quote, e.speaker, e.original_who, e.original_day, s.publication_day from evidence e '
                      'join evidence_sources s on s.evidence_id = e.evidence_id order by e.created_seq, cast(substr(e.evidence_id, 2) as integer)')]
    questions = json.loads((HERE.parent / 'delivery' / 'questions.json').read_text())
    (HERE / 'questions.json').write_text(json.dumps(questions, ensure_ascii=False, indent=1))
    parts = [statements[start:start + PART] for start in range(0, len(statements), PART)]
    for number, chosen in enumerate(parts, 1):
        (HERE / f'statements-part{number}.json').write_text(json.dumps(chosen, ensure_ascii=False, indent=1))
        (HERE / f'brief-class-part{number}.md').write_text(f'''# Blind reader: which tracked questions does each stored statement bear on? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/delivery-class/questions.json` and
`docs/research/2026-11-14-use-acceptance/delivery-class/statements-part{number}.json`. Open no other file in that folder or anywhere else,
and use nothing you know from elsewhere.

`questions.json` holds seven research questions a system tracks about NVIDIA and its themes (v1 to v7): what each asks, what settles
it, its due day and its possible answers. The other file holds {len(chosen)} statements the system stored from one week of news
(2026-09-22 to 09-28): each with an id, the day of its article, who said it, a one-line summary and the quote from the article.

Think as a hedge-fund analyst who must judge the seven questions. For each statement decide which of the seven questions, if any,
it **bears on**: it can change that question's answer or how likely an answer is. That covers the question's own event or figure,
and a fact an analyst would reason onward from to the answer (for example: one component of the amount the question asks for; the
price to go with a volume, or the volume to go with a price; the other party's figure in a deal; an assumption the question turns
on; an earlier decision by the same authority, when you can say why that decision changes the likelihood here and not merely that it
is similar). A statement qualifies for a question only if you can say which answer it makes more or less likely and why. Background
does not qualify: a statement about the company, its market or a neighbouring topic that would leave the judgement where it is. A
statement may hold several facts; it qualifies when any one of them bears.

Go through every statement in order, and for each one consider each of the seven questions. Write one JSON object per line and
nothing else, with no code fence, one line per statement, with all seven question keys in every line: null when the statement does
not bear on that question, else at most 25 words saying which fact in the statement bears, which answer it makes more or less
likely, and why:
{{"statement": "e12", "v1": null, "v2": null, "v3": "<which fact, which answer, why>", "v4": null, "v5": null, "v6": null, "v7": null}}
All {len(chosen)} statements must have exactly one line.
''')
    (HERE / 'parts.txt').write_text(str(len(parts)))
    print(f'{len(statements)} statements in {len(parts)} parts of at most {PART}; part sizes in characters: {[len(json.dumps(p)) for p in parts]}')


if __name__ == '__main__':
    main()
