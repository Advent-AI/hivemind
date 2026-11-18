"""The blind mapping of matters to each system-draw's questions (verdict-rule.json `covers` and `same_question`; plan §1.4 items 2–3;
week reading A2's form, `docs/research/2026-11-14-use-acceptance/week/brief-A2.md`). Every session is closed (census_readers.run).

    python3 mapping.py export <run root> <out folder>     # each draw's library (build_cards.library) under a random label; key kept outside
    python3 mapping.py read <out folder>                   # both families map every matter for every library; duplicates marked
    python3 mapping.py third <out folder>                  # a third reader of each family on every matter-question the families split on
    python3 mapping.py result <out folder>                 # mapping.json: covers true / false / "split" per matter and question; distinct bets

Covers: both families mark the question `opened`, or `narrower` with both saying it carries the matter's main outcome. A question one family
marks covering and the other not goes to two third readers; covering when both say yes, not covering when both say no, otherwise "split".
A duplicate is the later-opened question of a same-bet pair; "duplicates_both" counts those both families mark, "duplicates_split" those one
marks.
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
- **opened**: a question the same outcome would settle, in any reasonable wording, period or date the news supports (name its id);
- **narrower**: a question on part of the matter (name its id, and say whether it carries the matter's main outcome);
- **broader**: the matter is folded into a wider question;
- **missed**: no question on it.

Do not count a reasonable alternative shape as missed: a different deadline the news itself states, or one year of a two-year matter, is
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
    root = Path(run_root) / draw
    record = json.loads((root / 'run.json').read_text())
    if draw.startswith('new'):
        folder = root / record['components']['judge']['folder'] / f'draw-{draw}'
    else:
        folder = root / record['components']['prod']['folder']
    return folder / 'views.sqlite', folder / 'archive.sqlite'


def export(run_root, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    labels = [f'L{n}' for n in range(1, len(DRAWS) + 1)]
    random.Random(20261117).shuffle(labels)
    key = dict(zip(DRAWS, labels))
    KEY_FOLDER.mkdir(parents=True, exist_ok=True)
    (KEY_FOLDER / 'mapping-key.json').write_text(json.dumps(key, indent=1) + '\n')
    for draw, label in key.items():
        views, archive = store_paths(run_root, draw)
        lib = build_cards.library(views, archive, ITEMS)
        (out / f'library-{label}.json').write_text(json.dumps(lib, indent=1, ensure_ascii=False) + '\n')
    print('exported', len(key), 'libraries; key in', KEY_FOLDER / 'mapping-key.json')


def read(out):
    out = Path(out)
    text, keys = matters_text()
    jobs = []
    for path in sorted(out.glob('library-L*.json')):
        label = path.stem.split('-', 1)[1]
        lib = json.loads(path.read_text())
        prompt = READ.format(matters=text, label=label, library=library_text(lib))
        for family in FAMILIES:
            dest = out / f'map-{label}-{family}.txt'
            if not dest.exists():
                jobs.append((family, prompt, keys, dest))

    def one(job):
        family, prompt, keys, dest = job
        for attempt in (1, 2):
            answer, void = census_readers.run(family, prompt)
            if answer and not void:
                named = {r.get('matter') for r in json_lines(answer) if r.get('matter')}
                if set(keys) <= named:
                    dest.write_text(answer)
                    return dest.name, None
                void = f'{len(set(keys) - named)} matters not answered'
        return dest.name, void
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for name, void in pool.map(one, jobs):
            print(name, 'VOID ' + void if void else 'mapped', flush=True)


def marks(out, label, family):
    rows = json_lines((Path(out) / f'map-{label}-{family}.txt').read_text())
    covering = {}
    for r in rows:
        if r.get('matter') and r.get('status') in ('opened', 'narrower'):
            if r['status'] == 'opened' or r.get('main_outcome') is True:
                for q in r.get('ids') or []:
                    covering.setdefault(r['matter'], set()).add(str(q))
    duplicates = {str(r['duplicate']) for r in rows if r.get('duplicate')}
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


def third(out):
    out = Path(out)
    m = {x['matter']: x for x in json.loads(MATTERS.read_text())['matters']}
    libs = {p.stem.split('-', 1)[1]: {e['question_id']: e for e in json.loads(p.read_text())} for p in out.glob('library-L*.json')}
    jobs = []
    for label, matter, q in disagreements(out):
        entry = libs[label].get(q)
        if entry is None:
            continue
        for reader in FAMILIES:
            dest = out / 'third' / f'{label}--{matter}--{q}--{reader}.json'
            if not dest.exists():
                question = f"{entry['question']} (due {entry['due']}); possible answers: " + ' | '.join(entry['possible_answers'])
                jobs.append((reader, THIRD.format(matter=f"{m[matter]['name']} (e.g. {m[matter]['question']})", question=question), dest))

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
    key = json.loads((KEY_FOLDER / 'mapping-key.json').read_text())
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
                    thirds = [json.loads(p.read_text()).get('covers') for p in (out / 'third').glob(f'{label}--{matter}--{q}--*.json')]
                    covers = True if thirds == [True, True] else False if thirds == [False, False] else 'split'
                entries.append({'question': q, 'covers': covers})
            if any(e['covers'] is not False for e in entries):
                mapping[draw][matter] = [e for e in entries if e['covers'] is not False]
        distinct[draw] = {'ids': len(lib), 'duplicates_both': len(dup_a & dup_b), 'duplicates_split': len(dup_a ^ dup_b)}
    text = json.dumps({'mapping': mapping, 'distinct': distinct}, indent=1, ensure_ascii=False) + '\n'
    (out / 'mapping.json').write_text(text)
    print('mapping.json written', hashlib.sha256(text.encode()).hexdigest()[:16])


if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'export':
        export(sys.argv[2], sys.argv[3])
    else:
        {'read': read, 'third': third, 'result': result}[command](sys.argv[2])
