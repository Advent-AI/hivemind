"""D155: exact identity and same-answer coalescing, shared by matching and writing.

D197: a shared quantity (a candidate admitted as industry_aggregate / shared_quantity, a key stored with scope_source
'shared') is one thesis per theme, measure and period; its scope (the population or wording of the aggregate) is not
part of its identity."""
from ..universe import scope_key

KEY_VERSION = 2
SHARED_REASONS = ('industry_aggregate', 'shared_quantity')
EVENT_MEASURES = ('event', 'policy_event')


def is_shared(value):
    """A shared quantity: by its admission reason on a candidate, by its stored scope source on a key."""
    return value.get('measure') not in (None, 'other', *EVENT_MEASURES) and (value.get('scope_source') == 'shared' or value.get('opens_as') in SHARED_REASONS)


def automatic_key(value, object_id=None):
    """Return a complete, code-owned key, or None when identity still needs judgement."""
    if value.get('key_version') != KEY_VERSION:
        return None
    if value.get('measure') in (None, 'other'):
        return None
    if is_shared(value):
        return (object_id or value.get('object'), value['measure'], '', value.get('period_start'), value.get('period_end'),
                value.get('basis'), value.get('unit'), value.get('event_type'))
    if value.get('scope_source') not in ('none', 'watch'):
        return None
    if value['measure'] in EVENT_MEASURES and value.get('event_type') in (None, 'other', 'n/a'):
        return None
    return (object_id or value.get('object'), value['measure'], scope_key(value.get('scope', '')),
            value.get('period_start'), value.get('period_end'), value.get('basis'), value.get('unit'), value.get('event_type'))


GENERATION_MILESTONES = ('launch', 'shipment')


def same_generation_milestones(key, candidate):
    """D248 item 3: a product generation's launch and its shipments are milestones of one question, asked at the step that brings
    revenue; the judge of sameness (Jev) says whether they are the same generation, this only lifts the event-type conflict."""
    return key.get('measure') == 'event' and key.get('event_type') in GENERATION_MILESTONES and candidate.get('event_type') in GENERATION_MILESTONES


def one_process(key, candidate):
    """D258 (R2-f): a policy process's steps are one process; the model's event-type word for it (licence, approval, other) is not
    identity. One 14-day draw opened three questions on one licensing decision because that word varied."""
    return 'policy_event' in (key.get('measure'), candidate.get('measure'))


def conflicts(key, candidate, *, merging):
    """Known different quantities/events cannot merge; corrected scopes/periods bind only corrected keys. An event's period is its
    deadline: another deadline never conflicts (D248 item 2: while the earlier-deadline question is open, a later deadline is its
    evidence; a closed one is succeeded by `can_succeed`, which compares the periods itself). `event` and `policy_event` are one
    measure family (D258, R2-f): the model typed one licensing decision both ways, and the names and the judge of sameness decide."""
    if key['measure'] != candidate['measure'] and not (key['measure'] in EVENT_MEASURES and candidate['measure'] in EVENT_MEASURES):
        return True
    if (key['event_type'] != candidate.get('event_type', 'n/a') and not same_generation_milestones(key, candidate)
            and not one_process(key, candidate)):
        return True
    for field in ('basis', 'unit'):
        a, b = key[field], candidate.get(field, 'n/a')
        if a != 'n/a' and b != 'n/a' and a != b:
            return True
    if key.get('key_version') != KEY_VERSION or candidate.get('key_version') != KEY_VERSION:
        return False
    if (key.get('scope_source') in ('none', 'watch') and candidate.get('scope_source') in ('none', 'watch')
            and scope_key(key['scope']) != scope_key(candidate.get('scope', ''))):
        return True
    if key['measure'] in EVENT_MEASURES:
        return False
    return merging and (key['period_start'], key['period_end']) != (candidate.get('period_start'), candidate.get('period_end'))


def batch_plan(candidates, outcomes):
    """Resolve same-answer duplicates and validate dependencies on the resulting identities before retry ends."""
    aliases, first_by_key, errors = {}, {}, []
    for candidate in candidates:
        cid = candidate['id']
        outcome = outcomes.get(cid, ('skip', None, []))
        if outcome[0] not in ('new', 'succession'):
            continue
        key = automatic_key(candidate)
        first = first_by_key.setdefault(key, cid) if key is not None else cid
        aliases[cid] = first
        if outcome[:2] != outcomes[first][:2]:
            errors.append(f'candidate {cid}: same-key succession conflicts with {first}')
    graph, directions = {}, {}
    for cid, first in aliases.items():
        for dep in outcomes[cid][2]:
            target = aliases.get(dep['view_id'], dep['view_id'])
            chain = aliases.get(dep['wait_chain_view_id'], dep['wait_chain_view_id'])
            edge = (first, target, chain, dep['wait_year'])
            if edge in directions and directions[edge] != dep['direction']:
                errors.append(f'candidate {cid}: same-key dependency direction conflicts')
            directions[edge] = dep['direction']
            if target:
                graph.setdefault(first, set()).add(target)
    for cid in graph:
        stack, seen = list(graph[cid]), set()
        while stack:
            target = stack.pop()
            if target == cid:
                errors.append(f'candidate {cid}: coalesced dependencies lead back to itself')
                break
            if target not in seen:
                seen.add(target)
                stack.extend(graph.get(target, ()))
    return aliases, errors
