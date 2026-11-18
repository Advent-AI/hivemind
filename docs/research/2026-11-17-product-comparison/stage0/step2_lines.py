"""Step 2's three hard lines on draw new-1 (verdict-rule.json `hard_checks`; DESIGN-1.6.md §2, v6; D675), each read by closed reader
sessions (`census/census_readers.run`), one per family.

    python3 step2_lines.py line1|line2|line3 <run root> <eligibility.json> <out folder> [--keys <folder>]
    python3 step2_lines.py report <out folder>

Inputs: new-1's Step 1 trace and Step 2's `decisions.json` and `library.json`, each in the folder the draw's `run.json` names and each
read only through `eligibility.verified` (refused unless fingerprinted and unchanged). Each line writes `<out>/line-N/` (refused when it
exists): every prompt, answer and attempt (`sessions.jsonl`), and `result.json`; then `<out>/step2-lines.json` gives every line's
status: passed, failed or not measured. A void session, or an answer outside its closed form, is retried once and then reported
missing; a line with a missing mark is not measured. Which pair or rendering a packet id names is written to `--keys`
(`~/.hivemind-keys/comparison-2026-11-17/`), never overwritten. In every packet a passage Step 1 did not find in its source is shown as
"Unverified quote: …" and gives no source context.

Line 1, search: recall over known labelled counterparts, not over every real repeat. Records are drawn in rounds, one at random from
each of three equal strata of the run's manifest by the article's forward position, articles that hold no record included (seed
20261117 + 1); the records of the first article that holds any, with no earlier record, are left out as the Step 2 reference left out
article 1. Candidates are earlier-article records only: the top 10 by `views/matching._words` overlap over the entity's earlier records
(R0e, no embedding) and every earlier record of the same original party (equal after case folding) published within 3 days. The
whole-history scan (`build_reader_packets.py scan`, one record in full beside one chunk of the earlier records' summaries per session,
both families) audits the first 4 records drawn in each stratum; its flags are candidates, labelled like any other. Two readers, one per
family, answer question 1 of the Step 2 reference labelling (`v2-prompt-1.md`); a disagreement goes to one more session whose family is
drawn per pair by seed (with the reference's adjudication sentence). A counterpart is a pair labelled `same_statement`. Records are
labelled in waves until the first 100 labelled records in draw order are known or the strata are exhausted; the labels are frozen
(`labels.json` and its sha256) before `decisions.json` is read. Pass: for at least 90 of the 100, a group holding a labelled counterpart
is among the record's Step 2 candidates. Fewer than 100: not measured.

Line 2, clear wrong merges: 200 random repeats (seed + 2) of every repeat in `decisions.json` not refused, each joined to its recorded
`repeat_of` group, whose id is its original record's. The frozen merge reading (`merge-prompt-1.md`, packets of 26) by both families;
every pair either reader rejects goes to the frozen third reading (`merge-third-prompt.md`), its family drawn per pair by seed. Each
packet goes in the prompt in place of the file path. Pass: the third reader's `wrong` at most 4 of 200. Fewer than 200: not measured.

Line 3, later details of content: 30 random groups (seed + 3) whose original has at least one later report. The detail key is question
2's definition (`v2-prompt-1.md`) over each record's statement (summary, passages, original party, publication date, publisher); the
attribution fields `group_text` drops for a later report (tier, stated day, period, speaker) are not shown to the key readers, so the key
holds content only, and code counts the later reports whose attribution fields differ from their original's, printed beside. Two key
readers, one per family, list each later report's details; a third session (family drawn per group by seed) settles every group whose
two drafts differ. The key is frozen (`key.json` and its sha256) before any rendering is built. Each group's two renderings, the frozen
dossier (`step3/library.group_text(member_text=True)`) and each record apart (`record_text`), go to their own closed session in each
family, four per group, each after the same surrounding dossier: every other group linked to the sampled group's first thesis link, as
its original's `record_text`. A group whose key is empty states nothing in either and needs no session. Pass: the grouped detail total,
summed over both families, is no fewer than the apart total summed the same way (as the recorded reader test summed its readers); each
family's totals and the mean paired difference per group with a 95% bootstrap interval are printed beside. Fewer than 30 groups: not
measured.
"""
import argparse
import collections
import concurrent.futures
import datetime
import hashlib
import json
import math
import random
import re
import sqlite3
import sys
import threading
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
STAGE0 = ROOT / 'docs/research/2026-11-17-product-comparison/stage0'
sys.path[:0] = [str(STAGE0), str(STAGE0 / 'census'), str(ROOT / 'clean-arch/step2-validation-2026-11-07'), str(ROOT / 'src')]
import build_merge_packets  # noqa: E402  (the frozen merge prompts' file paths, and run_forward)
import census_readers  # noqa: E402
import eligibility  # noqa: E402
from hivemind.views import matching  # noqa: E402

run_forward = build_merge_packets.run_forward
library = run_forward.library

DRAW = 'new-1'
SEED = 20261117
KEY_FOLDER = Path.home() / '.hivemind-keys' / 'comparison-2026-11-17'
FAMILIES = census_readers.FAMILIES
WORKERS = 6
LINE1_RECORDS, LINE1_FOUND = 100, 90
LINE2_MERGES, LINE2_WRONG = 200, 4
LINE3_GROUPS = 30
TOP, PARTY_DAYS, STRATA, AUDITED_PER_STRATUM = 10, 3, 3, 4
LABEL_PACKET, MERGE_PACKET, KEY_PACKET, SCAN_CHUNK, FIRST_WAVE_ROUNDS = 40, 26, 6, 500, 10
CONTEXT_WIDTH = 300
LARGE_PROMPT = 250_000
BOOTSTRAP = 10000
ATTRIBUTION_FIELDS = ('tier', 'statement_date', 'evidence_period', 'reporting_speaker')   # what group_text drops for a later report

V2_PROMPT = ROOT / 'poc/data/step2-validation-2026-11-07/v2-prompt-1.md'
V2_ADJUDICATION = ROOT / 'poc/data/step2-validation-2026-11-07/v2-adjudication-prompt.md'
SCAN_PROMPT = ROOT / 'poc/data/step2-validation-2026-11-07/scan-prompt-template.md'
MERGE_PROMPT = ROOT / 'poc/data/clean-step2-forward-2026-11-08/merge-prompt-1.md'
MERGE_THIRD_PROMPT = ROOT / 'poc/data/clean-step2-forward-2026-11-08/merge-third-prompt.md'
SOURCES = (V2_PROMPT, V2_ADJUDICATION, SCAN_PROMPT, MERGE_PROMPT, MERGE_THIRD_PROMPT, Path(library.__file__), Path(run_forward.__file__))


def between(text, start, end):
    """The part of `text` from `start` up to `end` (exclusive); each must occur exactly once."""
    if text.count(start) != 1 or text.count(end) != 1 or text.index(end) < text.index(start):
        raise SystemExit(f'refused: the prompt source does not hold {start!r} … {end!r} once, in order')
    return text[text.index(start):text.index(end)]


def swap(text, old, new):
    """`text` with `old`, which must occur exactly once, replaced by `new`."""
    if text.count(old) != 1:
        raise SystemExit(f'refused: the prompt source does not hold {old!r} exactly once')
    return text.replace(old, new)


V2_TEXT = V2_PROMPT.read_text()
V2_READ = f'Read {V2_PROMPT.parent}/v2-packet-1.json. '
LABEL_HEAD = swap(V2_TEXT[:V2_TEXT.index('Answer two separate questions')], ' Do not open any other file in that folder.', '')
QUESTION_1 = between(V2_TEXT, 'Question 1, the relation', 'Question 2, independently')
DETAIL_DEFINITION = between(V2_TEXT, 'list each material fact in LATER', ' Then say whether')
RELATIONS = tuple(re.findall(r'^- "([a-z_]+)":', QUESTION_1, re.M))
ADJUDICATION_SENTENCE = between(V2_ADJUDICATION.read_text(), 'Two earlier readers disagreed', 'Return only')
SCAN_TEXT = swap(swap(SCAN_PROMPT.read_text(),
                      'and the list of every evidence record stored before it from earlier articles (key, one-line summary, original party).',
                      'and one chunk of the evidence records stored before it from earlier articles (key, one-line summary, original party); '
                      'the other chunks are read in other sessions.'),
                 'Then read every earlier record and list', 'Then read every earlier record in the chunk and list')
MERGE_TEXT, MERGE_THIRD_TEXT = MERGE_PROMPT.read_text(), MERGE_THIRD_PROMPT.read_text()
MERGE_READ = f'Read {build_merge_packets.OLD_RUN}merge-packet-1.json. '
MERGE_THIRD_READ = f'Read {build_merge_packets.OLD_RUN}merge-third-packet.json. '
VERDICTS = tuple(re.findall(r'^- "([a-z]+)":', MERGE_THIRD_TEXT, re.M))
KEY_PROMPT = ('You are an independent reader for a hedge-fund research system, building an answer key. Read-only task: do not edit files or '
              'run model calls.\n\nRead PACKET. Each entry is one group of stored evidence records about NVIDIA: "earlier", the first record '
              'of a statement, and "later", the later records grouped with it, each with its summary, verbatim source passages, original '
              'party, publication date and publisher. Do not open any file.\n\n'
              'For each LATER record, independently: ' + DETAIL_DEFINITION + '\n\nReturn only a JSON array with one object per later record, '
              'in packet order: [{"id": "K..", "details": ["..."]}].\n')
KEY_THIRD_PROMPT = ('You are the third reader settling an answer key. Read-only task: do not edit files or run model calls.\n\nRead PACKET. '
                    'Each entry is one group of stored evidence records about NVIDIA: "earlier", the first record of a statement, and "later", '
                    'the later records grouped with it, each with its summary, verbatim source passages, original party, publication date and '
                    'publisher. Under "drafts", each later record carries two independent readers\' lists of its details, A and B. Do not '
                    'open any file.\n\nEach reader was asked, for each LATER record, to ' + DETAIL_DEFINITION + '\n\nFor every LATER record, '
                    'compare the two drafts against the records. Keep once each detail both drafts name, in either wording. Decide each '
                    'detail only one draft names from the records: keep it if it is such a fact, otherwise drop it.\n\nReturn only a JSON '
                    'array with one object per later record, in packet order: [{"id": "K..", "details": ["..."], "dropped": ["..."]}].\n')
RENDERING_HEAD = ('You are an independent reader for a hedge-fund research system. Read-only task: do not edit files or run model calls.\n\n'
                  'Below are an excerpt from an evidence dossier about NVIDIA, as a research library shows it to an analyst, and a numbered '
                  'list of details. Do not open any file.\n\nFor each detail, mark whether the excerpt states it, in any wording: true if a '
                  'reader of the excerpt learns that detail from it, false if not.\n\nThe excerpt:\n\n<<<\n')
RENDERING_TAIL = '\n>>>\n\nThe details:\n\n```json\n{details}\n```\n\nReturn only a JSON array in list order: [{{"id": "D..", "stated": true|false}}].\n'


# ---- inputs -------------------------------------------------------------------------------------------------------------------------

def component_file(run_root, eligibility_record, component, name):
    """A file of new-1's `component`, in the folder its run record names, refused unless the eligibility check fingerprinted it."""
    record = json.loads((Path(run_root) / DRAW / 'run.json').read_text())
    entry = record['components'].get(component, {})
    if entry.get('state') != 'completed':
        raise SystemExit(f"refused: {DRAW}'s {component} is {entry.get('state')!r}, not completed")
    return eligibility.verified(eligibility_record, run_root, DRAW, f"{entry['folder']}/{name}")


def article_texts(trace):
    """Each article's source text by its manifest position (as run_forward.step1_records numbers articles), and the manifest's length."""
    texts, position = {}, None
    for part in trace.split('+'):
        conn = sqlite3.connect(f'file:{part}?mode=ro', uri=True)
        try:
            if position is None:
                position = {iid: n for n, iid in enumerate(json.loads(conn.execute('select manifest from run').fetchone()[0])['item_ids'], 1)}
            for iid, request in conn.execute("select input_id, request from trace where status='complete'"):
                texts[position[iid]] = json.JSONDecoder().raw_decode(json.loads(request)['messages'][1]['content'])[0]['source_item']['text']
        finally:
            conn.close()
    return texts, len(position)


def shown_passages(record):
    """Each passage as a reader sees it: the source text Step 1 found, or the model's text marked as an unverified quote."""
    return [text if kind == 'Quote' else f'Unverified quote: {text}' for kind, text in library.labelled_passages(record)]


def source_context(text, passage):
    at = text.find(passage)
    return text[max(0, at - CONTEXT_WIDTH):at + len(passage) + CONTEXT_WIDTH] if at >= 0 else None


def packet_entries(trace):
    """The run's records in forward order (step1_records), each record as a line 1 or line 2 packet shows it (the Step 2 merge packets'
    fields), and the manifest's length. Only passages Step 1 found in the source give source context."""
    articles, questions, _opened = run_forward.step1_records(trace)
    texts, manifest_length = article_texts(trace)
    entries = {}
    for article in articles:
        for r in article:
            found = [text for kind, text in library.labelled_passages(r) if kind == 'Quote']
            entries[r['id']] = {'summary': r['summary'], 'original_party': r['original_party'],
                                'statement_date': r['statement_date'] or r['statement_date_text'], 'period': r['evidence_period'],
                                'publication_date': r['publication_date'], 'tier': r['tier'], 'reporting_speaker': r['reporting_speaker'],
                                'publisher': r['publisher'], 'title': r['title'], 'passages': shown_passages(r),
                                'source_context': [c for c in (source_context(texts[r['article']], p) for p in found) if c],
                                'theses': [questions[t] for t in r['thesis_ids']]}
    return articles, entries, manifest_length


def fresh(folder):
    if folder.exists():
        raise SystemExit(f'refused: {folder} exists')
    folder.mkdir(parents=True)
    return folder


def fresh_key(path):
    if path.exists():
        raise SystemExit(f'refused: {path} exists; a key is never overwritten')
    return path


def write_key(path, key):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(key, indent=1, ensure_ascii=False) + '\n')


def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def freeze(path, payload):
    """Write `payload` and then its sha256 beside it; returns the digest."""
    text = json.dumps(payload, indent=1, ensure_ascii=False) + '\n'
    path.write_text(text)
    digest = sha256_text(text)
    Path(f'{path}.sha256').write_text(f'{digest}  {path.name}\n')
    return digest


def read_frozen(path):
    text = path.read_text()
    if Path(f'{path}.sha256').read_text().split()[0] != sha256_text(text):
        raise SystemExit(f'refused: {path} changed after it was frozen')
    return json.loads(text)


def sources():
    return {str(p.relative_to(ROOT)): eligibility.sha256(p) for p in SOURCES}


# ---- prompts and sessions -----------------------------------------------------------------------------------------------------------

def inline(prompt, read_sentence, packet):
    """The prompt with its packet in place of the file it names: a closed session opens no file."""
    if prompt.count(read_sentence) != 1:
        raise SystemExit(f'refused: the prompt does not name its packet exactly once ({read_sentence!r})')
    return prompt.replace(read_sentence, 'Read this packet:\n\n```json\n' + json.dumps(packet, ensure_ascii=False, indent=1) + '\n```\n\n')


def label_prompt(packet, adjudication=False):
    """Question 1 of the Step 2 reference labelling (`v2-prompt-1.md`) alone, with the reference's adjudication sentence for a third
    reader."""
    body = (LABEL_HEAD + 'Answer from the passages and context, not only the summaries.\n\n' + QUESTION_1
            + (ADJUDICATION_SENTENCE if adjudication else '')
            + 'Return only a JSON array in packet order: [{"id": "V..", "relation": "...", "why": "<one short sentence>"}].\n')
    return inline(body, V2_READ, packet)


def rendering_prompt(rendering, details):
    return RENDERING_HEAD + rendering + RENDERING_TAIL.format(details=json.dumps(details, ensure_ascii=False, indent=1))


def answer_rows(answer):
    """The JSON array of objects an answer returns (a code fence allowed); anything else is refused."""
    text = answer.strip()
    fenced = re.fullmatch(r'```(?:json)?\s*(.*?)\s*```', text, re.S)
    text = fenced.group(1) if fenced else text
    try:
        rows = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find('['), text.rfind(']')
        if start < 0 or end < start:
            raise ValueError('no JSON array in the answer')
        rows = json.loads(text[start:end + 1])
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ValueError('not an array of objects')
    return rows


def is_text_list(value):
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def rows_check(ids, fields):
    """A check: exactly the packet's ids, each once, and every field in its closed set."""
    def check(answer):
        rows = answer_rows(answer)
        got = [row.get('id') for row in rows]
        if sorted(map(str, got)) != sorted(ids) or len(set(map(str, got))) != len(got):
            raise ValueError(f'{len(got)} ids that are not the packet\'s {len(ids)}')
        for row in rows:
            for field, accepts in fields.items():
                if not accepts(row.get(field)):
                    raise ValueError(f"{row['id']}: {field} {row.get(field)!r}")
        return {row['id']: row for row in rows}
    return check


def sessions(folder, jobs):
    """Run each job's closed session ({name, family, prompt, check}). A void session, or an answer its check refuses, is retried once and
    then reported missing (None). Every prompt, answer and attempt is written to the folder."""
    for sub in ('prompts', 'answers'):
        (folder / sub).mkdir(exist_ok=True)
    lock = threading.Lock()

    def one(job):
        (folder / 'prompts' / f"{job['name']}.md").write_text(job['prompt'])
        for attempt in (1, 2):
            answer, void = census_readers.run(job['family'], job['prompt'])
            parsed = None
            if not void:
                try:
                    parsed = job['check'](answer)
                except ValueError as error:
                    void = f'answer refused: {error}'
            if answer:
                (folder / 'answers' / f"{job['name']}-{attempt}.txt").write_text(answer)
            with lock, open(folder / 'sessions.jsonl', 'a') as log:
                log.write(json.dumps({'session': job['name'], 'family': job['family'], 'attempt': attempt, 'void': void}) + '\n')
            if not void:
                return job['name'], parsed
        return job['name'], None

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        return dict(pool.map(one, jobs))


def session_counts(folder):
    path = folder / 'sessions.jsonl'
    lines = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    answered = {line['session'] for line in lines if not line['void']}
    names = {line['session'] for line in lines}
    return {'sessions': len(names), 'attempts': len(lines), 'missing': sorted(names - answered)}


def packets(items, size):
    return [items[start:start + size] for start in range(0, len(items), size)]


def drawn_family(seed, *parts):
    """The family of a third session, drawn per pair or group by seed so that no family settles every dispute."""
    return random.Random(':'.join(map(str, (seed, *parts)))).choice(FAMILIES)


def wilson(successes, trials, z=1.96):
    if not trials:
        return None
    share = successes / trials
    denominator = 1 + z * z / trials
    centre = (share + z * z / (2 * trials)) / denominator
    half = z * math.sqrt(share * (1 - share) / trials + z * z / (4 * trials * trials)) / denominator
    return [round(centre - half, 4), round(centre + half, 4)]


def finish(out, line, folder, result):
    result = {'line': line, 'draw': DRAW, **result, 'sessions': session_counts(folder), 'prompt sources': sources()}
    (folder / 'result.json').write_text(json.dumps(result, indent=1, ensure_ascii=False) + '\n')
    report(out)
    return result


# ---- line 1 -------------------------------------------------------------------------------------------------------------------------

def strata_of(articles, manifest_length):
    """Record ids in three equal strata of the run's manifest by each article's forward position (articles holding no record count
    towards the strata); the records of the first article that holds any have no earlier record and are left out."""
    strata = [[] for _ in range(STRATA)]
    for index, records in enumerate(articles):
        if index:
            for record in records:
                strata[(record['article'] - 1) * STRATA // manifest_length].append(record['id'])
    return strata


def draw_order(strata, seed):
    """Records drawn in rounds, one at random from each stratum per round until the strata are exhausted; the first 4 drawn in each
    stratum are the scan audit's."""
    chooser = random.Random(seed)
    shuffled = [chooser.sample(ids, len(ids)) for ids in strata]
    order = []
    for round_index in range(max(map(len, shuffled), default=0)):
        order += [{'record': ids[round_index], 'stratum': stratum, 'audited': round_index < AUDITED_PER_STRATUM}
                  for stratum, ids in enumerate(shuffled) if round_index < len(ids)]
    return order


def party_of(record):
    return (record['original_party'] or '').strip().casefold()


def day_of(record):
    try:
        return datetime.date.fromisoformat(str(record['publication_date'])[:10])
    except ValueError:
        return None


def route_candidates(record, earlier, words):
    """{earlier record id: routes}: R0e's top 10 by word overlap, scored as `retrieve.py` scores it, and the same original party within
    3 days. `earlier` holds only records of earlier articles, in forward order."""
    target = matching._words(record['summary'])
    routes = {}
    for candidate in sorted(earlier, key=lambda e: -len(target & words[e['id']]))[:TOP]:
        routes.setdefault(candidate['id'], []).append('words')
    day = day_of(record)
    for candidate in earlier:
        other = day_of(candidate)
        if party_of(record) and party_of(candidate) == party_of(record) and day and other and abs((day - other).days) <= PARTY_DAYS:
            routes.setdefault(candidate['id'], []).append('party')
    return routes


def scan(folder, tag, audited, earlier_of, entries):
    """The whole-history scan of the audited records, both families: {record: flagged earlier ids}, and the records whose scan has a
    missing session."""
    jobs = []
    for number, record_id in enumerate(audited, 1):
        for part, chunk in enumerate(packets(earlier_of(record_id), SCAN_CHUNK), 1):
            keys = {e['id'] for e in chunk}
            packet = [{'incoming_key': record_id, 'incoming': entries[record_id],
                       'earlier_items': [{'key': e['id'], 'summary': e['summary'], 'original_party': e['original_party']} for e in chunk]}]

            def check(answer, record_id=record_id, keys=keys):
                rows = [row for row in answer_rows(answer) if row.get('incoming_key') == record_id]
                if len(rows) != 1 or not is_text_list(rows[0].get('possible_earlier')):
                    raise ValueError(f'no single row for {record_id} with a list of keys')
                return {key for key in rows[0]['possible_earlier'] if key in keys}   # a key outside the chunk is not judged
            for family in FAMILIES:
                jobs.append({'name': f'scan-{tag}-r{number}-c{part}-{family}', 'family': family, 'record': record_id,
                             'prompt': inline(SCAN_TEXT, 'Read PACKET. ', packet), 'check': check})
    answers = sessions(folder, jobs)
    flags, missing = collections.defaultdict(set), set()
    for job in jobs:
        if answers[job['name']] is None:
            missing.add(job['record'])
        else:
            flags[job['record']] |= answers[job['name']]
    return flags, missing


def label(folder, tag, new_pairs, pairs, entries, packet_ids):
    """Two readers per pair, one per family, on question 1; each disagreement to one more session of a family drawn per pair."""
    keys = list(new_pairs)
    random.Random(f'{SEED + 1}:{tag}').shuffle(keys)
    for key in keys:
        packet_ids[key] = f'V{len(packet_ids) + 1}'
    check = lambda ids: rows_check(ids, {'relation': lambda value: value in RELATIONS})
    jobs = []
    for number, chunk in enumerate(packets(keys, LABEL_PACKET), 1):
        packet = [{'id': packet_ids[k], 'earlier': entries[k[0]], 'later': entries[k[1]]} for k in chunk]
        jobs += [{'name': f'label-{tag}-{number}-{family}', 'family': family, 'pairs': chunk, 'prompt': label_prompt(packet),
                  'check': check([packet_ids[k] for k in chunk])} for family in FAMILIES]
    answers = sessions(folder, jobs)
    for job in jobs:
        for key in job['pairs']:
            if answers[job['name']] is not None:
                pairs[key]['marks'][job['family']] = answers[job['name']][packet_ids[key]]['relation']
    disputed = collections.defaultdict(list)
    for key in keys:
        marks = pairs[key]['marks']
        if len(marks) == len(FAMILIES) and len(set(marks.values())) == 1:
            pairs[key]['label'] = marks[FAMILIES[0]]
        elif len(marks) == len(FAMILIES):
            disputed[drawn_family(SEED + 1, *key)].append(key)
    jobs = []
    for family, family_keys in sorted(disputed.items()):
        for number, chunk in enumerate(packets(family_keys, LABEL_PACKET), 1):
            packet = [{'id': packet_ids[k], 'earlier': entries[k[0]], 'later': entries[k[1]],
                       'first_relations': [pairs[k]['marks'][f] for f in FAMILIES]} for k in chunk]
            jobs.append({'name': f'third-{tag}-{number}-{family}', 'family': family, 'pairs': chunk,
                         'prompt': label_prompt(packet, adjudication=True), 'check': check([packet_ids[k] for k in chunk])})
    answers = sessions(folder, jobs)
    for job in jobs:
        for key in job['pairs']:
            if answers[job['name']] is not None:
                relation = answers[job['name']][packet_ids[key]]['relation']
                pairs[key]['third'] = {'family': job['family'], 'relation': relation}
                pairs[key]['label'] = relation


def labelled_in_order(order, by_later, scan_missing):
    """The labelled records in draw order up to the first 100, and the first record with a missing mark before them, if any."""
    labelled = []
    for item in order:
        record_id = item['record']
        if record_id in scan_missing or any(pair['label'] is None for pair in by_later[record_id]):
            return labelled, record_id
        if any(pair['label'] == 'same_statement' for pair in by_later[record_id]):
            labelled.append(record_id)
            if len(labelled) == LINE1_RECORDS:
                break
    return labelled, None


def line1(run_root, eligibility_record, out, keys=KEY_FOLDER):
    folder, key_file = fresh(Path(out) / 'line-1'), fresh_key(Path(keys) / 'step2-line1-key.json')
    trace = str(component_file(run_root, eligibility_record, 'step1', 'trace.sqlite'))
    articles, entries, manifest_length = packet_entries(trace)
    records = [record for article in articles for record in article]
    by_id = {record['id']: record for record in records}
    article_start, index = {}, 0
    for article_index, article in enumerate(articles):
        article_start[article_index] = index
        index += len(article)
    article_of = {record['id']: article_index for article_index, article in enumerate(articles) for record in article}
    forward = {record['id']: position for position, record in enumerate(records)}
    earlier_of = lambda record_id: records[:article_start[article_of[record_id]]]
    words = {record['id']: matching._words(record['summary'] + ' ' + ' '.join(record['passages'])) for record in records}
    order = draw_order(strata_of(articles, manifest_length), SEED + 1)
    pairs, packet_ids, by_later = {}, {}, collections.defaultdict(list)
    scan_flags, scan_missing = {}, set()
    done, wave, labelled, missing_at = 0, 0, [], None
    while done < len(order):
        size = FIRST_WAVE_ROUNDS * STRATA if not labelled else math.ceil((LINE1_RECORDS - len(labelled)) * done / len(labelled))
        batch, done, wave = order[done:done + max(1, size)], done + max(1, size), wave + 1
        flags, missing = scan(folder, f'w{wave}', [item['record'] for item in batch if item['audited']], earlier_of, entries)
        scan_flags.update(flags)
        scan_missing |= missing
        new_pairs = []
        for item in batch:
            record_id = item['record']
            routes = route_candidates(by_id[record_id], earlier_of(record_id), words)
            for earlier_id in flags.get(record_id, ()):
                routes.setdefault(earlier_id, []).append('scan')
            for earlier_id in sorted(routes, key=forward.get):
                pairs[(earlier_id, record_id)] = {'earlier': earlier_id, 'routes': routes[earlier_id], 'marks': {}, 'third': None, 'label': None}
                by_later[record_id].append(pairs[(earlier_id, record_id)])
                new_pairs.append((earlier_id, record_id))
        label(folder, f'w{wave}', new_pairs, pairs, entries, packet_ids)
        labelled, missing_at = labelled_in_order(order[:done], by_later, scan_missing)
        if missing_at or len(labelled) >= LINE1_RECORDS:
            break
    write_key(key_file, {packet_ids[key]: {'earlier': key[0], 'later': key[1], 'routes': pair['routes']} for key, pair in pairs.items()})
    drawn = order[:done]
    labels = {'draw': DRAW, 'seed': SEED + 1, 'manifest articles': manifest_length, 'records in draw order': len(order),
              'records drawn': len(drawn),
              'records': [{**item, 'scan missing': item['record'] in scan_missing,
                           'pairs': [{k: pair[k] for k in ('earlier', 'marks', 'third', 'label')} for pair in by_later[item['record']]]}
                          for item in drawn]}
    labels_sha = freeze(folder / 'labels.json', labels)
    # Step 2's output is read only now, after the labels are frozen.
    decisions = {d['id']: d for d in json.loads(component_file(run_root, eligibility_record, 'step2', 'decisions.json').read_text())}
    stored = json.loads(component_file(run_root, eligibility_record, 'step2', 'library.json').read_text())
    counterparts = {item['record']: {pair['earlier'] for pair in item['pairs'] if pair['label'] == 'same_statement'} for item in labels['records']}
    found = original_counterpart = 0
    for record_id in labelled:
        held = {stored['placement'][c] for c in counterparts[record_id] if c in stored['placement']} & set(decisions[record_id]['candidates'])
        found += bool(held)
        original_counterpart += any(stored['groups'][g]['original']['id'] in counterparts[record_id] for g in held)
    audited = [item['record'] for item in drawn if item['audited']]
    audit_pairs = [(c, r) for r in audited for c in counterparts.get(r, ())]
    result = {'labels sha256': labels_sha, 'labelled records': len(labelled), 'needed': LINE1_RECORDS, 'pass at': LINE1_FOUND,
              'records drawn': len(drawn), 'records in the strata': len(order), 'pairs labelled': len(pairs),
              'disputes sent to a third reader': sum(1 for pair in pairs.values() if pair['third']),
              'found': found, 'group original itself a counterpart': original_counterpart,
              'scan audit': {'records': len(audited), 'flags': sum(len(scan_flags.get(r, ())) for r in audited),
                             'counterparts': len(audit_pairs),
                             'counterparts the routes missed': sum(1 for key in audit_pairs if pairs[key]['routes'] == ['scan'])},
              'scope': 'recall over known labelled counterparts, not over every real repeat'}
    if missing_at:
        result.update(status='not measured', reason=f'a missing mark on {missing_at} before 100 labelled records')
    elif len(labelled) < LINE1_RECORDS:
        result.update(status='not measured', reason=f'{len(labelled)} labelled records of {LINE1_RECORDS} with the strata exhausted')
    else:
        result.update(status='passed' if found >= LINE1_FOUND else 'failed', share=found / LINE1_RECORDS,
                      wilson_95=wilson(found, LINE1_RECORDS))
    return finish(out, 1, folder, result)


# ---- line 2 -------------------------------------------------------------------------------------------------------------------------

def line2(run_root, eligibility_record, out, keys=KEY_FOLDER):
    folder, key_file = fresh(Path(out) / 'line-2'), fresh_key(Path(keys) / 'step2-line2-key.json')
    decisions = json.loads(component_file(run_root, eligibility_record, 'step2', 'decisions.json').read_text())
    population = [(d['outcome']['repeat_of'][0], d['id']) for d in decisions if d['outcome']['kind'] == 'repeat' and 'refused' not in d]
    if len(population) < LINE2_MERGES:
        return finish(out, 2, folder, {'status': 'not measured', 'reason': f'{len(population)} repeats, fewer than {LINE2_MERGES}',
                                       'repeats': len(population)})
    sample = random.Random(SEED + 2).sample(population, LINE2_MERGES)
    entries = packet_entries(str(component_file(run_root, eligibility_record, 'step1', 'trace.sqlite')))[1]
    ids = {f'X{number}': pair for number, pair in enumerate(sample, 1)}
    write_key(key_file, {mid: {'earlier': pair[0], 'later': pair[1]} for mid, pair in ids.items()})
    first_check = lambda chunk: rows_check(chunk, {'merge_acceptable': lambda value: isinstance(value, bool)})
    jobs = []
    for number, chunk in enumerate(packets(list(ids), MERGE_PACKET), 1):
        packet = [{'id': mid, 'earlier': entries[ids[mid][0]], 'later': entries[ids[mid][1]]} for mid in chunk]
        jobs += [{'name': f'merge-{number}-{family}', 'family': family, 'ids': chunk, 'prompt': inline(MERGE_TEXT, MERGE_READ, packet),
                  'check': first_check(chunk)} for family in FAMILIES]
    answers = sessions(folder, jobs)
    marks = collections.defaultdict(dict)
    for job in jobs:
        for mid in job['ids']:
            if answers[job['name']] is not None:
                marks[mid][job['family']] = answers[job['name']][mid]
    rejected = collections.defaultdict(list)
    for mid in ids:
        if len(marks[mid]) == len(FAMILIES) and not all(mark['merge_acceptable'] for mark in marks[mid].values()):
            rejected[drawn_family(SEED + 2, *ids[mid])].append(mid)
    third_check = lambda chunk: rows_check(chunk, {'verdict': lambda value: value in VERDICTS})
    jobs = []
    for family, family_ids in sorted(rejected.items()):
        for number, chunk in enumerate(packets(family_ids, MERGE_PACKET), 1):
            packet = [{'id': mid, 'earlier': entries[ids[mid][0]], 'later': entries[ids[mid][1]]} for mid in chunk]
            jobs.append({'name': f'merge-third-{number}-{family}', 'family': family, 'ids': chunk,
                         'prompt': inline(MERGE_THIRD_TEXT, MERGE_THIRD_READ, packet), 'check': third_check(chunk)})
    answers = sessions(folder, jobs)
    third = {mid: answers[job['name']][mid]['verdict'] for job in jobs if answers[job['name']] is not None for mid in job['ids']}
    verdicts = {}
    for mid in ids:
        if len(marks[mid]) == len(FAMILIES) and all(mark['merge_acceptable'] for mark in marks[mid].values()):
            verdicts[mid] = 'acceptable'
        elif mid in third:
            verdicts[mid] = third[mid]
    (folder / 'verdicts.json').write_text(json.dumps({mid: {'earlier': ids[mid][0], 'later': ids[mid][1], 'marks': marks[mid],
                                                            'verdict': verdicts.get(mid)} for mid in ids}, indent=1) + '\n')
    wrong = sum(1 for verdict in verdicts.values() if verdict == 'wrong')
    result = {'repeats': len(population), 'sample': LINE2_MERGES, 'pass at most': LINE2_WRONG,
              'accepted by both readers': sum(1 for mid in ids if mid in verdicts and mid not in third),
              'sent to the third reader': sum(len(v) for v in rejected.values()), 'verdicts': dict(collections.Counter(verdicts.values())),
              'wrong': wrong}
    unjudged = [mid for mid in ids if mid not in verdicts]
    if unjudged:
        result.update(status='not measured', reason=f'{len(unjudged)} merges with a missing mark (first {unjudged[0]})')
    else:
        result.update(status='passed' if wrong <= LINE2_WRONG else 'failed', share=wrong / LINE2_MERGES,
                      wilson_95=wilson(wrong, LINE2_MERGES))
    return finish(out, 2, folder, result)


# ---- line 3 -------------------------------------------------------------------------------------------------------------------------

def key_entry(record):
    """A record's statement as a key reader sees it: its summary, passages, party, publication date and publisher. The attribution
    fields the frozen dossier drops for a later report (tier, stated day, period, speaker) are left out, so the key holds content."""
    return {'summary': record['summary'], 'passages': shown_passages(record), 'original_party': record['original_party'],
            'publication_date': record['publication_date'], 'publisher': record['publisher']}


def attribution_differences(groups):
    """Later reports whose tier, stated day, period or speaker differ from their original's: the fields `group_text` does not print
    for a later report (printed beside line 3, never in its rule)."""
    by_field, reports, holding = collections.Counter(), 0, 0
    for group in groups:
        differing = 0
        for member in group['members']:
            fields = [f for f in ATTRIBUTION_FIELDS if member.get(f) != group['original'].get(f)]
            by_field.update(fields)
            differing += bool(fields)
        reports += differing
        holding += bool(differing)
    return {'later reports that differ': reports, 'later reports': sum(len(g['members']) for g in groups), 'groups holding one': holding,
            'groups': len(groups), 'by field': {f: by_field[f] for f in ATTRIBUTION_FIELDS}}


def surrounding_dossier(stored, group_id):
    """The other groups linked to the group's first thesis link, in library order (none when the group has no link)."""
    links = stored['groups'][group_id]['links']
    if not links:
        return []
    thesis = next(iter(links))
    return [g for g in stored['order'] if g != group_id and thesis in stored['groups'][g]['links']]


def renderings_of(store, stored, group_id):
    """The group's two renderings, each after the same surrounding dossier: its other groups' originals labelled E1..Ek, then the group
    from E(k+1), grouped (the frozen dossier entry) or apart (each record its own entry)."""
    others = surrounding_dossier(stored, group_id)
    labels = {g: f'E{n}' for n, g in enumerate(others, 1)}
    context = [library.record_text(stored['groups'][g]['original'], labels[g]) for g in others]
    start = len(others) + 1
    group = stored['groups'][group_id]
    grouped = library.group_text(store, group_id, f'E{start}', {**labels, group_id: f'E{start}'}, member_text=True)
    apart = [library.record_text(record, f'E{start + n}') for n, record in enumerate([group['original']] + group['members'])]
    return {'grouped': '\n\n'.join(context + [grouped]), 'apart': '\n\n'.join(context + apart)}, len(others)


def normal(detail):
    return ' '.join(detail.split()).casefold()


def line3(run_root, eligibility_record, out, keys=KEY_FOLDER):
    folder, key_file = fresh(Path(out) / 'line-3'), fresh_key(Path(keys) / 'step2-line3-key.json')
    stored = json.loads(component_file(run_root, eligibility_record, 'step2', 'library.json').read_text())
    eligible = [g for g in stored['order'] if stored['groups'][g]['members']]
    beside = {'groups with a later report': len(eligible),
              'attribution differences, all groups with a later report': attribution_differences([stored['groups'][g] for g in eligible])}
    if len(eligible) < LINE3_GROUPS:
        return finish(out, 3, folder, {'status': 'not measured', 'reason': f'{len(eligible)} groups with a later report, fewer than {LINE3_GROUPS}',
                                       **beside})
    sample = random.Random(SEED + 3).sample(eligible, LINE3_GROUPS)
    beside['attribution differences, sampled groups'] = attribution_differences([stored['groups'][g] for g in sample])
    member_of, groups = {}, []
    for number, group_id in enumerate(sample, 1):
        group = stored['groups'][group_id]
        later = []
        for member in group['members']:
            member_id = f'K{len(member_of) + 1}'
            member_of[member_id] = (group_id, member['id'])
            later.append({'id': member_id, **key_entry(member)})
        groups.append({'group': f'G{number}', 'id': group_id, 'earlier': key_entry(group['original']), 'later': later})
    shown = lambda entry: {k: v for k, v in entry.items() if k != 'id'}
    key_check = lambda ids: rows_check(ids, {'details': is_text_list})
    jobs = []
    for number, chunk in enumerate(packets(groups, KEY_PACKET), 1):
        ids = [member['id'] for entry in chunk for member in entry['later']]
        jobs += [{'name': f'key-{number}-{family}', 'family': family, 'ids': ids,
                  'prompt': inline(KEY_PROMPT, 'Read PACKET. ', [shown(entry) for entry in chunk]), 'check': key_check(ids)} for family in FAMILIES]
    answers = sessions(folder, jobs)
    drafts = collections.defaultdict(dict)
    for job in jobs:
        for member_id in job['ids']:
            if answers[job['name']] is not None:
                drafts[member_id][job['family']] = answers[job['name']][member_id]['details']
    final, unsettled = {}, collections.defaultdict(list)
    for entry in groups:
        ids = [member['id'] for member in entry['later']]
        if any(len(drafts[m]) < len(FAMILIES) for m in ids):
            continue
        if all(len({frozenset(map(normal, drafts[m][f])) for f in FAMILIES}) == 1 for m in ids):
            final.update({m: drafts[m][FAMILIES[0]] for m in ids})
        else:
            unsettled[drawn_family(SEED + 3, entry['id'])].append(entry)
    third_check = lambda ids: rows_check(ids, {'details': is_text_list, 'dropped': is_text_list})
    jobs = []
    for family, family_groups in sorted(unsettled.items()):
        for number, chunk in enumerate(packets(family_groups, KEY_PACKET), 1):
            ids = [member['id'] for entry in chunk for member in entry['later']]
            packet = [{**shown(entry), 'drafts': {m['id']: dict(zip('AB', (drafts[m['id']][f] for f in FAMILIES))) for m in entry['later']}}
                      for entry in chunk]
            jobs.append({'name': f'key-third-{number}-{family}', 'family': family, 'ids': ids,
                         'prompt': inline(KEY_THIRD_PROMPT, 'Read PACKET. ', packet), 'check': third_check(ids)})
    answers = sessions(folder, jobs)
    for job in jobs:
        if answers[job['name']] is not None:
            final.update({m: answers[job['name']][m]['details'] for m in job['ids']})
    unkeyed = [m for m in member_of if m not in final]
    if unkeyed:
        return finish(out, 3, folder, {'status': 'not measured', 'reason': f'{len(unkeyed)} later reports with no settled key (first {unkeyed[0]})',
                                       **beside})
    key = {'draw': DRAW, 'seed': SEED + 3, 'groups': [
        {'group': entry['id'], 'details': [{'id': f'D{n}', 'member': member_of[m][1], 'text': text}
                                           for n, (m, text) in enumerate(((m['id'], t) for m in entry['later'] for t in final[m['id']]), 1)]}
        for entry in groups]}
    key_sha = freeze(folder / 'key.json', key)
    # The renderings are built only now, from the frozen key.
    key = read_frozen(folder / 'key.json')
    store = library.Library()
    store.groups, store.order = stored['groups'], stored['order']
    codes = random.Random(f'{SEED + 3}:codes').sample(range(100, 1000), 2 * LINE3_GROUPS)
    code_key, jobs, dossier_sizes = {}, [], []
    for index, entry in enumerate(key['groups']):
        renderings, others = renderings_of(store, stored, entry['group'])
        dossier_sizes.append(others)
        if not entry['details']:
            continue
        details = [{'id': d['id'], 'detail': d['text']} for d in entry['details']]
        for offset, (rendering, text) in enumerate(renderings.items()):
            code = codes[2 * index + offset]
            code_key[str(code)] = {'group': entry['group'], 'rendering': rendering}
            jobs += [{'name': f'render-{code}-{family}', 'family': family, 'code': str(code), 'prompt': rendering_prompt(text, details),
                      'check': rows_check([d['id'] for d in details], {'stated': lambda value: isinstance(value, bool)})} for family in FAMILIES]
    write_key(key_file, code_key)
    sizes = sorted(len(job['prompt'].encode()) for job in jobs)
    answers = sessions(folder, jobs)
    stated = {}
    for job in jobs:
        if answers[job['name']] is not None:
            stated[(code_key[job['code']]['group'], code_key[job['code']]['rendering'], job['family'])] = \
                sum(1 for row in answers[job['name']].values() if row['stated'])
    missing = [job['name'] for job in jobs if answers[job['name']] is None]
    totals = {family: {'grouped': 0, 'apart': 0} for family in FAMILIES}
    differences = {family: [] for family in FAMILIES}
    for entry in key['groups']:
        for family in FAMILIES:
            grouped, apart = stated.get((entry['group'], 'grouped', family), 0), stated.get((entry['group'], 'apart', family), 0)
            totals[family]['grouped'] += grouped
            totals[family]['apart'] += apart
            differences[family].append(grouped - apart)
    pooled = {rendering: sum(totals[f][rendering] for f in FAMILIES) for rendering in ('grouped', 'apart')}
    pooled_differences = [sum(values) for values in zip(*differences.values())]
    result = {'key sha256': key_sha, 'groups': LINE3_GROUPS, 'key details': sum(len(e['details']) for e in key['groups']),
              'groups with an empty key': sum(1 for e in key['groups'] if not e['details']), 'pooled totals': pooled,
              'mean paired difference, pooled': sum(pooled_differences) / len(pooled_differences),
              'bootstrap_95, pooled': bootstrap_interval(pooled_differences, f'{SEED + 3}:pooled'),
              'totals by family': totals, 'mean paired difference by family': {f: sum(d) / len(d) for f, d in differences.items()},
              'bootstrap_95 by family': {f: bootstrap_interval(d, f'{SEED + 3}:{f}') for f, d in differences.items()},
              'surrounding dossier': {'groups with no thesis link': sum(1 for n in dossier_sizes if n == 0), 'largest': max(dossier_sizes)},
              'rendering prompt bytes': {'sessions': len(sizes), 'median': sizes[len(sizes) // 2] if sizes else None,
                                         'max': sizes[-1] if sizes else None, f'over {LARGE_PROMPT}': sum(1 for s in sizes if s > LARGE_PROMPT)},
              **beside}
    if missing:
        result.update(status='not measured', reason=f'{len(missing)} rendering sessions missing (first {missing[0]})')
    else:
        result.update(status='passed' if pooled['grouped'] >= pooled['apart'] else 'failed')
    return finish(out, 3, folder, result)


def bootstrap_interval(values, seed):
    """95% percentile interval of the mean over groups, resampled with replacement."""
    chooser = random.Random(seed)
    means = sorted(sum(chooser.choice(values) for _ in values) / len(values) for _ in range(BOOTSTRAP))
    return [means[int(0.025 * BOOTSTRAP)], means[int(0.975 * BOOTSTRAP) - 1]]


# ---- report -------------------------------------------------------------------------------------------------------------------------

def report(out):
    """`step2-lines.json`: each line's status, and the release line D675 prints beside the verdict (a failed line ahead of one not measured)."""
    lines = {}
    for line in (1, 2, 3):
        path = Path(out) / f'line-{line}' / 'result.json'
        lines[str(line)] = json.loads(path.read_text()) if path.exists() else {'line': line, 'status': 'not measured', 'reason': 'not run'}
    statuses = [result['status'] for result in lines.values()]
    status = 'failed' if 'failed' in statuses else 'not measured' if 'not measured' in statuses else 'passed'
    release = ([f'release blocked: Step 2 line {n} failed' for n, r in lines.items() if r['status'] == 'failed']
               + [f'release not cleared: Step 2 line {n} not measured' for n, r in lines.items() if r['status'] == 'not measured']
               or ['hard checks clear'])
    summary = {'draw': DRAW, 'status': status, 'release': release, 'lines': lines}
    (Path(out) / 'step2-lines.json').write_text(json.dumps(summary, indent=1, ensure_ascii=False) + '\n')
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command', choices=['line1', 'line2', 'line3', 'report'])
    parser.add_argument('paths', nargs='+')
    parser.add_argument('--keys', default=str(KEY_FOLDER))
    args = parser.parse_args(argv)
    if args.command == 'report':
        summary = report(args.paths[0])
    else:
        run_root, eligibility_path, out = args.paths
        Path(out).mkdir(parents=True, exist_ok=True)
        {'line1': line1, 'line2': line2, 'line3': line3}[args.command](run_root, json.loads(Path(eligibility_path).read_text()), out, args.keys)
        summary = json.loads((Path(out) / 'step2-lines.json').read_text())
    print(json.dumps({'status': summary['status'], 'release': summary['release'],
                      'lines': {n: {k: r.get(k) for k in ('status', 'reason')} for n, r in summary['lines'].items()}}, indent=1))


if __name__ == '__main__':
    main()
