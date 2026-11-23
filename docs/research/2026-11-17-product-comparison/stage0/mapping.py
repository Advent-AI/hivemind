"""The blind mapping of matters to each system-draw's questions (verdict-rule.json `covers` and `same_question`; plan §1.4 items 2–3;
week reading A2's form, `docs/research/2026-11-14-use-acceptance/week/brief-A2.md`). Every session is closed (census_readers.run).

    python3 mapping.py export <run root> <out folder> <eligibility.json>   # each draw's library under a random label; key kept outside
    python3 mapping.py read <out folder>                   # both families map every matter for every library; duplicates marked
    python3 mapping.py third <out folder>                  # a third reader of each family on every matter-question the families split on
    python3 mapping.py result <out folder>                 # mapping.json: covers true / false / "split" per matter and question; distinct bets

Covers: both families mark the question `opened`, or `narrower` with both saying it carries the matter's main outcome. A question one family
marks covering and the other not goes to two third readers; covering when both say yes, not covering when both say no, otherwise "split".
A duplicate is the later-opened question of a same-bet pair; "duplicates_both" counts those both families mark, "duplicates_split" those one
marks. Which question of a named pair is the later one is decided by code from the library's opening order, not by the reader.

Ids: each library is exported with neutral ids Q1..Qn in opening order (the system's own ids differ in form between the systems); the
system's id is kept as `source_id` beside it, and the guardrail sample draws from the system's ids as the frozen rule says (D675).
An answer naming an id the library does not hold, or a matter twice, or `opened` with no id, or `narrower` without a main-outcome judgement,
is void; a disagreement without both third readers' marks is refused. Third readers also see the article the question was opened from
(week reading A2's form), for coverage that turns on a date or period. Export refuses without a passing `eligibility.py` output whose store
fingerprints match the stores it reads.
"""
import concurrent.futures
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE / 'census')]
import build_cards  # noqa: E402
import census_readers  # noqa: E402
from census_merge import json_lines  # noqa: E402

FAMILIES = census_readers.FAMILIES
MATTERS = HERE / 'census' / 'matters.json'
ITEMS = Path('/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/items-comparison.sqlite')
KEY_FOLDER = Path.home() / '.hivemind-keys' / 'comparison-2026-11-17'
DRAWS = ['new-1', 'new-2', 'new-3', 'old-1', 'old-2', 'old-3']

READ = """# Blind reader: which of these big matters does this library hold a question on? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Below are the big matters readers listed from the news of 2026-09-07 to 09-20, each with
an example question, and the library of one research system as it stood on 2026-09-20: every question it held, open or closed, with its id,
due day and possible answers. Systems write their questions in different styles; ignore style.

For each matter choose one:
- **opened**: a question the same outcome would settle, in any reasonable wording, period or date (name its id);
- **narrower**: a question on part of the matter (name its id, and say whether it carries the matter's main outcome);
- **broader**: the matter is folded into a wider question;
- **missed**: no question on it.

Do not count a reasonable alternative shape as missed: a different deadline for the same outcome, or one year of a two-year matter, is
"opened" or "narrower" with a note. Several questions may cover one matter: name them all.

Then list the library's duplicates: two questions of the library are the same bet when the same outcome settles both and their answers
cannot move apart (another year of a figure is another bet). Of such a pair, the later-opened question is the duplicate.

Write one JSON object per line, and nothing else:
- per matter: {{"matter": "M01", "status": "opened|narrower|broader|missed", "ids": ["..."], "main_outcome": true|false|null, "note": "<= 30 words"}}
- per duplicate: {{"duplicate": "<later id>", "of": "<earlier id>"}}

## The matters

{matters}

## Library {label}

{library}
"""

THIRD = """# Third reader: does this question cover this matter? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Two readers disagreed on whether the question below covers the matter below. A question
covers a matter when the same outcome would settle both (any reasonable wording, period or date), or when it is on part of the matter and
carries the matter's main outcome. Answer from the two texts.

Write one JSON object and nothing else: {{"covers": true|false, "why": "<= 40 words"}}

## The matter

{matter}

## The question

{question}

## The article the question was opened from (for a date or period the question uses)

{article}
"""


def matters_text():
    m = json.loads(MATTERS.read_text())['matters']
    return '\n'.join(f"- {x['matter']}: {x['name']} (e.g. {x['question']})" for x in m), [x['matter'] for x in m]


def library_text(lib):
    lines = []
    for e in lib:
        lines.append(f"- id {e['question_id']} · opened {e['opened']} · due {e['due']}: {e['question']}")
        lines += [f'    possible answer: {a}' for a in e['possible_answers']]
    return '\n'.join(lines)


def store_paths(run_root, draw):
    """The draw's store at its cutoff: refused unless the draw is complete (plan §1.4 item 10). The new system's judge folder is the one its
    own record names as the completed attempt (`draw-<draw>` or, after D449's one redo, `draw-<draw>-redo`). None when the draw opened no
    question (the launcher's `skipped` judge)."""
    root = Path(run_root) / draw
    record = json.loads((root / 'run.json').read_text())
    if record.get('state') != 'complete':
        raise SystemExit(f'refused: {draw} is {record.get("state")!r}, not complete; no release verdict without six complete draws')
    if draw.startswith('new'):
        judge = record['components']['judge']
        if judge['state'] == 'skipped':
            return None
        inner = json.loads((root / judge['folder'] / 'run.json').read_text())[draw]
        if inner.get('state') != 'complete':
            raise SystemExit(f'refused: {draw} judge is {inner.get("state")!r}')
        folder = root / judge['folder'] / inner['attempts'][-1]['folder']
    else:
        folder = root / record['components']['prod']['folder']
    return folder / 'views.sqlite', folder / 'archive.sqlite'


def neutral_ids(lib):
    """Q1..Qn in the library's opening order; the system's id kept as `source_id`."""
    return [dict(e, question_id=f'Q{n}', source_id=e['question_id']) for n, e in enumerate(lib, 1)]


def answer_problem(rows, keys, ids):
    """Why a reader's mapping answer is void, or None: every matter exactly once with a known status, every id named in the library, every
    duplicate pair two different ids of the library."""
    matter_rows = [r for r in rows if r.get('matter')]
    named = [r['matter'] for r in matter_rows]
    if sorted(named) != sorted(keys):
        return f'matters answered {len(named)} ({len(set(keys) - set(named))} missing, {len(named) - len(set(named))} repeated)'
    for r in matter_rows:
        if r.get('status') not in ('opened', 'narrower', 'broader', 'missed'):
            return f"{r['matter']}: status {r.get('status')!r}"
        if r['status'] in ('opened', 'narrower') and not r.get('ids'):
            return f"{r['matter']}: {r['status']} names no id"
        if r['status'] == 'narrower' and not isinstance(r.get('main_outcome'), bool):
            return f"{r['matter']}: narrower without a main-outcome judgement"
        unknown = [q for q in (r.get('ids') or []) if str(q) not in ids]
        if unknown:
            return f"{r['matter']}: ids not in the library {unknown}"
    for r in rows:
        if r.get('duplicate') is not None:
            pair = {str(r['duplicate']), str(r.get('of'))}
            if len(pair) != 2 or not pair <= ids:
                return f"duplicate pair not two library ids: {r}"
    return None


def key_path(out):
    """The mapping key of an export: a diagnostic export (finished draws of a run that cannot give a release verdict) keeps its own key."""
    return KEY_FOLDER / ('mapping-key-diagnostic.json' if (Path(out) / 'DIAGNOSTIC').exists() else 'mapping-key.json')


def export(run_root, out, eligibility_path, diagnostic=False):
    """Export each draw's library. Refused unless the six draws are eligible; with `diagnostic`, the finished draws of an ineligible run
    are exported instead, marked DIAGNOSTIC, under their own key, and the scorer refuses them (their eligibility check does not pass;
    plan §1.4 item 10)."""
    eligibility = json.loads(Path(eligibility_path).read_text())
    if not eligibility.get('eligible') and not diagnostic:
        raise SystemExit(f"refused: the draws are not eligible: {eligibility.get('problems')}")
    out = Path(out)
    if out.exists():
        raise SystemExit(f'refused: {out} exists')
    labels = [f'L{n}' for n in range(1, len(DRAWS) + 1)]
    random.Random(20261117).shuffle(labels)
    key = dict(zip(DRAWS, labels))
    key_file = KEY_FOLDER / ('mapping-key-diagnostic.json' if diagnostic else 'mapping-key.json')
    if key_file.exists():
        raise SystemExit(f'refused: {key_file} exists; an export never overwrites a key')
    import eligibility as eligibility_tool
    libraries = {}
    for draw in key:
        if diagnostic and not eligibility['draws'].get(draw, {}).get('stores'):
            continue                                            # a draw that did not finish: nothing to export
        paths = store_paths(run_root, draw)
        for p in paths or ():
            if eligibility_tool.sha256(p) != eligibility['draws'][draw]['stores'][Path(p).name]['sha256']:
                raise SystemExit(f'refused: {p} changed since the eligibility check')
        libraries[draw] = neutral_ids(build_cards.library(*paths, ITEMS)) if paths else []
    key = {draw: label for draw, label in key.items() if draw in libraries}
    out.mkdir(parents=True)                                     # written only once every store passed its check
    if diagnostic:
        (out / 'DIAGNOSTIC').write_text('finished draws of a run that cannot give a release verdict (plan §1.4 item 10)\n')
    KEY_FOLDER.mkdir(parents=True, exist_ok=True)
    key_file.write_text(json.dumps(key, indent=1) + '\n')
    (out / 'eligibility.json').write_text(Path(eligibility_path).read_text())
    for draw, label in key.items():
        (out / f'library-{label}.json').write_text(json.dumps(libraries[draw], indent=1, ensure_ascii=False) + '\n')
    print('exported', len(key), 'libraries; key in', key_file)


def read(out):
    out = Path(out)
    text, keys = matters_text()
    jobs = []
    for path in sorted(out.glob('library-L*.json')):
        label = path.stem.split('-', 1)[1]
        lib = json.loads(path.read_text())
        prompt = READ.format(matters=text, label=label, library=library_text(lib))
        ids = {e['question_id'] for e in lib}
        for family in FAMILIES:
            dest = out / f'map-{label}-{family}.txt'
            if not dest.exists():
                jobs.append((family, prompt, ids, dest))

    def one(job):
        family, prompt, ids, dest = job
        for attempt in (1, 2):
            answer, void = census_readers.run(family, prompt)
            if answer and not void:
                void = answer_problem(json_lines(answer), keys, ids)
                if void is None:
                    dest.write_text(answer)
                    return dest.name, None
        return dest.name, void
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for name, void in pool.map(one, jobs):
            print(name, 'VOID ' + void if void else 'mapped', flush=True)


def marks(out, label, family):
    """{matter: covering ids} and the set of duplicates (the later-opened id of every pair named), from one family's valid answer."""
    path = Path(out) / f'map-{label}-{family}.txt'
    if not path.exists():
        raise SystemExit(f'refused: {path.name} missing (a void mapping is never counted)')
    rows = json_lines(path.read_text())
    order = {e['question_id']: k for k, e in enumerate(json.loads((Path(out) / f'library-{label}.json').read_text()))}
    covering = {}
    for r in rows:
        if r.get('matter') and r.get('status') in ('opened', 'narrower'):
            if r['status'] == 'opened' or r.get('main_outcome') is True:
                for q in r.get('ids') or []:
                    covering.setdefault(r['matter'], set()).add(str(q))
    duplicates = {max(str(r['duplicate']), str(r['of']), key=order.__getitem__) for r in rows if r.get('duplicate') is not None}
    return covering, duplicates


def disagreements(out):
    out = Path(out)
    split = []
    for path in sorted(out.glob('library-L*.json')):
        label = path.stem.split('-', 1)[1]
        a, _ = marks(out, label, 'codex')
        b, _ = marks(out, label, 'claude')
        for matter in sorted(set(a) | set(b)):
            for q in sorted(a.get(matter, set()) ^ b.get(matter, set())):
                split.append((label, matter, q))
    return split


def opening_article(input_id):
    """The opening article as week reading A2 showed it: title, publisher, day and text, from the comparison's item database."""
    conn = build_cards.ro(ITEMS)
    row = conn.execute('select title, publisher, publication_day, text from items where input_id=?', (input_id,)).fetchone()
    if row is None:
        return '(not an article: the question was not opened from a stored article)'
    return f"{row['title']} · {row['publisher']} · {row['publication_day']}\n\n{row['text']}"


def third(out):
    out = Path(out)
    m = {x['matter']: x for x in json.loads(MATTERS.read_text())['matters']}
    libs = {p.stem.split('-', 1)[1]: {e['question_id']: e for e in json.loads(p.read_text())} for p in out.glob('library-L*.json')}
    jobs = []
    for label, matter, q in disagreements(out):
        entry = libs[label][q]
        for reader in FAMILIES:
            dest = out / 'third' / f'{label}--{matter}--{q}--{reader}.json'
            if not dest.exists():
                question = f"{entry['question']} (due {entry['due']}); possible answers: " + ' | '.join(entry['possible_answers'])
                jobs.append((reader, THIRD.format(matter=f"{m[matter]['name']} (e.g. {m[matter]['question']})", question=question,
                                                  article=opening_article(entry.get('opened_from'))), dest))

    def one(job):
        reader, prompt, dest = job
        for attempt in (1, 2):
            answer, void = census_readers.run(reader, prompt)
            rows = json_lines(answer) if answer else []
            if rows and isinstance(rows[-1].get('covers'), bool) and not void:
                dest.parent.mkdir(exist_ok=True)
                dest.write_text(json.dumps(rows[-1], ensure_ascii=False) + '\n')
                return dest.name, None
        return dest.name, void or 'no covers mark'
    print(len(jobs), 'third-reader sessions')
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for name, void in pool.map(one, jobs):
            print(name, 'VOID ' + void if void else 'marked', flush=True)


def result(out):
    out = Path(out)
    key = json.loads(key_path(out).read_text())
    label_of = {d: l for d, l in key.items()}
    mapping, distinct = {}, {}
    for draw, label in label_of.items():
        a, dup_a = marks(out, label, 'codex')
        b, dup_b = marks(out, label, 'claude')
        lib = json.loads((out / f'library-{label}.json').read_text())
        mapping[draw] = {}
        for matter in sorted(set(a) | set(b)):
            entries = []
            for q in sorted(a.get(matter, set()) | b.get(matter, set())):
                if q in a.get(matter, set()) and q in b.get(matter, set()):
                    covers = True
                else:
                    paths = [out / 'third' / f'{label}--{matter}--{q}--{reader}.json' for reader in FAMILIES]
                    missing = [p.name for p in paths if not p.exists()]
                    if missing:
                        raise SystemExit(f'refused: third-reader marks missing {missing}')
                    thirds = [json.loads(p.read_text())['covers'] for p in paths]
                    covers = True if thirds == [True, True] else False if thirds == [False, False] else 'split'
                entries.append({'question': q, 'covers': covers})
            if any(e['covers'] is not False for e in entries):
                mapping[draw][matter] = [e for e in entries if e['covers'] is not False]
        distinct[draw] = {'ids': len(lib), 'duplicates_both': len(dup_a & dup_b), 'duplicates_split': len(dup_a ^ dup_b)}
    text = json.dumps({'mapping': mapping, 'distinct': distinct,
                       'eligibility_sha256': hashlib.sha256((out / 'eligibility.json').read_bytes()).hexdigest()},
                      indent=1, ensure_ascii=False) + '\n'
    (out / 'mapping.json').write_text(text)
    print('mapping.json written', hashlib.sha256(text.encode()).hexdigest()[:16])


if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'export':
        export(sys.argv[2], sys.argv[3], sys.argv[4], diagnostic='--diagnostic' in sys.argv[5:])
    else:
        {'read': read, 'third': third, 'result': result}[command](sys.argv[2])
