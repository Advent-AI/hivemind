"""The council's marking of the comparison cards (verdict-rule.json marks, controls; card-spec.md; Deck 1's protocol; D672). Every session is
closed (census_readers.run); no session sees the key, which is kept outside the repository.

    python3 mark_cards.py deck <mapping out> <deck folder>     # covering cards, the guardrail sample, the controls; shuffled, keyed
    python3 mark_cards.py mark <deck folder>                   # both families mark every card
    python3 mark_cards.py debate <deck folder> <round>         # rounds 1 and 2 on every card whose marks differ
    python3 mark_cards.py readings <mapping out> <deck folder> # readings.json for score_comparison.py

Marks: worth (worth / trivia / duplicate); answer (supported / unsupported / insufficient), not asked on a card with no answer. A mark still
split after two rounds is {"split": [codex mark, claude mark]}. A debate round reads only the rounds before it and resends the whole brief
(closed sessions remember nothing); a round is complete only when every mark it owes is written (`round-N.done`), and readings refuse a deck
whose three rounds are not complete. The guardrail sample draws from the system's own ids (`source_id`), sorted as strings (verdict-rule.json).
A field both families agree on in a round stays settled; later rounds change only fields still disputed. A plant moves the stored rung one
place and enters the deck only when a separate closed reader confirms the moved answer is not supported (as supported controls are confirmed
supported first). A card's covering mark is true, "split" (resolved per counting by the scorer) or false. The deck never overwrites a key.
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
1. `worth`: "Is this a question worth tracking for this company?" Answer worth, trivia, or duplicate (duplicate only when a question listed
   above this one in the card's opening-order list is the same bet: the same outcome settles both and their answers cannot move apart).
2. `answer` (only when the card shows a latest answer): "Is the latest answer supported by the material it was given?" Answer supported,
   unsupported (the material points to another answer, or the answer contradicts its reasons or material), or insufficient (the material is
   too thin to choose any answer). Judge whether the reasons and the material justify the chosen answer over its neighbours.
3. `why`: at most 40 words naming what decides your marks.

Return one JSON object and nothing else: {{"worth": "...", "answer": "..." or null, "why": "..."}}

## The card

{card}
"""

DEBATE = """

## A second look

You marked this card before; another reader marked it differently. Read the card again, your mark and reason, and the other reader's, against
the definitions above. The disputed marks are: {disputed}; the others are settled. Keep or change each disputed mark, with a reason. Return
one JSON object and nothing else: {{"worth": "...", "answer": "..." or null, "why": "..."}}

Your mark: {own}
The other reader's mark: {other}
"""

CONFIRM = """You are a senior hedge-fund analyst who follows NVIDIA. Is the latest answer on this card supported by the material it was
given? Judge whether the reasons and the material justify the chosen answer over its neighbours. Return one JSON object and nothing else:
{{"supported": true|false, "why": "<= 30 words"}}

## The card

{card}
"""


def libraries(mapping_out):
    key = json.loads(mapping_tool.key_path(mapping_out).read_text())
    return {draw: json.loads((Path(mapping_out) / f'library-{label}.json').read_text()) for draw, label in key.items()}


def guardrail_sample(lib):
    """The neutral ids of the guardrail sample: the system's own ids sorted as strings, random.Random(20261117).sample(ids, 35), or all of
    them when fewer (verdict-rule.json `guardrails.sample`)."""
    neutral = {e['source_id']: e['question_id'] for e in lib}
    ids = sorted(neutral)
    return {neutral[i] for i in (ids if len(ids) <= 35 else random.Random(SEED).sample(ids, 35))}


def plant(card_text, entry):
    """The card with its latest answer moved one rung from the stored rung (the next rung, or the previous at the end), or None when no
    adjacent rung differs."""
    answers = entry['possible_answers']
    k = entry.get('answer_index')
    if k is None or not 0 <= k < len(answers) or answers[k] != entry['answer']:
        return None
    moved = answers[k + 1] if k + 1 < len(answers) else (answers[k - 1] if k > 0 else None)
    if moved is None or moved == entry['answer']:
        return None
    planted = card_text.replace(f"Latest answer at the cutoff: {entry['answer']}", f'Latest answer at the cutoff: {moved}', 1)
    return planted if planted != card_text else None


def confirmed_by_reader(card_text, supported):
    """A separate closed reader's confirmation that the card's latest answer is (or is not) supported; None when the reader gave no mark."""
    answer, void = census_readers.run('claude', CONFIRM.format(card=card_text))
    rows = json_lines(answer) if answer else []
    if void or not rows or not isinstance(rows[-1].get('supported'), bool):
        return None, rows[-1] if rows else None
    return rows[-1]['supported'] is supported, rows[-1]


def record_confirmations(confirmations):
    """Every control confirmation of this deck attempt, appended beside the key (an earlier attempt's are kept)."""
    KEY.parent.mkdir(parents=True, exist_ok=True)
    with open(KEY.parent / 'control-confirmations.jsonl', 'a') as handle:
        handle.write(json.dumps({'attempt': confirmations}, ensure_ascii=False) + '\n')


def deck(mapping_out, folder):
    if KEY.exists():
        raise SystemExit(f'refused: {KEY} exists; a deck never overwrites a key')
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=False)
    libs = libraries(mapping_out)
    mapping = json.loads((Path(mapping_out) / 'mapping.json').read_text())['mapping']
    cards, rng = [], random.Random(SEED)
    for draw in sorted(libs):
        lib = libs[draw]
        by_id = {e['question_id']: e for e in lib}
        covering = {}
        for qs in mapping.get(draw, {}).values():
            for q in qs:
                covering[q['question']] = True if (q['covers'] is True or covering.get(q['question']) is True) else 'split'
        guard = guardrail_sample(lib)
        for qid in sorted(set(covering) | guard):
            e = by_id[qid]
            cards.append({'draw': draw, 'question': qid, 'role': 'product', 'guardrail': qid in guard, 'covering': covering.get(qid, False),
                          'opened': e.get('opened'),
                          'type': e.get('type'), 'answered': e['answer'] is not None, 'text': build_cards.card_text(e, lib)})
    controls, confirmations = [], []
    for system in ('new', 'old'):
        pool = []
        for c in cards:
            if c['draw'].startswith(system) and c['answered']:
                planted = plant(c['text'], {e['question_id']: e for e in libs[c['draw']]}[c['question']])
                if planted is not None:
                    pool.append(dict(c, role='plant', text=planted))
        random.Random(SEED + 1).shuffle(pool)
        admitted = []
        for c in pool:
            if len(admitted) == 3:
                break
            ok, mark = confirmed_by_reader(c['text'], supported=False)
            confirmations.append({'role': 'plant', 'draw': c['draw'], 'question': c['question'], 'mark': mark, 'admitted': bool(ok)})
            if ok:
                admitted.append(c)
        if len(admitted) < 3:
            record_confirmations(confirmations)
            raise SystemExit(f'{system}: only {len(admitted)} plants confirmed not supported of {len(pool)} candidates')
        controls += admitted
    candidates = random.Random(SEED + 2).sample([c for c in cards if c['answered']], min(12, sum(c['answered'] for c in cards)))
    confirmed = []
    for c in candidates:
        if len(confirmed) == 4:
            break
        ok, mark = confirmed_by_reader(c['text'], supported=True)
        confirmations.append({'role': 'supported control', 'draw': c['draw'], 'question': c['question'], 'mark': mark, 'admitted': bool(ok)})
        if ok:
            confirmed.append(dict(c, role='supported control'))

    record_confirmations(confirmations)
    if len(confirmed) < 4:
        raise SystemExit(f'only {len(confirmed)} supported controls confirmed of {len(candidates)} candidates')
    controls += confirmed
    for c in random.Random(SEED + 3).sample(cards, 3):
        controls.append(dict(c, role='repeat'))
    full = cards + controls
    random.Random(SEED).shuffle(full)
    key = {}
    for n, c in enumerate(full, 1):
        cid = f'C{n:03d}'
        key[cid] = {k: c[k] for k in ('draw', 'question', 'role', 'guardrail', 'covering', 'type', 'answered', 'opened')}
        (folder / f'{cid}.txt').write_text(c['text'])
    KEY.parent.mkdir(parents=True, exist_ok=True)
    KEY.write_text(json.dumps(key, indent=1) + '\n')
    print(f'{len(full)} cards: {len(cards)} product, {len(controls)} controls; key in {KEY}')


def normalised(row):
    """The mark as written: the string "null" for no answer becomes null, so two readers' empty answers compare equal."""
    return dict(row, answer=None) if isinstance(row, dict) and row.get('answer') == 'null' else row


def valid(row, answered):
    if not isinstance(row, dict) or row.get('worth') not in WORTH or len(str(row.get('why', '')).split()) > 40:
        return False
    return (row.get('answer') in ANSWER) if answered else row.get('answer') is None


def run_marks(folder, label, prompts):
    """Writes every owed mark of the round; the round is complete (`<label>.done`) only when none is void."""
    folder = Path(folder)
    key = json.loads(KEY.read_text())
    jobs = [(cid, family, prompt) for (cid, family), prompt in prompts.items() if not (folder / label / f'{cid}-{family}.json').exists()]

    def one(job):
        cid, family, prompt = job
        for attempt in (1, 2):
            answer, void = census_readers.run(family, prompt)
            rows = [normalised(r) for r in json_lines(answer)] if answer else []
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
    owed = [(cid, family) for (cid, family) in prompts if not (folder / label / f'{cid}-{family}.json').exists()]
    if owed:
        print(label, 'NOT complete:', len(owed), 'marks owed; run the round again', flush=True)
        return
    (folder / f'{label}.done').write_text(f'{len(prompts)} marks\n')
    print(label, 'complete', flush=True)


def mark(folder):
    folder = Path(folder)
    prompts = {(p.stem, f): BRIEF.format(card=p.read_text()) for p in sorted(folder.glob('C*.txt')) for f in FAMILIES}
    run_marks(folder, 'round-0', prompts)


def current(folder, cid, family, upto):
    """The family's latest mark on the card from rounds 0..upto (a debate round never reads its own round)."""
    for n in range(upto, -1, -1):
        p = Path(folder) / f'round-{n}' / f'{cid}-{family}.json'
        if p.exists():
            return json.loads(p.read_text())
    return None


def settled_marks(folder, cid, upto):
    """The fields both families agreed on in some round 0..upto (settled at the first such round), and each family's latest mark."""
    out, a, b = {}, None, None
    for n in range(upto + 1):
        a, b = current(folder, cid, 'codex', n), current(folder, cid, 'claude', n)
        if a is None or b is None:
            raise SystemExit(f'{cid}: a family has no valid mark by round {n}')
        for field in ('worth', 'answer'):
            if field not in out and a.get(field) == b.get(field):
                out[field] = a.get(field)
    return out, a, b


def debate(folder, round_number):
    folder = Path(folder)
    if not (folder / f'round-{round_number - 1}.done').exists():
        raise SystemExit(f'refused: round {round_number - 1} is not complete')
    prompts = {}
    for p in sorted(folder.glob('C*.txt')):
        settled, a, b = settled_marks(folder, p.stem, round_number - 1)
        disputed = [field for field in ('worth', 'answer') if field not in settled]
        if disputed:
            for family, own, other in (('codex', a, b), ('claude', b, a)):
                prompts[(p.stem, family)] = BRIEF.format(card=p.read_text()) + DEBATE.format(
                    disputed=', '.join(disputed), own=json.dumps(own, ensure_ascii=False), other=json.dumps(other, ensure_ascii=False))
    print(len(prompts) // 2, 'cards in debate round', round_number)
    run_marks(folder, f'round-{round_number}', prompts)


def final(folder, cid):
    """Each field's mark: settled at the first round both families agree on it (a later change to a settled field is ignored); a field
    never agreed is {"split": [codex, claude]} as the last round left it."""
    out, a, b = settled_marks(folder, cid, 2)
    for field in ('worth', 'answer'):
        out.setdefault(field, {'split': [a.get(field), b.get(field)]})
    return out


def matter_first_days():
    """Each frozen matter's earliest article day: the census numbered the kept articles 1.. by (day, published_at, id) from its source
    database (`census_readers.build`), so a matter's earliest article is its lowest number."""
    kept = json.loads(census_readers.KEPT.read_text())
    conn = build_cards.ro(census_readers.SOURCE)
    rows = sorted((tuple(conn.execute('select publication_day, coalesce(published_at, \'\') from items where input_id=?', (a,)).fetchone()) + (a,)
                   for a in kept['kept_ids']))
    day_of = {n: row[0] for n, row in enumerate(rows, 1)}
    return {m['matter']: day_of[min(m['articles'])] for m in json.loads(mapping_tool.MATTERS.read_text())['matters']}


def build_readings(mapping_out, folder):
    """The readings the scorer takes, built from the mapping output and the marks folder (the one writer of their shape;
    `score_comparison.score` builds them again and scores what is built). Every mapped draw has a card map, empty when it opened no question."""
    folder = Path(folder)
    for n in (0, 1, 2):
        if not (folder / f'round-{n}.done').exists():
            raise SystemExit(f'refused: round {n} is not complete')
    key = json.loads(KEY.read_text())
    matters = [{'matter': m['matter'], 'company_figure': m['company_figure']} for m in json.loads(mapping_tool.MATTERS.read_text())['matters']]
    mapped_text = (Path(mapping_out) / 'mapping.json').read_bytes()
    mapped = json.loads(mapped_text)
    cards = {draw: {} for draw in mapped['mapping']}
    plants, supported, repeats = [], [], []
    by_question = {}
    for cid, k in sorted(key.items()):
        f = final(folder, cid)
        answer = f['answer'] if k['answered'] else 'no answer'
        if k['role'] == 'product':
            cards.setdefault(k['draw'], {})[k['question']] = {'worth': f['worth'], 'answer': answer, 'type': k['type'], 'guardrail': k['guardrail'],
                                                              'covering': k['covering'], 'opened': k.get('opened')}
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
    out = {'matters': matters, 'matter_first_day': matter_first_days(), 'mapping': mapped['mapping'], 'distinct': mapped['distinct'], 'cards': cards,
           'controls': {'plants': plants, 'supported': supported, 'repeats_same': repeats},
           'inputs': {'matters_sha256': hashlib.sha256(mapping_tool.MATTERS.read_bytes()).hexdigest(),
                      'mapping_path': str((Path(mapping_out) / 'mapping.json').resolve()), 'mapping_sha256': hashlib.sha256(mapped_text).hexdigest(),
                      'eligibility_path': str((Path(mapping_out) / 'eligibility.json').resolve()), 'eligibility_sha256': mapped['eligibility_sha256'],
                      'deck_key_path': str(KEY), 'deck_key_sha256': hashlib.sha256(KEY.read_bytes()).hexdigest()}}
    return out


def readings(mapping_out, folder):
    """Writes the readings record (readings.json) beside the marks."""
    out = build_readings(mapping_out, folder)
    (Path(folder) / 'readings.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
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
