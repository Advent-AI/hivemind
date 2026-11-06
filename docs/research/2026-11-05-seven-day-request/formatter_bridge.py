"""Offline, position-bound bridge for saved simple-A answers; no matcher or writer."""
import copy
import datetime
from hivemind import extraction, model

class BridgeRefusal(ValueError):
    pass

CANDIDATE_FIELDS = frozenset(extraction.schema_for('v74i')['properties']['candidates']['items']['required']) - {'id','question','evidence_ids'}
META_FIELDS = frozenset(('speaker','original_who','original_day','tier','event_time'))
DATE_FIELDS = frozenset(('basis','reason','source_span','rung_reason'))


def build(raw_a, article, item, shown_ids, universe, prepared):
    """Copy A's questions/quotes/summaries and apply test-supplied missing fields.

    A valid shape does not authorize writing. Dates, rungs and source attribution need
    independent semantic review; an analyst-selected date is not a source fact.
    """
    import simple_new_question_poc as simple
    errors=model.check_schema(raw_a,simple.schema())
    if errors:raise BridgeRefusal('A schema: '+str(errors))
    if not isinstance(prepared,dict) or set(prepared)!={'candidate_fields','evidence_fields','date_notes','new_groups'}:
        raise BridgeRefusal('preparation keys')
    questions=raw_a['questions']; candidate_fields=prepared['candidate_fields']; evidence_fields=prepared['evidence_fields'];date_notes=prepared['date_notes']
    if len(candidate_fields)!=len(questions) or len(date_notes)!=len(questions):raise BridgeRefusal('candidate count')
    flat=[(ci,ei,e) for ci,q in enumerate(questions,1) for ei,e in enumerate(q['evidence'],1)]
    if len(evidence_fields)!=len(flat):raise BridgeRefusal('evidence count')
    if any(not q['evidence'] for q in questions):raise BridgeRefusal('A candidate has no evidence')
    candidates=[];evidence=[];trace=[]
    cursor=0
    for i,q in enumerate(questions,1):
        fields=candidate_fields[i-1]; date=date_notes[i-1]
        if not isinstance(fields,dict) or set(fields)!=CANDIDATE_FIELDS | {'candidate_id'} or fields['candidate_id']!=f'c{i}':raise BridgeRefusal('candidate fields or identity')
        if not isinstance(date,dict) or set(date)!=DATE_FIELDS or date['basis'] not in ('source','analyst_check') or not date['reason'].strip() or not date['rung_reason'].strip():raise BridgeRefusal('date or rung provenance')
        try:due=datetime.date.fromisoformat(fields['due_day']);publication=datetime.date.fromisoformat(item['publication_day'])
        except (ValueError,TypeError):raise BridgeRefusal('invalid date')
        if due<=publication:raise BridgeRefusal('due is not after publication')
        if date['basis']=='source' and (not date['source_span'] or date['source_span'] not in article or fields['due_day'] not in date['source_span']):raise BridgeRefusal('source date lacks exact ISO date in source span')
        if date['basis']=='analyst_check' and date['source_span']:raise BridgeRefusal('analyst date presented as source date')
        ids=[]
        for j,ev in enumerate(q['evidence'],1):
            cursor+=1; eid=f'e{cursor}';ids.append(eid);m=evidence_fields[cursor-1]
            if not isinstance(m,dict) or set(m)!=META_FIELDS | {'evidence_id'} or m['evidence_id']!=eid:raise BridgeRefusal('evidence metadata fields or identity')
            if m['original_day'] and m['original_day'] not in article:raise BridgeRefusal('original day is not an exact ISO date in article')
            if not ev['quote'].strip() or ev['quote'] not in article:raise BridgeRefusal('A quote absent from source')
            if not ev['what_it_shows'].strip():raise BridgeRefusal('empty A summary')
            evidence.append({'id':eid,'quote':ev['quote'],'one_line':ev['what_it_shows'],**{k:m[k] for k in META_FIELDS},'links':[f'c{i}']})
            trace.append({'candidate_position':i,'evidence_position':j,'id':eid,'a_original_speaker':ev['original_speaker']})
        c={k:copy.deepcopy(fields[k]) for k in CANDIDATE_FIELDS};c.update(id=f'c{i}',question=q['question'],evidence_ids=ids)
        if date['basis']=='analyst_check':c['looks_at']+=f" [Analyst-selected check date: {fields['due_day']}; not a source-stated date.]"
        candidates.append(c)
    out={'candidates':candidates,'evidence':evidence,'new_groups':copy.deepcopy(prepared['new_groups'])}
    schema=extraction.schema_for('v74i');errors=model.check_schema(out,schema)
    if errors:raise BridgeRefusal('product schema: '+str(errors))
    kept,kept_candidates,dropped,groups=extraction.sift_with_groups(out,item,article,set(shown_ids),universe)
    if dropped:raise BridgeRefusal('actual sift refused/merged: '+repr(dropped))
    if len(kept)!=len(evidence) or len(kept_candidates)!=len(candidates):raise BridgeRefusal('sift count changed')
    if groups!=out['new_groups']:raise BridgeRefusal('research groups changed during sift')
    old_e={e['id']:e for e in evidence};old_c={c['id']:c for c in candidates}
    for e in kept:
        original=old_e.get(e['id'])
        if not original or any(e.get(k)!=original.get(k) for k in ('quote','one_line','links','speaker','original_who','original_day','tier','event_time')):raise BridgeRefusal('evidence changed during sift')
    for c in kept_candidates:
        original=old_c.get(c['id'])
        if not original or any(c.get(k)!=original.get(k) for k in ('question','looks_at','object','kind','year','due_day','measure','scope','period_start','period_end','basis','unit','event_type','opens_as','settled_by','evidence_ids','rungs','group_refs')):raise BridgeRefusal('candidate changed during sift')
    return {'status':'structure_only_semantics_unverified','evidence':kept,'candidates':kept_candidates,'new_groups':groups,'trace':trace,'date_notes':copy.deepcopy(date_notes)}
