"""The same week, both systems, side by side ($0; D517, corrected after the council's round 8). Built by code from the stored runs of the
fresh week (2026-09-22..28) and the stored files of the two reviewing teams; read-only on the runs.

Printed as stored, never rewritten: every question, every possible answer with its full condition, the latest answer, its reasons, the
reviewers' marks and reasons, every cited statement with its stored passage. Written by hand, and marked so on the page: the pairing of
the two systems' questions by subject and the note on how each pair differs (`shared-subjects.json`; the notes are the council's words,
round 8). The same template serves both systems. The script refuses when a reviewer's mark, a cited statement or a stored request is
missing.

It writes two pages: SIDE-BY-SIDE-WEEK.md (a front page, then all 22 entries) and SIDE-BY-SIDE-WEEK-CITED.md (for each question, the
statements its latest answer cites, with the stored passage of each and the stored request's identity).

  python3 build_side_by_side.py <key folder outside the repository>
"""
import json
import random
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, '/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b')
import stored_judgements  # noqa: E402

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
USE = ROOT / 'docs/research/2026-11-14-use-acceptance'
WEEK = USE / 'week'
RUN = ROOT / 'poc/data/clean-lean-week-2026-11-14'
FOLDERS = {'old': RUN / 'week/p1/prod', 'new': RUN / 'week-r2/c1/judge/draw-c1'}
DRAW = {'old': 'p1', 'new': 'c1'}
NAMES = {'old': 'Old system', 'new': 'New system'}
TEAMS = (('codex', 'Team A (Codex)'), ('claude', 'Team B (Claude)'))
SEED = 20261202
CITED_PAGE = 'SIDE-BY-SIDE-WEEK-CITED.md'


def objects(path):
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"', position)
        if start == -1:
            return out
        try:
            row, position = decoder.raw_decode(text, start)
            out.append(row)
        except json.JSONDecodeError:
            position = start + 1


def cell(text):
    return str(text).replace('|', '/').replace('\n', ' ')


def load_entries(system, key_a, key_b, quality, support, confirmation):
    """Every question of one system with its stored answer, the reviewers' marks and the statements its latest answer cites."""
    store = sqlite3.connect(f"file:{FOLDERS[system] / 'views.sqlite'}?mode=ro", uri=True)
    stored_judgements.refuse_split_store(store, 'build_side_by_side')     # it maps a view to its topic by id (clean-<view number>)
    archive = sqlite3.connect(f"file:{FOLDERS[system] / 'archive.sqlite'}?mode=ro", uri=True)
    draw = DRAW[system]
    blind_id = {entry['own_id']: entry['system_id'] for entry in key_a[draw]}
    entries = []
    for number, (view_id, object_id, kind, question, due_day, created_seq) in enumerate(
            store.execute('select view_id, object_id, kind, question, due_day, created_seq from views order by created_seq, view_id'), 1):
        rungs = store.execute('select position, label, condition from rungs where view_id = ? order by position', (view_id,)).fetchall()
        last = store.execute('select seq, publication_day, rung, reasons, implied_outcome, cited_evidence_json, call_id, request_sha256 from judgements '
                             'where view_id = ? order by seq desc, judgement_id desc limit 1', (view_id,)).fetchone()
        if last is None:
            raise SystemExit(f'{system} {view_id} has no judgement: refused')
        if archive.execute('select 1 from model_calls where call_id = ?', (last[6],)).fetchone() is None:
            raise SystemExit(f'{system} {view_id}: the stored request of call {last[6]} is not in the archive: refused')
        cited = []
        for evidence_id in json.loads(last[5]):
            row = store.execute('select one_line, quote, original_who, tier, created_seq from evidence where evidence_id = ?', (evidence_id,)).fetchone()
            if row is None:
                raise SystemExit(f'{system} {view_id}: cited statement {evidence_id} is not in the store: refused')
            cited.append((evidence_id, *row))
        own = view_id if system == 'old' else f'clean-{view_id[1:]}'
        marks = {}
        for team, _ in TEAMS:
            question_mark = quality[team].get(blind_id.get(own, ''))
            item = next((entry for entry in key_b if entry['draw'] == draw and entry['view'] == view_id and not entry.get('planted')), None)
            answer_mark = support[team].get(item['item']) if item else None
            if question_mark is None or answer_mark is None:
                raise SystemExit(f'{system} {view_id}: a mark of {team} is missing: refused')
            marks[team] = (question_mark, answer_mark)
        separate = confirmation.get(item.get('candidate')) if item else None
        entries.append({
            'system': system, 'number': number, 'view': view_id, 'anchor': f'{system}-{view_id}', 'question': question, 'about': f'{object_id} ({kind})',
            'opened': created_seq, 'due': due_day, 'rungs': rungs, 'answer_day': last[1], 'answer_seq': last[0], 'rung': last[2], 'reasons': last[3],
            'expects': last[4], 'cited': cited, 'call_id': last[6], 'request_sha256': last[7], 'marks': marks, 'separate': separate,
            'links': store.execute('select count(*) from evidence_links where view_id = ?', (view_id,)).fetchone()[0],
            'judged': store.execute('select count(*) from judgements where view_id = ?', (view_id,)).fetchone()[0]})
    return entries, store, archive


def chosen(entry):
    position, label, condition = next(r for r in entry['rungs'] if r[0] == entry['rung'])
    return f"{position} {label}" + (f": {condition}" if condition else '')


def ref(entry):
    return f"[{NAMES[entry['system']]} {entry['number']} (`{entry['view']}`)](#{entry['anchor']})"


def question_marks(entry, own_ids):
    parts = []
    for team, team_name in TEAMS:
        mark = entry['marks'][team][0]
        duplicate = f" of `{own_ids.get(mark['duplicate_of'], mark['duplicate_of'])}`" if mark.get('duplicate_of') else ''
        parts.append((team_name, f"**{mark['verdict']}**{duplicate}", mark.get('why') or ''))
    return parts


def answer_marks(entry):
    return [(team_name, f"**{entry['marks'][team][1]['verdict']}**", entry['marks'][team][1].get('why') or '') for team, team_name in TEAMS]


def main():
    key_folder = Path(sys.argv[1])
    key_a = json.loads((key_folder / 'week-key-A2.json').read_text())
    key_b = json.loads((key_folder / 'week-key-B.json').read_text())
    quality = {team: {row['id']: row for row in objects(WEEK / f'{team}-A2.jsonl') if row.get('part') == 2} for team, _ in TEAMS}
    matters_marks = {team: [row for row in objects(WEEK / f'{team}-A2.jsonl') if row.get('part') == 1] for team, _ in TEAMS}
    support = {team: {row['item']: row for row in objects(WEEK / f'{team}-B.jsonl')} for team, _ in TEAMS}
    confirmation = {row['candidate']: row for row in objects(WEEK / 'control-confirmation.jsonl')}
    matters = json.loads((WEEK / 'matters-A2.json').read_text())
    subjects = json.loads((HERE / 'shared-subjects.json').read_text())
    own_ids = {entry['system_id']: entry['own_id'] for draw in DRAW.values() for entry in key_a[draw]}
    label_of = {key_a['labels'][draw]: system for system, draw in DRAW.items()}
    entries, stores, archives = {}, {}, {}
    for system in ('old', 'new'):
        entries[system], stores[system], archives[system] = load_entries(system, key_a, key_b, quality, support, confirmation)
    by_view = {system: {entry['view']: entry for entry in entries[system]} for system in entries}
    paired = {system: {view for subject in subjects for view in subject[system]} for system in entries}
    for subject in subjects:
        for system in entries:
            unknown = [view for view in subject[system] if view not in by_view[system]]
            if unknown:
                raise SystemExit(f"shared-subjects.json names {unknown} which the {system} system does not hold: refused")
    adapter = json.loads((FOLDERS['new'] / 'adapter-counts.json').read_text())

    def matter_rows(chosen_matters):
        rows = ['| Matter | Listed by | Old system | New system |', '|---|---|---|---|']
        for matter in chosen_matters:
            cells = {}
            for system in ('old', 'new'):
                parts = []
                for team, team_name in TEAMS:
                    mark = next((m for m in matters_marks[team] if m['matter'] == matter['matter'] and label_of.get(m['system']) == system), None)
                    if mark is None:
                        raise SystemExit(f"matter {matter['matter']}: no mark of {team} for the {system} system: refused")
                    ids = ', '.join(f"`{own_ids.get(i, i)}`" for i in mark.get('ids') or []) or 'no question'
                    parts.append(f"{team_name}: {mark['status']} ({ids})")
                cells[system] = '; '.join(parts)
            rows.append(f"| {matter['matter']} {cell(matter['name'])} | {cell(matter['listed_by'])} | {cells['old']} | {cells['new']} |")
        return rows

    out = ['# The same week, both systems, side by side', '',
           'Built by code on 2026-11-15 (D517; corrected after the council\'s review, round 8) from the stored runs of the week of 2026-09-22',
           'to 09-28 (235 articles; each system run once, starting with no questions) and from the stored notes of two independent reviewing',
           'teams (Team A: Codex; Team B: Claude), who read both systems\' output without knowing which system wrote it.', '',
           '- **Printed as stored:** every question, every possible answer with its full condition, each latest answer and its reasons, the',
           '  reviewers\' marks and reasons, and (on the second page) every statement an answer cites with its stored passage.',
           '- **Written by hand, and marked so:** which questions of the two systems are on the same subject, and the note on how each such',
           '  pair differs (`shared-subjects.json`; the notes are the council\'s words, `my-codex-8.md` and `my-codex-9.md`).',
           '- **It ranks nothing and proves no winner.** One week, one run of each system. The reviewers marked an answer against the passages',
           '  the judge was shown, not against the full articles.',
           f'- Second page: [`{CITED_PAGE}`]({CITED_PAGE}). Builder: `build_side_by_side.py`.', '',
           '## Front page', '',
           '### 1. The five matters both reviewing teams listed, and where each system has them', '',
           'Each team listed, from 40 sampled articles, the matters worth tracking on their own. "opened" means the system holds a question',
           'on it. The three matters only one team listed are in the table before the entries.', '']
    out += matter_rows([m for m in matters if str(m['listed_by']).startswith('both')])
    out += ['', '### 2. Subjects on which both systems hold a question', '',
            'The pairing is by hand. Everything in the tables is stored text. Read the two questions before comparing the two answers: on',
            'most subjects the systems ask different questions.', '']
    for subject in subjects:
        out += [f"**{subject['subject']}**", '', '| | Old system | New system |', '|---|---|---|']
        pair = {system: [by_view[system][view] for view in subject[system]] for system in ('old', 'new')}

        def row(title, text_of):
            return f"| {title} | " + ' | '.join('<br><br>'.join(cell(text_of(entry)) for entry in pair[system]) for system in ('old', 'new')) + ' |'
        out += [row('Question', lambda e: f"{ref(e)}: {e['question']}"),
                row('Latest answer', lambda e: f"{chosen(e)} (answered {e['answer_day']})"),
                row('Statements linked', lambda e: e['links']),
                row('Reviewers on the question', lambda e: '; '.join(f"{team}: {verdict}" for team, verdict, _ in question_marks(e, own_ids))),
                row('Reviewers on the answer', lambda e: '; '.join(f"{team}: {verdict}" for team, verdict, _ in answer_marks(e))), '']
        out += [f"How the pair differs (the council's words): {subject['difference']}" if subject['difference']
                else 'How the pair differs: no note was written; the questions and answers above are as stored.', '']
    out += ['### 3. Questions only one system holds', '']
    for system in ('old', 'new'):
        alone = [entry for entry in entries[system] if entry['view'] not in paired[system]]
        out += [f"**{NAMES[system]}: {len(alone)} of its {len(entries[system])}**", '']
        for entry in alone:
            out.append(f"- {ref(entry)}: {entry['question']} Latest answer: {chosen(entry)} (answered {entry['answer_day']}). On the question: "
                       + '; '.join(f"{team}: {verdict}" for team, verdict, _ in question_marks(entry, own_ids)) + '. On the answer: '
                       + '; '.join(f"{team}: {verdict}" for team, verdict, _ in answer_marks(entry)) + '.')
        out.append('')
    everything = entries['old'] + entries['new']
    not_passed = {team: [e for e in everything if e['marks'][team][1]['verdict'] != 'SUPPORTED'] for team, _ in TEAMS}
    both = [e for e in everything if all(e['marks'][team][1]['verdict'] != 'SUPPORTED' for team, _ in TEAMS)]
    one = [e for e in everything if sum(e['marks'][team][1]['verdict'] != 'SUPPORTED' for team, _ in TEAMS) == 1]
    out += ['### 4. Answers the reviewers did not both pass', '',
            f"Of the 22 latest answers, both teams pass {len(everything) - len(both) - len(one)}; both teams fail {len(both)}; one team alone fails {len(one)} "
            f"(Team A: {len(not_passed['codex'])} in all, Team B: {len(not_passed['claude'])}). For eight answers a separate reader had been asked, before the "
            'reading, whether the answer is supported; that mark is shown where it exists.', '']
    for title, group in (('Both teams fail', both), ('One team alone fails', one)):
        out += [f'**{title}**', '']
        for entry in group:
            out.append(f"- {ref(entry)}: {entry['question']} Latest answer: {chosen(entry).rstrip('.')}.")
            for team, verdict, why in answer_marks(entry):
                out.append(f"  - {team}: {verdict}. {why}")
            if entry['separate']:
                out.append(f"  - The separate reader, before the reading: **{entry['separate']['verdict']}**. {entry['separate'].get('why') or ''}")
        out.append('')
    page = (USE / 'DECISION-PAGE-2026-11-15.md').read_text()
    costs = page[page.index('## 3. What each system costs a reader today'):page.index('## 4. What is not known')].split('\n', 1)[1].strip()
    out += ['### 5. What each system is known to cost a reader', '',
            'Copied unchanged from section 3 of the decision page (`../DECISION-PAGE-2026-11-15.md`), which an independent reviewer read three',
            'times. Its counts of statements (569 written, 389 with no question) are the reading step\'s; the last part of this page explains the other count.', '',
            costs, '']
    rng = random.Random(SEED)
    unlinked = stores['new'].execute('select evidence_id, one_line, quote, original_who, created_seq from evidence where evidence_id not in '
                                     '(select evidence_id from evidence_links) order by cast(substr(evidence_id, 2) as integer)').fetchall()
    total_new = stores['new'].execute('select count(*) from evidence').fetchone()[0]
    dropped = []
    for input_id, seq, text in stores['old'].execute('select input_id, seq, handover_json from handovers order by seq'):
        dropped += [(input_id, seq, local_id) for local_id, reason in json.loads(text).get('dropped') or [] if reason == 'no home']
    examples = ['## Statements no question took: three examples from each system', '',
            '**These are illustrations, not a matched test.** The two lists are different populations: statements the new system still',
            f'holds with no question at the week\'s end, and statements the old system discarded at the moment it read them. Each list is a random draw of three with one fixed seed ({SEED}).',
            '"Stored attribution" is the speaker the system recorded; nobody checked it. The passage is the system\'s stored quotation from the article.', '',
            f"**The new system keeps them.** In the store its judge reads, {len(unlinked)} of {total_new} statements have no question. The week's result page counts "
            f"389 of 569 at the reading step; {adapter['records dropped: no verified passage']} records were dropped on the way to the judge's store for want of a "
            'verified passage (`adapter-counts.json`), and the rest of the difference has not been traced.', '']
    for evidence_id, one_line, quote, who, seq in rng.sample(unlinked, 3):
        examples += [f'- `{evidence_id}` (article {seq} of the week; stored attribution: {who}): {one_line}', f'  - Stored passage: "{quote}"']
    examples += ['', f"**The old system throws them away.** Its log records {len(dropped)} statements dropped as \"no home\" (no question took them).", '']
    for input_id, seq, local_id in rng.sample(dropped, 3):
        row = archives['old'].execute("select answer_json from model_calls where purpose = 'extract' and request_json like ? order by call_id desc limit 1", (f'%{input_id}%',)).fetchone()
        statement = next((e for e in (json.loads(row[0]).get('evidence') or []) if e.get('id') == local_id), None) if row and row[0] else None
        if statement is None:
            raise SystemExit(f'the dropped statement {local_id} of article {seq} is not in the stored answer: refused')
        examples += [f"- `{local_id}` of article {seq} of the week (stored attribution: {statement.get('original_who') or statement.get('speaker') or 'none stored'}): {statement.get('one_line')}",
                f"  - Stored passage: \"{statement.get('quote')}\""]
    out += ['### 6. Statements no question took', '',
            f"The new system keeps them ({len(unlinked)} of {total_new} in the store its judge reads); the old system discards them when it reads them ({len(dropped)} in its log). "
            'Three examples of each, with their stored passages, are at the end of this page. They illustrate; they are not a matched test of what either system loses.', '']
    front_words = sum(len(line.split()) for line in out)
    out.insert(out.index('## Front page') + 1, '')
    out.insert(out.index('## Front page') + 2, f'The front page is about {round(front_words, -2)} words; the entries and the second page are for checking it.')
    front_characters = sum(len(line) + 1 for line in out)
    out += ['', '## All 22 entries', '', '### The eight matters (five listed by both teams, three by one)', '']
    out += matter_rows(matters)
    cited_out = ['# The same week, both systems: the statements each latest answer cites', '',
                 f'Second page of [`SIDE-BY-SIDE-WEEK.md`](SIDE-BY-SIDE-WEEK.md), built by the same script. For each question: the stored request of its',
                 'latest answer (the call\'s number in the run\'s archive and the request\'s sha256), then every statement that answer cites, with the',
                 'system\'s stored summary and its stored passage from the article. "Stored attribution" is the speaker the system recorded; nobody checked it.',
                 f"In the new system's store the judge's copy of a passage is cut at 400 characters ({adapter['quotes cut by the judge at 400 characters']} passages in this run, `adapter-counts.json`).", '']
    for system in ('old', 'new'):
        relative = (FOLDERS[system] / 'archive.sqlite').relative_to(ROOT)
        out += ['', f"### {NAMES[system]}: {len(entries[system])} questions", '']
        cited_out += [f"## {NAMES[system]}", '', f'Stored requests: `{relative}`, table `model_calls`.', '']
        for entry in entries[system]:
            out += [f"<a id=\"{entry['anchor']}\"></a>", '', f"#### {NAMES[system]} {entry['number']} (`{entry['view']}`): {entry['question']}", '',
                    f"- About: {entry['about']}; opened at article {entry['opened']} of the week; due {entry['due']}; {entry['links']} statements linked; judged {entry['judged']} times.",
                    '- Possible answers:']
            out += [f"  - {position} {label}" + (f": {condition}" if condition else '') for position, label, condition in entry['rungs']]
            out += [f"- **Latest answer ({entry['answer_day']}, article {entry['answer_seq']}): {chosen(entry)}**",
                    f"- Its reasons, as stored: {entry['reasons']}"]
            if entry['expects']:
                out.append(f"- What it expects to happen, as stored: {entry['expects']}")
            for team, verdict, why in question_marks(entry, own_ids):
                out.append(f"- {team} on the question: {verdict}. {why}")
            for (team, verdict, why), (team_key, _) in zip(answer_marks(entry), TEAMS):
                flagged = entry['marks'][team_key][1].get('bad_citations')
                out.append(f"- {team} on the latest answer against what the judge was shown: {verdict}. {why}" + (f" Cited statements flagged: {flagged}." if flagged else ''))
            if entry['separate']:
                out.append(f"- A separate reader, asked before the reading whether this answer is supported: **{entry['separate']['verdict']}**. {entry['separate'].get('why') or ''}")
            out += [f"- The {len(entry['cited'])} statements this answer cites, each with its stored passage: [{CITED_PAGE}]({CITED_PAGE}#{entry['anchor']}); stored request: call {entry['call_id']}.", '']
            cited_out += [f"<a id=\"{entry['anchor']}\"></a>", '', f"### {NAMES[system]} {entry['number']} (`{entry['view']}`): {entry['question']}", '',
                          f"- Latest answer ({entry['answer_day']}): {chosen(entry)}",
                          f"- Stored request: call {entry['call_id']}; request sha256 `{entry['request_sha256']}`.",
                          f"- Cites {len(entry['cited'])} of the {entry['links']} statements linked to the question:", '']
            for evidence_id, one_line, quote, who, tier, seq in entry['cited']:
                cited_out += [f"  - `{evidence_id}` (article {seq}; stored attribution: {who}; stored kind: {tier}): {one_line}", f"    - Stored passage: \"{quote}\""]
            cited_out.append('')
    out += [''] + examples
    (HERE / 'SIDE-BY-SIDE-WEEK.md').write_text('\n'.join(out) + '\n')
    (HERE / CITED_PAGE).write_text('\n'.join(cited_out) + '\n')
    cut = sum(1 for system in entries for entry in entries[system] for _, _, condition in entry['rungs'] if condition and len(condition) >= 70)
    print(f"written: front page {front_characters} characters; whole first page {sum(len(l) + 1 for l in out)}; second page {sum(len(l) + 1 for l in cited_out)}; "
          f"questions old {len(entries['old'])}, new {len(entries['new'])}; cited statements old {sum(len(e['cited']) for e in entries['old'])}, new {sum(len(e['cited']) for e in entries['new'])}; "
          f"conditions of 70 characters or more now printed in full: {cut}; answers both fail {len(both)}, one alone {len(one)}; new unlinked {len(unlinked)} of {total_new}; old no home {len(dropped)}")


if __name__ == '__main__':
    main()
