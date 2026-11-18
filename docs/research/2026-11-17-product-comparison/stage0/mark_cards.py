"""The council's marking of the comparison cards (verdict-rule.json marks, controls; card-spec.md; Deck 1's protocol; D672). Every session is
closed (census_readers.run); no session sees the key, which is kept outside the repository.

    python3 mark_cards.py deck <mapping out> <deck folder>     # covering cards, the guardrail sample, the controls; shuffled, keyed
    python3 mark_cards.py mark <deck folder>                   # both families mark every card
    python3 mark_cards.py debate <deck folder> <round>         # rounds 1 and 2 on every card whose marks differ
    python3 mark_cards.py readings <mapping out> <deck folder> # readings.json for score_comparison.py

Marks: worth (worth / trivia / duplicate); answer (supported / unsupported / insufficient), not asked on a card with no answer. A mark still
split after two rounds is {"split": [codex mark, claude mark]}.
"""
import concurrent.futures
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE / 'census')]
import build_cards  # noqa: E402
import census_readers  # noqa: E402
from census_merge import json_lines  # noqa: E402
import mapping as mapping_tool  # noqa: E402

FAMILIES = census_readers.FAMILIES
SEED = 20261117
KEY = mapping_tool.KEY_FOLDER / 'deck-key.json'
WORTH = ('worth', 'trivia', 'duplicate')
ANSWER = ('supported', 'unsupported', 'insufficient')

BRIEF = """You are a senior hedge-fund analyst who follows NVIDIA. You are reviewing one card from a research library's output as it stood on 20
September 2026. Everything you may use is in this message. Do not read any file or run any command. Some cards in the deck are controls. Mark
the card on its own merits.

The house standard for what is worth tracking (quoted): "A question is a bet an analyst would hold a card for: a big matter, never trivia (a
deal, product or project opens one only when its scale can change revenue, profit, cash or credit risk). Small matters open no question …
wordings, deadlines, milestones and periods of one bet are one question." "Most of what an item says is noise … new information that changes
an answer is never missed."

Mark:
1. `worth`: "Is this a question worth tracking for this company?" Answer worth, trivia, or duplicate (duplicate only when an earlier-opened
   question in the same library listed on the card is the same bet: the same outcome settles both and their answers cannot move apart).
2. `answer` (only when the card shows a latest answer): "Is the latest answer supported by the material it was given?" Answer supported,
   unsupported (the material points to another answer, or the answer contradicts its reasons or material), or insufficient (the material is
   too thin to choose any answer). Judge whether the reasons and the material justify the chosen answer over its neighbours.
3. `why`: one or two sentences naming what decides your marks.

Return one JSON object and nothing else: {{"worth": "...", "answer": "..." or null, "why": "..."}}

## The card

{card}
"""

DEBATE = """You marked this card before; another reader marked it differently. Read the card again, your mark and reason, and the other
reader's. Keep or change each disputed mark, with a reason. Return one JSON object and nothing else: {{"worth": "...", "answer": "..." or null,
"why": "..."}}

Your mark: {own}
The other reader's mark: {other}

## The card

{card}
"""

CONFIRM = """You are a senior hedge-fund analyst who follows NVIDIA. Is the latest answer on this card supported by the material it was
given? Judge whether the reasons and the material justify the chosen answer over its neighbours. Return one JSON object and nothing else:
{{"supported": true|false, "why": "<= 30 words"}}

## The card

{card}
"""


def libraries(mapping_out):
    key = json.loads((mapping_tool.KEY_FOLDER / 'mapping-key.json').read_text())
    return {draw: json.loads((Path(mapping_out) / f'library-{label}.json').read_text()) for draw, label in key.items()}


def plant(card_text, entry):
    """The card with its latest answer moved one rung (the next rung, or the previous at the end)."""
    answers = entry['possible_answers']
    k = answers.index(entry['answer'])
    moved = answers[k + 1] if k + 1 < len(answers) else answers[k - 1]
    return card_text.replace(f"Latest answer at the cutoff: {entry['answer']}", f'Latest answer at the cutoff: {moved}', 1)


def deck(mapping_out, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=False)
    libs = libraries(mapping_out)
    mapping = json.loads((Path(mapping_out) / 'mapping.json').read_text())['mapping']
    cards, rng = [], random.Random(SEED)
    for draw in sorted(libs):
        lib = libs[draw]
        by_id = {e['question_id']: e for e in lib}
        covering = {q['question'] for qs in mapping.get(draw, {}).values() for q in qs}
        ids = sorted(by_id)
        guard = set(ids if len(ids) <= 35 else random.Random(SEED).sample(ids, 35))
        for qid in sorted(covering | guard):
            e = by_id[qid]
            cards.append({'draw': draw, 'question': qid, 'role': 'product', 'guardrail': qid in guard, 'covering': qid in covering,
                          'type': e.get('type'), 'answered': e['answer'] is not None, 'text': build_cards.card_text(e, lib)})
    controls = []
    for system in ('new', 'old'):
        pool = [c for c in cards if c['draw'].startswith(system) and c['answered'] and len(libs[c['draw']]) > 0]
        for c in random.Random(SEED + 1).sample(pool, 3):
            entry = {e['question_id']: e for e in libs[c['draw']]}[c['question']]
            controls.append(dict(c, role='plant', text=plant(c['text'], entry)))
    candidates = random.Random(SEED + 2).sample([c for c in cards if c['answered']], min(12, sum(c['answered'] for c in cards)))
    confirmed = []
    for c in candidates:
        if len(confirmed) == 4:
            break
        answer, void = census_readers.run('claude', CONFIRM.format(card=c['text']))
        rows = json_lines(answer) if answer else []
        if rows and rows[-1].get('supported') is True and not void:
            confirmed.append(dict(c, role='supported control'))
    if len(confirmed) < 4:
        raise SystemExit(f'only {len(confirmed)} supported controls confirmed of {len(candidates)} candidates')
    controls += confirmed
    for c in random.Random(SEED + 3).sample(cards, 3):
        controls.append(dict(c, role='repeat'))
    full = cards + controls
    random.Random(SEED + 4).shuffle(full)
    key = {}
    for n, c in enumerate(full, 1):
        cid = f'C{n:03d}'
        key[cid] = {k: c[k] for k in ('draw', 'question', 'role', 'guardrail', 'covering', 'type', 'answered')}
        (folder / f'{cid}.txt').write_text(c['text'])
    KEY.parent.mkdir(parents=True, exist_ok=True)
    KEY.write_text(json.dumps(key, indent=1) + '\n')
    print(f'{len(full)} cards: {len(cards)} product, {len(controls)} controls; key in {KEY}')


def valid(row, answered):
    if not isinstance(row, dict) or row.get('worth') not in WORTH:
        return False
    return (row.get('answer') in ANSWER) if answered else row.get('answer') in (None, 'null')


def run_marks(folder, label, prompts):
    folder = Path(folder)
    key = json.loads(KEY.read_text())
    jobs = [(cid, family, prompt) for (cid, family), prompt in prompts.items() if not (folder / label / f'{cid}-{family}.json').exists()]

    def one(job):
        cid, family, prompt = job
        for attempt in (1, 2):
            answer, void = census_readers.run(family, prompt)
            rows = json_lines(answer) if answer else []
            if rows and valid(rows[-1], key[cid]['answered']) and not void:
                (folder / label).mkdir(exist_ok=True)
                (folder / label / f'{cid}-{family}.json').write_text(json.dumps(rows[-1], ensure_ascii=False) + '\n')
                return cid, family, None
            void = void or 'invalid mark'
        return cid, family, void
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for cid, family, void in pool.map(one, jobs):
            if void:
                print(cid, family, 'VOID', void, flush=True)
    print(label, 'done', flush=True)


def mark(folder):
    folder = Path(folder)
    prompts = {(p.stem, f): BRIEF.format(card=p.read_text()) for p in sorted(folder.glob('C*.txt')) for f in FAMILIES}
    run_marks(folder, 'round-0', prompts)


def current(folder, cid, family):
    for label in ('round-2', 'round-1', 'round-0'):
        p = Path(folder) / label / f'{cid}-{family}.json'
        if p.exists():
            return json.loads(p.read_text())
    return None


def differs(a, b):
    return a is not None and b is not None and (a['worth'] != b['worth'] or a.get('answer') != b.get('answer'))


def debate(folder, round_number):
    folder = Path(folder)
    prompts = {}
    for p in sorted(folder.glob('C*.txt')):
        a, b = current(folder, p.stem, 'codex'), current(folder, p.stem, 'claude')
        if differs(a, b):
            for family, own, other in (('codex', a, b), ('claude', b, a)):
                prompts[(p.stem, family)] = DEBATE.format(own=json.dumps(own, ensure_ascii=False), other=json.dumps(other, ensure_ascii=False),
                                                          card=p.read_text())
    print(len(prompts) // 2, 'cards in debate round', round_number)
    run_marks(folder, f'round-{round_number}', prompts)


def final(folder, cid):
    a, b = current(folder, cid, 'codex'), current(folder, cid, 'claude')
    if a is None or b is None:
        raise SystemExit(f'{cid}: a family has no valid mark')
    out = {}
    for field in ('worth', 'answer'):
        out[field] = a.get(field) if a.get(field) == b.get(field) else {'split': [a.get(field), b.get(field)]}
    return out


def readings(mapping_out, folder):
    folder = Path(folder)
    key = json.loads(KEY.read_text())
    matters = [{'matter': m['matter'], 'company_figure': m['company_figure']} for m in json.loads(mapping_tool.MATTERS.read_text())['matters']]
    mapped = json.loads((Path(mapping_out) / 'mapping.json').read_text())
    cards, plants, supported, repeats = {}, [], [], []
    by_question = {}
    for cid, k in sorted(key.items()):
        f = final(folder, cid)
        answer = f['answer'] if k['answered'] else 'no answer'
        if k['role'] == 'product':
            cards.setdefault(k['draw'], {})[k['question']] = {'worth': f['worth'], 'answer': answer, 'type': k['type'], 'guardrail': k['guardrail']}
            by_question[(k['draw'], k['question'])] = (f['worth'], answer)
        elif k['role'] == 'plant':
            plants.append(answer)
        elif k['role'] == 'supported control':
            supported.append(answer)
    for cid, k in sorted(key.items()):
        if k['role'] == 'repeat':
            f = final(folder, cid)
            answer = f['answer'] if k['answered'] else 'no answer'
            repeats.append((f['worth'], answer) == by_question[(k['draw'], k['question'])])
    out = {'matters': matters, 'mapping': mapped['mapping'], 'distinct': mapped['distinct'], 'cards': cards,
           'controls': {'plants': plants, 'supported': supported, 'repeats_same': repeats}}
    (folder / 'readings.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    print('readings.json written')


if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'deck':
        deck(sys.argv[2], sys.argv[3])
    elif command == 'debate':
        debate(sys.argv[2], int(sys.argv[3]))
    elif command == 'readings':
        readings(sys.argv[2], sys.argv[3])
    else:
        mark(sys.argv[2])
