"""Extraction (docs/prd/05-extraction.md): the whole item goes to the model with its category's prompt, the questions open at the
start of the item's day (each with its takes line) and the filing rule beside the links field; the answer is evidence filed under those
questions or under this answer's candidate questions, and candidates written in full. Code checks the sources (the quote is in the
text, every link points at a shown question or a kept candidate), the ladders (five rungs or two) and the rule that quarterly numbers
are evidence, not questions; a statement filed nowhere is dropped as 'no home' (D209).

The request is the frozen production prompt, extraction v74i (D274). No other version is built: a configuration that names another
is refused before any call, and a new version is a new decision with its own code. Every answer is read in the canonical vocabulary."""
import dataclasses
import datetime
import difflib
import json
import re

from . import config, model, placement, vocabulary
from .universe import parse_year

TIERS = vocabulary.TIERS
MAX_TEXT_CHARS = 400_000
SUPPORTED_VERSIONS = ('v74i',)    # D274: the frozen production prompt
# D184: the closed set of reasons a candidate question may open; anything else is evidence to a shown question
ADMISSION_REASONS = ['main_driver', 'industry_aggregate', 'policy_stage', 'binding_obligation']
BINDING_HORIZON_DAYS = 548        # D185: a binding obligation is due within 18 months of the item, and is exempt from the next-year rule on quantities
# The three attribution fields carry their definitions in the schema, beside the field they govern (standard 5.4: the original
# claimant; an unknown statement day is unknown, never the report day; D220, D203; 5.5: relays of one report are one source)
FIELD_NOTES = {
    'speaker': 'Who says it in this item: the outlet, the author or the person quoted.',
    'original_who': ('The party whose statement, figure or action it is, even when the item reports it without attribution ("the insurer agreed '
                     'to buy the broker": the insurer; "the regulator fined the bank, a newspaper reported": the regulator); the outlet or author '
                     'only for its own estimate, analysis or unnamed-source report.'),
    'original_day': ('The day that party made it, as an ISO day when the item gives one ("signed on 3 March 2026": 2026-03-03); empty when the '
                     "item gives none or only a month; the publication day only when the item is that party's own release, filing, call or analysis."),
}


def require_supported(version):
    """Refuses a prompt version this code does not build, before any request is made."""
    if version not in SUPPORTED_VERSIONS:
        raise ValueError(f'extraction {version!r} is not built; this code builds only {", ".join(SUPPORTED_VERSIONS)} (D274)')


def shown_views(conn, cfg, item, objects):
    """The questions an item's extraction request shows (05-extraction block 5): the objects' questions open at the start of the
    item's day, the same list for every item of that day (D251), with the key, groups and aliases each had then (they feed its takes
    line) and its direct parents (they feed the narrowest rule). The one place the stream and the parallel runner take the list from."""
    require_supported(cfg.extraction_setting(item['category']).prompt_version.rpartition('-')[2])
    from .views import store
    return [dict(v, key=store.view_key(conn, v['view_id']) or {},
                 groups=[{'name': g['name'], 'scope': g['scope'], 'aliases': g.get('aliases') or []}
                         for g in store.groups_of_view_at(conn, v['view_id'], v['snapshot_seq'])],
                 parents=store.direct_parents(conn, v['view_id'], v['snapshot_seq']))
            for v in store.views_open_at_day_start(conn, objects, item['publication_day'])]


def narrowest_links(links, parents):
    """D207's one rule the filing enforces in code (2026-11-02, D265): a statement linked to a question and to a question that question
    depends on (a driver and its root, transitively) keeps the narrower one only. `parents` maps a view id to the ids it depends on."""
    def ancestors(view_id, seen):
        for parent in parents.get(view_id, ()):
            if parent not in seen:
                seen.add(parent)
                ancestors(parent, seen)
        return seen
    broader = set()
    for link in links:
        broader |= ancestors(link, set())
    return [l for l in links if l not in broader]



def base_schema():
    return {
        'type': 'object', 'additionalProperties': False, 'required': ['evidence', 'candidates'],
        'properties': {
            'evidence': {'type': 'array', 'items': {
                'type': 'object', 'additionalProperties': False,
                'required': ['id', 'quote', 'one_line', 'speaker', 'original_who', 'original_day', 'tier', 'event_time', 'links'],
                'properties': {
                    'id': {'type': 'string'}, 'quote': {'type': 'string'}, 'one_line': {'type': 'string'}, 'speaker': {'type': 'string'},
                    'original_who': {'type': 'string'}, 'original_day': {'type': 'string'}, 'tier': {'type': 'string', 'enum': TIERS},
                    'event_time': {'type': 'string'}, 'links': {'type': 'array', 'items': {'type': 'string'}}}}},
            'candidates': {'type': 'array', 'items': {
                'type': 'object', 'additionalProperties': False,
                'required': ['id', 'object', 'kind', 'looks_at', 'question', 'rungs', 'due_day', 'year', 'evidence_ids'],
                'properties': {
                    'id': {'type': 'string'}, 'object': {'type': 'string'}, 'kind': {'type': 'string', 'enum': vocabulary.KINDS},
                    'looks_at': {'type': 'string'}, 'question': {'type': 'string'},
                    'rungs': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['label', 'condition'],
                                                           'properties': {'label': {'type': 'string'}, 'condition': {'type': 'string'}}}},
                    'due_day': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'},      # a date, enforced by the schema, not by prose
                    'year': {'type': 'string'}, 'evidence_ids': {'type': 'array', 'items': {'type': 'string'}}}}},
        },
    }


# keyed-views-plan.md 2.1 and D167: the key a candidate carries; a market's size and a project's cost are measures of their own
MEASURES = ['total_revenue', 'segment_revenue', 'product_revenue', 'gross_margin', 'operating_margin', 'operating_expense_growth', 'total_expenses', 'operating_loss',
            'tax_rate', 'capex', 'shipments_or_capacity', 'run_rate', 'design_wins', 'event', 'spend_total', 'market_size', 'project_cost', 'financing_amount',
            'price', 'capacity', 'growth_rate', 'policy_event', 'other']
EVENT_TYPES = ['launch', 'shipment', 'licence', 'approval', 'deal_close', 'deployment', 'other', 'n/a']
BASES = ['GAAP', 'non_GAAP', 'n/a']
UNITS = ['USD', 'percent', 'count', 'GW', 'MW', 'TWD', 'multiple', 'n/a']


def key_fields():
    return {'measure': {'type': 'string', 'enum': list(MEASURES)}, 'scope': {'type': 'string'},
            'period_start': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'}, 'period_end': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'},
            'basis': {'type': 'string', 'enum': BASES}, 'unit': {'type': 'string', 'enum': UNITS}, 'event_type': {'type': 'string', 'enum': EVENT_TYPES}}


BOUND = {'anyOf': [{'type': 'number'}, {'type': 'null'}]}


def keyed_schema():
    """The base schema with the key fields on every candidate and numeric bounds on every rung."""
    schema = base_schema()
    candidate = schema['properties']['candidates']['items']
    fields = key_fields()
    candidate['properties'].update(fields)
    candidate['required'] += list(fields)
    rung = candidate['properties']['rungs']['items']
    rung['properties'].update({'lo': BOUND, 'hi': BOUND})
    rung['required'] += ['lo', 'hi']
    return schema


LOCAL_GROUP = r'n[1-9][0-9]*'
# a company's own reported or guided lines: they belong to the company and never found a research group by themselves
FINANCIAL_LINES = {'total_revenue', 'segment_revenue', 'gross_margin', 'operating_margin', 'operating_expense_growth', 'total_expenses', 'operating_loss', 'tax_rate', 'capex', 'run_rate'}


def tracks_a_matter(candidate):
    """A candidate that can start a research group: a theme quantity, an event or policy event, a product or market figure;
    not a company's own financial line (which may join a group another thesis started, never found one)."""
    return candidate.get('kind') == 'theme' or candidate.get('measure') not in FINANCIAL_LINES



def grouped_schema():
    """The keyed schema plus research-group membership (D149, D166, D211): the request shows no stored group, so each candidate cites
    only local ids it declares in new_groups with their aliases; code folds a declared group into a stored one by its names."""
    schema = keyed_schema()
    pattern = '^(?:' + LOCAL_GROUP + ')$'
    candidate = schema['properties']['candidates']['items']
    candidate['properties']['group_refs'] = {'type': 'array', 'items': {'type': 'string', 'pattern': pattern}}
    candidate['required'].append('group_refs')
    group_fields = {'id': {'type': 'string', 'pattern': '^' + LOCAL_GROUP + '$'}, 'name': {'type': 'string'}, 'scope': {'type': 'string'},
                    'aliases': {'type': 'array', 'items': {'type': 'string'}}}
    schema['properties']['new_groups'] = {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': list(group_fields), 'properties': group_fields}}
    schema['required'].append('new_groups')
    return schema


def with_field_notes(schema, notes):
    """The schema with the notes as the descriptions of the evidence fields they name."""
    fields = schema['properties']['evidence']['items']['properties']
    for name, note in notes.items():
        fields[name] = dict(fields[name], description=note)
    return schema


def schema_for(version, shown_view_ids=()):
    """The answer's schema: the grouped schema, the admission fields (D184: the reason a candidate opens and the material that settles
    it), the attribution fields' definitions and the filing rule beside the links field (D256, D274). The request shows its questions
    in the text and names none in the schema, so shown_view_ids does not change it."""
    require_supported(version)
    schema = grouped_schema()
    candidate = schema['properties']['candidates']['items']
    candidate['properties'].update({'opens_as': {'type': 'string', 'enum': list(ADMISSION_REASONS)}, 'settled_by': {'type': 'string'}})
    candidate['required'] += ['opens_as', 'settled_by']
    return with_field_notes(schema, dict(FIELD_NOTES, links=placement.FILING_RULE_ROOT_FALLBACK))


@dataclasses.dataclass
class Handover:
    evidence: list
    candidates: list
    dropped: list
    call_id: int
    request_sha256: str
    cached: bool
    cost_usd: float
    new_groups: list = dataclasses.field(default_factory=list)      # the declared groups a kept candidate cites: {id, name, scope}


SELF_PUBLISHER_TYPE = 'self'      # the owner's own memo (02-classification T8, D59): its judgements are candidates without evidence


def _read(name):
    with open(config.prompt_path(name), encoding='utf-8') as handle:
        return handle.read()


def _categories(version):
    return json.loads(_read(f'categories-{version}.json'))



GLYPHS = str.maketrans({'’': "'", '‘': "'", '“': '"', '”': '"', '—': '-', '–': '-'})


def normalise(text):
    """The form in which a quote is compared with the item's text: one space between words, no space before closing
    punctuation or after an opening bracket, plain quote and dash glyphs, lower case. The cleaned page text keeps a space
    where an inline tag stood (" , "); the model writes the sentence with ordinary punctuation, and both are the same text."""
    text = re.sub(r'\s+', ' ', text.translate(GLYPHS))
    text = re.sub(r"\s+([,.;:!?')\]])", r'\1', text)
    text = re.sub(r'([(\[])\s+', r'\1', text)
    return text.strip().lower()


# D236: a quote the plain check misses is still the item's text when it differs only by punctuation, quotation marks, footnote
# markers or case, or leaves out one run of words inside one sentence; the stored quote is then the exact source passage, so a
# stored quote is always verbatim. Any added, changed or reordered word or number, a dropped +/− on a number or a changed currency
# is refused; a comparison sign (>, ~, ≥) is not a token, so a quote that drops one is repaired to the source text that carries it.
QUOTE_TOKEN = re.compile(r"\[\d{1,3}\]|[-+−]?[$€£¥]?\d+(?:[.,:/]\d+)*%?|[^\W_]+(?:['./&-][^\W_]+)*|[$€£¥%]")
_FOOTNOTE = re.compile(r'\[\d{1,3}\]$')
_SENTENCE_END = re.compile(r"[.!?…][\"')\]”’]*\s|\n")
_OPENING = re.compile(r"[\"'(\[“‘]+$")
_CLOSING = re.compile(r"[.!?]?[\"')\]”’]*")


def _quote_tokens(text):
    """The words and numbers a quote is compared by, with their character spans in text (GLYPHS maps one character to one)."""
    plain = text.translate(GLYPHS)
    return [(m.group(0).lower(), m.start(), m.end()) for m in QUOTE_TOKEN.finditer(plain) if not _FOOTNOTE.match(m.group(0))]


def _source_passage(text, start, end):
    before = _OPENING.search(text[max(0, start - 3):start])
    if before:
        start -= len(before.group(0))
    return text[start:end + len(_CLOSING.match(text, end).group(0))]


def _runs(needle, tokens):
    return [i for i in range(len(tokens) - len(needle) + 1) if tokens[i] == needle[0] and tokens[i:i + len(needle)] == needle]


def repair_quote(quote, text, subject_names=()):
    """The source passage a refused quote stands for (D236, D266), or None. Accepted: the quote's words equal one passage's words
    (punctuation, quotation marks, footnote markers and case aside), or equal them with one run left out that lies inside one
    sentence and is shorter than the quote; or (D266) differ from them by a word or two that is a function word, a pronoun, a generic
    word for the company or one of `subject_names` (the subject company's own name), never a number or any other word; or copy one
    passage exactly and run on past its sentence end."""
    if len(normalise(quote)) < 8:
        return None
    spans = _quote_tokens(text)
    source_tokens = [token for token, _, _ in spans]
    quote_tokens = [token for token, _, _ in _quote_tokens(quote)]
    if not quote_tokens:
        return None
    found = _runs(quote_tokens, source_tokens)
    if found:
        return _source_passage(text, spans[found[0]][1], spans[found[0] + len(quote_tokens) - 1][2])
    best = None                                              # (left-out length, first token, last token) of the shortest gap
    for split in range(1, len(quote_tokens)):
        head, tail = quote_tokens[:split], quote_tokens[split:]
        for tail_start in _runs(tail, source_tokens):
            for gap_start in range(tail_start - 1, split - 1, -1):          # tokens gap_start..tail_start-1 are the left-out run
                if tail_start - gap_start >= len(quote_tokens) or _SENTENCE_END.search(text[spans[gap_start - 1][2]:spans[tail_start][1]]):
                    break
                if source_tokens[gap_start - split:gap_start] == head:
                    if best is None or tail_start - gap_start < best[0]:
                        best = (tail_start - gap_start, gap_start - split, tail_start + len(tail) - 1)
                    break
    if best is not None:
        return _source_passage(text, spans[best[1]][1], spans[best[2]][2])
    near = _near_run(quote_tokens, source_tokens, subject_names)   # D266: a function word or the company's own name changed, added or dropped
    if near is not None:
        return _source_passage(text, spans[near[0]][1], spans[near[1]][2])
    prefix = _exact_prefix(quote_tokens, source_tokens, spans, text)   # D266: a quote that runs on past the passage it copied keeps that passage
    if prefix is not None:
        return _source_passage(text, spans[prefix[0]][1], spans[prefix[1]][2])
    return None


# D266 (2026-11-02, Alex: the quote refusals of core statements are an important class, fix it quickly): the stored quote is still the exact
# source passage; what widens is which model quotes are matched to one. A quote of at least NEAR_MIN_TOKENS words whose words differ from one
# source window's by at most NEAR_EDITS(n) word edits, every edited word a function word, a pronoun, a generic word for the company or the
# subject company's own name ("the company's" written as the name; "While" as "As"), is that window; a quote that copies one passage
# exactly and then runs on into other text keeps the copied passage when it is at least NEAR_MIN_TOKENS words and ends at a sentence end.
# A changed month, party, product or number, a paraphrase, and two names swapped are refused as before (D236's tests hold).
NEAR_MIN_TOKENS = 8
HARMLESS_TOKENS = frozenset('''the a an this that these those it its it's he she they their his her hers we our ours my your you
    as while although though meanwhile however but and or so because since then also too for of to in on at by with from into over under
    about example instance first all additionally moreover further furthermore still yet now here there is are was were be been being
    has have had do does did will would could should might can that's which who whom whose what when where said says say
    company company's firm firm's chipmaker chipmaker's giant giant's maker maker's group group's'''.split())     # not "may": a month


def NEAR_EDITS(length):
    return 2 if length <= 30 else 3


def _harmless(subject_names):
    names = set()
    for name in subject_names:
        for token, _, _ in _quote_tokens(name):
            names.add(token)
            names.add(token + "'s")
    return HARMLESS_TOKENS | names


def _edited_tokens(quote_tokens, window):
    """(number of word edits, the words involved on both sides) between the quote and one source window, by the aligned difference."""
    edits, involved = 0, []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, quote_tokens, window, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        edits += max(i2 - i1, j2 - j1)
        involved += quote_tokens[i1:i2] + window[j1:j2]
    return edits, involved


def _near_run(quote_tokens, source_tokens, subject_names=()):
    """(first, last) source token indexes of a window the quote matches within NEAR_EDITS word edits that all fall on harmless words,
    anchored on the quote's first or last three words appearing exactly; None otherwise."""
    n = len(quote_tokens)
    if n < NEAR_MIN_TOKENS:
        return None
    limit = NEAR_EDITS(n)
    harmless = _harmless(subject_names)
    anchors = set()
    for position in _runs(quote_tokens[:3], source_tokens):
        anchors.update(range(position - limit, position + limit + 1))
    for position in _runs(quote_tokens[-3:], source_tokens):
        anchors.update(range(position + 3 - n - limit, position + 3 - n + limit + 1))
    best = None
    for start in sorted(a for a in anchors if a >= 0):
        window = source_tokens[start:start + n]             # the same length: words substituted, none added or dropped (a dropped last word
        if len(window) != n:                                # would otherwise match a passage cut short)
            continue
        edits, involved = _edited_tokens(quote_tokens, window)
        if 0 < edits <= limit and all(t in harmless for t in involved) and (best is None or edits < best[0]):
            best = (edits, start, start + n - 1)
    return best[1:] if best else None


def _exact_prefix(quote_tokens, source_tokens, spans, text):
    """(first, last) source token indexes of the longest prefix of the quote, at least NEAR_MIN_TOKENS words, that occurs exactly in
    the source and ends at a sentence end there; None otherwise."""
    for length in range(len(quote_tokens) - 1, NEAR_MIN_TOKENS - 1, -1):
        for position in _runs(quote_tokens[:length], source_tokens):
            end = spans[position + length - 1][2]
            if end >= len(text) or _SENTENCE_END.match(text[end:end + 4]) or _CLOSING.fullmatch(text[end:end + 2] or '') and text[end:end + 1] in '.!?':
                return position, position + length - 1
    return None


def item_header(item, category):
    """The line that opens the item in an English extraction request; preflight reads archived requests by it."""
    return (f'[Item] id {item["input_id"]}, category {category}, author {item.get("publisher")} ({item.get("publisher_type")}), '
            f'published {item.get("publication_day")}, title: {item.get("title") or ""}\n\n')


def _watched_lines(objects, universe):
    """keyed-views-plan.md 2.4 / D155: the quantities the analyst watches, as a reference, with the exact scope names."""
    watched = []
    for o in objects:
        entries = universe.watch_list(o) if hasattr(universe, 'watch_list') else []
        if entries:
            sep = '; '
            watched.append(f'  - {o}: ' + sep.join(e['measure'] + (f"[{e['scope']}]" if e.get('scope') else '') + (f"({e['event_type']})" if e.get('event_type') else '') for e in entries))
    return watched



# 05-extraction block 5b (D149, D166): the standing instruction; code folds a declared group into a stored one by its names
GROUPS_INSTRUCTION = ('[Research groups] None yet. For a candidate that tracks an ongoing matter (a product rollout, a deal, a policy process, an investment or demand cycle), '
                      'declare the group in new_groups (local ids n1, n2 …) and cite it in group_refs; leave group_refs empty for a company\'s own financial lines.')
CLOSING = ('Return evidence and candidates per the JSON schema. A candidate\'s evidence_ids are its own evidence ids; an evidence item\'s links are '
           'open question ids from [Open questions], this answer\'s candidate ids (such as c1), or empty. '
           'year names the fiscal or calendar year the figure covers (FY2027, or 2026 for a calendar year).')


def build_prompt(item, text, shown_views, universe, version):
    """The request's two texts. The system text is the role; the user text is the category and how to read it, the subjects with the
    theme list and the fiscal-year note, what to read out, the research reference, the questions open at the start of the item's day
    with their takes lines, the research-group instruction, the item, the closing sentence and the end-of-request check."""
    require_supported(version)
    category = item['category']
    categories = _categories(version)
    blocks = categories.get(category) or categories['T7']
    objects = [o['value'] for o in item.get('object_identifiers') or []]
    themes = '\n'.join(f'  - {theme_id}: {name}' for theme_id, name in universe.theme_list())
    fiscal = '\n'.join(note for note in (universe.fiscal_note(o, item['publication_day'], english=True) for o in objects) if note)
    parts = [
        f'[Category and how to read it] {category}. {blocks["what"]}',
        f'[Subjects] The objects this item concerns: {", ".join(objects) or "(not labelled upstream)"}. For a candidate thesis about a company, object is its ticker; '
        f'about a theme, choose an id from this list, or state what the matter is when none fits:\n{themes}'
        + (f'\nFiscal-year note (a numeric thesis takes its year and due date from it):\n{fiscal}' if fiscal else ''),
        f'[What to read out] {blocks["read"]}',
    ]
    watched = _watched_lines(objects, universe)
    if watched:
        parts.append('[Research reference] Existing quantities and scopes (measure[scope](event_type)). Reuse a name only when the meaning is the same; '
                     'propose important questions outside the list as usual, with their actual scope:\n' + '\n'.join(watched))
    lines = placement.question_lines(shown_views)
    parts.append(f'[Open questions at the start of {item["publication_day"]}]\n' + ('\n'.join(lines) if lines else '  None yet.'))
    parts.append(GROUPS_INSTRUCTION)
    parts.append(item_header(item, category) + text[:MAX_TEXT_CHARS])
    parts.append(CLOSING)
    parts.append(_read(f'review-{version}.txt').strip())
    return _read(f'role-{version}.txt'), '\n\n'.join(parts)


OBJECT_LABELS = vocabulary.ASSET_LABELS


def check_ladder(rungs, kind):
    """None when the ladder is well formed, else the problem. An asset ladder written from Strongly bearish up to
    Strongly bullish (the model often orders a revenue ladder by rising value) is the same ladder; normalise_ladder
    turns it round. Labels are compared in the canonical vocabulary."""
    if len(rungs) not in (2, 5):
        return f'ladder has {len(rungs)} rungs, needs 5 (or 2 for yes/no)'
    if any(not r['label'].strip() or not r['condition'].strip() for r in rungs):
        return 'a rung has an empty label or condition'
    if kind == 'asset' and len(rungs) == 5:
        labels = [vocabulary.canonical('label', r['label']) for r in rungs]
        if labels != OBJECT_LABELS and labels != OBJECT_LABELS[::-1]:
            return f'object view rungs must be {OBJECT_LABELS}, got {labels}'
    return None


def normalise_ladder(rungs, kind):
    """Position 1 is Strongly bullish (06-views): a reversed asset ladder is turned round, label and condition together."""
    if kind == 'asset' and len(rungs) == 5 and [vocabulary.canonical('label', r['label']) for r in rungs] == OBJECT_LABELS[::-1]:
        return list(reversed(rungs))
    return rungs


# 06-views ladder rule 6: a quarterly or half-year figure is evidence, not a view. The half-year forms name a revenue
# or sales figure (H1 收入, first-half revenue); an event scheduled in a half-year (ships in H2 2026) is not a figure.
QUARTERLY = re.compile(r'(\bQ[1-4]\b|第[一二三四1-4]季|季度|\bquarter(?!ly report)|fiscal Q[1-4]|\b(?:[12]H|H[12])\b(?:\s+(?:FY)?\d{4})?\s*收入|上半年收入|下半年收入'
                       r'|\b(?:[12]H|H[12])\b(?:\s+(?:FY)?\d{4})?\s+(?:revenue|sales|net sales)|\b(?:first|second)[- ]half(?:[- ]year)?\s+(?:revenue|sales|net sales)'
                       r'|\bhalf[- ]year\s+(?:revenue|sales|net sales))', re.I)


def request_for(cfg, item, text, shown_views, universe):
    """Build the setting, complete prompt and schema without making a call."""
    setting = cfg.extraction_setting(item['category'])
    version = setting.prompt_version.rpartition('-')[2]
    system, user = build_prompt(item, text, shown_views, universe, version)
    return setting, system, user, schema_for(version)


@dataclasses.dataclass
class Reading:
    """An item read: the extraction answer through the code checks, before the handover (the parallel day prepares it early and
    files it at the item's turn)."""
    evidence: list
    candidates: list
    dropped: list
    new_groups: list
    answer: object
    version: str


def read_item(archive, cfg, item, text, shown_views, universe, *, transport=None):
    """The extraction call and the code checks on its answer: a statement may link to a shown question or to a kept candidate."""
    setting, system, user, schema = request_for(cfg, item, text, shown_views, universe)
    answer = model.call(archive, cfg, setting, system, user, schema, 'extraction', 'extract', transport=transport)
    evidence, candidates, dropped, new_groups = sift_with_groups(answer.data, item, text, {v['view_id'] for v in shown_views}, universe)
    return Reading(evidence, candidates, dropped, new_groups, answer, setting.prompt_version.rpartition('-')[2])


def file_reading(reading, item, shown_views):
    """The handover: the extraction's own links are the filing (D256). A statement linked to a question and to a question that
    question depends on keeps the narrower one (D207); a statement no open question and no kept candidate takes is dropped as 'no
    home' (D209), like every other drop: a candidate left with none of its evidence is dropped too, and a statement whose only link was
    such a candidate has no home."""
    candidates, dropped, answer = reading.candidates, list(reading.dropped), reading.answer
    parents = {v['view_id']: v.get('parents') or [] for v in shown_views}
    evidence = [dict(e, links=narrowest_links(e['links'], parents)) for e in reading.evidence]
    while True:
        candidates = candidates_with_evidence(candidates, {e['id'] for e in evidence}, item, dropped)
        candidate_ids = {c['id'] for c in candidates}
        evidence = [dict(e, links=[l for l in e['links'] if not placement.CANDIDATE_ID.match(l) or l in candidate_ids]) for e in evidence]
        homeless = [e for e in evidence if not e['links']]
        if not homeless:
            break
        dropped.extend((e['id'], 'no home') for e in homeless)
        evidence = [e for e in evidence if e['links']]
    return Handover(evidence, candidates, dropped, answer.call_id, answer.request_sha256, answer.cached, answer.cost_usd, reading.new_groups)


def extract(archive, cfg, item, text, shown_views, universe, *, transport=None):
    """One item through extraction: read, then file under the questions shown."""
    return file_reading(read_item(archive, cfg, item, text, shown_views, universe, transport=transport), item, shown_views)


def check_bounds(rungs):
    """None when the rungs' numeric bounds form one unbroken partition (or none carries bounds), else the problem."""
    bounded = [r for r in rungs if r.get('lo') is not None or r.get('hi') is not None]
    if not bounded:
        return None
    if len(bounded) != len(rungs):
        return 'some rungs carry bounds and some do not'
    ordered = sorted(rungs, key=lambda r: -1e300 if r.get('lo') is None else float(r['lo']))
    for a, b in zip(ordered, ordered[1:]):
        if a.get('hi') is None or b.get('lo') is None or float(a['hi']) != float(b['lo']):
            return 'rung bounds overlap or leave a gap'
    if ordered[-1].get('hi') is not None:
        return 'the top rung must be open above'
    return None


def check_group_refs(c, declared):
    """None when a candidate's research-group references are well formed: no repeats, each a declared local id; empty is allowed
    (a company's own financial line belongs to the company, not to a group); else the problem."""
    refs = c.get('group_refs')
    if refs is None:
        return None
    if len(refs) != len(set(refs)):
        return 'group_refs repeats a group'
    unknown = [r for r in refs if r not in declared]
    if unknown:
        return f'group_refs cites a group not declared in this answer: {unknown}'
    return None


def check_admission(c, publication_day):
    """None when a candidate's admission fields are well formed (D184/D185), else the problem: settled_by is not blank, and a binding
    obligation is due within 18 months."""
    if not str(c.get('settled_by', '')).strip():
        return 'settled_by is empty'
    if c['opens_as'] == 'binding_obligation':
        limit = datetime.date.fromisoformat(publication_day) + datetime.timedelta(days=BINDING_HORIZON_DAYS)
        try:
            due = datetime.date.fromisoformat(c['due_day'])
        except ValueError:                       # the schema's pattern admits 2026-06-31
            return f'due_day is not a real date: {c["due_day"]!r}'
        if due > limit:
            return f'binding obligation due beyond 18 months ({c["due_day"]} > {limit.isoformat()})'
    return None


def sift_with_groups(data, item, text, shown_ids, universe=None):
    """sift, plus the research-group declarations (D149): a candidate citing anything but a well-formed declaration of the same answer
    is dropped; a declared group is kept only when a kept candidate cites it (an unused declaration is ignored, D147). Returns
    (evidence, candidates, dropped, new_groups)."""
    declared = {}
    for g in data.get('new_groups', []) or []:
        if g['id'] in declared or not g['name'].strip() or not g['scope'].strip():
            declared = None
            break
        declared[g['id']] = {'id': g['id'], 'name': g['name'].strip(), 'scope': g['scope'].strip(), 'aliases': [a.strip() for a in g.get('aliases') or [] if a.strip()]}
    dropped_refs = []
    if declared is None:         # malformed declarations: every candidate citing a local id is dropped, shown ids still work
        declared = {}
    checked = dict(data, candidates=[])
    for c in data.get('candidates', []):
        problem = check_group_refs(c, declared)
        if problem:
            dropped_refs.append((c['id'], f'candidate group: {problem}'))
            continue
        checked['candidates'].append(c)
    evidence, candidates, dropped = sift(checked, item, text, shown_ids, universe)
    used = {r for c in candidates for r in c.get('group_refs', [])}
    return evidence, candidates, dropped_refs + dropped, [declared[g] for g in declared if g in used]


ISO_DAY = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def statement_day(value):
    """D203: original_day is the day the statement was made, as an ISO day, or '' when the text does not state a day. A month, a
    range or text is not a day and becomes unknown; the quote and event_time keep the period as written."""
    value = (value or '').strip()
    return value if ISO_DAY.match(value) else ''


FISCAL_FORM = re.compile(r'\bFY|fiscal|财年', re.I)


def beyond_next_year(year, publication_day, object_name=None, universe=None):
    """06-views ladder rule 5: only this year and next year open. A fiscal year (FY2028, FY28, fiscal year 2028, 2028财年) counts in
    the company's own fiscal years: on 2026-07-02 NVIDIA is in FY2027 (it ends in January 2027), so FY2028 is next year. A
    calendar year counts in calendar years, and so does a bare year, since the request defines "2026 for a calendar year". Text
    naming more than one year is judged by its first year, in the company's fiscal years when it names them."""
    parsed = parse_year(year)
    if parsed is None:
        first = re.search(r'(\d{4})', year or '')
        if not first:
            return False
        parsed = ('fiscal' if FISCAL_FORM.search(year) else 'calendar', int(first.group(1)))
    kind, number = parsed
    current = int(publication_day[:4])
    if universe is not None and kind == 'fiscal':
        current = universe.fiscal_year_of(universe.resolve(object_name) or object_name, publication_day)
    return number > current + 1


def candidates_with_evidence(candidates, kept_ids, item, dropped, alias=None):
    """A candidate opens only with at least one of its evidence ids kept (an owner's memo excepted, 02-classification T8);
    the others are dropped with their reason. Applied after the sift and again after placement drops statements (D209)."""
    alias = alias or {}
    kept = []
    for c in candidates:
        ids = list(dict.fromkeys(alias.get(i, i) for i in c['evidence_ids'] if alias.get(i, i) in kept_ids))
        if not ids and item.get('publisher_type') != SELF_PUBLISHER_TYPE:
            dropped.append((c['id'], 'candidate without surviving evidence'))
            continue
        kept.append(dict(c, evidence_ids=ids))
    return kept


def sift(data, item, text, shown_ids, universe=None):
    """05-extraction step 3, the code checks on one answer: ladders, the quarter and year rules, due days, quotes in
    the text, links to shown questions or kept candidates, one piece per sentence. A statement whose links all fail keeps an empty
    list; the handover drops it as 'no home'. Returns (evidence, candidates, dropped); the preflight runs it over every stored answer.
    The answer is read in the canonical vocabulary; a bare year is a calendar year."""
    data = vocabulary.extraction_answer(data)
    body = normalise(text)
    dropped = []
    candidates = []
    candidate_ids = set()
    for c in data.get('candidates', []):
        problem = check_ladder(c['rungs'], c['kind'])
        if problem:
            dropped.append((c['id'], f'candidate ladder: {problem}'))
            continue
        c = dict(c, rungs=normalise_ladder(c['rungs'], c['kind']))
        if QUARTERLY.search(c['looks_at'] + ' ' + c['question']) and c['kind'] == 'asset' \
                and c.get('measure') not in ('event', 'policy_event'):          # a dated event that names its quarter is not a quarterly figure
            dropped.append((c['id'], 'quarterly number: evidence, not a view (06-views ladder rule 6)'))
            continue
        if c.get('measure') not in ('event', 'policy_event') and c.get('opens_as') != 'binding_obligation' \
                and beyond_next_year(c['year'], item['publication_day'], c.get('object'), universe):
            dropped.append((c['id'], f'year {c["year"]} is beyond next year: not opened (06-views 不开)'))
            continue
        if not re.match(r'\d{4}-\d{2}-\d{2}$', c['due_day']):
            dropped.append((c['id'], f'due_day not a date: {c["due_day"]!r}'))
            continue
        if c['due_day'] <= item['publication_day']:
            dropped.append((c['id'], f'due_day {c["due_day"]} not after the item'))
            continue
        if 'opens_as' in c:           # D184: the schema guarantees the fields, code checks their shape
            problem = check_admission(c, item['publication_day'])
            if problem:
                dropped.append((c['id'], f'candidate admission: {problem}'))
                continue
        if c.get('measure'):          # keyed candidates keep their actual scope; reference lists do not gate admission (D155)
            problem = check_bounds(c['rungs'])
            if problem:
                dropped.append((c['id'], f'candidate ladder bounds: {problem}'))
                continue
            if universe is not None:
                object_id = universe.resolve(c['object']) or c['object']
                scope, source = universe.scope_and_source(object_id, c['measure'], c.get('scope', ''), c.get('event_type', 'n/a'))
                c = dict(c, object=object_id, scope=scope, scope_source=source, key_version=2)
                if c['measure'] not in ('event', 'policy_event'):
                    period = universe.fiscal_period(object_id, c.get('year', ''), bare_is_calendar=True)                             # and the period of a yearly number
                    if period:
                        c = dict(c, period_start=period[0], period_end=period[1])
            try:
                start = datetime.date.fromisoformat(c['period_start'])
                end = datetime.date.fromisoformat(c['period_end'])
                if start > end:
                    raise ValueError('start after end')
            except (KeyError, ValueError):
                dropped.append((c['id'], 'invalid period: expected real dates with start <= end'))
                continue
        candidates.append(c)
        candidate_ids.add(c['id'])
    evidence = []
    kept_ids = set()
    by_quote = {}
    alias = {}
    for e in data.get('evidence', []):
        quote = normalise(e['quote'])
        if len(quote) < 8 or quote not in body:
            subject_names = [universe.companies[o['value']]['name'] for o in item.get('object_identifiers') or []
                             if universe is not None and o['value'] in getattr(universe, 'companies', {})]
            repaired = repair_quote(e['quote'], text, subject_names)
            if repaired is None or normalise(repaired) not in body:
                dropped.append((e['id'], 'quote not in item'))
                continue
            e = dict(e, quote=repaired)
            quote = normalise(repaired)
        links = [l for l in e['links'] if l in shown_ids or l in candidate_ids]
        if quote in by_quote:            # the same sentence read out twice is one piece with both links
            first = by_quote[quote]
            first['links'].extend(l for l in links if l not in first['links'])
            alias[e['id']] = first['id']
            dropped.append((e['id'], f'same quote as {first["id"]}; merged'))
            continue
        e = dict(e, links=links, original_day=statement_day(e.get('original_day')))
        by_quote[quote] = e
        evidence.append(e)
        kept_ids.add(e['id'])
    final_candidates = candidates_with_evidence(candidates, kept_ids, item, dropped, alias)
    for e in evidence:
        e['links'] = [l for l in e['links'] if l in shown_ids or any(c['id'] == l for c in final_candidates)]
    return evidence, final_candidates, dropped
