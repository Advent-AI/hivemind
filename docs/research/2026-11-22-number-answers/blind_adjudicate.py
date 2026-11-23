"""Adjudication and refusal-review packets for a judging-v13s blind test (SMALL-DESIGN.md §5, D742).

Adjudication: for every reply whose two readers disagree (a member's "supported", or any defect one reader marks), one packet holding
the two readings, the system text, the format rules the writer was given (every schema description), the request as the writer saw it
and the answer. Reader 1 is the Codex reading and Reader 2 the Claude reading; the adjudicators are not told which.

Refusal review: for every refused first reply, one packet with the refusal messages, the system text, the schema, the user text and the
answer, asking the two registered judgements apart: is the forecast and its reasoning financially sound, and does the exact request
clearly state the condition the refusal enforces (D742: a sound answer refused under a clearly stated condition still stops the run).

Usage: python3 blind_adjudicate.py <blind test folder> <packet id> [<packet id> ...]
       python3 blind_adjudicate.py refusal <blind test folder> <case> <writer>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from blind_rules import DEFINITIONS, descriptions, format_material  # noqa: E402

HEADER = """# Adjudication (judging-v13s blind test)

Two readers disagreed about the answer below. Settle each point against the passages in the request and the format rules quoted
below, not against either reader's threshold. Read only what is given here.

For each member, decide **supported** (yes or no). For each defect a reader marked, decide **uphold** or **reject**, quoting the
passage words or the format rule that decides it.

""" + DEFINITIONS + """

Return only JSON: {"members": {"<view id>": {"supported": "yes|no", "why": "..."}},
 "defects": [{"reader": "Reader 1|Reader 2", "type": "...", "figures": [...], "decision": "uphold|reject", "why": "..."}]}
"""


def _json(text):
    """A reading: the outermost JSON object in the file."""
    return json.loads(text[text.find('{'):text.rfind('}') + 1])


def reading_lines(label, reading):
    lines = []
    for member, mark in sorted(reading.get('members', {}).items()):
        line = f"- {label} on member {member}: supported = {mark.get('supported')}. Ground: {mark.get('ground', '')}"
        if mark.get('why_not'):
            line += f" Why not: {mark['why_not']}"
        lines.append(line)
    defects = reading.get('defects', [])
    if not defects:
        lines.append(f'- {label} marks no defect.')
    for defect in defects:
        lines.append(f"- {label} marks a defect: {defect.get('type')} (figures {defect.get('figures', [])}): {defect.get('detail', '')}")
    return lines


def build(folder, packet_ids, key_name='reader-key.json', packets='reader-packets', out_name='adjudication'):
    key = json.loads((folder / key_name).read_text())
    out = folder / out_name
    out.mkdir(exist_ok=True)
    for pid in packet_ids:
        case, writer = key[pid]['case'], key[pid]['writer']
        codex = _json((folder / packets / f'{pid}.codex.json').read_text())
        claude = _json((folder / packets / f'{pid}.claude.json').read_text())
        answer_path = folder / key[pid]['answer'] if key[pid].get('answer') else folder / case / 'answers' / f'{writer}.json'
        case_dir = Path(key[pid]['case_dir']) if key[pid].get('case_dir') else folder / case   # D747: the writer's own request
        text = '\n'.join([HEADER, '# The two readings', *reading_lines('Reader 1', codex), *reading_lines('Reader 2', claude), '',
                          format_material(case_dir), '',
                          '# The request (questions, ladders and every passage)', (case_dir / 'user.txt').read_text(), '',
                          '# The answer', answer_path.read_text()])
        target = out / f'{pid}.md'
        if target.exists():
            raise SystemExit(f'{target} exists')
        target.write_text(text)
        (out / f'{pid}.prompt.txt').write_text(f'Read the file {target} and nothing else (no other file, no web). Follow its '
                                               'instructions and return only the JSON it asks for.\n')
        print(f'{pid}: {case}/{writer}, {len(text)} chars')


REFUSAL_HEADER = """# Refusal review (judging-v13s blind test)

A code check refused the answer below. For each refusal message, give two judgements apart, from the request text and the passages
alone:
1. sound: is the forecast and its reasoning financially sound against the passages (would an analyst accept the number and the reasons
   that produce it)? Judge this on its own, apart from the format rule the check enforces. Answer yes or no, with why.
2. stated: does the exact request (system text, schema or user text below) clearly state the condition the refusal enforces? Answer
   yes or no, and quote the sentence that states it, or say none does.
Return only JSON: {"refusals": [{"message": "...", "sound": "yes|no", "why": "...", "stated": "yes|no", "sentence": "..."}]}
"""


def refusal(folder, case, writer):
    checked = {(r['case'], r['writer']): r for r in json.loads((folder / 'CHECKED.json').read_text())}
    row = checked[(case, writer)]
    if row.get('decision') == 'publish' or not row.get('errors'):
        raise SystemExit(f'{case}/{writer} was not refused')
    out = folder / 'refusal-review'
    out.mkdir(exist_ok=True)
    text = '\n'.join([REFUSAL_HEADER, '# Refusal messages', json.dumps(row['errors'], ensure_ascii=False), '',
                      '# The system text', (folder / case / 'system.txt').read_text(), '',
                      '# The schema', (folder / case / 'schema.json').read_text(), '',
                      '# The user text (the request, with every passage)', (folder / case / 'user.txt').read_text(), '',
                      '# The answer', (folder / case / 'answers' / f'{writer}.json').read_text()])
    target = out / f'{case}-{writer}.md'
    if target.exists():
        raise SystemExit(f'{target} exists')
    target.write_text(text)
    (out / f'{case}-{writer}.prompt.txt').write_text(f'Read the file {target} and nothing else (no other file, no web). Follow its '
                                                    'instructions and return only the JSON it asks for.\n')
    print(f'refusal review {case}/{writer}: {len(text)} chars')


if __name__ == '__main__':
    if len(sys.argv) == 5 and sys.argv[1] == 'refusal':
        refusal(Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4])
    elif len(sys.argv) >= 4 and sys.argv[2] == '--reread':        # D743: the re-read's packets, key and adjudication folder
        build(Path(sys.argv[1]).resolve(), sys.argv[3:], 'reread-key.json', 'reread-packets', 'reread-adjudication')
    elif len(sys.argv) >= 4 and sys.argv[2] == '--reread2':       # D744: the second re-read under the shared rule text
        build(Path(sys.argv[1]).resolve(), sys.argv[3:], 'reread2-key.json', 'reread2-packets', 'reread2-adjudication')
    elif len(sys.argv) >= 4 and sys.argv[2] == '--reread-d747':   # D747: the re-read under Alex's comparison ruling
        build(Path(sys.argv[1]).resolve(), sys.argv[3:], 'reread-key.json', 'reread-packets', 'reread-adjudication')
    elif len(sys.argv) >= 3 and sys.argv[1] != 'refusal':
        build(Path(sys.argv[1]).resolve(), sys.argv[2:])
    else:
        raise SystemExit(__doc__)
