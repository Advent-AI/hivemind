"""Split merged.jsonl into eight ranges balanced by the log's bytes and write one read-only Codex verification prompt per range.

usage: python3 make_verify_prompts.py   (writes verify-1.prompt.txt … verify-8.prompt.txt)
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = Path('/Users/lchingen/hivemind/docs/DECISIONS.md')
PARTS = 8

INSTRUCTIONS = """# Read-only check of a first-pass classification of recorded decisions

Repository: /Users/lchingen/hivemind (main at 20ab1bd). The decision log is `docs/DECISIONS.md`. Alex (the owner) asked for the
decisions and working rules to be consolidated; a first reader classified every decision. You are the second reader: check each
record below against the log text (and, where a record's status depends on whether a mechanism still exists, the PRDs under
`docs/prd/` or the code under `src/hivemind/`). You are read-only: do not modify any file.

Today (2026-11-05): replay default `poc/config/poc-v116.json` (D366) = `poc-v108` (frozen extraction prompt v74i, D274) + the
coverage-start reading (D363-D365); one-decider architecture (D264, no placement call); Jev matching with the collision judge
(D169, D190); judging-v7 (D263); steps 3-4 frozen (D354); closing at the due day by pull mode, no separate final verdict (D356); code
builds only the frozen versions (D359); frozen ruler D261/D262; English maintained docs (D163); served ledger sealed (D358); Idea API
poc-v33-idea (D290, D335); frontend rules in docs/poc/thesis-ui.md.

Record fields: area (system, universe, classification, config, dispatch, extraction, library, closing, review-pool, filing-phase,
ruler, idea-service, frontend, data, operations, working-rules); status (in-force: its rule still holds today, possibly amended;
superseded: a later decision replaced it; retired: what it governed was removed or abandoned with no replacement; record: an
experiment, measurement, run, probe, one-off step or a version adoption later replaced, with no standing rule of its own); rule (the
standing rule if in force, faithful, no strengthening or softening); by / amends; authority (alex: rests on Alex's own words or his
reply to that exact question; claude: Claude's detail or process choice without his words; unconfirmed); quote (verbatim from the log);
home (where the standing rule belongs) and home_agrees; conflicts.

For every record, read the decision in the log (grep its header, read it whole) and the later decisions that mention it (grep the
number). Report a problem only when the record is wrong: a wrong status or missing superseding decision, a standing rule that is
missing, invented, stronger or weaker than the log, a quote that is not verbatim or not Alex's, a wrong authority, a wrong or missing
conflict, or a home that contradicts the rule (quote the contradicting sentence). Do not report style.

Output JSON Lines only, no prose: one object per problem
{"id": "D…", "field": "status|rule|by|amends|authority|quote|home|home_agrees|conflicts|area", "problem": "…", "correct": "…",
 "evidence": "log or file passage, quoted briefly with its location"}
and, as the last line, {"checked": [every id you checked], "unchecked": [ids you could not check]}. Check every record; do not stop
early. If you cannot finish, list the rest under "unchecked".

## Records to check
"""


def main():
    text = LOG.read_text(encoding='utf-8')
    heads = [(m.start(), m.group(1)) for m in re.finditer(r'^## (D\d+) ', text, re.M)]
    sizes = {d: (heads[i + 1][0] if i + 1 < len(heads) else len(text)) - start for i, (start, d) in enumerate(heads)}
    records = [json.loads(line) for line in (HERE / 'merged.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    total, target, parts, current, acc = sum(sizes.values()), sum(sizes.values()) / PARTS, [], [], 0
    for record in records:
        current.append(record)
        acc += sizes.get(record['id'], 0)
        if acc >= target * (len(parts) + 1) and len(parts) < PARTS - 1:
            parts.append(current)
            current = []
    parts.append(current)
    for number, part in enumerate(parts, 1):
        body = INSTRUCTIONS + ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in part)
        (HERE / f'verify-{number}.prompt.txt').write_text(body, encoding='utf-8')
        print(f'verify-{number}: {part[0]["id"]}..{part[-1]["id"]} ({len(part)} records, {sum(sizes.get(r["id"], 0) for r in part) / 1e3:.0f} KB of log)')


if __name__ == '__main__':
    main()
