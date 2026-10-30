"""The final Idea assessment's representative selection; scores remain deterministic UI calculations."""
import copy

from . import model
from .views import store

PLAN_SCHEMA = {
    'type': 'object', 'additionalProperties': False, 'required': ['drivers', 'excluded'],
    'properties': {
        'drivers': {'type': 'array', 'items': {
            'type': 'object', 'additionalProperties': False,
            'required': ['thesis_id', 'label', 'supporting_end', 'reason'],
            'properties': {'thesis_id': {'type': 'string'}, 'label': {'type': 'string'},
                           'supporting_end': {'type': 'string', 'enum': ['first', 'last']},
                           'reason': {'type': 'string'}}}},
        'excluded': {'type': 'array', 'items': {
            'type': 'object', 'additionalProperties': False, 'required': ['thesis_id', 'reason'],
            'properties': {'thesis_id': {'type': 'string'}, 'reason': {'type': 'string'}}}},
    },
}
SCHEMA = {
    'type': 'object', 'additionalProperties': False, 'required': ['summary', 'composite'],
    'properties': {'summary': {'type': 'string'}, 'composite': PLAN_SCHEMA},
}


def disposition_schema(selected):
    """One required property per selected identity prevents missing, duplicate or foreign dispositions."""
    driver = {'type': 'object', 'additionalProperties': False,
              'required': ['kind', 'label', 'supporting_end', 'reason'],
              'properties': {'kind': {'type': 'string', 'enum': ['driver']}, 'label': {'type': 'string'},
                             'supporting_end': {'type': 'string', 'enum': ['first', 'last']}, 'reason': {'type': 'string'}}}
    excluded = {'type': 'object', 'additionalProperties': False, 'required': ['kind', 'reason'],
                'properties': {'kind': {'type': 'string', 'enum': ['excluded']}, 'reason': {'type': 'string'}}}
    ids = list(dict.fromkeys(entry['view_id'] for entry in selected))
    return {'type': 'object', 'additionalProperties': False, 'required': ['summary', 'composite'],
            'properties': {'summary': {'type': 'string'},
                           'composite': {'type': 'object', 'additionalProperties': False, 'required': ids,
                                         'properties': {ident: {'anyOf': [driver, excluded]} for ident in ids}}}}


def bind_dispositions(answer, selected, records, as_of):
    errors = model.check_schema(answer, disposition_schema(selected))
    if errors:
        raise model.SchemaError('; '.join(errors))
    plan = {'drivers': [], 'excluded': []}
    for ident, entry in answer['composite'].items():
        key = 'drivers' if entry['kind'] == 'driver' else 'excluded'
        plan[key].append({'thesis_id': ident, **{name: value for name, value in entry.items() if name != 'kind'}})
    return bind(plan, selected, records, as_of)


def disposition_prose(answer):
    return [answer['summary'], *([answer['outcome']] if 'outcome' in answer else []), *(value for entry in answer['composite'].values()
                                 for name, value in entry.items() if name in ('label', 'reason', 'weight_reason'))]


def outcome_schema(selected):
    schema = disposition_schema(selected)
    schema['required'] += ['outcome', 'claim_direction']
    schema['properties']['outcome'] = {'type': 'string'}
    schema['properties']['claim_direction'] = {'type': 'string', 'enum': ['higher', 'lower', 'unclear']}
    for choice in schema['properties']['composite']['properties'].values():
        driver = choice['anyOf'][0]
        driver['required'] = ['raises_outcome_end' if key == 'supporting_end' else key for key in driver['required']]
        driver['properties']['raises_outcome_end'] = driver['properties'].pop('supporting_end', {'type': 'string', 'enum': ['first', 'last']})
    return schema


def bind_outcome(answer, selected, records, as_of):
    errors = model.check_schema(answer, outcome_schema(selected))
    if errors:
        raise model.SchemaError('; '.join(errors))
    if not answer['outcome'].strip():
        raise model.SchemaError('composite: the assessed outcome must be named')
    dispositions = {}
    for ident, entry in answer['composite'].items():
        value = dict(entry)
        if entry['kind'] == 'driver':
            if answer['claim_direction'] == 'unclear':
                raise model.SchemaError('composite: an unclear claim cannot have scored drivers')
            end = value.pop('raises_outcome_end')
            value['supporting_end'] = end if answer['claim_direction'] == 'higher' else ('last' if end == 'first' else 'first')
        dispositions[ident] = value
    plan = bind_dispositions({'summary': answer['summary'], 'composite': dispositions}, selected, records, as_of)
    plan['target'] = {'outcome': answer['outcome'], 'direction': answer['claim_direction']}
    return plan


def endpoint_schema(theses):
    schema = outcome_schema([{'view_id': thesis['view_id']} for thesis in theses])
    properties = schema['properties']['composite']['properties']
    for thesis in theses:
        choice = copy.deepcopy(properties[thesis['view_id']])
        driver = choice['anyOf'][0]
        driver['required'] = ['raises_outcome_position' if key == 'raises_outcome_end' else key for key in driver['required']]
        del driver['properties']['raises_outcome_end']
        driver['properties']['raises_outcome_position'] = {'type': 'string', 'enum': [str(r['position']) for r in thesis['ladder']]}
        properties[thesis['view_id']] = choice
    return schema


def bind_endpoints(answer, selected, records, as_of, theses):
    errors = model.check_schema(answer, endpoint_schema(theses))
    if errors:
        raise model.SchemaError('; '.join(errors))
    first = {t['view_id']: str(t['ladder'][0]['position']) for t in theses}
    converted = copy.deepcopy(answer)
    for ident, entry in converted['composite'].items():
        if entry['kind'] == 'driver':
            position = entry.pop('raises_outcome_position')
            entry['raises_outcome_end'] = 'first' if position == first[ident] else 'last'
    return bind_outcome(converted, selected, records, as_of)


def weighted_schema(theses):
    schema = endpoint_schema(theses)
    for choice in schema['properties']['composite']['properties'].values():
        driver, excluded = choice['anyOf']
        driver['required'] += ['weight_percent', 'weight_reason']
        driver['properties'].update(weight_percent={'type': 'integer', 'minimum': 1, 'maximum': 100},
                                    weight_reason={'type': 'string'})
        excluded['required'].append('weight_percent')
        excluded['properties']['weight_percent'] = {'type': 'integer', 'enum': [0]}
    return schema


def bind_weighted(answer, selected, records, as_of, theses):
    """Bind explicit impact percentages without normalizing or changing the selected identities."""
    errors = model.check_schema(answer, weighted_schema(theses))
    if errors:
        raise model.SchemaError('; '.join(errors))
    total = 0
    drivers = 0
    stripped = copy.deepcopy(answer)
    for ident, entry in answer['composite'].items():
        weight = entry['weight_percent']
        if entry['kind'] == 'driver':
            if not 1 <= weight <= 100 or not entry['weight_reason'].strip():
                raise model.SchemaError(f'composite {ident}: a driver needs 1–100 impact percent and a reason')
            total += weight
            drivers += 1
            del stripped['composite'][ident]['weight_reason']
        elif weight != 0:
            raise model.SchemaError(f'composite {ident}: an excluded thesis must have zero weight')
        del stripped['composite'][ident]['weight_percent']
    if total != (100 if drivers else 0):
        raise model.SchemaError(f'composite: impact weights must sum to 100, got {total}')
    plan = bind_endpoints(stripped, selected, records, as_of, theses)
    for entry in plan['drivers'] + plan['excluded']:
        original = answer['composite'][entry['thesis_id']]
        entry['weight_percent'] = original['weight_percent']
        if 'weight_reason' in original:
            entry['weight_reason'] = original['weight_reason']
    plan.update(version='idea-composite/3', method='weighted')
    return plan


def positive_schema(theses):
    ids = [t['view_id'] for t in theses]
    properties = {
        'thesis_id': {'type': 'string', **({'enum': ids} if ids else {})},
        'label': {'type': 'string'},
        'raises_outcome_position': {'type': 'string', 'enum': ['1', '2', '3', '4', '5']},
        'reason': {'type': 'string'},
        'weight_percent': {'type': 'integer', 'minimum': 1, 'maximum': 100},
        'weight_reason': {'type': 'string'},
    }
    return {'type': 'object', 'additionalProperties': False,
            'required': ['summary', 'outcome', 'claim_direction', 'composite'],
            'properties': {'summary': {'type': 'string'}, 'outcome': {'type': 'string'},
                           'claim_direction': {'type': 'string', 'enum': ['higher', 'lower', 'unclear']},
                           'composite': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False,
                                         'required': list(properties), 'properties': properties}}}}


def bind_positive(answer, selected, records, as_of, theses):
    """Only positively weighted model choices become Idea associations."""
    errors = model.check_schema(answer, positive_schema(theses))
    if errors:
        raise model.SchemaError('; '.join(errors))
    allowed = {s['view_id'] for s in selected}
    dispositions = {}
    for entry in answer['composite']:
        ident = entry['thesis_id']
        if ident not in allowed or ident in dispositions:
            raise model.SchemaError(f'composite {ident}: must be a unique supplied candidate')
        dispositions[ident] = {'kind': 'driver', **{k: v for k, v in entry.items() if k != 'thesis_id'}}
    converted = {**answer, 'composite': dispositions}
    adopted = [s for s in selected if s['view_id'] in dispositions]
    plan = bind_weighted(converted, adopted, records, as_of, [t for t in theses if t['view_id'] in dispositions])
    del plan['excluded']
    plan['version'] = 'idea-composite/4'
    return plan


def positive_prose(answer):
    return [answer['summary'], answer['outcome'], *(entry[key] for entry in answer['composite']
             for key in ('label', 'reason', 'weight_reason'))]


def adoption_schema(theses):
    """The positive-selection answer with one item shape per candidate: each pins its thesis_id and offers only that
    thesis's own endpoint positions, so the request cannot ask for an endpoint the binder refuses."""
    def item(thesis_id=None, positions=('1', '2', '3', '4', '5')):
        return {'type': 'object', 'additionalProperties': False,
                'required': ['thesis_id', 'label', 'raises_outcome_position', 'reason', 'weight_percent', 'weight_reason'],
                'properties': {'thesis_id': {'type': 'string', **({'enum': [thesis_id]} if thesis_id else {})},
                               'label': {'type': 'string'},
                               'raises_outcome_position': {'type': 'string', 'enum': list(positions)},
                               'reason': {'type': 'string'},
                               'weight_percent': {'type': 'integer', 'minimum': 1, 'maximum': 100},
                               'weight_reason': {'type': 'string'}}}
    choices = [item(t['view_id'], [str(rung['position']) for rung in t['ladder']]) for t in theses]
    return {'type': 'object', 'additionalProperties': False,
            'required': ['summary', 'outcome', 'claim_direction', 'composite'],
            'properties': {'summary': {'type': 'string'}, 'outcome': {'type': 'string'},
                           'claim_direction': {'type': 'string', 'enum': ['higher', 'lower', 'unclear']},
                           'composite': {'type': 'array', 'items': {'anyOf': choices} if choices else item()}}}


def bind_adoption(answer, selected, records, as_of, theses, schema):
    """Bind an answer checked against the exact schema that was sent; code checks only what a schema cannot say."""
    errors = model.check_schema(answer, schema)
    if errors:
        raise model.SchemaError('; '.join(errors))
    if not answer['outcome'].strip():
        raise model.SchemaError('composite: the assessed outcome must be named')
    if answer['composite'] and answer['claim_direction'] == 'unclear':
        raise model.SchemaError('composite: an unclear claim cannot have scored drivers')
    first = {t['view_id']: str(t['ladder'][0]['position']) for t in theses}
    allowed = {s['view_id'] for s in selected} & set(first)
    drivers, seen, total = [], set(), 0
    for entry in answer['composite']:
        ident = entry['thesis_id']
        if ident not in allowed or ident in seen:
            raise model.SchemaError(f'composite {ident}: must be a unique supplied candidate')
        if not all(entry[key].strip() for key in ('label', 'reason', 'weight_reason')):
            raise model.SchemaError(f'composite {ident}: label, reason and weight reason must be nonempty')
        seen.add(ident)
        total += entry['weight_percent']
        raises = 'first' if entry['raises_outcome_position'] == first[ident] else 'last'
        supporting = raises if answer['claim_direction'] == 'higher' else ('last' if raises == 'first' else 'first')
        drivers.append({'thesis_id': ident, 'label': entry['label'], 'reason': entry['reason'], 'supporting_end': supporting,
                        'question': records[ident]['question'], 'weight_percent': entry['weight_percent'],
                        'weight_reason': entry['weight_reason']})
    if total != (100 if drivers else 0):
        raise model.SchemaError(f'composite: impact weights must sum to 100, got {total}')
    return {'version': 'idea-composite/4', 'method': 'weighted', 'as_of': as_of, 'drivers': drivers,
            'target': {'outcome': answer['outcome'], 'direction': answer['claim_direction']}}


def contract(prompt_version, selected, ledger=None):
    """The schema, prose fields and binder belonging to each versioned composite prompt."""
    if prompt_version == 'idea-summary-v8':
        theses = add_ladders(ledger, [{'view_id': entry['view_id']} for entry in selected], endpoints_only=True)
        schema = adoption_schema(theses)
        return schema, positive_prose, lambda answer, *args: bind_adoption(answer, *args, theses, schema)
    if prompt_version == 'idea-summary-v7':
        theses = add_ladders(ledger, [{'view_id': entry['view_id']} for entry in selected], endpoints_only=True)
        return positive_schema(theses), positive_prose, lambda answer, *args: bind_positive(answer, *args, theses)
    if prompt_version == 'idea-summary-v6':
        theses = add_ladders(ledger, [{'view_id': entry['view_id']} for entry in selected], endpoints_only=True)
        return weighted_schema(theses), disposition_prose, lambda answer, *args: bind_weighted(answer, *args, theses)
    if prompt_version == 'idea-summary-v5':
        theses = add_ladders(ledger, [{'view_id': entry['view_id']} for entry in selected], endpoints_only=True)
        return endpoint_schema(theses), disposition_prose, lambda answer, *args: bind_endpoints(answer, *args, theses)
    if prompt_version == 'idea-summary-v4':
        return outcome_schema(selected), disposition_prose, bind_outcome
    if prompt_version == 'idea-summary-v3':
        return disposition_schema(selected), disposition_prose, bind_dispositions
    if prompt_version == 'idea-summary-v2':
        return SCHEMA, prose, lambda answer, *args: bind(answer['composite'], *args)
    return None


def add_ladders(ledger, theses, endpoints_only=False):
    """Supply the immutable ordered outcomes, without copying evidence or guessing UI score orientation."""
    result = []
    for thesis in theses:
        rungs = store.rungs_of(ledger, thesis['view_id'])
        if endpoints_only:
            rungs = [rungs[0], rungs[-1]]
        result.append({**thesis, 'ladder': [{key: rung[key] for key in ('position', 'label', 'condition')} for rung in rungs]})
    return result


def prose(answer):
    return [answer['summary'], *(value for driver in answer['composite']['drivers'] for value in (driver['label'], driver['reason'])),
            *(entry['reason'] for entry in answer['composite']['excluded'])]


def bind(plan, selected, records, as_of):
    """Require one disposition per chosen thesis and bind identity/date metadata from trusted records."""
    errors = model.check_schema(plan, PLAN_SCHEMA)
    if errors:
        raise model.SchemaError('; '.join(errors))
    expected = {entry['view_id'] for entry in selected}
    seen = set()
    result = {}
    for kind in ('drivers', 'excluded'):
        result[kind] = []
        for entry in plan[kind]:
            ident = entry['thesis_id']
            if ident not in expected or ident in seen:
                raise model.SchemaError(f'composite {ident}: must be one unique chosen thesis')
            if not entry['reason'].strip() or (kind == 'drivers' and not entry['label'].strip()):
                raise model.SchemaError(f'composite {ident}: explanation and driver label must be nonempty')
            seen.add(ident)
            result[kind].append({**entry, 'question': records[ident]['question']})
    if seen != expected:
        raise model.SchemaError(f'composite: missing dispositions for {sorted(expected - seen)}')
    return {'version': 'idea-composite/2', 'method': 'equal_weight', 'as_of': as_of, **result}
