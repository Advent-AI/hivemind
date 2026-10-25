"""D162 positive controls: lost source content and silent omission must fail the relevant assertions."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[3];out=Path(__file__).resolve().parent
path=root/'poc/hierarchy_study/source_first.py';original=path.read_text()
variants={
 'changed_quote':original.replace("evidence.append(dict(copy.deepcopy(observation), links=copy.deepcopy(decision['links'])))", "evidence.append(dict(copy.deepcopy(observation), quote='fabricated quotation', links=copy.deepcopy(decision['links'])))"),
 'silent_omission':original.replace("errors = model.check_schema(organised, organisation_schema(observations, offered))", "errors = []").replace("for observation in observations:","for observation in (e for e in observations if e['id'] in organised['dispositions']):")}
selectors={'changed_quote':'every_stored_answer', 'silent_omission':'disposition_refuses and missing'}
launcher='''import sys,types,pytest
module=types.ModuleType('source_first');module.__file__=sys.argv[1];sys.modules['source_first']=module
exec(compile(sys.stdin.read(),module.__file__,'exec'),module.__dict__)
raise SystemExit(pytest.main(['-q',sys.argv[2],'-k',sys.argv[3]]))
'''
for name,code in variants.items():
 assert code!=original
 p=subprocess.run([sys.executable,'-c',launcher,str(path),str(root/'poc/hierarchy_study/test_source_first.py'),selectors[name]],input=code,text=True,capture_output=True)
 (out/f'mutant-{name}.txt').write_text(p.stdout+p.stderr)
 assert p.returncode==1 and ('AssertionError' in p.stdout if name=='changed_quote' else 'DID NOT RAISE' in p.stdout),p.stdout
 print(name,'caught')
