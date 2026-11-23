"""Fake-only tests of original identity, request isolation, all-answer replay and fail-stop."""
import json
import fcntl
import http.server
import hashlib
import os
import subprocess
import sys
import threading
from unittest import mock
import pathlib
import sqlite3
import tempfile
import unittest
import probe
SECRET='FAKE_KEY_ONLY_FOR_TEST_298451'
class ProbeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.root=pathlib.Path(cls.temp.name)
        cls.candidate=cls.root/'candidate.txt';cls.candidate.write_text(probe.ORIGINAL+' Test-only instruction.',encoding='utf-8');cls.plan=probe.make_plan(cls.candidate)
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def fake_response(self,arm,body,secret,timeout):
        request=json.loads(body);answer={'type':'choice','choice':'different','confidence':.8,'probabilities':{'different':.8,'same_statement':.1,'supersedes':.1}}
        full={'model':'jev-1.14.0','answers':{q:answer.copy() for q in request['questions']},'usage':{'input_tokens':100,'output_tokens':0}}
        return {'status':'complete','result':probe.old.validate(body,arm,full)}
    def test_original_identity_candidate_only_and_preserved_historical_outcome(self):
        self.assertEqual(len(self.plan['rows']),7);self.assertEqual(len(self.plan['jobs']),42)
        for case,row in self.plan['rows'].items():
            base=json.loads(row['baseline']);new=json.loads(row['candidate']);self.assertEqual(base['state'],new['state']);self.assertEqual(set(base['questions']),set(new['questions']))
            for q in base['questions']:
                self.assertEqual(new['questions'][q]['criteria']['supersedes'],self.candidate.read_text())
                new['questions'][q]['criteria']['supersedes']=probe.ORIGINAL
            self.assertEqual(base,new);self.assertEqual(probe.digest(row['baseline'].encode()),row['sha256'])
            tag,_,_=probe.CASES[case];db=sqlite3.connect(f'file:{probe.RUNS[tag]}/jev.sqlite?mode=ro',uri=True)
            answer=json.loads(db.execute('select answer_json from model_calls where request_sha256=?',(row['sha256'],)).fetchone()[0]);db.close()
            self.assertEqual(probe.replay_result(row,answer),row['historic_outcome'],case)
    def test_valid_saved_jev_envelope_and_mutated_answer_rejected(self):
        row=self.plan['rows']['C036'];db=sqlite3.connect(f'file:{probe.RUNS["d1"]}/jev.sqlite?mode=ro',uri=True)
        response=json.loads(db.execute('select response_json from model_calls where request_sha256=?',(row['sha256'],)).fetchone()[0]);db.close()
        clean=probe.old.validate(row['baseline'].encode(),'jev_control',response);self.assertEqual(clean['answers']['q9']['choice'],'supersedes')
        response['answers'].pop('q9')
        with self.assertRaises(probe.old.Refuse):probe.old.validate(row['baseline'].encode(),'jev_control',response)
    def test_valid_fake_dispatches_exactly_42_and_replays_every_answer(self):
        calls=[]
        def send(*args):calls.append(args[0]);return self.fake_response(*args)
        dest=self.root/'success';self.assertTrue(probe.execute(self.plan,dest,SECRET,send,lambda:None))
        events=[json.loads(x) for x in (dest/'events.jsonl').read_text().splitlines()];self.assertEqual(len(calls),42);self.assertEqual(sum(x.get('status')=='complete' for x in events),42);self.assertEqual(json.loads((dest/'complete').read_text())['attempts'],42)
        self.assertTrue(all(e['outcome']['kind']=='new' for e in events if e.get('status')=='complete'));self.assertNotIn(SECRET,(dest/'events.jsonl').read_text())
        with self.assertRaises(ValueError):probe.execute(self.plan,dest,SECRET,send,lambda:None)
    def test_failed_or_secret_response_stops_after_first_batch(self):
        for name,mode in [('failure','fail'),('echo','echo')]:
            calls=[]
            def send(*args):
                calls.append(args[0])
                if len(calls)==1:
                    if mode=='fail':return {'status':'failed','reason':'injected'}
                    response=self.fake_response(*args);response['result']['usage']['injected']=SECRET;return response
                return self.fake_response(*args)
            dest=self.root/name;self.assertFalse(probe.execute(self.plan,dest,SECRET,send,lambda:None));self.assertLessEqual(len(calls),8);self.assertFalse((dest/'complete').exists());self.assertNotIn(SECRET,(dest/'events.jsonl').read_text())
            events=[json.loads(x) for x in (dest/'events.jsonl').read_text().splitlines()];self.assertEqual(events[-1]['status'],'incomplete')
    def test_candidate_hash_change_refuses_dispatch(self):
        path=self.root/'mutable.txt';path.write_text(probe.ORIGINAL+' Temporary change.');plan=probe.make_plan(path);path.write_text(probe.ORIGINAL+' Another change.')
        with self.assertRaises(ValueError):probe.execute(plan,self.root/'changed',SECRET,self.fake_response,lambda:None)
        self.assertFalse((self.root/'changed').exists())
    def registration(self,name):
        directory=self.root/(name+'-plan');probe.prepare(self.candidate,directory);plan_path=directory/'plan.json';plan=json.loads(plan_path.read_text());ph=probe.file_hash(plan_path);ch=plan['candidate_sha256']
        review=self.root/(name+'-review');audit=self.root/(name+'-audit')
        for p in (review,audit):p.write_text('READY TO SEND\nplan-sha256: '+ph+'\ncandidate-sha256: '+ch+'\n')
        dest=(self.root/(name+'-output')).resolve();reg={'format':'jev-step2-probe-v1','plan_sha256':ph,'candidate_sha256':ch,'review_file':str(review),'review_sha256':probe.file_hash(review),'audit_file':str(audit),'audit_sha256':probe.file_hash(audit),'preflight_sha256':probe.file_hash(probe.HERE/'preflight-v108-current.log'),'output_path':str(dest)}
        path=self.root/(name+'-registration.json');path.write_text(json.dumps(reg));return plan_path,path,probe.file_hash(path),dest
    def test_locked_process_refuses_before_credentials(self):
        args=self.registration('locked');lock=self.root/'lock-test';fd=os.open(str(lock),os.O_CREAT|os.O_RDWR,0o600);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);reads=[]
        try:
            with self.assertRaisesRegex(ValueError,'experiment_locked'):probe.launch(*args,key_reader=lambda:reads.append(1),sender=self.fake_response,state_check=lambda:None,preflight_fn=lambda:(probe.HERE/'preflight-v108-current.log').read_text(),lock_path=lock,hard_exit=False)
            self.assertEqual(reads,[]);self.assertFalse(args[3].exists())
        finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
    def test_changed_registration_review_and_preflight_refuse_before_credentials(self):
        for mode in ('reg','review','preflight'):
            args=self.registration('changed-'+mode);reads=[];reg=json.loads(args[1].read_text());pre=lambda:(probe.HERE/'preflight-v108-current.log').read_text()
            if mode=='reg':args[1].write_text(args[1].read_text()+' ')
            if mode=='review':pathlib.Path(reg['review_file']).write_text('tampered')
            if mode=='preflight':pre=lambda:'different preflight'
            with self.assertRaises(ValueError):probe.launch(*args,key_reader=lambda:reads.append(1),sender=self.fake_response,state_check=lambda:None,preflight_fn=pre,lock_path=self.root/('lock-'+mode),hard_exit=False)
            self.assertEqual(reads,[]);self.assertFalse(args[3].exists())
    def test_journal_failure_with_inflight_workers_stops_after_first_batch(self):
        gate=threading.Event();calls=[];orig=probe.old.append_event
        def sender(*args):calls.append(1);gate.wait(2);return self.fake_response(*args)
        def journal(handle,event):
            if event.get('status')=='unknown':raise OSError('simulated disk failure')
            return orig(handle,event)
        dest=self.root/'journal-failure'
        try:
            with mock.patch.object(probe.old,'append_event',side_effect=journal):
                with self.assertRaises(OSError):probe.execute(self.plan,dest,SECRET,sender,lambda:None,batch_seconds=.05,hard_exit=False)
        finally:gate.set()
        self.assertLessEqual(len(calls),8);self.assertFalse((dest/'complete').exists())
        events=[json.loads(x) for x in (dest/'events.jsonl').read_text().splitlines()];self.assertEqual(sum(x.get('status')=='may_have_been_sent' for x in events),8)
        self.assertEqual(events[-1]['status'],'incomplete')
    def test_inflight_journal_failure_hard_stops_real_entry(self):
        gate=threading.Event();calls=[];orig=probe.old.append_event; caught=None
        def sender(*args):calls.append(1);gate.wait(2);return self.fake_response(*args)
        def journal(handle,event):
            if event.get('status')=='unknown':raise OSError('simulated disk failure')
            return orig(handle,event)
        dest=self.root/'journal-hard-failure'
        try:
            with mock.patch.object(probe.old,'append_event',side_effect=journal), mock.patch.object(probe.os,'_exit',side_effect=SystemExit(2)) as stop:
                try:probe.execute(self.plan,dest,SECRET,sender,lambda:None,batch_seconds=.05,hard_exit=True)
                except BaseException as error:caught=error
                self.assertIsInstance(caught,SystemExit);self.assertEqual(caught.code,2);stop.assert_called_once_with(2)
        finally:gate.set()
        self.assertLessEqual(len(calls),8);self.assertFalse((dest/'complete').exists())
    def test_interrupted_submission_hard_stops_without_untracked_threads(self):
        gate=threading.Event();submitted=[]; original=probe.concurrent.futures.ThreadPoolExecutor.submit; caught=None
        def sender(*args):gate.wait(2);return self.fake_response(*args)
        def submit(pool,*args,**kwargs):
            submitted.append(1)
            if len(submitted)==2:raise KeyboardInterrupt()
            return original(pool,*args,**kwargs)
        dest=self.root/'submission-interrupt'
        try:
            with mock.patch.object(probe.concurrent.futures.ThreadPoolExecutor,'submit',autospec=True,side_effect=submit), mock.patch.object(probe.os,'_exit',side_effect=SystemExit(2)) as stop:
                try:probe.execute(self.plan,dest,SECRET,sender,lambda:None,hard_exit=True)
                except BaseException as error:caught=error
                self.assertIsInstance(caught,SystemExit);self.assertEqual(caught.code,2);stop.assert_called_once_with(2)
        finally:gate.set()
        self.assertEqual(len(submitted),2);self.assertFalse((dest/'complete').exists())
        events=[json.loads(x) for x in (dest/'events.jsonl').read_text().splitlines()];self.assertEqual(sum(x.get('status')=='may_have_been_sent' for x in events),8)
        self.assertEqual(events[-1]['status'],'incomplete')
    def test_registered_send_cli_fake_transport(self):
        args=self.registration('cli'); script="""
import json,sys,probe
original=probe.launch
lock=sys.argv[5]
def sender(arm,body,secret,timeout):
 request=json.loads(body); answer={'type':'choice','choice':'different','confidence':.8,'probabilities':{'different':.8,'same_statement':.1,'supersedes':.1}}
 obj={'model':'jev-1.14.0','answers':{q:answer.copy() for q in request['questions']},'usage':{'input_tokens':100,'output_tokens':0}}
 return {'status':'complete','result':probe.old.validate(body,arm,obj)}
def injected(*args):
 return original(*args,key_reader=lambda:'FAKE_KEY_ONLY_FOR_TEST_298451',sender=sender,state_check=lambda:None,preflight_fn=lambda:(probe.HERE/'preflight-v108-current.log').read_text(),lock_path=lock,hard_exit=False)
probe.launch=injected
sys.argv=['probe.py','--send']+sys.argv[1:5]
probe.main()
"""
        result=subprocess.run([sys.executable,'-c',script,*map(str,args),str(self.root/'cli-lock')],cwd=probe.HERE,capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(json.loads((args[3]/'complete').read_text())['attempts'],42)
        self.assertNotIn(SECRET,(args[3]/'events.jsonl').read_text())
    def test_registered_cli_real_sender_local_http_exact_bodies(self):
        args=self.registration('local-http');seen=[];errors=[];guard=threading.Lock()
        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                try:
                    body=self.rfile.read(int(self.headers['Content-Length'])); request=json.loads(body)
                    with guard:seen.append(hashlib.sha256(body).hexdigest())
                    if self.headers.get('Authorization')!='Bearer '+SECRET:raise ValueError('not fake key')
                    answer={'type':'choice','choice':'different','confidence':.8,'probabilities':{'different':.8,'same_statement':.1,'supersedes':.1}}
                    response={'model':'jev-1.14.0','answers':{q:answer.copy() for q in request['questions']},'usage':{'input_tokens':100,'output_tokens':0}}
                    raw=json.dumps(response).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
                except Exception as error:
                    with guard:errors.append(type(error).__name__)
                    self.send_response(500);self.end_headers()
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        script="""
import sys,probe
original=probe.launch;lock=sys.argv[5];endpoint=sys.argv[6]
probe.old.jev.ENDPOINT=endpoint
def injected(*args):
 return original(*args,key_reader=lambda:'FAKE_KEY_ONLY_FOR_TEST_298451',state_check=lambda:None,lock_path=lock,hard_exit=False)
probe.launch=injected
sys.argv=['probe.py','--send']+sys.argv[1:5]
probe.main()
"""
        try:
            result=subprocess.run([sys.executable,'-c',script,*map(str,args),str(self.root/'http-lock'),f'http://127.0.0.1:{server.server_port}/jev'],cwd=probe.HERE,capture_output=True,text=True,timeout=30)
        finally:server.shutdown();server.server_close();thread.join()
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(errors,[]);self.assertEqual(len(seen),42)
        plan=json.loads(args[0].read_text());expected=[]
        for case,arm,draw,reserved in plan['jobs']:
            row=plan['rows'][case];expected.append(row['sha256'] if arm=='control' else row['candidate_sha256'])
        self.assertCountEqual(seen,expected);self.assertNotIn(SECRET,(args[3]/'events.jsonl').read_text())
if __name__=='__main__':unittest.main()
