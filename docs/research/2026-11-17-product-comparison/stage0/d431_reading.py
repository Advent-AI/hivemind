"""D431's frozen-reference reading at 2026-07-14, printed beside the verdict and never a gate (DESIGN-1.6.md §3; D665).

D442's procedure, steps 3 to 6 (`clean-arch/e2e-comparison-2026-11-13/DESIGN.md`, "Procedure"), run as it was run then, on both systems'
six draws as they stood at 07-14. It compares the answers the systems actually gave; no adapter re-asks the ruler's question.

- **Step 3, the as-of state.** Every view whose `created_seq` is at most the store's last sequence of 07-14 (`days_completed`), closed
  views included, in creation order; then `service.state_as_of` at 07-14 for each. A store that does not record 07-14 as completed is
  refused. Where the store holds processing steps, the listing must equal `service.view_exists` at 07-14, or it is refused. A new-system
  view is joined to its unit by `clean_ladders.view_id` (split children included). Each view's stored unit is read as the system wrote
  it: the old system's `view_keys.unit`, the new system's checked answer `figure.unit` (one closed list in both: `hivemind/extraction.py`
  UNITS, `ladder/candidate-schema.json`; "n/a" and "other" name no unit).
- **Step 4, matching** (`clean-arch/unseeded-2026-11-10/MATCHING-v2.md` §1): each draw's views under a neutral run name and neutral ids
  (`extract_opened_prod.py`'s row shape, no view or thesis id), read by both families in closed sessions (`census_readers.run`). A reader
  says SAME when its relation is "same" (the precedent's derivation). A pair one family calls SAME and the other not goes to two third
  readers, one of each family, as the full run read it (`clean-arch/e2e-comparison-2026-11-13/READING-COMMITMENT.md`, "Families": "Third
  readers: one of each family on every difference"; council round 8): both SAME, SAME; both not, NOT SAME; otherwise unresolved. A ruler
  question's candidates (views either family called SAME) resolve as D442 point 4 says: any confirmed SAME, matched; else any unresolved,
  "unresolved"; else "not opened in the ruler's shape". A missing mark (a session void twice) is "not measured", never a split.
- **Step 5, eligibility** of each judged view of a graded question (D430): `same_question` and `same_due` by both families (the precedent's
  control-reader brief, questions 1 and 2 unchanged; the judged question carries its stored unit, shown "n/a" when none is stored or
  the stored word names no unit, so both systems' "no unit" words look the same; the output keeps the stored value), the same
  two third readers on each difference; the literal reading (the two due days equal) beside.
- **Step 6, outcomes**, the first that applies: (i) reader B's gold opens no view or gives no answer: "not graded"; (ii) matching
  unresolved: "unresolved"; (iii) "not opened in the ruler's shape"; (iv) several views matched SAME: the first created is judged, the
  others (and unresolved candidates) listed; (v) eligibility unresolved: "unresolved"; (vi) "opened, not eligible" with the reason;
  (vii) "no judgement" by 07-14; (viii) for a figure question, "no comparison (unit)" when the view's stored unit and the ruler question's
  unit differ or either cannot be established (no conversion; the ruler's unit texts are read by the closed table `RULER_UNITS`), then a
  chosen rung with no bound: "no comparison"; (ix) "agree" or "disagree" by the frozen scorer's rule: `prod_records.outcome` for the old
  system, `control_theses.agrees` (Stage B's count: "Ruled out" and "Still open" answer no) for the new. The decisive reading (a decided
  "no" makes a view not eligible whatever the other field) is printed beside (v).

    python3 d431_reading.py run <run root> <eligibility.json> <out folder> [--diagnostic]     # every session not yet answered, then the result
    python3 d431_reading.py result <run root> <eligibility.json> <out folder> [--diagnostic]  # the result from the stored answers only

Writes `<out>/d431-0714.json` and prints it as a table. The draw-to-run key is kept outside the repository (`mapping.KEY_FOLDER`). Every
prompt is rebuilt from the stores; a session is named by its prompt's sha256 and counts only for that prompt (a packet that changes, as
when a missing mark is filled in later, is a new session). Stores are opened read-only
(`mode=ro&immutable=1`) and must carry the fingerprints of the eligibility check (`eligibility.py`); a run that is not eligible is read
only with `--diagnostic` (the finished draws, under their own key).
"""
import concurrent.futures
import hashlib
import json
import random
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(HERE), str(HERE / 'census'), str(ROOT / 'src'), str(ROOT / 'clean-arch/e2e-comparison-2026-11-13'),
                str(ROOT / 'clean-arch/step4-2026-11-10/stage_b')]
import census_readers  # noqa: E402
import control_theses  # noqa: E402
import eligibility as eligibility_tool  # noqa: E402
import mapping  # noqa: E402
import prod_records  # noqa: E402
from census_merge import json_lines  # noqa: E402
from hivemind import service  # noqa: E402

DAY = '2026-07-14'
SEED = 20261117 + 3                      # the comparison's seed plus the design section (§3)
CONTROLS_A_PACKET = 4                    # as the precedent's eligibility packets
MATCHING_RULE = ROOT / 'clean-arch/unseeded-2026-11-10/MATCHING-v2.md'
EARLIER_RULINGS = ROOT / 'clean-arch/e2e-comparison-2026-11-13/full-matching/adjudication-earlier-rulings.md'
QUESTIONS_FILE = prod_records.GOLD_DIR / 'questions-v1.json'
RELATIONS = ('same', 'broader', 'narrower', 'overlapping', 'unrelated')
YES_NO = ('yes', 'no')
FIELDS = ('same_question', 'same_due')
NOT_OPENED = "not opened in the ruler's shape"
NO_UNIT = 'no comparison (unit)'
# The frozen ruler's unit texts (questions-v1.json), each read as a unit of the systems' closed list, or None when that list has no
# such unit (it cannot be established). A full match: any other text is refused.
RULER_UNITS = {'USD': 'USD', 'percent': 'percent', 'percent (75 means 75%)': 'percent',
               'percent change 2027 vs 2026 (10 means up 10%)': 'percent', 'percent growth 2026 vs 2025': 'percent',
               'USD per share': None, 'wafers per month': None}

# The precedent's run brief (`full-matching/reader-brief-run.md`), its words unchanged except that the material is given inline.
MATCH_BRIEF = """# Question identity reading for a measured run (read-only)

You decide, for each question a system opened by itself in one run, whether it is the same question as one of 23 reference questions.

**The material** is below, and you have no other:
- the run's opened questions (run, id, the item where opened, description, outcome, period);
- the 23 reference questions, each with its full entry;
- `MATCHING-v2.md`, the rule.

**The rule.** Apply MATCHING-v2.md §1, read in full.
- An opened question is the same as a reference question when the same reported figure or event settles both.
- Three kinds of extra wording do not separate them:
  - a part, programme or single deal of a reference total;
  - the same event under another deadline;
  - a later milestone, variant or parenthetical widening that the question's own check does not rest on.
- An amount held at a different date is not the same.
- A yes/no signing question beside an amount question stays apart.
- Extra scope that is its own check and could resolve on its own stays apart.

**For every opened question, write one line of JSON:**

{{"run": ..., "id": ..., "match": "q05" or "none", "relation": "same" | "broader" | "narrower" | "overlapping" | "unrelated", "reason": "<one sentence>"}}

Judge from the texts alone; do not consider how either question would be scored. Output only the JSON lines.

Return exactly {count} lines, one JSON object per line, in the order of the opened questions, and nothing else: no prose before or after,
no code fence.

## MATCHING-v2.md

{rule}

## The 23 reference questions, each with its full entry

{questions}

## Run {run}: the opened questions

{rows}
"""

# The precedent's third-reader brief (`full-matching/third-reader-brief.md`), the material given inline.
MATCH_THIRD_BRIEF = """# Third reader: disputed identities (read-only)

You decide, for each disputed pair below, whether the opened question is the SAME question as the named reference question.

The material is below, and you have no other: `MATCHING-v2.md` (the rule; read §1 in full), `adjudication-earlier-rulings.md` (earlier
rulings under the same rule), each reference question's full entry, and the disputed pairs.

For each pair, one JSON line: `{{"dispute": 1, "same": true|false, "reason": "<one sentence naming the rule text that decides>"}}`.
Judge from the texts and the rule alone. Output only the JSON lines.

Return exactly {count} lines, one JSON object per line, in dispute order, and nothing else: no prose before or after, no code fence.

## MATCHING-v2.md

{rule}

## adjudication-earlier-rulings.md

{rulings}

## The 23 reference questions, each with its full entry

{questions}

## The disputed pairs

{pairs}
"""

# The precedent's control-reader brief (`full-eligibility/control-reader-brief.md`), questions 1 and 2 unchanged; its third question
# (reader B's items shown to the judge) serves the loss trace, which this reading does not run.
ELIGIBILITY_RULES = """You are an independent reader. You have no material other than this brief and the packet below.

Each item of your packet pairs a **ruler question** (a question written by hand for an earlier, frozen measurement, with its
unit, due day and ladder of rungs) with a **judged question** the system wrote itself for a thesis it opened (its question, the
outcome it looks at, its unit as stored ("n/a" when none is stored), due day, year and rungs). You are not told either answer, and
you do not judge which answer is right.

For each item, answer two questions.

1. `same_question`: **yes** when the judged question asks what the ruler question asks: the same quantity measured the same way
   (the same total, scope and unit: not a part of it, a ceiling on it, another quantity or another unit), or the same event,
   for the same period. **no** otherwise. Wording may differ; a judged question that asks for more or less than the ruler's,
   or for another period, is **no**.
2. `same_due`: for an **event** (a yes-or-no question), **yes** only when the judged question's deadline is the ruler's
   deadline. For a **figure**, **yes** when the two due days both mark the publication of the same period's figure (for
   example, both the annual report of the same fiscal year, even if the two days differ); **no** otherwise.
"""

ELIGIBILITY_BRIEF = """# Reading the control questions (read-only)

""" + ELIGIBILITY_RULES + """
Return one JSON object per item, one per line, in packet order, and nothing else (no prose, no code fence):
`{{"control": 3, "same_question": "yes"|"no", "same_due": "yes"|"no", "why": "one sentence naming what decides each no"}}`.
There are {count} items.

## The packet

{packet}
"""

ELIGIBILITY_THIRD_BRIEF = """# Third reader: the disputed points of the control questions (read-only)

""" + ELIGIBILITY_RULES + """
You are a third reader. Two readers differed on the points each item lists under `points_to_rule` (`same_question` or `same_due`); you
are not given their answers. For each point, answer that one question afresh by the rules above and return one JSON object per point,
one per line, in packet order, and nothing else (no prose, no code fence):
`{{"control": 3, "field": "same_due", "ruling": "yes"|"no", "why": "one sentence"}}`. There are {count} points.

## The packet

{packet}
"""


def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def connect(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- step 3: the as-of state

def last_sequence(conn, day=DAY):
    """The store's last sequence of the day, as its writer recorded the day's completion."""
    rows = conn.execute('select seq from days_completed where day = ?', (day,)).fetchall()
    if len(rows) != 1:
        raise SystemExit(f'refused: the store records {len(rows)} completions of {day} (its last completed day is '
                         f'{conn.execute("select max(day) from days_completed").fetchone()[0]}); its state on {day} cannot be read')
    return rows[0]['seq']


def ladder_unit(conn, view_id):
    """A new-system view's unit: its one `clean_ladders` row (a split child's row carries its year), and the checked answer's figure unit."""
    columns = {row[1] for row in conn.execute('pragma table_info(clean_ladders)')}
    if not columns:
        raise SystemExit('refused: a new-system store without clean_ladders')
    rows = conn.execute('select * from clean_ladders where view_id = ?', (view_id,)).fetchall()
    if len(rows) != 1:
        raise SystemExit(f'refused: view {view_id} has {len(rows)} clean_ladders rows, not one')
    row = dict(rows[0])
    checked = json.loads(row['checked_answer']) if row.get('checked_answer') else {}
    figure = (checked.get('ladder') or {}).get('figure')
    return {'thesis': row['thesis_id'], 'period': row.get('period') or '', 'unit': figure.get('unit') if figure else None}


def listed_views(conn, system, day=DAY, last_seq=None):
    """(the last sequence used, where it came from, the views created on or before the day in creation order, closed ones included,
    each with its rungs and its state as of the day). `last_seq` is given only for a stored store that records no completed day."""
    source = 'given' if last_seq is not None else 'days_completed'
    last = last_seq if last_seq is not None else last_sequence(conn, day)
    views = []
    for row in conn.execute('select rowid as created_order, * from views order by created_seq, rowid'):
        record = dict(row)
        if record['created_seq'] > last:
            continue
        state = service.state_as_of(conn, record['view_id'], day)
        rungs = [dict(r) for r in conn.execute('select position, label, condition, lo, hi from rungs where view_id = ? order by position',
                                               (record['view_id'],))]
        view = {key: record[key] for key in ('view_id', 'created_seq', 'created_order', 'created_from_input', 'question', 'looks_at',
                                             'due_day', 'year', 'kind')}
        view['rungs'] = rungs
        view['state'] = None if state is None else {'position': state['position'], 'judgement_day': state['judgement_day'],
                                                    'since_day': state['since_day'], 'rounds': state['rounds']}
        if system == 'new':
            view.update(ladder_unit(conn, record['view_id']))
        else:
            key = conn.execute('select unit from view_keys where view_id = ?', (record['view_id'],)).fetchone()
            view['unit'] = key['unit'] if key else None
        views.append(view)
    if conn.execute('select 1 from processing_steps limit 1').fetchone() is not None:
        by_product = {r['view_id'] for r in conn.execute('select * from views') if service.view_exists(conn, dict(r), day)}
        if by_product != {v['view_id'] for v in views}:
            raise SystemExit(f'refused: the listing by sequence differs from service.view_exists on {day}: '
                             f'{sorted(by_product ^ {v["view_id"] for v in views})}')
    return last, source, views


def read_store(entry, day=DAY):
    """One draw's store as of the day: {'system', 'views' path, 'last_sequence', 'from', 'listed'}. A draw with no store (a new
    draw whose judge was skipped: no question opened) lists nothing."""
    if entry['views'] is None:
        return {'system': entry['system'], 'views': None, 'last_sequence': None, 'from': 'no store (no question opened)', 'listed': []}
    conn = connect(entry['views'])
    try:
        last, source, views = listed_views(conn, entry['system'], day, entry.get('last_seq'))
    finally:
        conn.close()
    return {'system': entry['system'], 'views': str(entry['views']), 'last_sequence': last, 'from': source, 'listed': views}


# ---------- the frozen inputs

def frozen_inputs():
    gold, questions = prod_records.gold_and_questions()          # refuses a gold that is not the frozen one
    entries = json.loads(QUESTIONS_FILE.read_text(encoding='utf-8'))['questions']
    unread = sorted({q['unit'] for q in entries} - set(RULER_UNITS) - {'yes/no'})
    if unread:
        raise SystemExit(f'refused: ruler units {unread} are not in RULER_UNITS')
    return {'gold': gold, 'questions': questions, 'entries': entries,
            'graded_subset': [q['id'] for q in entries if q.get('covers_must_open')],
            'rule': MATCHING_RULE.read_text(), 'rulings': EARLIER_RULINGS.read_text(),
            'sha256': {'gold-v1.json': prod_records.GOLD_SHA256,
                       'questions-v1.json': hashlib.sha256(QUESTIONS_FILE.read_bytes()).hexdigest(),
                       'MATCHING-v2.md': hashlib.sha256(MATCHING_RULE.read_bytes()).hexdigest(),
                       'adjudication-earlier-rulings.md': hashlib.sha256(EARLIER_RULINGS.read_bytes()).hexdigest()}}


def graded(frozen, question_id):
    """(i): reader B's gold opens a view and gives an answer."""
    entry = frozen['gold'][question_id]
    return not entry.get('no_view') and bool(entry.get('implied_outcome'))


# ---------- sessions

def session_name(phase, family, prompt):
    """A session is named by its phase, family and prompt: a packet that changes (a mark filled in later) is a new session."""
    return f'{phase}-{family}-{sha256_text(prompt)[:12]}'


def session(out, name, family, prompt, problem):
    """One closed session, reused when already answered on this very prompt; a void answer is retried once, then recorded missing."""
    path = Path(out) / 'sessions' / f'{name}.json'
    digest = sha256_text(prompt)
    if path.exists():
        saved = json.loads(path.read_text())
        if saved['prompt_sha256'] != digest:
            raise SystemExit(f'refused: session {name} holds an answer to another prompt')
        if saved['answer'] is not None:
            return saved['answer']
    voids, answer = [], None
    for _ in (1, 2):
        answer, void = census_readers.run(family, prompt)
        if answer and not void:
            void = problem(answer)
        if not void:
            break
        voids.append(void)
        answer = None
    path.parent.mkdir(parents=True, exist_ok=True)
    (Path(out) / 'prompts').mkdir(exist_ok=True)
    (Path(out) / 'prompts' / f'{name}.md').write_text(prompt)
    path.write_text(json.dumps({'name': name, 'family': family, 'prompt_sha256': digest, 'answer': answer, 'voids': voids},
                               indent=1, ensure_ascii=False) + '\n')
    return answer


def stored_answer(out, name, prompt):
    """A session's answer for the result: None when missing; refused when it answered another prompt."""
    path = Path(out) / 'sessions' / f'{name}.json'
    if not path.exists():
        return None
    saved = json.loads(path.read_text())
    if saved['prompt_sha256'] != sha256_text(prompt):
        raise SystemExit(f'refused: session {name} holds an answer to another prompt')
    return saved['answer']


def run_sessions(out, jobs):
    """jobs: [(name, family, prompt, problem)], run six at a time."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        answers = list(pool.map(lambda job: session(out, *job), jobs))
    for (name, *_), answer in zip(jobs, answers):
        print(f'{name}: {"answered" if answer is not None else "MISSING after two attempts"}', flush=True)


def rows_problem(answer, key, expected, check):
    """Why an answer is void: it must hold each expected key exactly once, each row passing `check`."""
    rows = [r for r in json_lines(answer) if isinstance(r, dict)]
    found = [r.get(key) for r in rows]
    if sorted(map(str, found)) != sorted(map(str, expected)):
        return f'{len(rows)} rows for {len(expected)} expected, or a {key} missing or repeated'
    for r in rows:
        problem = check(r)
        if problem:
            return f'{key} {r.get(key)}: {problem}'
    return None


# ---------- step 4: matching

def draw_labels(draws):
    """{draw: neutral run name}: the draws in a seeded order, named r1.. (as the precedent's packets)."""
    order = list(draws)
    random.Random(SEED).shuffle(order)
    return {draw: f'r{n}' for n, draw in enumerate(order, 1)}


def opened_rows(run, views):
    """The precedent's row shape (`extract_opened_prod.py`), under neutral ids t01.. in creation order."""
    return [{'run': run, 'id': f't{n:02d}', 'article': v['created_from_input'], 'description': v['question'], 'outcome': v['looks_at'],
             'period': f"year {v['year']}; due {v['due_day']}"} for n, v in enumerate(views, 1)]


def match_prompt(frozen, run, rows):
    return MATCH_BRIEF.format(count=len(rows), rule=frozen['rule'], run=run,
                              questions=json.dumps(frozen['entries'], indent=1, ensure_ascii=False),
                              rows=json.dumps(rows, indent=1, ensure_ascii=False))


def match_problem(rows, ruler_ids):
    def check(r):
        if r.get('run') != rows[0]['run']:
            return f"run {r.get('run')!r}"
        if r.get('match') not in (*ruler_ids, 'none') or r.get('relation') not in RELATIONS:
            return f"match {r.get('match')!r}, relation {r.get('relation')!r}"
        if not isinstance(r.get('reason'), str) or not r['reason'].strip():
            return 'no reason'
        return None
    return lambda answer: rows_problem(answer, 'id', [r['id'] for r in rows], check)


def same_marks(answer):
    """{neutral id: ruler question} of the rows a reader calls SAME: relation "same" and a ruler question named."""
    return {r['id']: r['match'] for r in json_lines(answer) if r.get('relation') == 'same' and r.get('match') not in (None, 'none')}


def pair_marks(answers):
    """{(neutral id, question): {family: bool}} for every pair either family calls SAME; None when a family's answer is missing."""
    if any(answers[family] is None for family in census_readers.FAMILIES):
        return None
    marks = {family: same_marks(answers[family]) for family in census_readers.FAMILIES}
    pairs = {}
    for family, same in marks.items():
        for neutral, question in same.items():
            pairs.setdefault((neutral, question), {})
    for (neutral, question), by in pairs.items():
        for family in census_readers.FAMILIES:
            by[family] = marks[family].get(neutral) == question
    return pairs


def match_third_prompt(frozen, disputes):
    pairs = [{'dispute': n, 'opened_question': {k: d['row'][k] for k in ('description', 'outcome', 'period')}, 'reference_question': d['question']}
             for n, d in enumerate(disputes, 1)]
    return MATCH_THIRD_BRIEF.format(count=len(pairs), rule=frozen['rule'], rulings=frozen['rulings'],
                                    questions=json.dumps(frozen['entries'], indent=1, ensure_ascii=False),
                                    pairs=json.dumps(pairs, indent=1, ensure_ascii=False))


def match_third_problem(count):
    def check(r):
        return None if isinstance(r.get('same'), bool) and isinstance(r.get('reason'), str) and r['reason'].strip() else 'same is true or false, with a reason'
    return lambda answer: rows_problem(answer, 'dispute', list(range(1, count + 1)), check)


def ruling(values):
    """Two third readers' rulings: agreed, or unresolved; a missing ruling is not measured."""
    if any(v is None for v in values):
        return 'not measured'
    return values[0] if values[0] == values[1] else 'unresolved'


# ---------- step 5: eligibility

def ruler_unit(frozen, question_id):
    """The ruler question's unit in the systems' closed list, None when it cannot be established; an unknown text is refused."""
    text = frozen['questions'][question_id]['unit']
    if text not in RULER_UNITS:
        raise SystemExit(f'refused: {question_id} has the unit {text!r}, which RULER_UNITS does not read')
    return RULER_UNITS[text]


def same_unit(frozen, question_id, view):
    """Numeric agreement may be compared: the ruler's unit is established and equals the view's stored unit ("n/a", "other" or no
    stored unit never equal one)."""
    unit = ruler_unit(frozen, question_id)
    return unit is not None and view['unit'] == unit


def control_item(number, frozen, question_id, view):
    ruler = frozen['questions'][question_id]
    judged = {key: view[key] for key in ('question', 'looks_at', 'due_day', 'year', 'kind')}
    judged['unit'] = view['unit'] if view['unit'] not in (None, 'other') else 'n/a'     # both systems' "no unit" words look alike
    return {'control': number, 'ruler_question': {key: ruler[key] for key in ('question', 'unit', 'due_day', 'rungs')},
            'judged_question': judged, 'judged_rungs': view['rungs']}


def eligibility_problem(controls):
    def check(r):
        if set(r) != {'control', 'same_question', 'same_due', 'why'} or r['same_question'] not in YES_NO or r['same_due'] not in YES_NO:
            return 'a row is {control, same_question, same_due, why}, each answer "yes" or "no"'
        return None if isinstance(r['why'], str) and r['why'].strip() else 'no why'
    return lambda answer: rows_problem(answer, 'control', controls, check)


def eligibility_third_problem(points):
    def check(r):
        if set(r) != {'control', 'field', 'ruling', 'why'} or r['ruling'] not in YES_NO or r['field'] not in FIELDS:
            return 'a ruling is {control, field, ruling "yes" or "no", why}'
        return None
    def problem(answer):
        rows = [r for r in json_lines(answer) if isinstance(r, dict)]
        named = sorted((str(r.get('control')), str(r.get('field'))) for r in rows)
        if named != sorted((str(c), f) for c, f in points):
            return f'{len(rows)} rulings for {len(points)} points, or a point missing or repeated'
        return next((p for p in map(check, rows) if p), None)
    return problem


# ---------- the reading

class Reading:
    """Everything the sessions are asked and everything the result counts, rebuilt from the stores, the frozen files and the key."""

    def __init__(self, stores, out, key_path, diagnostic=False):
        self.out, self.diagnostic = Path(out), diagnostic
        marker = self.out / 'DIAGNOSTIC'
        if self.out.exists() and any(self.out.iterdir()) and marker.exists() != diagnostic:
            raise SystemExit(f'refused: {self.out} holds a {"diagnostic" if marker.exists() else "release"} reading')
        self.frozen = frozen_inputs()
        self.draws = {draw: read_store(entry) for draw, entry in stores.items()}
        labels = draw_labels(self.draws)
        key_path = Path(key_path)
        if key_path.exists():
            if json.loads(key_path.read_text()) != labels:
                raise SystemExit(f'refused: {key_path} names other draws than this reading')
        else:
            key_path.parent.mkdir(parents=True, exist_ok=True)
            key_path.write_text(json.dumps(labels, indent=1) + '\n')
        self.labels = labels
        self.out.mkdir(parents=True, exist_ok=True)
        if diagnostic:
            marker.write_text('finished draws of a run that cannot give a release verdict (plan §1.4 item 10)\n')
        self.rows = {draw: opened_rows(labels[draw], d['listed']) for draw, d in self.draws.items()}
        self.view_of = {draw: {row['id']: view for row, view in zip(self.rows[draw], d['listed'])} for draw, d in self.draws.items()}
        self.ruler_ids = [q['id'] for q in self.frozen['entries']]
        self.used = {}                   # session name -> answer or None, for every session the result read

    def answer(self, phase, family, prompt):
        name = session_name(phase, family, prompt)
        self.used[name] = stored_answer(self.out, name, prompt)
        return self.used[name]

    # matching
    def match_jobs(self):
        jobs = []
        for draw, rows in sorted(self.rows.items(), key=lambda item: self.labels[item[0]]):
            if rows:
                prompt = match_prompt(self.frozen, self.labels[draw], rows)
                jobs += [(session_name(f'match-{self.labels[draw]}', family, prompt), family, prompt, match_problem(rows, self.ruler_ids))
                         for family in census_readers.FAMILIES]
        return jobs

    def first_marks(self):
        """{draw: {(neutral id, question): {family: bool}} or None when a family's session is missing}."""
        marks = {}
        for draw, rows in self.rows.items():
            if not rows:
                marks[draw] = {}
                continue
            prompt = match_prompt(self.frozen, self.labels[draw], rows)
            answers = {family: self.answer(f'match-{self.labels[draw]}', family, prompt) for family in census_readers.FAMILIES}
            marks[draw] = pair_marks(answers)
        return marks

    def match_disputes(self, marks):
        disputes = []
        for draw in sorted(self.rows, key=self.labels.get):
            rows = {row['id']: row for row in self.rows[draw]}
            for (neutral, question), by in sorted((marks.get(draw) or {}).items()):
                if len(set(by.values())) == 2:
                    disputes.append({'draw': draw, 'id': neutral, 'question': question, 'row': rows[neutral]})
        return disputes

    def match_third_jobs(self, disputes):
        if not disputes:
            return []
        prompt = match_third_prompt(self.frozen, disputes)
        return [(session_name('match-third', family, prompt), family, prompt, match_third_problem(len(disputes)))
                for family in census_readers.FAMILIES]

    def pair_status(self):
        """{draw: {(neutral id, question): 'same' | 'not same' | 'unresolved' | 'not measured'}}, or a draw's value None when its first
        matching is missing."""
        marks = self.first_marks()
        disputes = self.match_disputes(marks)
        rulings = {}
        if disputes:
            prompt = match_third_prompt(self.frozen, disputes)
            for family in census_readers.FAMILIES:
                answer = self.answer('match-third', family, prompt)
                by_number = {r['dispute']: r['same'] for r in json_lines(answer)} if answer is not None else {}
                for n, dispute in enumerate(disputes, 1):
                    rulings.setdefault((dispute['draw'], dispute['id'], dispute['question']), []).append(by_number.get(n))
        status = {}
        for draw, pairs in marks.items():
            if pairs is None:
                status[draw] = None
                continue
            status[draw] = {}
            for (neutral, question), by in pairs.items():
                if all(by.values()):
                    status[draw][(neutral, question)] = 'same'
                else:
                    decided = ruling(rulings[(draw, neutral, question)])
                    status[draw][(neutral, question)] = {True: 'same', False: 'not same'}.get(decided, decided)
        return status

    def matched(self):
        """{draw: {question: {'resolution', 'judged', 'listed', 'candidates'}}} by D442 point 4 and step 6 (iv)."""
        out = {}
        for draw, pairs in self.pair_status().items():
            out[draw] = {}
            for question in self.ruler_ids:
                if pairs is None:
                    out[draw][question] = {'resolution': 'not measured', 'detail': 'a matching session is missing', 'judged': None,
                                           'listed': [], 'candidates': []}
                    continue
                candidates = sorted(((self.view_of[draw][neutral], status) for (neutral, q), status in pairs.items() if q == question),
                                    key=lambda item: (item[0]['created_seq'], item[0]['created_order']))
                confirmed = [view for view, status in candidates if status == 'same']
                described = [{'view': view['view_id'], 'status': status} for view, status in candidates]
                if confirmed:
                    entry = {'resolution': 'matched', 'judged': confirmed[0],
                             'listed': [c for c in described if c['view'] != confirmed[0]['view_id'] and c['status'] != 'not same']}
                elif any(status == 'not measured' for _, status in candidates):
                    entry = {'resolution': 'not measured', 'detail': 'a third matching session is missing', 'judged': None, 'listed': []}
                elif any(status == 'unresolved' for _, status in candidates):
                    entry = {'resolution': 'unresolved', 'detail': 'matching: the third readers split', 'judged': None, 'listed': []}
                else:
                    entry = {'resolution': NOT_OPENED, 'judged': None, 'listed': []}
                entry['candidates'] = described
                out[draw][question] = entry
        return out

    # eligibility
    def controls(self, matched):
        """[(draw, question, view)] of every graded question's judged view, in a seeded order: control n is the n-th."""
        found = [(draw, question, entry['judged']) for draw in sorted(matched, key=self.labels.get) for question, entry in matched[draw].items()
                 if entry['resolution'] == 'matched' and graded(self.frozen, question)]
        random.Random(SEED).shuffle(found)
        return found

    def packets(self, controls):
        items = [control_item(n, self.frozen, question, view) for n, (_, question, view) in enumerate(controls, 1)]
        return [items[start:start + CONTROLS_A_PACKET] for start in range(0, len(items), CONTROLS_A_PACKET)]

    def eligibility_jobs(self, controls):
        jobs = []
        for packet in self.packets(controls):
            prompt = ELIGIBILITY_BRIEF.format(count=len(packet), packet=json.dumps(packet, indent=1, ensure_ascii=False))
            jobs += [(session_name('eligibility', family, prompt), family, prompt, eligibility_problem([item['control'] for item in packet]))
                     for family in census_readers.FAMILIES]
        return jobs

    def first_eligibility(self, controls):
        """{control: {family: row or None}}."""
        rows = {}
        for packet in self.packets(controls):
            prompt = ELIGIBILITY_BRIEF.format(count=len(packet), packet=json.dumps(packet, indent=1, ensure_ascii=False))
            for family in census_readers.FAMILIES:
                answer = self.answer('eligibility', family, prompt)
                by_control = {r['control']: r for r in json_lines(answer)} if answer is not None else {}
                for item in packet:
                    rows.setdefault(item['control'], {})[family] = by_control.get(item['control'])
        return rows

    def eligibility_points(self, controls, rows):
        return [(control, field) for control in sorted(rows) for field in FIELDS
                if all(rows[control].values()) and rows[control]['codex'][field] != rows[control]['claude'][field]]

    def eligibility_third_prompt(self, controls, points):
        items = {item['control']: item for packet in self.packets(controls) for item in packet}
        packet = [dict(items[control], points_to_rule=[f for c, f in points if c == control]) for control in sorted({c for c, _ in points})]
        return ELIGIBILITY_THIRD_BRIEF.format(count=len(points), packet=json.dumps(packet, indent=1, ensure_ascii=False))

    def eligibility_third_jobs(self, controls):
        points = self.eligibility_points(controls, self.first_eligibility(controls))
        if not points:
            return []
        prompt = self.eligibility_third_prompt(controls, points)
        return [(session_name('eligibility-third', family, prompt), family, prompt, eligibility_third_problem(points))
                for family in census_readers.FAMILIES]

    def decided_eligibility(self, controls):
        """{control: {'same_question', 'same_due'}}, each 'yes', 'no', 'unresolved' or 'not measured'."""
        rows = self.first_eligibility(controls)
        points = self.eligibility_points(controls, rows)
        rulings = {}
        if points:
            prompt = self.eligibility_third_prompt(controls, points)
            for family in census_readers.FAMILIES:
                answer = self.answer('eligibility-third', family, prompt)
                found = {(r['control'], r['field']): r['ruling'] for r in json_lines(answer)} if answer is not None else {}
                for point in points:
                    rulings.setdefault(point, []).append(found.get(point))
        decided = {}
        for control, by in rows.items():
            decided[control] = {}
            for field in FIELDS:
                if not all(by.values()):
                    decided[control][field] = 'not measured'
                elif by['codex'][field] == by['claude'][field]:
                    decided[control][field] = by['codex'][field]
                else:
                    decided[control][field] = ruling(rulings[(control, field)])
        return decided

    # step 6
    def answer_vs_reader_b(self, draw, question, view):
        """(vii)–(ix) for the judged view, whatever its eligibility: 'no judgement', 'no comparison (unit)', 'no comparison', 'agree'
        or 'disagree'. The frozen rule is applied first (and the old system's two readings of it must agree); a figure answer is then
        withheld when the units are not the same."""
        system = self.draws[draw]['system']
        state = view['state']
        record = {'last_judgement': None if state is None else {'rung': state['position'], 'day': state['judgement_day']},
                  'gold_open': False, 'rungs': view['rungs'], 'gold_answer': self.frozen['gold'][question]['implied_outcome'],
                  'ruler': {'unit': self.frozen['questions'][question]['unit']}}
        if state is None:
            stage_b = 'no judgement'
        else:
            agreed = control_theses.agrees(record)
            stage_b = 'no comparison' if agreed is None else ('agree' if agreed else 'disagree')
        if system == 'old':
            scorer = prod_records.outcome(self.draws[draw]['views'], question, view['view_id'], DAY, self.frozen['gold'],
                                          self.frozen['questions'])['outcome']
            if scorer != stage_b:
                raise SystemExit(f'refused: {draw} {view["view_id"]} {question}: prod_records reads {scorer}, the state as of {DAY} reads {stage_b}')
        figure = self.frozen['questions'][question]['unit'] != 'yes/no'
        if stage_b != 'no judgement' and figure and not same_unit(self.frozen, question, view):
            return NO_UNIT
        return stage_b

    def result(self):
        self.used = {}
        matched = self.matched()
        controls = self.controls(matched)
        decided = self.decided_eligibility(controls)
        control_of = {(draw, question): n for n, (draw, question, _) in enumerate(controls, 1)}
        outcomes = {}
        for question in self.ruler_ids:
            outcomes[question] = {}
            for draw in self.draws:
                entry = matched[draw][question]
                record = {'candidates': entry['candidates']}
                if not graded(self.frozen, question):
                    gold = self.frozen['gold'][question]
                    record.update(outcome='not graded', detail='reader B opens no view' if gold.get('no_view') else 'reader B gives no answer')
                elif entry['resolution'] != 'matched':
                    record.update(outcome=entry['resolution'], detail=entry.get('detail', ''))
                else:
                    view = entry['judged']
                    fields = decided[control_of[(draw, question)]]
                    literal = view['due_day'] == self.frozen['questions'][question]['due_day']
                    answer = self.answer_vs_reader_b(draw, question, view)
                    record.update(judged_view=view['view_id'], listed_views=entry['listed'], due_day=view['due_day'], state=view['state'],
                                  eligibility=dict(fields, literal_due_same=literal), answer_vs_reader_b=answer,
                                  unit=view['unit'], ruler_unit=self.frozen['questions'][question]['unit'])
                    if self.draws[draw]['system'] == 'new':
                        record.update(thesis=view['thesis'], period=view['period'])
                    values = [fields[f] for f in FIELDS]
                    noes = [f.split('_')[1] for f in FIELDS if fields[f] == 'no']
                    if 'not measured' in values:
                        record.update(outcome='not measured', detail='an eligibility session is missing')
                    elif 'unresolved' in values:
                        record.update(outcome='unresolved', detail='eligibility: the third readers split',
                                      decisive_reading=f"opened, not eligible ({' '.join(noes)})" if noes else 'unresolved')
                    elif noes:
                        record.update(outcome='opened, not eligible', detail=' '.join(noes))
                    else:
                        record.update(outcome=answer, detail='')
                    literal_eligible = fields['same_question'] if fields['same_question'] != 'yes' else ('yes' if literal else 'no')
                    record['literal_reading'] = answer if literal_eligible == 'yes' else f'eligible: {literal_eligible}'
                outcomes[question][draw] = record
        subset = self.frozen['graded_subset']
        agreements = {}
        for draw, store in self.draws.items():
            agreeing = [q for q in subset if outcomes[q][draw]['outcome'] == 'agree']
            literal = [q for q in subset if outcomes[q][draw].get('literal_reading') == 'agree']
            agreements[draw] = {'system': store['system'], 'agree': len(agreeing), 'of': len(subset), 'questions': agreeing,
                                'literal_reading_agree': len(literal), 'literal_reading_questions': literal}
        missing = sorted(name for name, answer in self.used.items() if answer is None)
        return {'reading': f"D431's frozen-reference reading at {DAY} (DESIGN-1.6.md §3; D442 steps 3 to 6); printed beside, not a gate",
                'diagnostic': self.diagnostic, 'day': DAY, 'graded_subset': subset, 'sources': self.frozen['sha256'],
                'draws': {draw: {k: v for k, v in store.items() if k != 'listed'} | {'views_listed': [
                    {k: view.get(k) for k in ('view_id', 'created_seq', 'due_day', 'question', 'thesis', 'period', 'unit') if k in view}
                    | {'state': view['state']} for view in store['listed']]} for draw, store in self.draws.items()},
                'outcomes': outcomes, 'agreements': agreements, 'missing_sessions': missing}


def read(reading, run=True):
    """Run every phase's sessions not yet answered (when `run`), then write and print the result."""
    if run:
        run_sessions(reading.out, reading.match_jobs())
        run_sessions(reading.out, reading.match_third_jobs(reading.match_disputes(reading.first_marks())))
        controls = reading.controls(reading.matched())
        run_sessions(reading.out, reading.eligibility_jobs(controls))
        run_sessions(reading.out, reading.eligibility_third_jobs(controls))
    result = reading.result()
    (reading.out / 'd431-0714.json').write_text(json.dumps(result, indent=1, ensure_ascii=False) + '\n')
    print_result(result)
    return result


def print_result(result):
    draws = list(result['draws'])
    print(result['reading'] + (' [DIAGNOSTIC]' if result['diagnostic'] else ''))
    for draw in draws:
        d = result['draws'][draw]
        print(f"{draw} ({d['system']}): {len(d['views_listed'])} views listed at {result['day']} (last sequence {d['last_sequence']}, from {d['from']})")
    for question, by_draw in result['outcomes'].items():
        marker = '*' if question in result['graded_subset'] else ' '
        cells = []
        for draw in draws:
            r = by_draw[draw]
            cell = r['outcome'] + (f" ({r['detail']})" if r.get('detail') else '') + (f" {r['judged_view']}" if r.get('judged_view') else '')
            cells.append(f'{draw}: {cell}')
        print(f'{marker}{question}  ' + ' | '.join(cells))
    for draw, a in result['agreements'].items():
        print(f"{draw} ({a['system']}): agree {a['agree']} of {a['of']} graded {a['questions']}; literal reading {a['literal_reading_agree']}")
    if result['missing_sessions']:
        print('missing sessions (their marks are not measured):', ', '.join(result['missing_sessions']))


def stores_of_run(run_root, eligibility_path, diagnostic):
    """{draw: {'system', 'views'}} from each draw's run record (`mapping.store_paths`), every store checked against the eligibility
    check's fingerprint. A run that is not eligible is read only as a diagnostic, of the draws that finished."""
    eligibility = json.loads(Path(eligibility_path).read_text())
    if not eligibility.get('eligible') and not diagnostic:
        raise SystemExit(f"refused: the draws are not eligible: {eligibility.get('problems')}")
    stores = {}
    for draw in mapping.DRAWS:
        try:
            paths = mapping.store_paths(run_root, draw)
        except SystemExit as refusal:
            if not diagnostic:
                raise
            print(f'{draw} left out of the diagnostic: {refusal}')
            continue
        if paths is not None:
            recorded = eligibility['draws'].get(draw, {}).get('stores', {}).get('views.sqlite', {}).get('sha256')
            if recorded is None or eligibility_tool.sha256(paths[0]) != recorded:
                raise SystemExit(f'refused: {paths[0]} is not fingerprinted by the eligibility check, or changed since')
        stores[draw] = {'system': 'new' if draw.startswith('new') else 'old', 'views': paths[0] if paths else None}
    return stores


if __name__ == '__main__':
    if len(sys.argv) < 5 or sys.argv[1] not in ('run', 'result'):
        raise SystemExit(__doc__)
    diagnostic = '--diagnostic' in sys.argv[5:]
    key = mapping.KEY_FOLDER / ('d431-key-diagnostic.json' if diagnostic else 'd431-key.json')
    reading = Reading(stores_of_run(sys.argv[2], sys.argv[3], diagnostic), sys.argv[4], key, diagnostic)
    read(reading, run=sys.argv[1] == 'run')
