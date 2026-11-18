"""Isolated selected-case Jev probe. Preparation is offline; sending requires a reviewed registration.

Original archive requests stay untouched. This does not produce a precision or acceptance score.
"""
import concurrent.futures
import datetime
import fcntl
import hashlib
import importlib.util
import json
import os
import pathlib
import random
import sqlite3
import subprocess
import sys
import time

ROOT = pathlib.Path('/Users/lchingen/hivemind')
HERE = pathlib.Path(__file__).resolve().parent
OLD = pathlib.Path('/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09')
RUNS = {'d1': ROOT/'poc/data/clean-e2e-2026-11-09/stage2-clean-d1-segment-2/step2', 'fresh': ROOT/'poc/data/clean-acceptance-2026-11-09/step2'}
CASES = {'C036':('d1','92:e2','45:e3'), 'C057':('d1','108:e2','8:e2'), 'C035':('d1','108:e6','58:e3'), 'C073':('d1','100:e1','24:e10'), 'C021':('d1','54:e3','45:e1'), 'C059':('d1','203:e1','119:e1'), 'B01':('fresh','37:e4','29:ev-3')}
ORIGINAL = "a later version of the stored piece's main statement, changed: the same speaker revises that guidance, forecast or event-progress statement, an official confirms or denies that reported claim, or the original source revises it; another statement on the same topic is not this"
ARMS = ('control','candidate')
DRAWS = 3
MAX_ATTEMPTS = 42
MAX_RESERVATION = 0.10
MAX_BATCH_SECONDS = 60
MAX_TOTAL_SECONDS = 1800


def module(name, path):
    spec=importlib.util.spec_from_file_location(name,path); obj=importlib.util.module_from_spec(spec); spec.loader.exec_module(obj); return obj
compare = module('probe_compare', ROOT/'clean-arch/step2/compare.py')
old = module('prior_reviewed_jev_sender', OLD/'diagnostic.py')


def digest(value): return hashlib.sha256(value).hexdigest()
def canonical(payload): return json.dumps(payload,sort_keys=True,ensure_ascii=False).encode('utf-8')
def read_json(path): return old.json_load(pathlib.Path(path).read_bytes())


def originals():
    """Return exact archived request bytes, verified target q, order, and immutable source hashes."""
    out={};deps={}
    for tag,path in RUNS.items():
        paths=[path/'library.json',path/'decisions.json',path/'jev.sqlite']
        for p in paths: deps[str(p)]=digest(p.read_bytes())
        lib=read_json(paths[0]);decisions={x['id']:x for x in read_json(paths[1])};records={r['id']:r for g in lib['groups'].values() for r in [g['original']]+g['members']}
        db=sqlite3.connect(f'file:{paths[2]}?mode=ro',uri=True); archived=[]
        for sha,text,answer in db.execute("select request_sha256,request_json,answer_json from model_calls where purpose='clean_step2'"):
            raw=text.encode('utf-8'); payload=old.json_load(raw)
            if digest(raw)!=sha or canonical(payload)!=raw: raise ValueError('original_bytes')
            archived.append((sha,raw,payload,old.json_load(answer)))
        db.close()
        for case,(case_tag,record_id,target_group) in CASES.items():
            if case_tag!=tag:continue
            d=decisions[record_id]; state=compare.piece_text(records[record_id],'INCOMING PIECE');groups=d['candidates'];qs={f'q{i}':compare.piece_question(compare.piece_text(lib['groups'][g]['original'],'STORED PIECE')) for i,g in enumerate(groups)}
            qid='q'+str(groups.index(target_group)); hits=[(sha,raw,payload,answer) for sha,raw,payload,answer in archived if payload['state']==state and payload['questions']==qs and answer[qid]['choice']==d['answers'][target_group]['choice'] and answer[qid]['probabilities']==d['answers'][target_group]['probabilities']]
            if len(hits)!=1:raise ValueError('archive_identity_'+case)
            sha,raw,payload,answer=hits[0]
            if old.jev.validate(answer,qs):raise ValueError('historic_answer_'+case)
            out[case]={'baseline':raw.decode('utf-8'),'sha256':sha,'target_qid':qid,'record_id':record_id,'groups':groups,'group_order':lib['order'],'historic_outcome':d['outcome']}
    if set(out)!=set(CASES):raise ValueError('case_set')
    return out,deps


def candidate_request(raw, criterion):
    payload=old.json_load(raw)
    if not isinstance(criterion,str) or not criterion.strip() or criterion==ORIGINAL:raise ValueError('criterion')
    modified=old.json_load(raw)
    for question in modified['questions'].values():
        if question.get('type')!='choice' or question.get('criteria',{}).get('supersedes')!=ORIGINAL:raise ValueError('unexpected_question')
        question['criteria']['supersedes']=criterion
    restored=old.json_load(canonical(modified))
    for question in restored['questions'].values():question['criteria']['supersedes']=ORIGINAL
    if restored!=payload or canonical(payload)!=raw:raise ValueError('changed_other_input')
    return canonical(modified)


def make_plan(candidate_path):
    """Build data in memory without credentials or network."""
    candidate_bytes=pathlib.Path(candidate_path).read_bytes(); criterion=candidate_bytes.decode('utf-8')
    if criterion.endswith('\n'):raise ValueError('candidate_trailing_newline')
    rows,inputs=originals(); jobs=[];reserve=0.0
    for case in sorted(rows):
        baseline=rows[case]['baseline'].encode();edited=candidate_request(baseline,criterion)
        rows[case]['candidate']=edited.decode();rows[case]['candidate_sha256']=digest(edited)
        for arm,body in [('control',baseline),('candidate',edited)]:
            for draw in range(DRAWS):
                amount=old.reservation('jev_'+arm,body);reserve+=amount;jobs.append([case,arm,draw,amount])
    if len(jobs)!=MAX_ATTEMPTS or reserve>MAX_RESERVATION:raise ValueError('plan_limit')
    random.Random(20261109).shuffle(jobs)
    # Pin all inputs and code. No key is read here.
    fixed=[pathlib.Path(__file__),HERE/'test_probe.py',ROOT/'clean-arch/step2/compare.py',ROOT/'src/hivemind/jev.py',ROOT/'src/hivemind/model.py',ROOT/'src/hivemind/views/jev_matching.py',OLD/'diagnostic.py',ROOT/'scripts/preflight.py',ROOT/'reports/step2-revision-census-2026-11-09/key-private.json',ROOT/'reports/step2-revision-census-2026-11-09/reader-a.json',ROOT/'reports/step2-revision-census-2026-11-09/reader-b.json',OLD/'source-blind-packet.json']
    for path in fixed:inputs[str(path)]=digest(path.read_bytes())
    plan={'candidate_sha256':digest(candidate_bytes),'candidate_file':str(pathlib.Path(candidate_path).resolve()),'cases':sorted(CASES),'draws':DRAWS,'arms':list(ARMS),'jobs':jobs,'reserved_usd':reserve,'max_reservation_usd':MAX_RESERVATION,'inputs':inputs,'rows':rows}
    return plan


def check_plan(plan):
    if make_plan(plan['candidate_file'])!=plan:raise ValueError('plan_or_input_changed')


def prepare(candidate_path, destination):
    plan=make_plan(candidate_path); dest=pathlib.Path(destination)
    if dest.exists():raise ValueError('destination_exists')
    dest.mkdir(mode=0o700,parents=False)
    write_durable(dest/'plan.json',json.dumps(plan,ensure_ascii=False,indent=2).encode())
    fsync_dir(dest);fsync_dir(dest.parent)
    return {'cases':len(plan['cases']),'attempts':len(plan['jobs']),'reserved_usd':plan['reserved_usd'],'candidate_sha256':plan['candidate_sha256'],'plan_sha256':digest((dest/'plan.json').read_bytes())}


def fsync_dir(path):
    fd=os.open(str(path),os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)


def write_durable(path,data):
    with pathlib.Path(path).open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())


def replay_result(row,answers):
    """Replay all choices and probabilities into the existing Step 2 outcome."""
    groups=row['groups'];expected={f'q{i}' for i in range(len(groups))}
    if set(answers)!=expected:raise ValueError('answers_incomplete')
    ordered={g:{'choice':answers[f'q{i}']['choice'],'probabilities':answers[f'q{i}']['probabilities']} for i,g in enumerate(groups)}
    return compare.outcome(ordered,row['group_order'])


def execute(plan, dest, secret, sender=old.send_one, state_check=old.run_state, batch_seconds=MAX_BATCH_SECONDS, hard_exit=True, preflight_text=None):
    """One bounded dispatch, with up to eight threads; a failing batch stops further batches."""
    if not isinstance(secret,str) or not secret:raise ValueError('missing_key')
    dest=pathlib.Path(dest)
    if dest.exists():raise ValueError('destination_exists')
    check_plan(plan);state_check();dest.mkdir(mode=0o700,parents=False);fsync_dir(dest.parent)
    write_durable(dest/'plan.json',json.dumps(plan,ensure_ascii=False,indent=2).encode())
    if preflight_text is not None:write_durable(dest/'preflight.log',preflight_text.encode())
    fsync_dir(dest)
    started=time.monotonic();spent=0.0
    def stamp():return {'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-started}
    with (dest/'events.jsonl').open('x',buffering=1) as log:
        for start in range(0,len(plan['jobs']),8):
            state_check();check_plan(plan)
            if time.monotonic()-started>=MAX_TOTAL_SECONDS:old.append_event(log,{'status':'incomplete','reason':'time_cap'});return False
            batch=plan['jobs'][start:start+8];amount=sum(j[3] for j in batch)
            if spent+amount>MAX_RESERVATION:old.append_event(log,{'status':'incomplete','reason':'cost_cap'});return False
            spent+=amount
            for n,(case,arm,draw,reserve) in enumerate(batch,start):
                row=plan['rows'][case];sha=row['sha256'] if arm=='control' else row['candidate_sha256']
                old.append_event(log,{'sequence':n,'case':case,'arm':arm,'draw':draw,'sha256':sha,'reserved_usd':reserve,'status':'may_have_been_sent',**stamp()})
            deadline=min(started+MAX_TOTAL_SECONDS,time.monotonic()+batch_seconds)
            pool=concurrent.futures.ThreadPoolExecutor(max_workers=8);futuremap={};submission_failure=False
            try:
                for case,arm,draw,_ in batch:
                    if time.monotonic()>=deadline:submission_failure=True;break
                    row=plan['rows'][case];body=row['baseline' if arm=='control' else 'candidate'].encode()
                    try:futuremap[pool.submit(sender,'jev_'+arm,body,secret,max(.001,deadline-time.monotonic()))]=(case,arm,draw)
                    except Exception:submission_failure=True;break
                done,pending=concurrent.futures.wait(futuremap,timeout=max(0,deadline-time.monotonic()));failed=submission_failure or len(futuremap)!=len(batch)
                for fut in done:
                    case,arm,draw=futuremap[fut]
                    try:result=fut.result()
                    except Exception:result={'status':'failed','reason':'worker_failure'}
                    if result.get('status')=='complete':
                        try:result['outcome']=replay_result(plan['rows'][case],result['result']['answers'])
                        except Exception:result={'status':'failed','reason':'outcome_replay'}
                    failed|=result.get('status')!='complete'
                    if old.has_secret(result,secret):result={'status':'failed','reason':'secret_echo'};failed=True
                    old.append_event(log,{'case':case,'arm':arm,'draw':draw,**result,**stamp()})
                if pending:
                    for fut in pending:
                        case,arm,draw=futuremap[fut];old.append_event(log,{'case':case,'arm':arm,'draw':draw,'status':'unknown','reason':'deadline',**stamp()})
                    old.append_event(log,{'status':'incomplete','reason':'deadline',**stamp()});pool.shutdown(wait=False,cancel_futures=True)
                    if hard_exit:os._exit(2)
                    return False
            except BaseException:
                # Every attempt in this batch is already durably marked as potentially sent.
                # If the journal fails, do not allow active network threads to continue unobserved.
                try:old.append_event(log,{'status':'incomplete','reason':'journal_or_worker_failure',**stamp()})
                except BaseException:pass
                pool.shutdown(wait=False,cancel_futures=True)
                if hard_exit:os._exit(2)
                raise
            pool.shutdown(wait=True)
            if failed:old.append_event(log,{'status':'incomplete','reason':'batch_failure'});return False
    events=[old.json_load(line) for line in (dest/'events.jsonl').read_bytes().splitlines()]; key=lambda x:(x['case'],x['arm'],x['draw']);wanted={(c,a,d) for c,a,d,_ in plan['jobs']};starts=[x for x in events if x.get('status')=='may_have_been_sent'];completed=[x for x in events if x.get('status')=='complete']
    if len(wanted)!=MAX_ATTEMPTS or len(starts)!=MAX_ATTEMPTS or len(completed)!=MAX_ATTEMPTS or {key(x) for x in starts}!=wanted or {key(x) for x in completed}!=wanted:raise ValueError('incomplete_events')
    write_durable(dest/'complete',json.dumps({'attempts':len(completed),'reserved_usd':spent}).encode());fsync_dir(dest);return True


def reviewed_preflight():
    """Replay frozen v108 stored data; the clean Jev archive is checked separately in originals()."""
    cmd=[sys.executable,str(ROOT/'scripts/preflight.py'),'--archive',str(ROOT/'poc/data/e2e-r9-frozen-v108-2026-11-03/d1/archive.sqlite'),'--items',str(ROOT/'poc/data/items-nvda-2026-07-01-10-27.sqlite'),'--views',str(ROOT/'poc/data/e2e-r9-frozen-v108-2026-11-03/d1/views.sqlite')]
    result=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
    baseline=(HERE/'preflight-v108-current.log').read_text()
    if result.returncode!=0 or result.stdout!=baseline:raise ValueError('preflight_mismatch')
    return result.stdout


def file_hash(path):return digest(pathlib.Path(path).read_bytes())


def validate_registration(plan_path,registration_path,registration_sha,output_path):
    """Verify an independent reviewed registration before keys are read."""
    reg_bytes=pathlib.Path(registration_path).read_bytes()
    if digest(reg_bytes)!=registration_sha:raise ValueError('registration_hash')
    reg=old.json_load(reg_bytes); expected={'format','plan_sha256','candidate_sha256','review_file','review_sha256','audit_file','audit_sha256','preflight_sha256','output_path'}
    if set(reg)!=expected or reg['format']!='jev-step2-probe-v1':raise ValueError('registration_shape')
    if reg['output_path']!=str(pathlib.Path(output_path).resolve()) or pathlib.Path(output_path).exists():raise ValueError('output_path')
    if file_hash(plan_path)!=reg['plan_sha256']:raise ValueError('plan_hash')
    plan=read_json(plan_path);check_plan(plan)
    if plan['candidate_sha256']!=reg['candidate_sha256']:raise ValueError('candidate_hash')
    for kind in ('review','audit'):
        path=pathlib.Path(reg[kind+'_file']); raw=path.read_bytes()
        if digest(raw)!=reg[kind+'_sha256']:raise ValueError(kind+'_hash')
        lines=raw.decode('utf-8').splitlines()
        if not lines or lines[0].strip()!='READY TO SEND' or 'plan-sha256: '+reg['plan_sha256'] not in lines or 'candidate-sha256: '+reg['candidate_sha256'] not in lines:raise ValueError(kind+'_registration')
    if file_hash(HERE/'preflight-v108-current.log')!=reg['preflight_sha256']:raise ValueError('preflight_hash')
    return plan,reg


def launch(plan_path,registration_path,registration_sha,output_path, *, key_reader=None, sender=old.send_one, state_check=old.run_state, preflight_fn=reviewed_preflight, lock_path=HERE/'experiment.lock', hard_exit=True):
    """Enforce exclusive scope, reviewed exact inputs, replay and only then read credential."""
    fd=os.open(str(lock_path),os.O_CREAT|os.O_RDWR,0o600)
    try:
        try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise ValueError('experiment_locked')
        state_check();plan,reg=validate_registration(plan_path,registration_path,registration_sha,output_path)
        preflight_text=preflight_fn()
        if digest(preflight_text.encode())!=reg['preflight_sha256']:raise ValueError('preflight_changed')
        state_check();plan2,reg2=validate_registration(plan_path,registration_path,registration_sha,output_path)
        if plan2!=plan or reg2!=reg:raise ValueError('registration_changed')
        secret=(key_reader or old.jev._key)()
        return execute(plan,output_path,secret,sender,state_check,hard_exit=hard_exit,preflight_text=preflight_text)
    finally:
        fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)


def main():
    args=sys.argv[1:]
    if len(args)==3 and args[0]=='--prepare':
        print(json.dumps(prepare(args[1],args[2]),indent=2));return
    if len(args)==5 and args[0]=='--send':
        success=launch(args[1],args[2],args[3],args[4]);raise SystemExit(0 if success else 2)
    raise SystemExit('usage: probe.py --prepare CANDIDATE_TEXT NEW_PLAN_DIR | --send PLAN_JSON REGISTRATION_JSON REGISTRATION_SHA256 NEW_OUTPUT_DIR')
if __name__=='__main__':main()
