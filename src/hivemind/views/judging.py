"""06-views.md step 7: one re-judging round. Open views whose reading changed are judged in dependency order, each
once; a view whose conclusion changed adds its open dependants. The model reads the evidence in force (with each
replaced predecessor), the dependencies' current conclusions and its own last conclusion (for comparison only).
Code checks every citation and that a rung move or a first judgement says changed; one retry, then the item fails.

The request is judging-v7 (D354, frozen with steps 3 and 4), or the candidate judging-v8, which reads and rewrites the thesis's
argument card (D201; docs/research/2026-11-04-argument-record/design.md); no other version is built, and a configuration that names
another is refused before any call. Every answer is stored in the canonical vocabulary.

The theme block (D191, D195): an asset thesis is judged with every open, judged theme thesis in view and answers, in theme_pushes,
which way each theme it weighed pushes it; theme theses are judged before asset theses in a round, and a theme judgement that says
changed queues every open asset thesis with evidence in force, once. The round's queue is derived from the ledger (the day's changed
views, the dependants of views judged at this sequence number with a changed conclusion, and the asset theses a changed theme queues),
so a resumed round recovers what an earlier commit had queued.

The evidence in view (D198): a judgement reads the arrivals and the basis among the evidence in force, not everything in force.

The reference (D260): the rung is the forecast the evidence in force makes most likely, judged against what the market expects
(consensus, guidance, the stated plan); the answer states the reference and the outcome the evidence implies, both stored beside the
rung, and an empty one is refused."""
import dataclasses
import json
import re

from .. import config, model, vocabulary
from . import store

PUSHES = vocabulary.PUSHES
SUPPORTED_VERSIONS = ('judging-v7', 'judging-v8')   # D354: the frozen judging prompt; judging-v8, the argument card, under measurement
CARD_VERSIONS = ('judging-v8',)
ARRIVAL_READINGS = 3              # judging-v8: a new piece is shown in the thesis's first three judgements after it arrives
CARD_CLAIMS = 5                   # at most this many claims for, and as many against
CARD_REFS = 4                     # each claim cites one to this many supplied ids
CLAIM_CHARS = 300
NOTE_ITEMS = 3                    # watch and gaps each hold at most this many items
NOTE_CHARS = 200
UPGRADE_BASIS = 40                # a thesis judged before the card starts its first card from at most this many pieces its recent judgements cited
FALLBACK_PIECES = 40              # a reading that would show no evidence shows this many most recently linked pieces in force
READINGS = 5                      # a piece is shown in the thesis's first five judgements after it arrives
BASIS = 10                        # and while one of the last ten judgements cited it
THEME_REASONS_CHARS = 300
UPDATED_MARK = 'updated since this thesis was last judged'


def writes_card(prompt_version):
    return prompt_version in CARD_VERSIONS


def require_supported(prompt_version):
    """Refuses a judging prompt version this code does not build, before any request is made."""
    if prompt_version not in SUPPORTED_VERSIONS:
        raise ValueError(f'judging {prompt_version!r} is not built; this code builds only {", ".join(SUPPORTED_VERSIONS)} (D354)')


def evidence_in_view(conn, view_id):
    """(the pieces a judgement of this thesis reads, how many pieces in force are not shown): the arrivals (linked after the
    READINGS-th most recent judgement, or all when there are fewer) and the basis (cited by one of the last BASIS judgements),
    both among the evidence in force."""
    in_force = store.evidence_in_force(conn, view_id)
    recent = store.recent_judgements(conn, view_id, BASIS)
    arrivals_after = recent[READINGS - 1]['seq'] if len(recent) >= READINGS else -1
    basis = {evidence_id for j in recent for evidence_id in j['cites']}
    linked_at = {r['evidence_id']: r['seq'] for r in conn.execute('select evidence_id, seq from evidence_links where view_id=?', (view_id,))}
    shown = [p for p in in_force if linked_at.get(p['evidence_id'], -1) > arrivals_after or p['evidence_id'] in basis]
    return shown, len(in_force) - len(shown)


def schema_for(prompt_version):
    require_supported(prompt_version)
    if writes_card(prompt_version):
        return card_schema()
    pushes = PUSHES
    schema = {
        'type': 'object', 'additionalProperties': False,
        'required': ['rung', 'reasons', 'cites', 'cites_views', 'pushes', 'changed', 'why_changed'],
        'properties': {
            'rung': {'type': 'integer'}, 'reasons': {'type': 'string'},
            'cites': {'type': 'array', 'items': {'type': 'string'}}, 'cites_views': {'type': 'array', 'items': {'type': 'string'}},
            'pushes': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['evidence_id', 'push'],
                                                  'properties': {'evidence_id': {'type': 'string'}, 'push': {'type': 'string', 'enum': pushes}}}},
            'changed': {'type': 'boolean'}, 'why_changed': {'type': 'string'},
        },
    }
    schema['required'].append('theme_pushes')
    schema['properties']['theme_pushes'] = {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['view_id', 'push'],
                                                                       'properties': {'view_id': {'type': 'string'}, 'push': {'type': 'string', 'enum': pushes}}}}
    schema['required'][1:1] = STANCE_FIELDS           # after rung: the reference and the implied outcome are written before the reasons
    schema['properties'].update({field: {'type': 'string'} for field in STANCE_FIELDS})
    return schema


def themes_in_force(conn, view_id):
    """The theme block of an asset thesis: every open theme thesis with a current state, with its rung label and whether a
    changed conclusion was recorded after this thesis's last judgement. Empty for a theme thesis."""
    if store.view(conn, view_id)['object_kind'] == 'theme':
        return []
    last = store.current_state(conn, view_id)
    out = []
    for row in conn.execute("select view_id from views where object_kind='theme' order by view_id"):
        theme_id = row['view_id']
        state = store.current_state(conn, theme_id)
        if not state or not store.is_open(conn, theme_id):
            continue
        updated = bool(last) and bool(conn.execute('select 1 from judgements where view_id=? and changed=1 and judgement_id>? limit 1',
                                                   (theme_id, last['judgement_id'])).fetchone())
        rung = store.rungs_of(conn, theme_id)[state['rung'] - 1]
        out.append({'view_id': theme_id, 'view': store.view(conn, theme_id), 'state': state, 'rung_label': rung['label'], 'updated': updated})
    return out


STANCE_FIELDS = ['reference', 'implied_outcome']   # D260: what the market expects, and the figure or date the evidence implies


class JudgementRefused(Exception):
    pass


def topological(conn, view_ids):
    """Dependencies first: a view comes after every view it depends on that is also in the set."""
    remaining = list(dict.fromkeys(view_ids))
    ordered, placed = [], set()
    while remaining:
        progressed = False
        for view_id in list(remaining):
            deps = {d['resolved_to'] for d in store.dependencies_of(conn, view_id) if d['resolved_to']}
            if deps.isdisjoint(set(remaining) - {view_id}) or deps <= placed:
                ordered.append(view_id)
                placed.add(view_id)
                remaining.remove(view_id)
                progressed = True
        if not progressed:                 # a cycle slipped through: keep going in the given order
            ordered.extend(remaining)
            break
    return ordered


def _piece_lines(p, shown_ids=None):
    """One evidence piece as the request prints it, with its replaced predecessor and the matcher's opinions. shown_ids limits the
    same-claim list to the pieces this request also shows and counts the rest (judging-v8); None lists them all (judging-v7)."""
    src = p['sources'][0] if p['sources'] else {}
    lines = [f'- {p["evidence_id"]} [{p["tier"]}; {p["speaker"]}; original source {p["original_who"]} {p["original_day"]}; from {src.get("input_id")} {src.get("publication_day")}] {p["one_line"]}\n    Quote: {p["quote"][:400]}']
    if p.get('replaced'):
        lines.append(f'    It replaces {p["replaced"]["evidence_id"]} ({p["replaced"]["original_day"]}): {p["replaced"]["one_line"]}')
    if p.get('same_as'):
        if shown_ids is None:
            lines.append(f'    Opinion, not verified: the matcher read this as the same claim as {", ".join(p["same_as"])}; the argument counts one claim, one more outlet.')
        else:
            listed = [x for x in p['same_as'] if x in shown_ids]
            others = len(p['same_as']) - len(listed)
            named = ', '.join(listed) + (f' and {others} more' if listed and others else f'{others} pieces not shown' if others else '')
            lines.append(f'    Opinion, not verified: the matcher read this as the same claim as {named}; the argument counts one claim, one more outlet.')
    if p.get('revises'):
        lines.append(f'    Opinion, not verified: the matcher read it as a later version of {p["revises"]["evidence_id"]} ({p["revises"]["original_day"]}); both are in force: {p["revises"]["one_line"]}')
    return lines


def _dependency_lines(conn, deps):
    lines = []
    if deps:
        lines.append('\n[Current conclusions of the theses it depends on]')
        for d in deps:
            target = d['resolved_to']
            if not target:
                lines.append(f'- the {d["wait_year"]} thesis on chain {d["wait_chain_view_id"]}: not yet created ({d["direction"]})')
                continue
            tv = store.view(conn, target)
            state = store.current_state(conn, target)
            flag = 'historical only' if d['resolution'] == 'history_only' else ('closed' if not store.is_open(conn, target) else 'open')
            rung_label = store.rungs_of(conn, target)[state['rung'] - 1]['label'] if state else 'not judged yet'
            lines.append(f'- {target} ({flag}; {d["direction"]}) {tv["question"]}: now rung {state["rung"] if state else "-"} {rung_label}; reasons: {(state or {}).get("reasons", "")[:600]}')
    return lines


def _theme_lines(themes):
    lines = []
    if themes:
        lines.append(f'\n[Themes in force, {len(themes)}]')
        for theme in themes:
            tv, state = theme['view'], theme['state']
            mark = f'; {UPDATED_MARK}' if theme['updated'] else ''
            lines.append(f'- {theme["view_id"]} ({tv["object_id"]}, due {tv["due_day"]}) {tv["question"]}: now rung {state["rung"]} {theme["rung_label"]}; '
                         f'judged {state["publication_day"]}{mark}; reasons: {(state["reasons"] or "")[:THEME_REASONS_CHARS]}')
    return lines


def _previous_lines(last):
    if last:
        return [f'\n[Previous conclusion, for comparison only] rung {last["rung"]}; reasons: {last["reasons"][:800]}']
    return ['\n[Previous conclusion] none: this is the first judgement, so changed must be true.']


def _lines_english(conn, view_id, v, rungs, pieces, deps, last, themes=(), hidden=0):
    """hidden: how many pieces in force are not shown."""
    lines = [f'Thesis {view_id} ({v["object_id"]}, {v["kind"]}, focus "{v["looks_at"]}", {v["year"] or ""}, due {v["due_day"]}): {v["question"]}',
             'Ladder: ' + ' / '.join(f'rung {r["position"]} {r["label"]}: {r["condition"]}' for r in rungs), '',
             f'[Evidence in view under this thesis, {len(pieces)} items]']
    if hidden:
        lines.append(f'[Not shown: {hidden} more pieces in force, read in earlier judgements; the previous conclusion carries them]')
    for p in pieces:
        lines.extend(_piece_lines(p))
    lines.extend(_dependency_lines(conn, deps))
    lines.extend(_theme_lines(themes))
    lines.extend(_previous_lines(last))
    lines.append('\nAnswer per the JSON schema. cites may name only the evidence ids listed above; '
                 + ('cites_views only the dependency thesis ids listed above' if deps else 'cites_views must be empty: this thesis depends on no other thesis')
                 + ('; theme_pushes only the theme ids listed above; a theme id goes only in theme_pushes, never in cites or cites_views' if themes else '') + '.')
    return lines


def build_prompt(conn, view_id, prompt_version):
    require_supported(prompt_version)
    v = store.view(conn, view_id)
    rungs = store.rungs_of(conn, view_id)
    deps = store.dependencies_of(conn, view_id)
    last = store.current_state(conn, view_id)
    if writes_card(prompt_version):
        argument, cited, new, fallback, hidden = card_in_view(conn, view_id)
        lines = _lines_card(conn, view_id, v, rungs, argument, cited, new, fallback, hidden, deps, last, themes_in_force(conn, view_id))
    else:
        pieces, hidden = evidence_in_view(conn, view_id)
        lines = _lines_english(conn, view_id, v, rungs, pieces, deps, last, themes_in_force(conn, view_id), hidden=hidden)
    with open(config.prompt_path(prompt_version + '.txt'), encoding='utf-8') as handle:
        return handle.read(), '\n'.join(lines)


def retry_note(errors):
    return '\n\nThe code returned the previous answer because: ' + '; '.join(errors) + '\nCorrect it and answer again, citing only the listed ids.'


def themes_shown_in(request_text):
    """The theme ids of the block a request carried: the ids the answer may name, whatever the ledger says now."""
    block = request_text.split('\n[Themes in force, ', 1)
    return set(re.findall(r'^- (v\d+) \(', block[1].split('\n\n[', 1)[0], re.M)) if len(block) == 2 else set()


def evidence_shown_in(request_text):
    """The evidence ids the request listed: the ids the answer may cite and push."""
    block = request_text.split('\n[Evidence in ', 1)
    return set(re.findall(r'^- (e\d+) \[', block[1].split('\n\n[', 1)[0], re.M)) if len(block) == 2 else set()


def check_answer(conn, view_id, data, request_text=None, previous=None):
    """request_text: the user message that was sent, so theme and evidence ids are checked against what it carried (a theme may have
    closed or opened since); without it, against what the ledger would show now. previous: (the thesis's last judgement before this one,
    unused) when checking a stored answer later; by default the ledger's latest."""
    errors = []
    shown = themes_shown_in(request_text) if request_text is not None else {theme['view_id'] for theme in themes_in_force(conn, view_id)}
    named = []
    for entry in data.get('theme_pushes', []):
        if entry['view_id'] in named:
            errors.append(f'{entry["view_id"]} is named twice in theme_pushes')
        elif entry['view_id'] not in shown:
            errors.append(f'{entry["view_id"]} is not a theme in force shown to {view_id}')
        named.append(entry['view_id'])
    # the closed set is what the request showed (D198), read from the text that was sent, else computed from the ledger
    allowed = evidence_shown_in(request_text) if request_text is not None else {p['evidence_id'] for p in evidence_in_view(conn, view_id)[0]}
    not_allowed = lambda e: f'{e} is not among the evidence shown to {view_id}'
    bad_push = lambda e: f'push on {e} which was not shown to {view_id}'
    if previous is not None and request_text is not None:        # a stored answer: the dependencies its request showed
        deps = _ids_in_block(request_text, DEPENDENCY_BLOCK, r'^- (v\d+) \(')
    else:
        deps = {d['resolved_to'] for d in store.dependencies_of(conn, view_id) if d['resolved_to']}
    rungs = store.rungs_of(conn, view_id)
    if not 1 <= data['rung'] <= len(rungs):
        errors.append(f'rung {data["rung"]} outside 1..{len(rungs)}')
    for cited in data['cites']:
        if cited not in allowed:
            errors.append(not_allowed(cited))
    for cited in data['cites_views']:
        if cited not in deps:
            errors.append(f'{cited} is not a dependency of {view_id}')
    for push in data['pushes']:
        if push['evidence_id'] not in allowed:
            errors.append(bad_push(push['evidence_id']))
    for field in STANCE_FIELDS:
        if not str(data.get(field) or '').strip():
            errors.append(f'{field} is empty: state what the market expects and the figure or date the evidence implies')
    last = store.current_state(conn, view_id) if previous is None else previous[0]
    if last is None and not data['changed']:
        errors.append('first judgement must say changed')
    if last is not None and last['rung'] != data['rung'] and not data['changed']:
        errors.append(f'rung moved from {last["rung"]} to {data["rung"]} but changed is false')
    return errors


def _record(conn, cfg, view_id, seq, item, answer):
    data = vocabulary.judgement_answer(answer.data)
    judgement_id = store.insert(conn, 'judgements', view_id=view_id, seq=seq, input_id=item['input_id'], rung=data['rung'],
                                reasons=data['reasons'], cited_evidence_json=json.dumps(data['cites']), cited_views_json=json.dumps(data['cites_views']),
                                pushes_json=json.dumps(data['pushes'], ensure_ascii=False), changed=1 if data['changed'] else 0,
                                theme_pushes_json=json.dumps(data.get('theme_pushes', []), ensure_ascii=False),
                                reference=data.get('reference'), implied_outcome=data.get('implied_outcome'),
                                why_changed=data['why_changed'], config_checksum=cfg.checksum, call_id=answer.call_id,
                                request_sha256=answer.request_sha256, publication_day=item['publication_day'])
    conn.commit()
    return {'view_id': view_id, 'judgement_id': judgement_id, 'rung': data['rung'], 'changed': data['changed'], 'cost': answer.cost_usd, 'cached': answer.cached}


JUDGE_WORKERS = 32     # a day's round is up to 40 judgements of about 16 s each in two dependency levels (themes, then assets); 32 at a time makes a round about two calls long (2026-11-02)


def upstream(conn, view_id):
    """Every view this one depends on, directly or through its dependencies."""
    seen, stack = set(), [view_id]
    while stack:
        for dep in store.dependencies_of(conn, stack.pop()):
            target = dep['resolved_to']
            if target and target not in seen:
                seen.add(target)
                stack.append(target)
    return seen


def open_asset_views(conn):
    return [v for v in store.open_views(conn) if store.view(conn, v)['object_kind'] != 'theme']


def queued_by_change(conn, view_id):
    """What a changed conclusion of this view queues: its dependants and, for a theme thesis, every open asset thesis. The one rule,
    read for a live judgement and for the judgements a resumed round finds committed."""
    queued = store.dependants_of(conn, view_id)
    if store.view(conn, view_id)['object_kind'] == 'theme':
        queued = queued + open_asset_views(conn)
    return queued


def queued_by_ledger(conn, seq):
    """What the judgements already committed at this sequence number queued; a fresh round finds nothing here, a resumed round
    finds what the interrupted one had queued in memory."""
    queued = []
    for row in conn.execute('select view_id from judgements where seq=? and changed=1 order by judgement_id', (seq,)):
        queued.extend(queued_by_change(conn, row['view_id']))
    return queued


# ---------- judging-v8: the argument card (D201; docs/research/2026-11-04-argument-record/design.md) ----------

EVIDENCE_ID = re.compile(r'^e\d+$')
CARD_BLOCK, NEW_BLOCK, FALLBACK_BLOCK = '\n[Evidence the card cites, ', '\n[New evidence, ', '\n[Evidence in force, most recently linked, '
DEPENDENCY_BLOCK = '\n[Current conclusions of the theses it depends on]'


def card_schema():
    """judging-v8's answer: v7's conclusion fields and theme pushes, the card in place of cites and cites_views (code derives them from
    the card's refs), and pushes only on the evidence the card cites. Field limits sit in the descriptions and are enforced by code."""
    claim = {'type': 'object', 'additionalProperties': False, 'required': ['keep', 'text', 'refs', 'relays', 'independent_sources'], 'properties': {
        'keep': {'type': 'string', 'description': "The id of the previous card's claim this one keeps, such as k3; empty for a new claim."},
        'text': {'type': 'string', 'description': f'One sentence of at most {CLAIM_CHARS} characters stating the figure, step or fact the claim rests on.'},
        'refs': {'type': 'array', 'items': {'type': 'string'}, 'description': f'One to {CARD_REFS} supplied ids the claim rests on: evidence, a dependency or a theme.'},
        'relays': {'type': 'array', 'items': {'type': 'string'}, 'description': 'The refs that only relay the same original report as another ref.'},
        'independent_sources': {'type': 'integer', 'description': "How many distinct original reports stand behind the claim; 0 when it rests only on a dependency's or a theme's conclusion."}}}
    note = {'type': 'array', 'items': {'type': 'string'}}
    card = {'type': 'object', 'additionalProperties': False, 'required': ['for', 'against', 'watch', 'gaps', 'removed'], 'properties': {
        'for': {'type': 'array', 'items': claim, 'description': f'At most {CARD_CLAIMS} claims for the answer.'},
        'against': {'type': 'array', 'items': claim, 'description': f'At most {CARD_CLAIMS} claims against the answer.'},
        'watch': dict(note, description=f'At most {NOTE_ITEMS} pieces of coming information that would move the answer, each in at most {NOTE_CHARS} characters.'),
        'gaps': dict(note, description=f'At most {NOTE_ITEMS} things not verified or not known, each in at most {NOTE_CHARS} characters.'),
        'removed': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['id', 'reason'], 'properties': {
            'id': {'type': 'string', 'description': 'A claim of the previous card that this card drops.'},
            'reason': {'type': 'string', 'description': f'Why, in at most {NOTE_CHARS} characters, such as the piece that superseded it.'}}}}}}
    push = {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['evidence_id', 'push'],
                                       'properties': {'evidence_id': {'type': 'string'}, 'push': {'type': 'string', 'enum': PUSHES}}}}
    return {'type': 'object', 'additionalProperties': False,
            'required': ['rung', 'reference', 'implied_outcome', 'reasons', 'card', 'pushes', 'changed', 'why_changed', 'theme_pushes'],
            'properties': {'rung': {'type': 'integer'}, 'reference': {'type': 'string'}, 'implied_outcome': {'type': 'string'}, 'reasons': {'type': 'string'},
                           'card': card, 'pushes': push, 'changed': {'type': 'boolean'}, 'why_changed': {'type': 'string'},
                           'theme_pushes': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['view_id', 'push'],
                                                                       'properties': {'view_id': {'type': 'string'}, 'push': {'type': 'string', 'enum': PUSHES}}}}}}


def card_claims(card):
    return [c for side in ('for', 'against') for c in card.get(side, [])]


def card_evidence_refs(card):
    return list(dict.fromkeys(r for c in card_claims(card) for r in c['refs'] if EVIDENCE_ID.match(r)))


def card_in_view(conn, view_id):
    """judging-v8's reading: (the latest card, the pieces it cites, the pieces that arrived in the last ARRIVAL_READINGS judgements and that
    it does not cite, the fallback pieces, how many pieces in force are not shown), all among the evidence in force. Without a card, a
    thesis judged before starts from the pieces its last BASIS judgements cited, newest first, at most UPGRADE_BASIS; a thesis judged
    fewer than ARRIVAL_READINGS times sees every piece as new. A reading that would show no piece at all (a thesis whose judgements cited
    nothing and saw nothing arrive lately) shows the FALLBACK_PIECES most recently linked pieces in force instead, so every request
    carries something a claim can cite."""
    in_force = store.evidence_in_force(conn, view_id)
    argument = store.latest_argument(conn, view_id)
    if argument:
        basis = set(card_evidence_refs(argument['card']))
    else:
        basis = set(list(dict.fromkeys(e for j in store.recent_judgements(conn, view_id, BASIS) for e in j['cites']))[:UPGRADE_BASIS])
    recent = store.recent_judgements(conn, view_id, ARRIVAL_READINGS)
    arrivals_after = recent[ARRIVAL_READINGS - 1]['seq'] if len(recent) >= ARRIVAL_READINGS else -1
    linked_at = {r['evidence_id']: r['seq'] for r in conn.execute('select evidence_id, seq from evidence_links where view_id=?', (view_id,))}
    cited = [p for p in in_force if p['evidence_id'] in basis]
    new = [p for p in in_force if p['evidence_id'] not in basis and linked_at.get(p['evidence_id'], -1) > arrivals_after]
    fallback = []
    if not cited and not new:
        fallback = sorted(in_force, key=lambda p: -linked_at.get(p['evidence_id'], -1))[:FALLBACK_PIECES]
        fallback = [p for p in in_force if p in fallback]
    return argument, cited, new, fallback, len(in_force) - len(cited) - len(new) - len(fallback)


def read_versions(conn, view_id):
    """The judgement of each resolved dependency and each theme in force that a judging-v8 request shows, by thesis id (None when not
    judged yet): the card records which conclusion a claim citing them read."""
    read = {d['resolved_to']: (store.current_state(conn, d['resolved_to']) or {}).get('judgement_id') for d in store.dependencies_of(conn, view_id) if d['resolved_to']}
    read.update({t['view_id']: t['state']['judgement_id'] for t in themes_in_force(conn, view_id)})
    return read


def _card_lines(argument):
    if not argument:
        return ['[Argument card] none yet: write the first card.']
    card = argument['card']

    def claim(c):
        relays = f'; relays {", ".join(c["relays"])}' if c['relays'] else ''
        return f'- {c["id"]} [refs {", ".join(c["refs"])}{relays}; {c["independent_sources"]} independent source{"s" if c["independent_sources"] != 1 else ""}] {c["text"]}'
    lines = ['[Argument card, as last written]', 'For:'] + ([claim(c) for c in card['for']] or ['- none'])
    lines += ['Against:'] + ([claim(c) for c in card['against']] or ['- none'])
    lines.append('Would move it: ' + ('; '.join(card['watch']) or 'none'))
    lines.append('Not known: ' + ('; '.join(card['gaps']) or 'none'))
    return lines


def _lines_card(conn, view_id, v, rungs, argument, cited, new, fallback, hidden, deps, last, themes):
    shown = {p['evidence_id'] for p in cited + new + fallback}
    lines = [f'Thesis {view_id} ({v["object_id"]}, {v["kind"]}, focus "{v["looks_at"]}", {v["year"] or ""}, due {v["due_day"]}): {v["question"]}',
             'Ladder: ' + ' / '.join(f'rung {r["position"]} {r["label"]}: {r["condition"]}' for r in rungs), '']
    lines.extend(_card_lines(argument))
    lines.append(f'{CARD_BLOCK}{len(cited)} items]')
    for p in cited:
        lines.extend(_piece_lines(p, shown))
    lines.append(f'{NEW_BLOCK}{len(new)} items, arrived in the last {ARRIVAL_READINGS} judgements]')
    for p in new:
        lines.extend(_piece_lines(p, shown))
    if fallback:
        lines.append(f'{FALLBACK_BLOCK}{len(fallback)} items; nothing above was shown, so these are the latest linked]')
        for p in fallback:
            lines.extend(_piece_lines(p, shown))
    if hidden:
        lines.append(f'[Not shown: {hidden} more pieces in force, read in earlier judgements; the card carries what they established]')
    lines.extend(_dependency_lines(conn, deps))
    lines.extend(_theme_lines(themes))
    lines.extend(_previous_lines(last))
    lines.append('\nAnswer per the JSON schema. A claim\'s refs may name only the evidence, dependency and theme ids listed above; pushes only the evidence ids the card cites'
                 + ('; theme_pushes only the theme ids listed above' if themes else '') + '.')
    return lines


def _ids_in_block(request_text, header, pattern):
    block = request_text.split(header, 1)
    return set(re.findall(pattern, block[1].split('\n\n[', 1)[0], re.M)) if len(block) == 2 else set()


def card_request_ids(request_text):
    """The closed sets a judging-v8 request carried: (evidence ids it showed, the new ones among them, dependency ids, theme ids)."""
    cited = _ids_in_block(request_text, CARD_BLOCK, r'^- (e\d+) \[')
    new = _ids_in_block(request_text, NEW_BLOCK, r'^- (e\d+) \[')
    fallback = _ids_in_block(request_text, FALLBACK_BLOCK, r'^- (e\d+) \[')
    deps = _ids_in_block(request_text, DEPENDENCY_BLOCK, r'^- (v\d+) \(')
    return cited | new | fallback, new, deps, themes_shown_in(request_text)


def check_card_answer(conn, view_id, data, request_text, previous=None):
    """judging-v8's checks: v7's on the conclusion and the theme pushes, and the card's: each ref among the ids the request showed, the
    limits, the claim ids (a kept id is a claim of the previous card; every previous claim is kept or removed with a reason), relays within
    the refs, and pushes only on the evidence the card cites. previous: (the thesis's last judgement, its latest card) before this one,
    when checking a stored answer later; by default the ledger's latest."""
    errors = []
    evidence, _, deps, themes = card_request_ids(request_text)
    allowed = evidence | deps | themes
    named = []
    for entry in data.get('theme_pushes', []):
        if entry['view_id'] in named:
            errors.append(f'{entry["view_id"]} is named twice in theme_pushes')
        elif entry['view_id'] not in themes:
            errors.append(f'{entry["view_id"]} is not a theme in force shown to {view_id}')
        named.append(entry['view_id'])
    rungs = store.rungs_of(conn, view_id)
    if not 1 <= data['rung'] <= len(rungs):
        errors.append(f'rung {data["rung"]} outside 1..{len(rungs)}')
    for field in STANCE_FIELDS:
        if not str(data.get(field) or '').strip():
            errors.append(f'{field} is empty: state what the market expects and the figure or date the evidence implies')
    last, argument = (store.current_state(conn, view_id), store.latest_argument(conn, view_id)) if previous is None else previous
    if last is None and not data['changed']:
        errors.append('first judgement must say changed')
    if last is not None and last['rung'] != data['rung'] and not data['changed']:
        errors.append(f'rung moved from {last["rung"]} to {data["rung"]} but changed is false')
    card = data['card']
    previous = {c['id'] for c in card_claims(argument['card'])} if argument else set()
    if not card_claims(card):
        errors.append('the card holds no claim')
    kept = []
    for side in ('for', 'against'):
        if len(card[side]) > CARD_CLAIMS:
            errors.append(f'the card holds {len(card[side])} claims {side}, at most {CARD_CLAIMS}')
        for number, c in enumerate(card[side], 1):
            label = c['keep'] or f'new claim {number} {side}'
            if not c['text'].strip() or len(c['text']) > CLAIM_CHARS:
                errors.append(f'{label}: the claim must be one sentence of 1 to {CLAIM_CHARS} characters')
            if not 1 <= len(c['refs']) <= CARD_REFS or len(set(c['refs'])) != len(c['refs']):
                errors.append(f'{label}: refs must be 1 to {CARD_REFS} distinct ids')
            errors += [f'{label} cites {r}, which was not shown to {view_id}' for r in c['refs'] if r not in allowed]
            errors += [f'{label}: relay {r} is not among its refs' for r in c['relays'] if r not in c['refs']]
            relayed = {r for r in c['relays'] if r in c['refs']}
            if len(set(c['relays'])) != len(c['relays']) or (relayed and len(relayed) >= len(set(c['refs']))):
                errors.append(f'{label}: relays must be distinct refs that leave at least one ref they relay')
            reports = any(EVIDENCE_ID.match(r) for r in c['refs'])          # a dependency's or a theme's conclusion is our own judgement, not a report
            if c['independent_sources'] < (1 if reports else 0):
                errors.append(f'{label}: independent_sources must be at least 1 for a claim citing evidence' if reports else f'{label}: independent_sources cannot be negative')
            if c['keep']:
                if c['keep'] not in previous:
                    errors.append(f'{c["keep"]} is not a claim of the previous card')
                kept.append(c['keep'])
    errors += [f'{k} is kept twice' for k in sorted({k for k in kept if kept.count(k) > 1})]
    removed = [r['id'] for r in card['removed']]
    errors += [f'removed {k} is listed twice' for k in sorted({k for k in removed if removed.count(k) > 1})]
    for r in card['removed']:
        if r['id'] not in previous:
            errors.append(f'removed {r["id"]} is not a claim of the previous card')
        elif r['id'] in kept:
            errors.append(f'{r["id"]} is both kept and removed')
        if not r['reason'].strip() or len(r['reason']) > NOTE_CHARS:
            errors.append(f'removed {r["id"]}: the reason must be 1 to {NOTE_CHARS} characters')
    missing = sorted(previous - set(kept) - set(removed), key=lambda x: int(x[1:]))
    if missing:
        errors.append(f'claims of the previous card neither kept nor removed: {", ".join(missing)}')
    for field in ('watch', 'gaps'):
        if len(card[field]) > NOTE_ITEMS or any(not n.strip() or len(n) > NOTE_CHARS for n in card[field]):
            errors.append(f'{field}: at most {NOTE_ITEMS} items of 1 to {NOTE_CHARS} characters')
    cited = set(card_evidence_refs(card))
    pushed = [p['evidence_id'] for p in data['pushes']]
    errors += [f'push on {e} which the card does not cite' for e in pushed if e not in cited]
    errors += [f'{e} is pushed twice' for e in sorted({e for e in pushed if pushed.count(e) > 1})]
    return errors


def _record_card(conn, cfg, view_id, seq, item, answer, request_text, read):
    """The judgement, its card and the use of the new pieces, written in one transaction: a failure rolls all three back before the
    caller records it. A new claim takes the next claim number this thesis has never used."""
    data = vocabulary.judgement_answer(answer.data)
    _, new, deps, _ = card_request_ids(request_text)
    used = store.claim_numbers_used(conn, view_id)
    next_number = max(used, default=0) + 1
    stored = {'for': [], 'against': [], 'watch': data['card']['watch'], 'gaps': data['card']['gaps'], 'removed': data['card']['removed'], 'read': {}}
    for side in ('for', 'against'):
        for c in data['card'][side]:
            if c['keep']:
                claim_id = c['keep']
            else:
                claim_id, next_number = f'k{next_number}', next_number + 1
            stored[side].append({'id': claim_id, 'text': c['text'], 'refs': c['refs'], 'relays': c['relays'], 'independent_sources': c['independent_sources']})
    refs = [r for c in card_claims(stored) for r in c['refs']]
    stored['read'] = dict(read)            # the judgement of every dependency and theme the request showed, cited or only weighed
    arrival_use = {e: [c['id'] for c in card_claims(stored) if e in c['refs']] for e in sorted(new, key=lambda x: int(x[1:]))}
    try:
        judgement_id = store.insert(conn, 'judgements', view_id=view_id, seq=seq, input_id=item['input_id'], rung=data['rung'], reasons=data['reasons'],
                                    cited_evidence_json=json.dumps(card_evidence_refs(stored)), cited_views_json=json.dumps(list(dict.fromkeys(r for r in refs if r in deps))),
                                    pushes_json=json.dumps(data['pushes'], ensure_ascii=False), changed=1 if data['changed'] else 0,
                                    theme_pushes_json=json.dumps(data.get('theme_pushes', []), ensure_ascii=False),
                                    reference=data.get('reference'), implied_outcome=data.get('implied_outcome'), why_changed=data['why_changed'],
                                    config_checksum=cfg.checksum, call_id=answer.call_id, request_sha256=answer.request_sha256,
                                    publication_day=item['publication_day'], arrival_use_json=json.dumps(arrival_use))
        store.insert(conn, 'arguments', view_id=view_id, judgement_id=judgement_id, seq=seq, card_json=json.dumps(stored, ensure_ascii=False),
                     prompt_version=cfg.rejudging.prompt_version)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return {'view_id': view_id, 'judgement_id': judgement_id, 'rung': data['rung'], 'changed': data['changed'], 'cost': answer.cost_usd, 'cached': answer.cached}


def round_of_judgements(archive, cfg, conn, changed_views, seq, item, *, transport=None):
    """Judge the open views in changed_views, dependencies first; a changed conclusion queues open dependants.

    Views that do not depend on each other are judged at the same time: each level of the dependency order is sent
    to the model concurrently (the prompts are built and the answers checked and written in this thread, so the
    database connection never crosses threads). A view waits while anything upstream of it is still pending, so a
    dependant always reads this round's conclusion of its dependency. A view with no evidence in force stays
    unjudged (D59), and a view already judged at this sequence number (a resumed round) is not judged twice.

    Among the views ready to be judged, theme theses go first, so an asset thesis reads this round's theme conclusions; a theme judgement that says changed queues every open asset thesis with
    evidence in force. The starting queue adds what the ledger says earlier commits at this sequence number queued."""
    import concurrent.futures

    version = cfg.rejudging.prompt_version
    schema = schema_for(version)
    card = writes_card(version)

    def checked(view_id, data, request_text):
        return check_card_answer(conn, view_id, data, request_text) if card else check_answer(conn, view_id, data, request_text)

    def eligible(view_id):
        return store.is_open(conn, view_id) and not store.has_judgement(conn, view_id, seq) and bool(store.evidence_in_force(conn, view_id))

    def is_theme(view_id):
        return store.view(conn, view_id)['object_kind'] == 'theme'

    pending = [v for v in topological(conn, list(changed_views) + queued_by_ledger(conn, seq)) if eligible(v)]
    done, results = set(), []
    while pending:
        ready = [v for v in pending if upstream(conn, v).isdisjoint(set(pending) - {v})] or pending[:1]
        level = [v for v in ready if is_theme(v)] or ready
        prompts = {v: build_prompt(conn, v, version) for v in level}
        read = {v: read_versions(conn, v) for v in level} if card else {}

        def ask(view_id, note=''):
            system, user = prompts[view_id]
            return model.call(archive, cfg, cfg.rejudging, system, user + note, schema, 'judgement', 'judge', transport=transport)

        with concurrent.futures.ThreadPoolExecutor(max_workers=JUDGE_WORKERS) as pool_:
            answers = dict(zip(level, pool_.map(ask, level)))
        for view_id in level:
            answer = answers[view_id]
            errors = checked(view_id, answer.data, prompts[view_id][1])
            if errors:
                archive.retire(answer.call_id)                 # a refused answer never answers the same request again (a resume re-samples)
                answer = ask(view_id, retry_note(errors))
                errors = checked(view_id, answer.data, prompts[view_id][1])
                if errors:
                    archive.retire(answer.call_id)
                    raise JudgementRefused(f'{view_id}: ' + '; '.join(errors))
            result = _record_card(conn, cfg, view_id, seq, item, answer, prompts[view_id][1], read[view_id]) if card else _record(conn, cfg, view_id, seq, item, answer)
            done.add(view_id)
            results.append(result)
            if result['changed']:
                for dependant in queued_by_change(conn, view_id):
                    if dependant not in done and dependant not in pending and eligible(dependant):
                        pending.append(dependant)
        pending = [v for v in topological(conn, pending) if v not in done and eligible(v)]
    return results
