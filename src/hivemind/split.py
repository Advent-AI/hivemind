"""The split extraction (docs/research/2026-11-05-production-plan/plan-final.md, adopted by Alex on 2026-11-05).

One item, read against every question open immediately before its dispatch sequence (D375; the 2026-11-05 all-open record), by two calls on
that same snapshot: A proposes important new questions with the article's passages for them; B files the article's evidence under the existing
questions. Record preparation then reads the whole article and fills, for A's questions, the subject (a listed id or a new research subject),
the admission reason, dates, the favourable end and the ladder, and for every A passage its attribution; it also decides the attribution of a
statement A and B both quoted, and which of B's unfiled passages an A question of the same item takes. Code checks shapes and identity only
(AGENTS §2): source quotes, one record per quoted statement, the ladder's order, bounds and stated band, each admission reason's limits, an
analyst check date when no exact date is supported. The handover then goes through the existing matching and writer (views.round)."""
import calendar
import concurrent.futures
import copy
import datetime
import difflib
import hashlib
import json
import re

from . import extraction, model, placement
from .views import identity, store

LOCAL_GROUP = extraction.LOCAL_GROUP
OBJECT_LABELS = extraction.OBJECT_LABELS
SECTION_CHARS = extraction.MAX_TEXT_CHARS
REQUEST_ALERT_TOKENS = 200000          # the all-open request-size alert (2026-11-05 decision 3): logged, never a cap
SHARED_MEASURES = ('spend_total', 'capacity', 'market_size')
REASONS = ('main_driver', 'product_node', 'binding_obligation', 'shared_quantity', 'policy_stage')
ANNUAL_REASONS = ('main_driver', 'shared_quantity')
OPEN_HEAD = '[Open questions immediately before this item]'
CHECK_HEAD = 'Before you return the answer, check it once.'
CHECK_END = 'Return only the evidence items you keep.'
B_CLOSING = 'Return only evidence per the schema. Each evidence link must be an ID of a supplied existing question.'
B_LINKS = ("The questions this statement is filed under, decided after you have decided it is evidence: the id of the narrowest open question in "
           "[Open questions] whose answer this statement makes more or less likely, as that question's own figure, step or estimate or through the "
           "demand, supply, competition or pricing behind its answer; compare the specific questions before a company-wide revenue or margin question "
           "and take that one only, never a broader question beside it; a shared company, industry, event or ecosystem is not a connection, and the "
           "statement need not repeat the question's words (a variant, sibling or other name of the subject counts); whoever says it, and even when it "
           "gives no period, basis or exact amount, because the weight is judged later; an estimate for another period or population of a question's "
           "quantity is filed under it when no open question covers that period; when no specific question is connected, a statement that moves the "
           "demand, supply, competition or pricing behind the company's results goes to the company-wide revenue question of its period. A relevant "
           "quarterly actual or forecast can inform an annual question. A material assumption or condition of a forecast can inform the same question "
           "when it changes how the forecast is understood; preserve its uncertainty. Use only the supplied existing question ids; empty when no question "
           "is connected, however important the statement sounds.")


# The evidence call's own copy of the closing check, per prompt version (results-reading.md §4, 2026-11-06): the exception for newly disclosed
# figures names every party the standard's evidence rule names and the figures its §6 lists. The frozen production check is not changed.
B_CHECK_REVISIONS = {
    'split-b-v2': [("nor a customer's, supplier's or partner's newly disclosed revenue, capacity, orders or contracted amount;",
                    "nor a customer's, supplier's, competitor's or partner's newly disclosed figure, such as revenue, margin, capacity, orders or a "
                    "contracted amount;")],
}


class SplitError(ValueError):
    pass


# ---------------------------------------------------------------- the snapshot and research subjects

def latest_library(conn, sequence):
    """Every question open immediately before the item's dispatch sequence (D375), in creation order, with its key, groups and parents as of
    that sequence; A, B, matching and the stored request all read this one list."""
    if sequence < 1:
        raise SplitError('item sequence must be positive')
    before = sequence - 1
    shown = []
    for row in conn.execute('select view_id, object_id, object_kind, kind, looks_at, question, due_day, year, created_seq from views '
                            'where created_seq<=? order by created_seq, view_id', (before,)):
        view = dict(row)
        switch = conn.execute('select open from view_switches where view_id=? and after_seq<=? order by after_seq desc, id desc limit 1',
                              (view['view_id'], before)).fetchone()
        if not switch or not switch['open']:
            continue
        key = store.view_key(conn, view['view_id']) or {}
        if key and key.get('seq', 0) > before:
            key = {}
        view.update(snapshot_seq=before, key=key,
                    groups=[{'name': g['name'], 'scope': g['scope'], 'aliases': g.get('aliases') or []} for g in store.groups_of_view_at(conn, view['view_id'], before)],
                    parents=store.direct_parents(conn, view['view_id'], before))
        shown.append(view)
    return shown


def load_subjects(conn, universe):
    """Restore the research subjects the ledger holds into the universe this process uses (a restart resolves each to its id)."""
    for row in conn.execute('select object_id, name, kind from research_subjects order by rowid'):
        record = {'id': row['object_id'], 'name': row['name'], 'categories': [], 'aliases': []}
        if row['kind'] == 'theme':
            universe.themes[row['object_id']] = record
            universe.theme_names[row['name']] = row['object_id']
        else:
            universe.companies[row['object_id']] = record


def register_subjects(conn, universe, candidates, seq, input_id):
    """A candidate's subject is a listed id, or a new research subject named by record preparation: its id is derived from its kind and name
    and written to the ledger with the item; an id already written under another name or kind refuses the item (an identity collision)."""
    for c in candidates:
        if universe.has(c['object']):
            continue
        name = c['object'].strip()
        kind = 'theme' if c['kind'] == 'theme' else 'company'
        known = next((key for key, record in (universe.themes if kind == 'theme' else universe.companies).items()
                      if record['name'].casefold() == name.casefold()), None)
        if known:
            c['object'] = known
            continue
        object_id = 'research:' + hashlib.sha256((kind + '\0' + name.casefold()).encode()).hexdigest()[:20]
        prior = conn.execute('select name, kind from research_subjects where object_id=?', (object_id,)).fetchone()
        if prior and (prior['name'].casefold() != name.casefold() or prior['kind'] != kind):
            raise SplitError('research subject identity collision: ' + object_id)
        if not prior:
            store.insert(conn, 'research_subjects', object_id=object_id, name=name, kind=kind, created_seq=seq, created_from_input=input_id)
        record = {'id': object_id, 'name': name, 'categories': [], 'aliases': []}
        if kind == 'theme':
            universe.themes[object_id] = record
            universe.theme_names[name] = object_id
        else:
            universe.companies[object_id] = record
        c['looks_at'] = 'Subject: ' + name + ' | ' + c['looks_at']
        c['object'] = object_id


def subject_names(item, universe):
    """The item's subject companies' own names, as production's sift passes them to the quote repair (D266)."""
    return [universe.companies[o['value']]['name'] for o in item.get('object_identifiers') or [] if o.get('value') in universe.companies]


# ---------------------------------------------------------------- source quotes

HYPHEN_GLYPHS = str.maketrans({'‐': '-', '‑': '-'})


def compare_form(text):
    """The text as quotes are compared with it, and for each character the index of the source character it came from. Hyphen glyphs compare
    as '-'; an em dash closed up after a letter ("report—$96.2") compares as a space, any other em dash as the production '-'; a space between a
    digit and '%' ("28.1 %") is left out. Compared, never stored."""
    plain = text.translate(HYPHEN_GLYPHS)
    chars, index = [], []
    for i, ch in enumerate(plain):
        if ch == '—' and i > 0 and plain[i - 1].isalpha():
            ch = ' '
        if ch in '  ' and plain[i + 1:i + 2] == '%' and chars and chars[-1].isdigit():
            continue
        chars.append(ch)
        index.append(i)
    return ''.join(chars), index


def source_quote(quote, text, names=()):
    """The exact source passage a quote stands for under the production contract (D236, D266: punctuation, the subject company's own name for
    "the company", a copied passage that runs on), or None."""
    plain, index = compare_form(text)
    quote = compare_form(quote)[0]

    def intact_at(passage):
        start = 0
        while True:
            pos = plain.find(passage, start)
            if pos < 0:
                return -1
            left = plain[pos - 1:pos] if pos else ''
            right = plain[pos + len(passage):pos + len(passage) + 1]
            first, last = passage[:1], passage[-1:]
            partial = (left and first and left.isalnum() and first.isalnum()) or (right and last and right.isalnum() and last.isalnum())
            unsigned = first and first.isdigit() and left and left in '-+−$€£¥'
            fragment = first and first.isdigit() and left in '.,' and pos > 1 and plain[pos - 2].isdigit()
            if not partial and not unsigned and not fragment:
                return pos
            start = pos + 1

    def original(passage):
        pos = intact_at(passage)
        return None if pos < 0 else text[index[pos]:index[pos + len(passage) - 1] + 1]

    if not quote.strip():
        return None
    if intact_at(quote) >= 0:
        return original(quote)
    restored = extraction.repair_quote(quote, plain, tuple(names))
    if not restored or intact_at(restored) < 0:
        return None
    restored_words = [t[0] for t in extraction._quote_tokens(restored)]
    quote_words = [t[0] for t in extraction._quote_tokens(quote)]
    runs_on = len(restored_words) >= extraction.NEAR_MIN_TOKENS and quote_words[:len(restored_words)] == restored_words
    if restored_words == quote_words or runs_on or extraction.normalise(restored) == extraction.normalise(quote):
        return original(restored)
    if len(quote_words) >= extraction.NEAR_MIN_TOKENS:
        spans = extraction._quote_tokens(restored)
        source_words = [t[0] for t in spans]
        blocks = [b for b in difflib.SequenceMatcher(None, quote_words, source_words, autojunk=False).get_matching_blocks() if b.size]
        if blocks:
            start, end = blocks[0].b, blocks[-1].b + blocks[-1].size
            edits, changed = extraction._edited_tokens(quote_words, source_words[start:end])
            if edits <= extraction.NEAR_EDITS(len(quote_words)) and all(t in extraction._harmless(tuple(names)) for t in changed):
                passage = extraction._source_passage(restored, spans[start][1], spans[end - 1][2])
                if intact_at(passage) >= 0:
                    return original(passage)
    return None


# ---------------------------------------------------------------- long items

def sections(text, limit=SECTION_CHARS):
    """The item cut at paragraph ends into parts no longer than the limit (2026-11-05 decision 6: long items are read in sections, never cut
    off); a paragraph longer than the limit is cut at the limit."""
    if len(text) <= limit:
        return [text]
    parts, current = [], ''
    for paragraph in text.split('\n'):
        while len(paragraph) > limit:
            if current:
                parts.append(current)
                current = ''
            parts.append(paragraph[:limit])
            paragraph = paragraph[limit:]
        if len(current) + len(paragraph) + 1 > limit:
            parts.append(current)
            current = paragraph
        else:
            current = (current + '\n' + paragraph) if current else paragraph
    if current:
        parts.append(current)
    return parts


# ---------------------------------------------------------------- requests

def _obj(props):
    return {'type': 'object', 'additionalProperties': False, 'properties': props, 'required': list(props)}


def question_schema(shown_ids):
    text = {'type': 'string'}
    passage = _obj({'quote': text, 'what_it_shows': text, 'original_speaker': text})
    question = _obj({
        'question': text, 'why_it_matters': text,
        'closest_existing_question': {'type': 'string', 'enum': ['none'] + list(shown_ids),
                                      'description': 'The id of the existing question whose outcome is closest to this one, or none when no existing question concerns the same subject and matter.'},
        'what_separates_it': {'type': 'string', 'description': "A result that would settle this question while the closest existing question's answer stays unchanged, and why an analyst would bet on each separately. Another estimate, source, wording, scope name, direction, population or proxy of the same quantity, or a later deadline for the same event, does not separate them: then propose nothing."},
        'how_and_when_to_check': text,
        'group_refs': {'type': 'array', 'items': {'type': 'string', 'pattern': '^(?:' + LOCAL_GROUP + ')$'}},
        'evidence': {'type': 'array', 'items': passage, 'minItems': 1}})
    group = _obj({'id': {'type': 'string', 'pattern': '^' + LOCAL_GROUP + '$'}, 'name': text, 'scope': text, 'aliases': {'type': 'array', 'items': text}})
    return _obj({'questions': {'type': 'array', 'items': question}, 'new_groups': {'type': 'array', 'items': group}})


def _frozen_user(cfg, item, text, shown, universe):
    """The evidence call's user text is the frozen extraction's (role-v74i), read against the item's own snapshot."""
    setting, _, old, schema = extraction.request_for(cfg, item, text, shown, universe)
    old_head = f'[Open questions at the start of {item["publication_day"]}]'
    if old.count(old_head) != 1:
        raise SplitError('open question block absent')
    return setting, old.replace(old_head, OPEN_HEAD, 1), schema


def basis_labels(user, shown):
    """Append each recorded accounting basis to its own question line (a GAAP and a non-GAAP figure are different quantities)."""
    start = user.index(OPEN_HEAD)
    end = user.index('[Research groups]', start)
    block = user[start:end]
    for view in shown:
        basis = (view.get('key') or {}).get('basis')
        if basis not in ('GAAP', 'non_GAAP'):
            continue
        line = placement.question_lines([view])[0]
        if block.count(line) != 1:
            raise SplitError('question identity/line mismatch: ' + view['view_id'])
        block = block.replace(line, line + '\n      accounting basis: ' + ('GAAP' if basis == 'GAAP' else 'non-GAAP'), 1)
    return user[:start] + block + user[end:]


def requests(cfg, item, text, shown, universe, proposed=()):
    """(setting, A spec, B spec) for one section of an item; a spec is (system, user, schema, name). proposed: questions A already proposed
    from earlier sections of the same item, shown to A as not to propose again."""
    setting, old, schema = _frozen_user(cfg, item, text, shown, universe)
    subject = old[old.index('[Subjects]'):old.index('[What to read out]')]
    subject = subject.replace('; use that day as the due date.', '.').replace(
        'Fiscal-year note (a numeric thesis takes its year and due date from it):', "Fiscal-year context for the company's own quantities:")
    category = old[:old.index('[Subjects]')]
    questions = old[old.index(OPEN_HEAD):old.index('[Research groups]')]
    if proposed:
        questions += '[Questions already proposed from earlier parts of this item]\n' + '\n'.join('  - ' + q for q in proposed) + '\n\n'
    article = f"[Article] id {item['input_id']}; date {item['publication_day']}; title {item['title']}; publisher {item['publisher']}\n{text[:extraction.MAX_TEXT_CHARS]}"
    if not old.endswith(CHECK_END) or old.count(CHECK_HEAD) != 1:
        raise SplitError('closing check anchors absent')
    closing = old[old.index(CHECK_HEAD):-len(CHECK_END)] + 'Return only the evidence passages you keep; a question left with none is not proposed.'
    a_user = category + subject + questions + article + '\n\n[Closing check for every evidence passage]\n' + closing
    shown_ids = list(dict.fromkeys(v['view_id'] for v in shown))
    a_spec = (_prompt(cfg.split['a']), a_user, question_schema(shown_ids), 'new_question')
    b_user = old.replace(extraction.GROUPS_INSTRUCTION, '[Research groups] Use the supplied question descriptions to understand their scope.', 1)
    start, end = b_user.find('[Research reference]'), b_user.find(OPEN_HEAD)
    if start != -1:
        b_user = b_user[:start] + b_user[end:]
    b_user = b_user.replace('For a candidate thesis about a company, object is its ticker; about a theme, choose an id from this list, or state what the matter is when none fits:', 'Theme identifiers:', 1)
    b_user = b_user.replace(extraction.CLOSING, B_CLOSING, 1)
    anchor = "- a share-price move, an investor's position or trade, or the market value"
    if b_user.count(anchor) != 1:
        raise SplitError('evidence review anchor missing')
    b_user = b_user.replace(anchor, "- a share-price move or an investor's position or trade", 1).replace(
        'it does not cover the news behind the move;', "it does not cover the news behind the move; the covered company's market value, a standalone valuation multiple, and its share-price reaction after earnings are optional;", 1)
    b_user = b_user.replace(CHECK_HEAD, CHECK_HEAD + ' A clearly retold past actual figure may be kept or omitted; still-effective guidance and forecasts retain their usual weight. For a company statement retold by a news author, the article publication day is not the original statement day unless the article says so; otherwise leave original_day empty.', 1)
    for before, after in B_CHECK_REVISIONS.get(cfg.split['b'].prompt_version, []):
        if b_user.count(before) != 1:
            raise SplitError('evidence closing-check anchor missing for ' + cfg.split['b'].prompt_version)
        b_user = b_user.replace(before, after, 1)
    b_user = basis_labels(b_user, shown)
    b_schema = {'type': 'object', 'additionalProperties': False, 'properties': {'evidence': copy.deepcopy(schema['properties']['evidence'])}, 'required': ['evidence']}
    b_schema['properties']['evidence']['items']['properties']['links']['description'] = B_LINKS
    if shown_ids:
        b_schema['properties']['evidence']['items']['properties']['links']['items']['pattern'] = '^(?:' + '|'.join(re.escape(v) for v in shown_ids) + ')$'
    b_spec = (_prompt(cfg.split['b']), b_user, b_schema, 'extraction')
    return setting, a_spec, b_spec


def _prompt(setting):
    from . import config
    with open(config.prompt_path(setting.prompt_version + '.txt'), encoding='utf-8') as handle:
        return handle.read()


ATTRIBUTION_FIELDS = ('speaker', 'original_who', 'original_day', 'tier', 'event_time')


def preparation_schema(subject_ids, candidate_count, evidence_count, unfiled_count):
    text = {'type': 'string'}
    frozen = extraction.schema_for('v74i')['properties']['evidence']['items']['properties']
    rung = _obj({'label': text, 'condition': text, 'lo': {'anyOf': [{'type': 'number'}, {'type': 'null'}]}, 'hi': {'anyOf': [{'type': 'number'}, {'type': 'null'}]}})
    candidate = _obj({
        'object': {'type': 'string', 'enum': list(subject_ids) + ['new']}, 'new_subject': text,
        'new_subject_kind': {'type': 'string', 'enum': ['company', 'theme', 'none']},
        'opens_as': {'type': 'string', 'enum': list(REASONS)}, 'obligation_state': {'type': 'string', 'enum': ['signed', 'unsigned', 'none']},
        'shared_measure': {'type': 'string', 'enum': ['none'] + list(SHARED_MEASURES)}, 'unit': {'type': 'string', 'enum': list(extraction.UNITS)},
        'year': text, 'due_day': text, 'date_basis': {'type': 'string', 'enum': ['source_stated', 'analyst_check', 'unknown']}, 'date_provenance': text,
        'favourable_end': {'type': 'string', 'enum': ['higher', 'lower', 'none']}, 'rungs': {'type': 'array', 'items': rung}})
    evidence = _obj({'speaker': {'type': 'string', 'description': frozen['speaker'].get('description', '')},
                     'original_who': {'type': 'string', 'description': frozen['original_who'].get('description', '')},
                     'original_day': {'type': 'string', 'description': frozen['original_day'].get('description', '')},
                     'tier': {'type': 'string', 'enum': ['fact', 'party_statement', 'third_party_view', 'rumour', 'unknown']}, 'event_time': text})
    candidate_ids = ['c' + str(i) for i in range(1, candidate_count + 1)]
    unfiled = _obj({'links': {'type': 'array', 'items': {'type': 'string', 'enum': candidate_ids}}})
    out = _obj({'candidates': _obj({c: {'$ref': '#/$defs/candidate'} for c in candidate_ids}),
                'evidence': _obj({'e' + str(i): {'$ref': '#/$defs/evidence'} for i in range(1, evidence_count + 1)}),
                'unfiled': _obj({'u' + str(i): {'$ref': '#/$defs/unfiled'} for i in range(1, unfiled_count + 1)})})
    out['$defs'] = {'candidate': candidate, 'evidence': evidence, 'unfiled': unfiled}
    return out


def preparation_request(cfg, item, text, universe, stage):
    """Record preparation for A's questions: the subject list, the article, the questions, every A passage (with the other reading when B quoted
    the same statement) and B's unfiled passages."""
    subjects = [(k, v['name'], 'company') for k, v in universe.companies.items()] + [(k, v['name'], 'theme') for k, v in universe.themes.items()]
    questions = [{'id': c['id'], 'question': q['question'], 'why_it_matters': q['why_it_matters'], 'how_and_when_to_check': q['how_and_when_to_check']}
                 for c, q in zip(stage['candidate_slots'], stage['questions'])]
    passages = []
    for position, e in enumerate(stage['a_passages'], 1):
        entry = {'id': 'e' + str(position), 'original_speaker': e['original_speaker'], 'quote': e['quote'], 'summary': e['what_it_shows']}
        other = stage['other_readings'].get(e['id'])
        if other:
            entry['other_reading'] = {k: other.get(k, '') for k in ATTRIBUTION_FIELDS}
        passages.append(entry)
    unfiled = [{'id': u['uid'], 'quote': u['quote'], 'summary': u['one_line']} for u in stage['unfiled']]
    user = ('[Subjects]\n' + '\n'.join(f'  - {k}: {name} ({kind})' for k, name, kind in subjects) + '\n\n[Article]\n' + text[:extraction.MAX_TEXT_CHARS] +
            '\n\n[Questions]\n' + json.dumps(questions, ensure_ascii=False) + '\n\n[Evidence]\n' + json.dumps(passages, ensure_ascii=False) +
            '\n\n[Unfiled passages]\n' + (json.dumps(unfiled, ensure_ascii=False) if unfiled else 'None.'))
    schema = preparation_schema([k for k, _, _ in subjects], len(questions), len(passages), len(unfiled))
    return _prompt(cfg.split['preparation']), user, schema, 'record_preparation'


# ---------------------------------------------------------------- record checks (code owns shape and identity, AGENTS §2)

def chosen_subject(m, question):
    if m['object'] != 'new':
        return m['object'], None
    return (m.get('new_subject', '').strip() or 'Subject not stated: ' + question), ('theme' if m.get('new_subject_kind') == 'theme' else 'company')


FISCAL_YEAR = re.compile(r'\b(?:FY\s?|fiscal(?:\s+year)?\s+)(\d{4})\b', re.I)


def question_year(question, year):
    """The period the year limit reads: record preparation's year, read as a fiscal year only when the question names that same year as fiscal."""
    year = (year or '').strip()
    bare = re.fullmatch(r'(\d{4})', year)
    if bare:
        for named in FISCAL_YEAR.finditer(question):
            if named.group(1) == bare.group(1):
                return 'FY' + bare.group(1)
    return year


def shared_key(m, kind):
    """D197: a theme quantity summed over one calendar year carries a code-owned key (theme, measure, period)."""
    measure, year = m.get('shared_measure', 'none'), (m.get('year') or '').strip()
    found = re.fullmatch(r'(?:CY)?(\d{4})', year)
    if kind != 'theme' or measure not in SHARED_MEASURES or not found:
        return {}
    y = found.group(1)
    return {'measure': measure, 'opens_as': 'shared_quantity', 'scope': '', 'period_start': y + '-01-01', 'period_end': y + '-12-31',
            'basis': 'n/a', 'unit': m.get('unit', 'n/a'), 'event_type': 'n/a', 'key_version': identity.KEY_VERSION}


SCALE = {'trillion': 1e12, 'billion': 1e9, 'million': 1e6, 'thousand': 1e3}
BAND = re.compile(r'within\s+(\d+(?:\.\d+)?)\s*%[^0-9]{0,60}?(?:US\$|NT\$|\$)?\s*([\d,]+(?:\.\d+)?)\s*(trillion|billion|million|thousand)?', re.I)


def empty_rung(rungs):
    """A rung's lower bound is inclusive and its upper bound exclusive, so a rung with lo not below hi holds no value (exactly one rung must hold)."""
    for r in rungs:
        if r.get('lo') is not None and r.get('hi') is not None and float(r['lo']) >= float(r['hi']):
            return f'rung {r.get("label", "")} holds no value ({r["lo"]:g} to below {r["hi"]:g})'
    return None


def band_problem(rungs):
    """When a rung states "within X% of <reference>", its bounds must be the reference times (1 ± X%) (the bounds are the contract)."""
    for r in rungs:
        found = BAND.search(r.get('condition', ''))
        if not found or r.get('lo') is None or r.get('hi') is None:
            continue
        share = float(found.group(1)) / 100
        reference = float(found.group(2).replace(',', '')) * SCALE.get((found.group(3) or '').lower(), 1)
        for bound, expected in ((r['lo'], reference * (1 - share)), (r['hi'], reference * (1 + share))):
            if expected and abs(bound - expected) > abs(expected) * 0.001:
                return f'rung bounds {r["lo"]}..{r["hi"]} differ from the stated band of {found.group(1)}% around {reference:g}'
    return None


def _number(value):
    return f'{value:,.0f}' if float(value).is_integer() and abs(value) >= 1000 else f'{value:g}'


def render(lo, hi, unit):
    unit = '' if unit in ('n/a', None) else ' ' + unit
    if lo is None:
        return f'below {_number(hi)}{unit}'
    if hi is None:
        return f'{_number(lo)}{unit} or more'
    return f'from {_number(lo)}{unit} to below {_number(hi)}{unit}'


def ordered_ladder(rungs, kind, favourable_end, unit):
    """(rungs, problem). A numeric asset ladder is ordered by code from its bounds and the favourable end record preparation chose (D186): the
    Strongly bullish rung holds the favourable range; each numeric condition carries its interval rendered from the bounds."""
    rungs = copy.deepcopy(rungs or [])
    if not rungs:
        return [], None
    problem = extraction.check_ladder(rungs, kind) or extraction.check_bounds(rungs) or empty_rung(rungs) or band_problem(rungs)
    if problem:
        return [], problem
    numeric = all(r.get('lo') is not None or r.get('hi') is not None for r in rungs)
    if not numeric:
        return extraction.normalise_ladder(rungs, kind), None
    ranked = sorted(rungs, key=lambda r: float('-inf') if r.get('lo') is None else float(r['lo']))
    if kind == 'asset' and len(ranked) == 5:
        if favourable_end not in ('higher', 'lower'):
            return [], 'a numeric company ladder needs a favourable end'
        ordered = list(reversed(ranked)) if favourable_end == 'higher' else ranked
        ordered = [dict(r, label=label) for r, label in zip(ordered, OBJECT_LABELS)]
    else:
        ordered = ranked
    return [dict(r, condition=r['condition'].rstrip() + f' [{render(r.get("lo"), r.get("hi"), unit)}]') for r in ordered], None


def _month_end(year, month):
    return datetime.date(year, month, calendar.monthrange(year, month)[1]).isoformat()


def analyst_check_day(c, m, universe, publication_day):
    """2026-11-05 decision 4: when no exact day is supported, the day the settling material is expected, stored as an analyst check. An annual
    company quantity: the end of the month after its fiscal year ends; an obligation already taken on: the current fiscal year's annual report;
    a calendar-year shared quantity: the end of the next March; a pending policy step: the current fiscal year-end (standard §3 E). Others: none."""
    reason, subject = m['opens_as'], c['object']
    if reason in ('main_driver', 'binding_obligation') and subject in universe.companies and universe.companies[subject].get('fiscal_year_end_month'):
        if reason == 'binding_obligation' and m.get('obligation_state') != 'signed':
            return ''
        year = question_year(c['question'], m.get('year', '')) if reason == 'main_driver' else 'FY' + str(universe.fiscal_year_of(subject, publication_day))
        period = universe.fiscal_period(subject, year, bare_is_calendar=True)
        if not period:
            return ''
        end = datetime.date.fromisoformat(period[1])
        month = end.month % 12 + 1
        return _month_end(end.year + (1 if end.month == 12 else 0), month)
    if reason == 'shared_quantity':
        found = re.fullmatch(r'(?:CY)?(\d{4})', (m.get('year') or '').strip())
        return f'{int(found.group(1)) + 1}-03-31' if found else ''
    if reason == 'policy_stage':
        if subject in universe.companies and universe.companies[subject].get('fiscal_year_end_month'):
            period = universe.fiscal_period(subject, 'FY' + str(universe.fiscal_year_of(subject, publication_day)), bare_is_calendar=True)
            return period[1] if period else ''
        return publication_day[:4] + '-12-31'
    return ''


def explicit_day(day, words):
    """Whether the supporting words contain the same complete calendar day."""
    try:
        value = datetime.date.fromisoformat(day)
    except (TypeError, ValueError):
        return False
    if value.isoformat() != day:
        return False
    if re.search(r'(?<!\d)' + re.escape(day) + r'(?!\d)', words):
        return True
    month, abbr = calendar.month_name[value.month], calendar.month_abbr[value.month]
    names = '(?:' + '|'.join(re.escape(x) for x in [month, abbr] + (['Sept'] if value.month == 9 else [])) + r')\.?'
    day_word = str(value.day) + r'(?:st|nd|rd|th)?'
    if re.search(r'\b' + names + r'\s+' + day_word + r'\s*,?\s+' + str(value.year) + r'\b', words, re.I) or \
            re.search(r'\b' + day_word + r'\s+' + names + r'\s*,?\s+' + str(value.year) + r'\b', words, re.I):
        return True
    for m in re.finditer(r'(?<!\d)(\d{1,2})[/-](\d{1,2})[/-](\d{4})(?!\d)', words):
        first, second, year = map(int, m.groups())
        if year == value.year and (first, second) in ((value.month, value.day), (value.day, value.month)) and (first > 12 or second > 12 or first == second):
            return True
    return False


def admission_problem(c, m, question, publication_day, universe):
    """Each admission reason's limits (standard §3–§4, D184, D185, D210), with or without a ladder. Missing material or dates never reject."""
    reason = m['opens_as']
    if reason in ANNUAL_REASONS:
        if reason == 'main_driver' and c['kind'] == 'asset' and extraction.QUARTERLY.search(question):
            return 'quarterly number: evidence, not a question (06-views ladder rule 6)'
        year = question_year(question, m.get('year', ''))
        if year and extraction.beyond_next_year(year, publication_day, c['object'], universe):
            return f'year {year} is beyond next year: not opened (06-views ladder rule 5)'
    if reason == 'binding_obligation' and m.get('obligation_state') == 'unsigned' and c.get('due_day'):
        limit = datetime.date.fromisoformat(publication_day) + datetime.timedelta(days=extraction.BINDING_HORIZON_DAYS)
        if datetime.date.fromisoformat(c['due_day']) > limit:
            return f'an unsigned obligation is checked within 18 months ({c["due_day"]} > {limit.isoformat()})'
    return None


# ---------------------------------------------------------------- the handover

def stage_answers(item, text, answers, names):
    """Source-check every passage of every section's A and B answers; find statements both calls quoted and B's passages with no home."""
    questions, slots, a_passages, b_passages, dropped, groups = [], [], [], [], [], []
    group_offset = 0
    for a, b in answers:
        local = {}
        for g in a.get('new_groups', []):
            group_offset += 1
            local[g['id']] = 'n' + str(group_offset)
            groups.append(dict(g, id=local[g['id']]))
        for q in a['questions']:
            cid = 'c' + str(len(questions) + 1)
            refs = [local.get(r, '?' + r) for r in q.get('group_refs', [])]
            questions.append(q)
            slots.append({'id': cid, 'group_refs': refs, 'passage_ids': []})
            for e in q['evidence']:
                eid = 'e' + str(len(a_passages) + 1)
                exact = source_quote(e['quote'], text, names)
                a_passages.append(dict(e, id=eid, cid=cid, exact=exact))
                if exact is None:
                    dropped.append((eid, 'A quote absent from the article'))
                else:
                    slots[-1]['passage_ids'].append(eid)
        for e in b['evidence']:
            bid = 'b' + str(len(b_passages) + 1)
            exact = source_quote(e['quote'], text, names)
            b_passages.append(dict(e, bid=bid, exact=exact))
            if exact is None:
                dropped.append((bid + ' ' + e['id'], 'B quote absent from the article'))
    a_by_quote = {}
    for e in a_passages:
        if e['exact'] is not None:
            a_by_quote.setdefault(extraction.normalise(e['exact']), e['id'])
    other, unfiled = {}, []
    for e in b_passages:
        if e['exact'] is None:
            continue
        twin = a_by_quote.get(extraction.normalise(e['exact']))
        if twin and twin not in other:
            other[twin] = e
        if not e['links'] and not twin:
            unfiled.append(dict(e, uid='u' + str(len(unfiled) + 1), quote=e['exact']))
    return {'questions': questions, 'candidate_slots': slots, 'a_passages': [e for e in a_passages if e['exact'] is not None],
            'all_a_passages': a_passages, 'b_passages': b_passages, 'other_readings': other, 'unfiled': unfiled, 'dropped': dropped, 'groups': groups}


def _ordered(values, prefix, count):
    expected = [prefix + str(i) for i in range(1, count + 1)]
    if not isinstance(values, dict) or set(values) != set(expected):
        raise SplitError('record preparation ids differ from the answer')
    return [values[k] for k in expected]


def build_handover(item, text, shown, universe, stage, prep):
    """The checked handover: one record per quoted statement (every distinct summary and every link kept, attribution from record preparation),
    candidates with their checked fields, B's unfiled passages kept only where record preparation linked them to a candidate."""
    shown_ids = {v['view_id'] for v in shown}
    dropped = list(stage['dropped'])
    metas = _ordered(prep['candidates'], 'c', len(stage['questions'])) if stage['questions'] else []
    attributions = _ordered(prep['evidence'], 'e', len(stage['a_passages'])) if stage['a_passages'] else []
    unfiled_links = _ordered(prep['unfiled'], 'u', len(stage['unfiled'])) if stage['unfiled'] and stage['questions'] else None
    # A passages: record preparation numbered them in order e1..; map its numbering back to the stage ids
    prepared = {e['id']: attributions[i] for i, e in enumerate(stage['a_passages'])}
    records, by_quote = [], {}

    def add(piece, links, summary):
        key = extraction.normalise(piece['quote'])
        if key in by_quote:
            first = by_quote[key]
            first['links'].extend(l for l in links if l not in first['links'])
            if summary and summary not in first['summaries']:
                first['summaries'].append(summary)
            return first['id']
        record = dict(piece, links=list(links), summaries=[summary] if summary else [])
        by_quote[key] = record
        records.append(record)
        return record['id']

    alias = {}
    for e in stage['a_passages']:
        fields = prepared[e['id']]
        piece = {'id': e['id'], 'quote': e['exact'], 'speaker': fields['speaker'], 'original_who': fields['original_who'],
                 'original_day': extraction.statement_day(fields['original_day']), 'tier': fields['tier'], 'event_time': fields['event_time']}
        alias[e['id']] = add(piece, [e['cid']], e['what_it_shows'])
    for e in stage['b_passages']:
        if e['exact'] is None:
            continue
        if any(x not in shown_ids for x in e['links']):
            raise SplitError('B link was not shown')
        links = list(e['links'])
        unfiled = next((u for u in stage['unfiled'] if u['bid'] == e['bid']), None)
        if unfiled is not None:
            links = list(unfiled_links[int(unfiled['uid'][1:]) - 1]['links']) if unfiled_links is not None else []
            if not links:
                dropped.append((e['bid'] + ' ' + e['id'], 'no home: no existing question and no new question of this item takes it'))
                continue
        key = extraction.normalise(e['exact'])
        if key not in by_quote:
            piece = {'id': 'e' + str(len(stage['all_a_passages']) + int(e['bid'][1:])), 'quote': e['exact'], 'speaker': e['speaker'],
                     'original_who': e['original_who'], 'original_day': extraction.statement_day(e.get('original_day')), 'tier': e['tier'], 'event_time': e['event_time']}
            add(piece, links, e['one_line'])
        else:
            merged_into = by_quote[key]['id']
            from_a = merged_into in alias.values()
            add({'quote': e['exact']}, links, e['one_line'])
            dropped.append((e['bid'] + ' ' + e['id'], f'same statement as {merged_into}; merged' + (' (attribution from record preparation)' if from_a else '')))
    evidence = []
    for r in records:
        summary = ' | '.join(r.pop('summaries'))
        evidence.append(dict(r, one_line=summary))
    # candidates
    candidates = []
    for slot, q, m in zip(stage['candidate_slots'], stage['questions'], metas):
        cid = slot['id']
        ids = list(dict.fromkeys(alias[p] for p in slot['passage_ids']))
        kept = [e['id'] for e in evidence if cid in e['links']]
        if not kept:
            dropped.append((cid, 'candidate without surviving evidence'))
            continue
        subject, new_kind = chosen_subject(m, q['question'])
        kind = ('theme' if new_kind == 'theme' else 'asset') if new_kind else ('theme' if subject in universe.themes else 'asset')
        check = q['how_and_when_to_check'].strip()
        basis, provenance, due = m.get('date_basis', 'unknown'), m.get('date_provenance', ''), m.get('due_day', '')
        try:
            if due:
                datetime.date.fromisoformat(due)
        except ValueError:
            due = ''
        if due and (basis == 'unknown' or not provenance or not explicit_day(due, provenance)
                    or (basis == 'source_stated' and provenance not in text) or (basis == 'analyst_check' and provenance not in check)):
            due = ''
        c = {'id': cid, 'kind': kind, 'object': subject, 'question': q['question'], 'year': m.get('year', ''), 'due_day': due, 'group_refs': [],
             'evidence_ids': kept, 'opens_as_reason': m['opens_as']}
        problem = admission_problem(c, m, q['question'], item['publication_day'], universe)
        if problem:
            dropped.append((cid, problem))
            continue
        rungs, ladder_problem = ordered_ladder(m.get('rungs'), kind, m.get('favourable_end'), m.get('unit'))
        if ladder_problem:
            dropped.append((cid + ' ladder', ladder_problem))
        c['rungs'] = rungs
        focus = q['question'] + (' | How to check: ' + check if check else '')
        if due:
            focus += ' | Date basis: ' + basis + '; words: ' + provenance
        else:
            estimate = analyst_check_day(c, m, universe, item['publication_day'])
            if estimate and estimate > item['publication_day']:
                c['due_day'] = estimate
                focus += ' | Date basis: analyst_check (expected settling material; not a source date)'
        c['looks_at'] = focus
        if q.get('closest_existing_question', 'none') != 'none':
            c['closest_existing'] = q['closest_existing_question']
        c['group_refs'] = [r for r in slot['group_refs'] if not r.startswith('?')]
        c.update(shared_key(m, kind))
        candidates.append(c)
    kept_ids = {c['id'] for c in candidates}
    final = []
    for e in evidence:
        links = [l for l in e['links'] if l in shown_ids or l in kept_ids]
        if not links:
            dropped.append((e['id'], 'no home: its only question was not opened'))
            continue
        final.append(dict(e, links=extraction.narrowest_links(links, {v['view_id']: v.get('parents') or [] for v in shown})))
    used = {r for c in candidates for r in c['group_refs']}
    groups = [{'id': g['id'], 'name': g['name'].strip(), 'scope': g['scope'].strip(), 'aliases': [a.strip() for a in g.get('aliases') or [] if a.strip()]}
              for g in stage['groups'] if g['id'] in used and g['name'].strip() and g['scope'].strip()]
    for c in candidates:
        c['group_refs'] = [r for r in c['group_refs'] if r in {g['id'] for g in groups}]
    return final, candidates, dropped, groups


# ---------------------------------------------------------------- one item

def extract(archive, cfg, item, text, shown, universe, *, conn, seq, transport=None, log=print):
    """One item through A, B and record preparation; returns the checked handover (subjects registered in the ledger with the item)."""
    names = subject_names(item, universe)
    answers, cost, cached, call_id, shas, proposed = [], 0.0, True, 0, [], []
    for part in sections(text):
        setting, a_spec, b_spec = requests(cfg, item, part, shown, universe, proposed)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(model.call, archive, cfg, cfg.split[lane], spec[0], spec[1], spec[2], spec[3], 'split_' + lane, transport=transport)
                       for lane, spec in (('a', a_spec), ('b', b_spec))]
            a_answer, b_answer = [f.result() for f in futures]
        for answer in (a_answer, b_answer):
            cost += answer.cost_usd
            cached = cached and answer.cached
            call_id = answer.call_id
            shas.append(answer.request_sha256)
            if answer.input_tokens > REQUEST_ALERT_TOKENS:
                log(f'  request-size alert: {answer.input_tokens} input tokens for {item["input_id"]}')
        answers.append((a_answer.data, b_answer.data))
        proposed += [q['question'] for q in a_answer.data['questions']]
    stage = stage_answers(item, text, answers, names)
    prep = {'candidates': {}, 'evidence': {}, 'unfiled': {}}
    if stage['questions']:
        spec = preparation_request(cfg, item, text, universe, stage)
        answer = model.call(archive, cfg, cfg.split['preparation'], spec[0], spec[1], spec[2], spec[3], 'split_preparation', transport=transport)
        prep = answer.data
        cost += answer.cost_usd
        cached = cached and answer.cached
        call_id = answer.call_id
        shas.append(answer.request_sha256)
    evidence, candidates, dropped, groups = build_handover(item, text, shown, universe, stage, prep)
    register_subjects(conn, universe, candidates, seq, item['input_id'])
    return extraction.Handover(evidence, candidates, dropped, call_id, hashlib.sha256('+'.join(shas).encode()).hexdigest(), cached, cost, groups)
