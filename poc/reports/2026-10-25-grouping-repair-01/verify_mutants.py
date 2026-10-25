from pathlib import Path
import json,shutil,subprocess,tempfile
root=Path(__file__).resolve().parents[3];out=Path(tempfile.mkdtemp(prefix='hivemind-mutation-results-'))
mutations=[
 ('period','src/hivemind/universe.py',"re.fullmatch(r'(?:FY\\s*)?(\\d{4})(?:年|财年)?', (year or '').strip(), re.I)","re.search(r'(\\d{4})', year or '')",'test_identity_repair.py::test_stored_multiyear_and_ambiguous_scope_survive_unchanged'),
 ('alias','src/hivemind/universe.py',"scope_key(entry['scope']) == scope_key(scope)","(scope_key(entry['scope']) == scope_key(scope) or any(scope_key(a) in scope_key(scope) for a in entry.get('aliases', [])))",'test_identity_repair.py::test_stored_multiyear_and_ambiguous_scope_survive_unchanged'),
 ('qualifier','src/hivemind/universe.py',"if measure in self.SCOPELESS and plain.casefold() in redundant:","if measure in self.SCOPELESS:",'test_identity_repair.py::test_restored_candidates_keep_department_and_cash_qualifiers'),
 ('event','src/hivemind/views/identity.py',"value.get('period_start'), value.get('period_end'), value.get('basis'), value.get('unit'), value.get('event_type'))", "value.get('period_start'), value.get('period_end'), value.get('basis'), value.get('unit'), None)",'test_identity_repair.py::test_event_type_distinguishes_search_identity_and_merge'),
 ('batch','src/hivemind/views/identity.py',"first = first_by_key.setdefault(key, cid) if key is not None else cid", "first = cid",'test_identity_repair.py::test_same_answer_coalesces_without_losing_evidence'),
 ('dependency','src/hivemind/views/matching.py',"refusals.extend(coalescing_errors)","pass",'test_identity_repair.py::test_coalesced_dependency_is_refused_before_matching_retry_ends'),
 ('legacy','src/hivemind/views/identity.py',"value.get('key_version') != KEY_VERSION or ","",'test_identity_repair.py::test_unknown_basis_and_legacy_key_never_authorize_automatic_merge'),
 ('rollback','src/hivemind/views/writing.py',"conn.execute('rollback to view_write')", "pass",'test_identity_repair.py::test_conflict_rolls_back_entire_write_and_free_scope_remains_free'),
 ('failed_day','src/hivemind/replay.py',"raise RuntimeError(f'item failed; day {day} remains resumable: {result.failed}')", "pass",'test_identity_repair.py::test_failed_replay_day_is_not_completed_and_can_resume'),
 ('reference','src/hivemind/extraction.py',"scope, source = universe.scope_and_source(object_id, c['measure'], c.get('scope', ''), c.get('event_type', 'n/a'))", "if c['measure'] == 'other':\n                    continue\n                scope, source = universe.scope_and_source(object_id, c['measure'], c.get('scope', ''), c.get('event_type', 'n/a'))",'test_keyed_views.py::test_reference_list_does_not_veto_model_candidates'),
]
results=[]
for name,file,old,new,test in mutations:
 with tempfile.TemporaryDirectory(prefix='hivemind-mutant-') as temp:
  work=Path(temp)
  shutil.copytree(root/'src',work/'src',ignore=shutil.ignore_patterns('__pycache__'))
  shutil.copytree(root/'tests',work/'tests',ignore=shutil.ignore_patterns('__pycache__'))
  shutil.copytree(root/'poc/config',work/'poc/config')
  shutil.copy2(root/'poc/universe.json',work/'poc/universe.json')
  p=work/file;s=p.read_text();assert s.count(old)==1,(name,s.count(old));p.write_text(s.replace(old,new))
  run=subprocess.run(['python3','-m','pytest','-q',str(work/'tests'/test)],cwd=work,capture_output=True,text=True)
  text=run.stdout+run.stderr;(out/f'mutant-{name}.txt').write_text(text)
  caught=run.returncode==1 and ('AssertionError' in text or 'DID NOT RAISE' in text or (name == 'batch' and 'WriteConflict: candidate c2: existing exact identity requires matching' in text)) and 'ERROR collecting' not in text
  results.append({'mutation':name,'test':test,'exit_code':run.returncode,'caught':caught})
  print(name,caught,flush=True)
(out/'mutation-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(out)
assert all(r['caught'] for r in results)
