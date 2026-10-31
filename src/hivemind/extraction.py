"""Extraction (docs/prd/05-extraction.md): the whole item goes to the model with the five-block prompt of its
category; the answer is evidence linked to the shown views or to this item's candidate views, and candidate views
written in full. Code checks the sources (the quote is in the text, every link points at a shown view or a
candidate), the ladders (five rungs or two) and the rule that quarterly numbers are evidence, not views.

Prompt versions 1–5 ask and answer in Chinese; version 6 and later ask and answer in English (D163). The schema,
the request text and the retry note follow the version; every answer is read in the canonical vocabulary."""
import dataclasses
import datetime
import json
import re

from . import config, model, vocabulary
from .universe import parse_year

TIERS = vocabulary.TIERS
LEGACY_TIERS = list(vocabulary.LEGACY['tier'])
LEGACY_KINDS = list(vocabulary.LEGACY['kind'])
MAX_TEXT_CHARS = 400_000
ENGLISH_FROM = 6                  # the first extraction prompt version written in English
GROUPS_FROM = 7                   # the first version whose candidates carry research-group membership (D149)
ALIASES_FROM = 9                  # the first version whose declared groups carry aliases, so code decides identity and membership (D166)
ADMISSION_FROM = 12               # the first version whose candidates state why they open (D184): one of four reasons, the settling material, the loss if folded
# D184: the closed set of reasons a candidate thesis may open; anything else is evidence to a shown thesis
ADMISSION_REASONS = ['main_driver', 'industry_aggregate', 'policy_stage', 'binding_obligation']
ADMISSION_REASONS_V13 = ['main_driver', 'shared_quantity', 'policy_stage', 'binding_obligation']    # D191: a quantity or price outside any one company
EMPTY_LINE_FROM = 16              # D199: from role-v16 the request no longer says 'return empty arrays when there is nothing to extract'; the gate rule decides
EMPTY_LINE_DROPPED_VERSIONS = (58,)   # noise arm (2026-10-30, prompt-standard audit N9): the closing names no condition for an empty answer; the keep rule decides
REVIEW_FROM = 59     # AGENTS §6 (2026-10-30): from role-v59 the request ends with a check that reads the evidence list back by standard 5.1 (prompts/review-v<N>.txt) and names no empty-answer condition
SHARED_QUANTITY_VERSIONS = (13, 14, 15)    # D191: the schemas of role-v13..v15 name shared_quantity in place of industry_aggregate (role-v15's text already
                                           # says industry_aggregate; its schema stays so stored requests stay byte-identical); every later version names the four reasons above
THEMES_SHOWN_FROM = 19            # A (2026-10-28): from v19 the request shows every open theme thesis to every item and the groups block prints only linkable member ids
PLACEMENT_FROM = 20               # 2026-10-28 (routing-analysis.md §6): from v20 a statement without a link is kept, and a separate placement call decides the links to existing theses
LEDGER_BLIND_FROM = 22            # D211 (2026-10-28 night): from v22 the extraction request shows no thesis and no group, so its bytes depend on the item alone; links go to the answer's
                                  # own candidates, the placement call files statements under the open theses, matching folds a candidate into an open thesis (D190), aliases fold a declared group (D166)
ACCOUNT_VERSIONS = (17,)          # D199/D200: v17 alone answers with an account per mandatory paragraph (statements or a skip reason); v18 was measured with the flat shape and sends it
ACCOUNT_LIMIT = 30                # at most this many mandatory paragraphs are required per answer: a 60-paragraph page spent the whole 8,000-token cap on reasoning and returned nothing (2026-10-27 19:16); later paragraphs may still yield extra statements
SKIP_REASONS = ['boilerplate', 'navigation', 'repeat', 'no_claim']
MONTH_NAME = re.compile(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b')
MANDATORY_CHARS = 120
BINDING_HORIZON_DAYS = 548        # D185: a binding obligation is due within 18 months of the item, and is exempt from the next-year rule on quantities
# role-v53 (2026-10-30, record-field class): the three attribution fields carry their definitions in the schema, beside the
# field they govern, so the role text that decides which statements to keep stays as it was (standard 5.4: the original
# claimant; an unknown statement day is unknown, never the report day; D220, D203; 5.5: relays of one report are one source)
FIELD_NOTES_FROM = 53
FIELD_NOTES = {
    'speaker': 'Who says it in this item: the outlet, the author or the person quoted.',
    'original_who': ('The party whose statement, figure or action it is, even when the item reports it without attribution ("the insurer agreed '
                     'to buy the broker": the insurer; "the regulator fined the bank, a newspaper reported": the regulator); the outlet or author '
                     'only for its own estimate, analysis or unnamed-source report.'),
    'original_day': ('The day that party made it, as an ISO day when the item gives one ("signed on 3 March 2026": 2026-03-03); empty when the '
                     "item gives none or only a month; the publication day only when the item is that party's own release, filing, call or analysis."),
}
# role-v54: the role text no longer states the attribution rule, so the schema is its one owner; the wording follows the signed gold's
# who column (the party that announced or did it, a relaying outlet named only as the relay, an unnamed source with the outlet that
# carried it) and 5.4's statement day (never the publication day in place of an unknown day); v54–v56 alone, later versions carry v53's notes (D247)
FIELD_NOTES_V54_VERSIONS = (54, 55, 56)
FIELD_NOTES_V54 = {
    'speaker': 'Who says it in this item: the outlet, the author or the person quoted.',
    'original_who': ('The party that made the statement, took the action or produced the figure, even when the item reports it without '
                     'attribution ("the insurer agreed to buy the broker": the insurer); an outlet that only relays it is not the original party; '
                     'for a claim from unnamed sources, the unnamed source and the outlet that carried it; the outlet or author for its own '
                     'estimate or analysis.'),
    'original_day': ('The day that party made the statement or took the action, as an ISO day when the item gives one ("announced on 3 March '
                     '2026": 2026-03-03); empty when the item gives no day or only a month, never the publication day in place of an unknown '
                     "day. A party's own release, filing, call or analysis is dated its publication day."),
}
# role-v55 alone (refuted on its small sample, loop log row 32): the source tier's rule moved from the role text to the tier field
# as standard 5.5's table, the first row that applies; later versions keep the tier rule in the role text
TIER_NOTE_VERSIONS = (55,)
TIER_NOTE = ('Take the first row that applies. (1) The item credits the claim to someone unnamed or calls it unconfirmed, even an '
             'announcement or a figure: rumour. (2) An official action, a published actual figure, a completed transaction, or an '
             'announcement the item reports, even when the reporter names no source: fact. (3) Company guidance, a management statement or '
             "an official's remark: party_statement. (4) An analyst's, outlet's or expert's view or estimate: third_party_view. (5) Anything "
             'else with no source: rumour. A record that mixes a fact with a plan or a rumour takes the tier of its main claim.')


def version_number(version):
    return int(str(version or '').lstrip('v') or 0)


def is_english(version):
    return version_number(version) >= ENGLISH_FROM


def accounts(version):
    return version_number(version) in ACCOUNT_VERSIONS


def shows_themes(version):
    return version_number(version) >= THEMES_SHOWN_FROM


def ledger_blind(version):
    return version_number(version) >= LEDGER_BLIND_FROM


def places(version):
    return version_number(version) >= PLACEMENT_FROM


def shown_views(conn, cfg, item, objects):
    """The theses an item's extraction request shows (05-extraction block 5): the objects' open theses and their dependencies;
    from v19 also every open theme thesis. The one place the stream and the parallel runner take the list from."""
    version = cfg.extraction_setting(item['category']).prompt_version.rpartition('-')[2]
    from .views import store
    views = store.views_for_prompt(conn, objects, themes=shows_themes(version))
    return [dict(v, key=store.view_key(conn, v['view_id']) or {}, groups=[{'name': g['name'], 'scope': g['scope'], 'aliases': g.get('aliases') or []} for g in store.groups_of_view(conn, v['view_id'])])
            for v in views]       # the key and the groups feed the placer's 'takes' line


def has_groups(version):
    return version_number(version) >= GROUPS_FROM


def base_schema(english):
    kinds = vocabulary.KINDS if english else LEGACY_KINDS
    tiers = TIERS if english else LEGACY_TIERS
    return {
        'type': 'object', 'additionalProperties': False, 'required': ['evidence', 'candidates'],
        'properties': {
            'evidence': {'type': 'array', 'items': {
                'type': 'object', 'additionalProperties': False,
                'required': ['id', 'quote', 'one_line', 'speaker', 'original_who', 'original_day', 'tier', 'event_time', 'links'],
                'properties': {
                    'id': {'type': 'string'}, 'quote': {'type': 'string'}, 'one_line': {'type': 'string'}, 'speaker': {'type': 'string'},
                    'original_who': {'type': 'string'}, 'original_day': {'type': 'string'}, 'tier': {'type': 'string', 'enum': tiers},
                    'event_time': {'type': 'string'}, 'links': {'type': 'array', 'items': {'type': 'string'}}}}},
            'candidates': {'type': 'array', 'items': {
                'type': 'object', 'additionalProperties': False,
                'required': ['id', 'object', 'kind', 'looks_at', 'question', 'rungs', 'due_day', 'year', 'evidence_ids'],
                'properties': {
                    'id': {'type': 'string'}, 'object': {'type': 'string'}, 'kind': {'type': 'string', 'enum': kinds},
                    'looks_at': {'type': 'string'}, 'question': {'type': 'string'},
                    'rungs': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['label', 'condition'],
                                                           'properties': {'label': {'type': 'string'}, 'condition': {'type': 'string'}}}},
                    'due_day': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'},      # a date, enforced by the schema, not by prose
                    'year': {'type': 'string'}, 'evidence_ids': {'type': 'array', 'items': {'type': 'string'}}}}},
        },
    }


SCHEMA = base_schema(english=False)          # the shape of the answers stored under versions 1–3

# keyed-views-plan.md 2.1: the key a candidate carries from prompt version v4 on; the ladder's rungs carry numeric bounds
MEASURES = ['total_revenue', 'segment_revenue', 'product_revenue', 'gross_margin', 'operating_margin', 'operating_expense_growth', 'total_expenses', 'operating_loss',
            'tax_rate', 'capex', 'shipments_or_capacity', 'run_rate', 'design_wins', 'event', 'spend_total', 'financing_amount', 'price', 'capacity', 'growth_rate', 'policy_event', 'other']
EVENT_TYPES = ['launch', 'shipment', 'licence', 'approval', 'deal_close', 'deployment', 'other', 'n/a']
BASES = ['GAAP', 'non_GAAP', 'n/a']
UNITS = ['USD', 'percent', 'count', 'GW', 'MW', 'TWD', 'multiple', 'n/a']
# D167 (2026-10-25): from version 10 the vocabulary names a market's size and a project's cost as their own measures; the week filed an
# accelerator TAM and a data-center project's cost as spend_total, the aggregate of spending, which no identity rule could then tell apart
MEASURES_V10 = MEASURES[:MEASURES.index('spend_total') + 1] + ['market_size', 'project_cost'] + MEASURES[MEASURES.index('spend_total') + 1:]
MEASURES_V10_FROM = 10


def key_fields(measures=MEASURES):
    return {'measure': {'type': 'string', 'enum': list(measures)}, 'scope': {'type': 'string'},
            'period_start': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'}, 'period_end': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'},
            'basis': {'type': 'string', 'enum': BASES}, 'unit': {'type': 'string', 'enum': UNITS}, 'event_type': {'type': 'string', 'enum': EVENT_TYPES}}


BOUND = {'anyOf': [{'type': 'number'}, {'type': 'null'}]}


def keyed_schema(english=False, measures=MEASURES):
    """The base schema with the key fields on every candidate and numeric bounds on every rung."""
    schema = base_schema(english)
    candidate = schema['properties']['candidates']['items']
    fields = key_fields(measures)
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


def grouped_schema(shown_group_ids, aliases=False, measures=MEASURES):
    """The English keyed schema plus research-group membership (D149, the D147 reference shape): each candidate cites one or
    more groups, each either a group id shown in this request or a local id declared in new_groups; the pattern is built
    from the shown ids, so an unseen group cannot be cited."""
    schema = keyed_schema(english=True, measures=measures)
    pattern = '^(?:' + LOCAL_GROUP + ''.join('|' + re.escape(g) for g in shown_group_ids) + ')$'
    candidate = schema['properties']['candidates']['items']
    candidate['properties']['group_refs'] = {'type': 'array', 'items': {'type': 'string', 'pattern': pattern}}
    candidate['required'].append('group_refs')
    group_fields = {'id': {'type': 'string', 'pattern': '^' + LOCAL_GROUP + '$'}, 'name': {'type': 'string'}, 'scope': {'type': 'string'}}
    if aliases:
        group_fields['aliases'] = {'type': 'array', 'items': {'type': 'string'}}
    schema['properties']['new_groups'] = {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': list(group_fields), 'properties': group_fields}}
    schema['required'].append('new_groups')
    return schema


def admission_schema(shown_view_ids, shown_group_ids, measures=MEASURES_V10, reasons=ADMISSION_REASONS, blind=False):
    """The grouped schema plus the admission fields (D184): opens_as names one of the four reasons; folds_into names the shown
    thesis the statement would otherwise attach to, or is empty (the pattern is built from the shown ids, so an unseen thesis
    cannot be named); lost_if_folded says what investment implication is lost if it only attached there; settled_by names the
    public material that resolves the question."""
    schema = grouped_schema(shown_group_ids, aliases=True, measures=measures)
    candidate = schema['properties']['candidates']['items']
    if blind:                                    # v22: no thesis is shown, so nothing to fold into; matching folds (D190)
        candidate['properties'].update({'opens_as': {'type': 'string', 'enum': list(reasons)}, 'settled_by': {'type': 'string'}})
        candidate['required'] += ['opens_as', 'settled_by']
        return schema
    candidate['properties'].update({
        'opens_as': {'type': 'string', 'enum': list(reasons)},
        'folds_into': {'type': 'string', 'pattern': '^(?:' + ''.join('|' + re.escape(v) for v in shown_view_ids) + ')$'},
        'lost_if_folded': {'type': 'string'},
        'settled_by': {'type': 'string'}})
    candidate['required'] += ['opens_as', 'folds_into', 'lost_if_folded', 'settled_by']
    return schema


def paragraphs_of(text):
    """The page as numbered paragraphs: one non-blank line each, ids p0001 … in page order."""
    lines = [line.strip() for line in text[:MAX_TEXT_CHARS].split('\n') if line.strip()]
    return [(f'p{index:04}', line) for index, line in enumerate(lines, 1)]


def mandatory_paragraph(line):
    """A paragraph the answer must account for: it carries a digit, a month name or MANDATORY_CHARS characters or more."""
    return bool(re.search(r'\d', line) or MONTH_NAME.search(line) or len(line) >= MANDATORY_CHARS)


def mandatory_ids(text):
    ids = [pid for pid, line in paragraphs_of(text) if mandatory_paragraph(line)]
    return ids[:ACCOUNT_LIMIT]


def accounted_schema(base, mandatory):
    """v17: the base answer with its evidence array replaced by an account per mandatory paragraph (statements or a skip
    reason, an anyOf the provider enforces) and an extra array for statements from other paragraphs; the piece shape is
    shared under $defs so the schema does not grow with the page."""
    piece = base['properties']['evidence']['items']
    entry = {'anyOf': [
        {'type': 'object', 'properties': {'statements': {'type': 'array', 'minItems': 1, 'items': {'$ref': '#/$defs/piece'}}}, 'required': ['statements'], 'additionalProperties': False},
        {'type': 'object', 'properties': {'skip': {'type': 'string', 'enum': SKIP_REASONS}}, 'required': ['skip'], 'additionalProperties': False}]}
    paragraphs = {'type': 'object', 'properties': {pid: entry for pid in mandatory}, 'required': list(mandatory), 'additionalProperties': False}
    properties = {'paragraphs': paragraphs, 'extra': {'type': 'array', 'items': {'$ref': '#/$defs/piece'}}}
    properties.update({k: v for k, v in base['properties'].items() if k != 'evidence'})
    return {'type': 'object', '$defs': {'piece': piece}, 'properties': properties, 'required': list(properties), 'additionalProperties': False}


def flatten_account(data):
    """A v17 answer read as the evidence list every check expects: the statements of every paragraph entry, in page
    order, then the extra statements. Any other answer is returned as it is."""
    if 'paragraphs' not in data:
        return data
    pieces = [p for entry in (data.get('paragraphs') or {}).values() for p in (entry.get('statements') or [])]
    flat = {k: v for k, v in data.items() if k not in ('paragraphs', 'extra')}
    flat['evidence'] = pieces + list(data.get('extra') or [])
    return flat


def field_notes(number):
    """The evidence fields' descriptions a prompt version's schema carries: none before v53, FIELD_NOTES_V54 in v54–v56, FIELD_NOTES
    in v53 and from v57, and the tier's in v55 alone."""
    if number < FIELD_NOTES_FROM:
        return {}
    notes = dict(FIELD_NOTES_V54 if number in FIELD_NOTES_V54_VERSIONS else FIELD_NOTES)
    if number in TIER_NOTE_VERSIONS:
        notes['tier'] = TIER_NOTE
    return notes


def with_field_notes(schema, notes):
    """The schema with the notes as the descriptions of the evidence fields they name."""
    fields = schema['properties']['evidence']['items']['properties']
    for name, note in notes.items():
        fields[name] = dict(fields[name], description=note)
    return schema


def schema_for(version, shown_group_ids=(), shown_view_ids=(), mandatory=()):
    number = version_number(version)
    measures = MEASURES_V10 if number >= MEASURES_V10_FROM else MEASURES
    if number >= ADMISSION_FROM:
        base = admission_schema(shown_view_ids, shown_group_ids, measures=measures, reasons=ADMISSION_REASONS_V13 if number in SHARED_QUANTITY_VERSIONS else ADMISSION_REASONS,
                                blind=number >= LEDGER_BLIND_FROM)
        if number >= FIELD_NOTES_FROM:
            base = with_field_notes(base, field_notes(number))
        return accounted_schema(base, mandatory) if accounts(version) else base
    if number >= GROUPS_FROM:
        return grouped_schema(shown_group_ids, aliases=number >= ALIASES_FROM, measures=measures)
    if number >= ENGLISH_FROM:
        return keyed_schema(english=True)
    return keyed_schema() if number >= 4 else SCHEMA


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


def repair_quote(quote, text):
    """The source passage a refused quote stands for (D236), or None. Accepted: the quote's words equal one passage's words
    (punctuation, quotation marks, footnote markers and case aside), or equal them with one run left out that lies inside one
    sentence and is shorter than the quote."""
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
    if best is None:
        return None
    return _source_passage(text, spans[best[1]][1], spans[best[2]][2])


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


def _build_prompt_chinese(item, text, shown_views, universe, version, category, blocks, objects):
    themes = '\n'.join(f'  - {theme_id}：{name}' for theme_id, name in universe.theme_list(legacy=True))
    fiscal = '\n'.join(note for note in (universe.fiscal_note(o, item['publication_day']) for o in objects) if note)
    parts = [
        f'【这一类是什么、怎么读】{category}。{blocks["what"]}',
        f'【讲的是谁】这条信息的相关对象：{"、".join(objects) or "（上游没有标）"}。候选观点讲的是公司时，object 写股票代码；讲的是主题时，从下面名单里挑一个写编号，名单里没有的写清是什么事：\n{themes}'
        + (f'\n财年说明（数字观点的年份和到期日按这个算）：\n{fiscal}' if fiscal else ''),
        f'【这一类要读出什么】{blocks["read"]}',
    ]
    if version_number(version) >= 4:
        watched = []
        for o in objects:
            entries = universe.watch_list(o) if hasattr(universe, 'watch_list') else []
            if entries:
                watched.append(f'  - {o}：' + '；'.join(e['measure'] + (f"[{e['scope']}]" if e.get('scope') else '') + (f"({e['event_type']})" if e.get('event_type') else '') for e in entries))
        if watched:
            parts.append('【研究参考】已有的量和范围（measure[scope](event_type)）。含义相同可用现有名称；清单外的重要问题照常提出，保留实际范围：\n' + '\n'.join(watched))
    if shown_views:
        lines = []
        for v in shown_views:       # 05-extraction block 5: question, looks_at, due day and who depends on whom; no state, no evidence
            deps = f'；依赖：{"、".join(v["depends_on"])}' if v.get('depends_on') else ''
            lines.append(f'  - {v["view_id"]}（{v["object_id"]}，看的是「{v["looks_at"]}」，到期 {v["due_day"]}）：{v["question"]}{deps}')
        parts.append('【这些对象已有的观点】证据连到这些观点上，用它们的编号；它们管不到的才写候选观点：\n' + '\n'.join(lines))
    else:
        parts.append('【这些对象已有的观点】还没有。该开的都写成候选观点。')
    parts.append(f'【信息】编号 {item["input_id"]}，类别 {category}，作者 {item.get("publisher")}（{item.get("publisher_type")}），发布日 {item.get("publication_day")}，标题：{item.get("title") or ""}\n\n' + text[:MAX_TEXT_CHARS])
    parts.append('按 JSON schema 交出 evidence 和 candidates。候选观点的 evidence_ids 填它自己的证据编号；证据的 links 填已有观点编号或这次候选观点的编号（如 c1）。没有可抽的就都交空数组。')
    return '\n\n'.join(parts)


def dependency_text(view, english):
    """Who a shown view depends on, for block 5: resolved theses by id, a waiting dependency by its chain and year."""
    entries = view.get('dependencies')
    if entries is None:                                   # a caller that built the view without the structured list
        return list(view.get('depends_on') or [])
    out = []
    for entry in entries:
        if entry.get('view_id'):
            out.append(entry['view_id'])
        elif english:
            out.append(f'(waiting for the {entry["wait_year"]} thesis on chain {entry["wait_chain_view_id"]})')
        else:
            out.append(f'（等 {entry["wait_chain_view_id"]} 这条链上 {entry["wait_year"]} 年的那条）')
    return out


def groups_block(shown_groups):
    """05-extraction block 5b (D149): the research groups the model may cite, with each member's focus."""
    if not shown_groups:
        return ('[Research groups] None yet. For a candidate that tracks an ongoing matter (a product rollout, a deal, a policy process, an investment or demand cycle), '
                'declare the group in new_groups (local ids n1, n2 …) and cite it in group_refs; leave group_refs empty for a company\'s own financial lines.')
    lines = []
    for g in shown_groups:
        members = '; '.join(f'{m["view_id"]} ({m["object_id"]}) {m["looks_at"]}' for m in g.get('members', [])[:8])
        names = ', '.join(a for a in (g.get('aliases') or []) if a != g['name'])
        lines.append(f'  - {g["group_id"]} "{g["name"]}": {g["scope"]}' + (f' (also: {names})' if names else '') + (f' — members: {members}' if members else ''))
    return ('[Research groups] Cite one of these ids in group_refs when the candidate tracks that matter; declare a new group in new_groups for a matter none of them is; '
            'leave group_refs empty for a company\'s own financial lines:\n'
            + '\n'.join(lines))


def _build_prompt_english(item, text, shown_views, universe, version, category, blocks, objects, shown_groups=()):
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
    blind = ledger_blind(version)
    if blind:
        pass                        # v22: the request shows no thesis; the placement call reads the open theses, matching folds a candidate into one
    elif shown_views:
        lines = []
        for v in shown_views:       # 05-extraction block 5: question, looks_at, due day and who depends on whom; no state, no evidence
            deps = dependency_text(v, english=True)
            tail = f'; depends on: {", ".join(deps)}' if deps else ''
            lines.append(f'  - {v["view_id"]} ({v["object_id"]}, focus "{v["looks_at"]}", due {v["due_day"]}): {v["question"]}{tail}')
        parts.append('[Existing theses of these objects] Link evidence to them by id; write a candidate thesis only for a question they do not cover:\n' + '\n'.join(lines))
    else:
        parts.append('[Existing theses of these objects] None yet. Write every thesis that should open as a candidate.')
    if blind:
        parts.append(groups_block(()))     # the standing instruction only: declare the matter; code folds a declared group into a stored one by its names (D166)
    elif has_groups(version):
        if shows_themes(version):          # a member id the answer may not link to is not printed (the link check would refuse it)
            linkable = {v['view_id'] for v in shown_views}
            shown_groups = [dict(g, members=[m for m in g.get('members', []) if m['view_id'] in linkable]) for g in shown_groups]
        parts.append(groups_block(shown_groups))
    if accounts(version):
        page = '\n'.join(f'{pid} {line}' for pid, line in paragraphs_of(text))
        parts.append(item_header(item, category) + page)
        parts.append('[Paragraphs to account for] Every paragraph listed here gets an entry: its evidence statements, or a skip reason (boilerplate, navigation, repeat, no_claim). '
                     'Statements from other paragraphs go in extra. ' + ', '.join(mandatory_ids(text)))
    else:
        parts.append(item_header(item, category) + text[:MAX_TEXT_CHARS])
    parts.append(('Return evidence and candidates per the JSON schema. A candidate\'s evidence_ids are its own evidence ids; an evidence item\'s links are '
                  + ('this answer\'s candidate ids (such as c1), or empty. ' if blind else 'existing thesis ids or this answer\'s candidate ids (such as c1). ')
                  + 'year names the fiscal or calendar year the figure covers (FY2027, or 2026 for a calendar year). '
                  + ('' if version_number(version) in EMPTY_LINE_DROPPED_VERSIONS or version_number(version) >= REVIEW_FROM
                     else 'Return empty arrays only for a page with no business content.' if version_number(version) >= EMPTY_LINE_FROM
                     else 'Return empty arrays when there is nothing to extract.')).rstrip())
    if version_number(version) >= REVIEW_FROM:
        parts.append(_read(f'review-{version}.txt').strip())
    return '\n\n'.join(parts)


def build_prompt(item, text, shown_views, universe, version='v1', shown_groups=()):
    """The five blocks of 05-extraction: role; this category and how to read it; who it is about plus the list's
    themes; what to read out; the objects' existing views with who depends on whom (no state, no evidence)."""
    category = item['category']
    categories = _categories(version)
    blocks = categories.get(category) or categories['T7']
    objects = [o['value'] for o in item.get('object_identifiers') or []]
    system = _read(f'role-{version}.txt')
    if is_english(version):
        return system, _build_prompt_english(item, text, shown_views, universe, version, category, blocks, objects, shown_groups)
    return system, _build_prompt_chinese(item, text, shown_views, universe, version, category, blocks, objects)


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


def request_for(cfg, item, text, shown_views, universe, shown_groups=()):
    """Build the setting, complete prompt and schema without making a call."""
    setting = cfg.extraction_setting(item['category'])
    version = setting.prompt_version.rpartition('-')[2]
    if ledger_blind(version):                  # D211: the request's bytes depend on the item alone
        shown_views, shown_groups = [], []
    system, user = build_prompt(item, text, shown_views, universe, version, shown_groups)
    group_ids = [g['group_id'] for g in shown_groups]
    shown_ids = [v['view_id'] for v in shown_views]
    if accounts(version):
        return setting, system, user, schema_for(version, group_ids, shown_ids, mandatory_ids(text))
    return setting, system, user, schema_for(version, group_ids, shown_ids)


@dataclasses.dataclass
class Reading:
    """An item read: the extraction answer through the code checks, before placement (D211: the read never depends on the ledger
    under a ledger-blind version, so the parallel day prepares it early and files it at the item's turn)."""
    evidence: list
    candidates: list
    dropped: list
    new_groups: list
    answer: object
    version: str


def read_item(archive, cfg, item, text, shown_views, universe, *, shown_groups=(), transport=None):
    """The extraction call and the code checks on its answer. A ledger-blind version ignores shown_views and shown_groups for the
    request (request_for drops them) and lets a statement link only to this answer's candidates."""
    setting, system, user, schema = request_for(cfg, item, text, shown_views, universe, shown_groups)
    version = setting.prompt_version.rpartition('-')[2]
    blind = ledger_blind(version)
    group_ids = [] if blind else [g['group_id'] for g in shown_groups]
    shown_ids = set() if blind else {v['view_id'] for v in shown_views}
    if places(version) and cfg.placement is None:            # refused before the paid call
        raise ValueError(f'extraction {setting.prompt_version} files statements by a placement call, but the configuration has no placement setting')
    answer = model.call(archive, cfg, setting, system, user, schema, 'extraction', 'extract', transport=transport)
    evidence, candidates, dropped, new_groups = sift_with_groups(answer.data, item, text, shown_ids, universe, english=is_english(version),
                                                                  shown_group_ids=group_ids, version=version, keep_unlinked=places(version))
    return Reading(evidence, candidates, dropped, new_groups, answer, version)


def file_reading(reading, archive, cfg, item, shown_views, *, transport=None):
    """The handover: from v20 the placement call files the read statements under the open theses shown now (D207); earlier versions
    hand the read over as it is. A statement no open question takes is dropped as 'no home' (D209), like every other drop: a
    candidate left with none of its evidence is dropped too, and a statement whose only link was such a candidate has no home."""
    evidence, candidates, dropped, answer = reading.evidence, reading.candidates, list(reading.dropped), reading.answer
    cost, cached = answer.cost_usd, answer.cached
    if places(reading.version):
        from . import placement
        evidence, unfiled, placed_answer = placement.place(archive, cfg, evidence, shown_views, transport=transport, item=item)
        dropped.extend((e['id'], 'no home') for e in unfiled)
        if placed_answer is not None:
            cost += placed_answer.cost_usd
            cached = cached and placed_answer.cached
        while True:
            candidates = candidates_with_evidence(candidates, {e['id'] for e in evidence}, item, dropped)
            candidate_ids = {c['id'] for c in candidates}
            evidence = [dict(e, links=[l for l in e['links'] if not placement.CANDIDATE_ID.match(l) or l in candidate_ids]) for e in evidence]
            homeless = [e for e in evidence if not e['links']]
            if not homeless:
                break
            dropped.extend((e['id'], 'no home') for e in homeless)
            evidence = [e for e in evidence if e['links']]
    return Handover(evidence, candidates, dropped, answer.call_id, answer.request_sha256, cached, cost, reading.new_groups)


def extract(archive, cfg, item, text, shown_views, universe, *, shown_groups=(), transport=None):
    """One item through extraction: read, then file under the theses shown."""
    reading = read_item(archive, cfg, item, text, shown_views, universe, shown_groups=shown_groups, transport=transport)
    return file_reading(reading, archive, cfg, item, shown_views, transport=transport)


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


def check_group_refs(c, shown_group_ids, declared):
    """None when a candidate's research-group references are well formed: no repeats, each a shown group id or a declared
    local id; empty is allowed (a company's own financial line belongs to the company, not to a group); else the problem."""
    refs = c.get('group_refs')
    if refs is None:
        return None                     # a version before groups
    if len(refs) != len(set(refs)):
        return 'group_refs repeats a group'
    unknown = [r for r in refs if r not in shown_group_ids and r not in declared]
    if unknown:
        return f'group_refs cites a group neither shown nor declared: {unknown}'
    return None


def check_admission(c, shown_ids, publication_day):
    """None when a version-12 candidate's admission fields are well formed (D184/D185), else the problem:
    settled_by is not blank, folds_into is empty or a shown thesis, lost_if_folded is not blank when folds_into names one, and a binding
    obligation is due within 18 months."""
    if not str(c.get('settled_by', '')).strip():
        return 'settled_by is empty'
    if c.get('folds_into') and c['folds_into'] not in shown_ids:
        return f'folds_into names a thesis not shown: {c["folds_into"]!r}'
    if c.get('folds_into') and not str(c.get('lost_if_folded', '')).strip():      # a named thesis it could attach to needs the reason it does not
        return 'lost_if_folded is empty although folds_into names a thesis'
    if c['opens_as'] == 'binding_obligation':
        limit = datetime.date.fromisoformat(publication_day) + datetime.timedelta(days=BINDING_HORIZON_DAYS)
        try:
            due = datetime.date.fromisoformat(c['due_day'])
        except ValueError:                       # the schema's pattern admits 2026-06-31
            return f'due_day is not a real date: {c["due_day"]!r}'
        if due > limit:
            return f'binding obligation due beyond 18 months ({c["due_day"]} > {limit.isoformat()})'
    return None


def sift_with_groups(data, item, text, shown_ids, universe=None, english=False, shown_group_ids=(), version=None, keep_unlinked=False):
    """sift, plus the research-group declarations (D149): candidates with bad references are dropped; a declared group is
    kept only when a kept candidate cites it (an unused declaration is ignored, D147). Returns (evidence, candidates, dropped, new_groups)."""
    data = flatten_account(data)
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
        problem = check_group_refs(c, set(shown_group_ids), declared)
        if problem:
            dropped_refs.append((c['id'], f'candidate group: {problem}'))
            continue
        checked['candidates'].append(c)
    evidence, candidates, dropped = sift(checked, item, text, shown_ids, universe, english=english, keep_unlinked=keep_unlinked)
    used = {r for c in candidates for r in c.get('group_refs', [])}
    return evidence, candidates, dropped_refs + dropped, [declared[g] for g in declared if g in used]


ISO_DAY = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def statement_day(value):
    """D203: original_day is the day the statement was made, as an ISO day, or '' when the text does not state a day. A month, a
    range or text is not a day and becomes unknown; the quote and event_time keep the period as written."""
    value = (value or '').strip()
    return value if ISO_DAY.match(value) else ''


FISCAL_FORM = re.compile(r'\bFY|fiscal|财年', re.I)


def beyond_next_year(year, publication_day, object_name=None, universe=None, english=True):
    """06-views ladder rule 5: only this year and next year open. A fiscal year (FY2028, FY28, fiscal year 2028, 2028财年) counts in
    the company's own fiscal years: on 2026-07-02 NVIDIA is in FY2027 (it ends in January 2027), so FY2028 is next year. A
    calendar year counts in calendar years, and so does a bare year under the English versions, whose request defines "2026 for a
    calendar year". Text naming more than one year is judged by its first year, in the company's fiscal years when it names them."""
    parsed = parse_year(year)
    if parsed is None:
        first = re.search(r'(\d{4})', year or '')
        if not first:
            return False
        parsed = ('fiscal' if FISCAL_FORM.search(year) else 'calendar', int(first.group(1)))
    kind, number = parsed
    current = int(publication_day[:4])
    if universe is not None and (kind == 'fiscal' or (kind == 'bare' and not english)):
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


def sift(data, item, text, shown_ids, universe=None, english=False, keep_unlinked=False):
    """05-extraction step 3, the code checks on one answer: ladders, the quarter and year rules, due days, quotes in
    the text, links to shown views or kept candidates, one piece per sentence. Returns (evidence, candidates,
    dropped); the preflight runs it over every stored answer. The answer is read in the canonical vocabulary,
    whichever prompt version wrote it; english says which version's year contract applies (a bare year is a calendar
    year under the English versions, the company's fiscal year under the Chinese ones)."""
    data = vocabulary.extraction_answer(flatten_account(data))
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
                and beyond_next_year(c['year'], item['publication_day'], c.get('object'), universe, english):
            dropped.append((c['id'], f'year {c["year"]} is beyond next year: not opened (06-views 不开)'))
            continue
        if not re.match(r'\d{4}-\d{2}-\d{2}$', c['due_day']):
            dropped.append((c['id'], f'due_day not a date: {c["due_day"]!r}'))
            continue
        if c['due_day'] <= item['publication_day']:
            dropped.append((c['id'], f'due_day {c["due_day"]} not after the item'))
            continue
        if 'opens_as' in c:           # a version-12 answer (D184): the schema guarantees the fields, code checks their shape
            problem = check_admission(c, shown_ids, item['publication_day'])
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
                    period = universe.fiscal_period(object_id, c.get('year', ''), bare_is_calendar=english)                             # and the period of a yearly number
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
            repaired = repair_quote(e['quote'], text)
            if repaired is None or normalise(repaired) not in body:
                dropped.append((e['id'], 'quote not in item'))
                continue
            e = dict(e, quote=repaired)
            quote = normalise(repaired)
        links = [l for l in e['links'] if l in shown_ids or l in candidate_ids]
        if not links and not keep_unlinked:
            dropped.append((e['id'], f'links to nothing shown: {e["links"]}'))
            continue
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
    if not keep_unlinked:
        evidence = [e for e in evidence if e['links']]
    return evidence, final_candidates, dropped
