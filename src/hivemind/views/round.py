"""One item = one round (06-views.md 进库): source check → store → lists → the matching calls → checks → write.
Re-judging is the day's step (D63, 2026-10-24: once a day, over every view whose reading changed that day), run by
the replay after the day's items and before pull mode; see judge_day. Each step appends its processing row in the
same commit as its writes; a resume continues at the step the processing record names (after an ok step, or the
failed step itself) and never repeats a completed step."""
import dataclasses
import json

from .. import dispatch, extraction, vocabulary
from . import jev_matching, judging, matching, store, writing


@dataclasses.dataclass
class RoundResult:
    input_id: str
    evidence: int = 0
    candidates: int = 0
    new_views: int = 0
    judged: int = 0
    changed: int = 0
    cost: float = 0.0
    cached_calls: int = 0
    failed: str = ''
    dropped: int = 0


def _fail(conn, item, seq, result, step, kind, detail, pool_key):
    dispatch.mark(conn, item, seq, step, 'failed', detail[:300])
    store.pool(conn, kind, pool_key, {'input_id': item['input_id'], 'error': detail[:300]}, seq)
    result.failed = detail[:200]
    conn.commit()
    return result


def _match(conn, archive, cfg, universe, item, seq, result, candidates, evidence, lists, shown, *, extra_views=(), call_offset=0, transport=None, workers=1):
    """One matching call with one retry on a refused check. Returns Checked, or None after marking the failure."""
    note = ''
    checked = None
    engine = jev_matching if cfg.matching.engine == 'jev' else matching      # Jev answers once; a retry would be the same answer
    for attempt in range(1 if engine is jev_matching else 2):
        try:
            options = {'workers': workers} if engine is jev_matching else {}
            answer = engine.decide(archive, cfg, conn, item, candidates, evidence, lists, shown, extra_views=extra_views, retry_note=note, transport=transport, **options)
        except Exception as error:
            _fail(conn, item, seq, result, 'matched', 'matching_failed', 'matching: ' + repr(error), type(error).__name__)
            return None
        result.cost += answer.cost_usd
        result.cached_calls += int(answer.cached)
        checked = matching.check(conn, universe, answer.data, candidates, evidence, lists, shown)
        shown_record = {'candidates': lists.candidate_lists, 'evidence': {f'{k[0]}|{k[1]}': v for k, v in lists.evidence_lists.items()}}
        if getattr(answer, 'request_records', None):
            shown_record['requests'] = answer.request_records
        store.insert(conn, 'match_records', seq=seq, input_id=item['input_id'], call_no=call_offset + attempt + 1,
                     shown_json=json.dumps(shown_record),
                     request_sha256=answer.request_sha256, call_id=answer.call_id, decisions_json=json.dumps(answer.data, ensure_ascii=False),
                     checks_json=json.dumps({'refusals': checked.refusals, 'not_opened': checked.not_opened, 'notes': checked.notes}, ensure_ascii=False), written_json=None)
        if not checked.refusals:
            return checked
        note = '；'.join(checked.refusals)
    _fail(conn, item, seq, result, 'matched', 'matching_refused_twice', 'matching refused twice: ' + note, item['category'])
    return None


def changed_views_of_day(conn, day):
    """The views whose reading changed on a replay day: the union of the 'written' records of that day's items."""
    changed = set()
    for row in conn.execute("select reason from processing_steps where step='written' and result='ok' and publication_day=?", (day,)):
        changed.update(json.loads(row['reason']).get('changed', []))
    return changed


def judge_day(conn, archive, cfg, day, seq, *, transport=None, log=print):
    """D63: one re-judging round per day over every open view whose reading changed that day, dependencies first,
    recorded under the day's own processing record (input 'day:<date>'); a view already judged at this sequence
    number (a resumed day) is not judged twice."""
    marker = {'input_id': f'day:{day}', 'publication_day': day}
    changed = changed_views_of_day(conn, day)
    result = RoundResult(marker['input_id'])
    if not changed:
        return result
    try:
        judged = judging.round_of_judgements(archive, cfg, conn, sorted(changed), seq, marker, transport=transport)
        result.judged = len(judged)
        result.changed = sum(1 for j in judged if j['changed'])
        result.cost += sum(j['cost'] for j in judged)
        result.cached_calls += sum(1 for j in judged if j['cached'])
        dispatch.mark(conn, marker, seq, 'judged', 'ok', f'{len(changed)} views changed, {len(judged)} judged, {result.changed} changed conclusions')
        conn.commit()
    except judging.JudgementRefused as error:
        return _fail(conn, marker, seq, result, 'judged', 'judgement_refused_twice', 'judgement refused twice: ' + str(error), 'day')
    except Exception as error:
        return _fail(conn, marker, seq, result, 'judged', 'judging_failed', 'judging: ' + repr(error), type(error).__name__)
    return result


def run(conn, archive, cfg, universe, item, seq, *, resume_from=None, transport=None, log=print, extractor=None, matching_workers=1):
    result = RoundResult(item['input_id'])
    if resume_from in ('judged', 'handed_over'):       # written already; judging is the day's step
        dispatch.mark(conn, item, seq, 'handed_over', 'ok', 'resumed')
        conn.commit()
        return result
    objects = [o['value'] for o in item.get('object_identifiers') or [] if universe.has(o['value'])]
    shown = store.views_for_prompt(conn, objects)
    # extraction (or its stored handover on resume)
    handover = None
    if resume_from and resume_from != 'extracted':
        row = conn.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (item['input_id'],)).fetchone()
        if row:
            saved = vocabulary.extraction_answer(json.loads(row['handover_json']))          # a handover saved by a Chinese version reads in the canonical vocabulary
            handover = extraction.Handover(saved['evidence'], saved['candidates'], saved['dropped'], 0, '', True, 0.0, saved.get('new_groups') or [])
    if handover is None:
        try:
            shown_groups = store.groups_for_prompt(conn, objects, item.get('title') or '')
            handover = (extractor or extraction.extract)(archive, cfg, item, item['text'], shown, universe, shown_groups=shown_groups, transport=transport)
        except Exception as error:
            return _fail(conn, item, seq, result, 'extracted', 'extraction_failed', 'extraction: ' + repr(error), type(error).__name__)
        result.cost += handover.cost_usd
        result.cached_calls += int(handover.cached)
        store.insert(conn, 'handovers', input_id=item['input_id'], seq=seq,
                     handover_json=json.dumps({'evidence': handover.evidence, 'candidates': handover.candidates, 'dropped': handover.dropped, 'new_groups': handover.new_groups}, ensure_ascii=False))
        dispatch.mark(conn, item, seq, 'extracted', 'ok', f'{len(handover.evidence)} evidence, {len(handover.candidates)} candidates, {len(handover.dropped)} dropped')
        conn.commit()
    result.evidence, result.candidates, result.dropped = len(handover.evidence), len(handover.candidates), len(handover.dropped)
    if not handover.evidence and not handover.candidates:
        dispatch.mark(conn, item, seq, 'handed_over', 'ok', 'nothing to match')
        conn.commit()
        return result
    # first matching call: the candidates and the evidence linked straight to existing views
    lists = matching.build_lists(conn, handover, shown, cfg.search_top_n)
    checked = _match(conn, archive, cfg, universe, item, seq, result, handover.candidates, handover.evidence, lists, shown, transport=transport, workers=matching_workers)
    if checked is None:
        return result
    # second call: evidence linked to candidates that attached to an existing view, compared under that view
    second_pass = {}
    pending = []
    for e in handover.evidence:
        for link in e['links']:
            outcome = checked.outcomes.get(link)
            if outcome and outcome[0] == 'merge':
                pending.append((e, outcome[1]))
    if pending:
        lists2 = matching.Lists({}, {(e['id'], view_id): matching.rank_evidence(conn, view_id, e['one_line'], cfg.search_top_n) for e, view_id in pending})
        evidence2, seen = [], set()
        for e, view_id in pending:
            if e['id'] not in seen:
                evidence2.append(dict(e, links=[v for x, v in pending if x['id'] == e['id']]))
                seen.add(e['id'])
        checked2 = _match(conn, archive, cfg, universe, item, seq, result, [], evidence2, lists2, [], extra_views=sorted({v for _, v in pending}),
                          call_offset=2, transport=transport, workers=matching_workers)
        if checked2 is None:
            return result
        second_pass = checked2.evidence
    dispatch.mark(conn, item, seq, 'matched', 'ok', f'{len(checked.outcomes)} candidates placed')
    # write, and record what changed in the same commit (a resume at 'judged' reads it)
    try:
        written = writing.write(conn, universe, seq, item, handover, checked, second_pass)
    except Exception as error:
        return _fail(conn, item, seq, result, 'written', 'writing_failed', 'writing: ' + repr(error), type(error).__name__)
    result.new_views = len(set(written.new_views.values()))
    dispatch.mark(conn, item, seq, 'written', 'ok', json.dumps({'changed': sorted(written.changed_views), 'new': written.new_views, 'notes': written.notes[:20]}, ensure_ascii=False))
    dispatch.mark(conn, item, seq, 'handed_over', 'ok', '')
    conn.commit()
    return result
