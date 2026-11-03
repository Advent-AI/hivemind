"""Complete the current-code recorded-response fixture; not a latency benchmark."""
from pathlib import Path
import json,sqlite3,sys,time
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'poc'))
from hivemind import config,model,replay,universe
from concurrency_study.budget import GuardedTransport,single_attempt_http
from concurrency_study.ingestion import StudyTransport
HERE=Path(__file__).resolve().parent
old=ROOT/'poc/reports/2026-10-25-ingestion-v11/budget.sqlite'
with sqlite3.connect(old.as_uri()+'?mode=ro',uri=True) as db:
    cap,max_calls=db.execute('select cap,max_calls from settings').fetchone()
    used,held=db.execute('select count(*),sum(coalesce(charged,reserved)) from attempts').fetchone()
remaining=cap-held
assert remaining==933938 and max_calls-used==120
assert not (HERE/'budget.sqlite').exists()
(HERE/'allocation.json').write_text(json.dumps({'original_cap_microdollars':cap,'prior_held_microdollars':held,'remaining_cap_microdollars':remaining,'max_calls':max_calls-used,'note':'Prior unknown reservation retained; this allocation cannot increase the original total cap.'},indent=2))
prepare=single_attempt_http()
count=0
def traced(provider,request):
    send=prepare(provider,request)
    def run():
        global count
        count+=1
        print(json.dumps({'physical_call':count,'provider':provider,'model':request['model']}),flush=True)
        return send()
    return run
transport=StudyTransport(GuardedTransport(HERE/'budget.sqlite',traced,cap_microdollars=remaining,max_calls=max_calls-used),workers=1)
archive=model.Archive(HERE/'archive.sqlite')
started=time.perf_counter()
try:
    result=replay.run(testdb_path=str(HERE/'items.sqlite'),views_path=str(HERE/'views.sqlite'),archive=archive,cfg=config.load(ROOT/'poc/config/poc-v23.json'),universe=universe.load(ROOT/'poc/universe.json'),from_day='2026-07-27',until_day='2026-07-27',transport=transport)
    (HERE/'result.json').write_text(json.dumps({'result':result,'elapsed_seconds':time.perf_counter()-started,'budget':transport.guard.summary(),'purpose':'Fixture completion; not a fresh full latency baseline.'},indent=2))
finally:
    archive.conn.close()
