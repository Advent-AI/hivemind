"""Dispatch (docs/prd/04-dispatch.md): the only entrance. For each item, three questions in order: is it complete?
was it processed before? what is its classification result? Items that go to extraction get a sequence number in
arrival order; the processing record is a row per step; the review pool a row per occurrence."""
import dataclasses
import time

from .views import store

REQUIRED = ('input_id', 'publisher', 'published_at', 'publication_day', 'category', 'source_uri')


@dataclasses.dataclass
class Route:
    kind: str                     # returned | skipped | not_processed | merged | extract
    sequence_no: int = 0
    resume_from: str = None       # extracted | matched | written | judged, for an unfinished item
    reason: str = ''


STEPS = ('dispatched', 'extracted', 'matched', 'written', 'judged', 'handed_over')


def route(conn, item, universe):
    missing = [field for field in REQUIRED if not item.get(field)]
    if missing:
        store.pool(conn, 'incomplete_item', ','.join(missing), {'input_id': item.get('input_id'), 'missing': missing}, 0)
        return Route('returned', reason=f'missing {missing}')
    input_id = item['input_id']
    if store.is_processed(conn, input_id):
        return Route('skipped', reason='already processed')
    last = store.last_step(conn, input_id)
    if last and last['step'] in STEPS and last['sequence_no']:
        # unfinished work keeps its sequence number: after an ok step it continues at the next step, after a
        # failed step it retries that step (06-views: 失败从失败的那一步重试)
        position = STEPS.index(last['step'])
        resume_from = STEPS[position + 1] if last['result'] == 'ok' else last['step']
        return Route('extract', sequence_no=last['sequence_no'], resume_from=resume_from, reason='resuming')
    if item.get('copy_of'):
        return Route('merged', reason=f'copy of {item["copy_of"]}')
    if item.get('supersedes'):
        store.pool(conn, 'correction_not_supported', item['supersedes'], {'input_id': input_id}, 0)
        return Route('not_processed', reason='correction (supersedes) not supported in the POC')
    category = item['category']
    objects = [o['value'] for o in item.get('object_identifiers') or [] if universe.has(o['value'])]
    if not objects:
        return Route('not_processed', reason='no object on the research list')
    if not any(universe.watches(o, category) for o in objects):
        return Route('not_processed', reason=f'category {category} not watched for {objects}')
    # the sequence number is taken in arrival order and written at once, so two items routed before either is
    # processed (a whole day is routed first, then run) never share a number
    sequence_no = store.next_sequence(conn)
    store.mark_step(conn, input_id, sequence_no, 'dispatched', 'ok', '', item.get('publication_day'), time.strftime('%Y-%m-%dT%H:%M:%S'))
    conn.commit()
    return Route('extract', sequence_no=sequence_no, reason='')


def mark(conn, item, sequence_no, step, result='ok', reason=''):
    store.mark_step(conn, item['input_id'], sequence_no, step, result, reason, item.get('publication_day'), time.strftime('%Y-%m-%dT%H:%M:%S'))
