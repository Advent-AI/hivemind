"""Seven-day split extraction diagnostic on an isolated historical ledger.

Start with `preview OUT`, then `run OUT SHA256`. A/B and metadata are experimental;
the matcher and writer are the actual library path. A failed item stops the run.
"""
import calendar,copy,datetime,difflib,fcntl,hashlib,json,os,re,shutil,sqlite3,sys,traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];REF=ROOT/'docs/research/2026-11-05-parallel-refinement'
sys.path[:0]=[str(HERE),str(REF),str(ROOT/'src')]
import existing_path as prior
import simple_new_question_poc as simple
import run_structure_v2
from hivemind import config,dispatch,extraction,model,pull,research_context,testdb,universe
from hivemind.views import identity,matching,round as rounds,store

INPUT=ROOT/'poc/data/parallel-thesis-evidence-input-2026-11-05/items.sqlite'
DAYS=['2026-08-29','2026-08-30','2026-08-31','2026-09-01','2026-09-02','2026-09-03','2026-09-04']
CENSUS=HERE/'seven-day-source-census-2026-11-05.json'
REUSE=ROOT/'poc/data/split-seven-day-optional-2026-11-05-v3'
CONFIG=ROOT/'poc/config/poc-split-v2.json'

def digest(b):return hashlib.sha256(b).hexdigest()
def encode(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(p,x):
 temporary=p.with_name(p.name+'.tmp')
 temporary.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
 os.replace(temporary,p)
def read(p):return json.loads(p.read_text())

def item_requests(cfg,uni,item,shown):
 setting,_,old,schema=extraction.request_for(cfg,item,item['text'],shown,uni)
 old_head=f'[Open questions at the start of {item["publication_day"]}]'
 head='[Open questions immediately before this item]'
 if old.count(old_head)!=1:raise ValueError('open question block absent')
 subject=old[old.index('[Subjects]'):old.index('[What to read out]')]
 subject=subject.replace('; use that day as the due date.','.')
 subject=subject.replace('Fiscal-year note (a numeric thesis takes its year and due date from it):','Fiscal-year context for the company\'s own quantities:')
 category=old[:old.index('[Subjects]')]
 questions=old[old.index(old_head):old.index('[Research groups]')].replace(old_head,head,1)
 article=f"[Article] id {item['input_id']}; date {item['publication_day']}; title {item['title']}; publisher {item['publisher']}\n{item['text'][:extraction.MAX_TEXT_CHARS]}"
 check_start=old.index(CHECK_HEAD)
 if not old.endswith(CHECK_END):raise ValueError('closing check end absent')
 closing=old[check_start:-len(CHECK_END)]+'Return only the evidence passages you keep; a question left with none is not proposed.'
 a_user=category+subject+questions+article+'\n\n[Closing check for every evidence passage]\n'+closing
 a_system=(REF/A_PROMPT).read_text()
 b_user=old.replace(old_head,head,1).replace(extraction.GROUPS_INSTRUCTION,'[Research groups] Use the supplied question descriptions to understand their scope.',1)
 start=b_user.find('[Research reference]');end=b_user.find(head)
 if start!=-1:b_user=b_user[:start]+b_user[end:]
 b_user=b_user.replace('For a candidate thesis about a company, object is its ticker; about a theme, choose an id from this list, or state what the matter is when none fits:','Theme identifiers:',1)
 b_user=b_user.replace(extraction.CLOSING,'Return only evidence per the schema. Each evidence link must be an ID of a supplied existing question.',1)
 a='- a share-price move, an investor\'s position or trade, or the market value';b='- a share-price move or an investor\'s position or trade'
 if b_user.count(a)!=1:raise ValueError('B review anchor missing')
 b_user=b_user.replace(a,b,1).replace('it does not cover the news behind the move;','it does not cover the news behind the move; the covered company\'s market value, a standalone valuation multiple, and its share-price reaction after earnings are optional;',1)
 b_user=b_user.replace('Before you return the answer, check it once.','Before you return the answer, check it once. A clearly retold past actual figure may be kept or omitted; still-effective guidance and forecasts retain their usual weight. For a company statement retold by a news author, the article publication day is not the original statement day unless the article says so; otherwise leave original_day empty.',1)
 b_user,_=run_structure_v2.basis_labels(b_user,shown)
 b_system=(REF/'structure-v2-existing-evidence.txt').read_text()
 b_schema={'type':'object','additionalProperties':False,'properties':{'evidence':copy.deepcopy(schema['properties']['evidence'])},'required':['evidence']}
 b_schema['properties']['evidence']['items']['properties']['links']['description']=prior.b_arm.NEW
 shown_ids=list(dict.fromkeys(v['view_id'] for v in shown))
 if shown_ids:b_schema['properties']['evidence']['items']['properties']['links']['items']['pattern']='^(?:'+'|'.join(re.escape(v) for v in shown_ids)+')$'
 a_schema=a_question_schema(shown_ids)
 return setting,{'a':(a_system,a_user,a_schema,'new_question'),'b':(b_system,b_user,b_schema,'extraction')}

CHECK_HEAD='Before you return the answer, check it once.'
CHECK_END='Return only the evidence items you keep.'
A_PROMPT='split-a-v2-prompt.txt'
# A field description on the quote ("copied character for character") made the model copy article text into the question, why and check
# fields in 4 of 6 sends (poc/data/a-v2-variants-2026-11-05); quote fidelity is held by code (source_quote) instead.

def a_question_schema(shown_ids):
 """The new-question answer: each question names its closest existing question and the result that separates them (D248's test),
 and brings at least one evidence passage."""
 schema=simple.schema();q=schema['properties']['questions']['items']
 props=q['properties'];props.pop('why_not_already_covered')
 props['closest_existing_question']={'type':'string','enum':['none']+list(shown_ids),
  'description':'The id of the existing question whose outcome is closest to this one, or none when no existing question concerns the same subject and matter.'}
 props['what_separates_it']={'type':'string','description':'A result that would settle this question while the closest existing question\'s answer stays unchanged, and why an analyst would bet on each separately. Another estimate, source, wording, scope name, direction, population or proxy of the same quantity, or a later deadline for the same event, does not separate them: then propose nothing.'}
 props['evidence']['minItems']=1
 order=['question','why_it_matters','closest_existing_question','what_separates_it','how_and_when_to_check','evidence']
 q['properties']={k:props[k] for k in order};q['required']=order
 return schema

SHARED_MEASURES=['spend_total','capacity','market_size']

def meta_schema(candidate_count=None,evidence_count=None,subject_ids=None):
 def obj(props):return {'type':'object','additionalProperties':False,'properties':props,'required':list(props)}
 s={'type':'string'}
 rung=obj({'label':s,'condition':s,'lo':{'anyOf':[{'type':'number'},{'type':'null'}]},'hi':{'anyOf':[{'type':'number'},{'type':'null'}]}})
 if subject_ids is None:
  candidate={'object':s,'kind':{'type':'string','enum':['asset','theme']},'year':s,'due_day':s,'date_basis':{'type':'string','enum':['source_stated','analyst_check','unknown']},'date_provenance':s,'rungs':{'type':'array','items':rung}}
 else:
  candidate={'object':{'type':'string','enum':list(subject_ids)+['new']},'new_subject':s,'new_subject_kind':{'type':'string','enum':['company','theme','none']},
             'shared_measure':{'type':'string','enum':['none']+SHARED_MEASURES},'unit':{'type':'string','enum':list(extraction.UNITS)},
             'year':s,'due_day':s,'date_basis':{'type':'string','enum':['source_stated','analyst_check','unknown']},'date_provenance':s,'rungs':{'type':'array','items':rung}}
 evidence={'speaker':s,'original_who':s,'original_day':s,'tier':{'type':'string','enum':['fact','party_statement','third_party_view','rumour','unknown']},'event_time':s}
 if candidate_count is None and evidence_count is None:
  return obj({'candidates':{'type':'array','items':obj(dict(id=s,**candidate))},'evidence':{'type':'array','items':obj(dict(id=s,**evidence))}})
 if candidate_count is None or evidence_count is None or candidate_count<1 or evidence_count<1:raise ValueError('metadata requires candidates and evidence')
 out=obj({'candidates':obj({'c'+str(i):{'$ref':'#/$defs/candidate'} for i in range(1,candidate_count+1)}),
          'evidence':obj({'e'+str(i):{'$ref':'#/$defs/evidence'} for i in range(1,evidence_count+1)})})
 out['$defs']={'candidate':obj(candidate),'evidence':obj(evidence)}
 return out

LEGACY_META_SYSTEM=('For the A answer, identify subject, attribution and optional details supported by the source or A answer. Describe every supplied ID; do not judge relevance or omit evidence. '
         'object is the subject ticker or known research theme if the question is about that subject; kind is asset or theme. '
         'year is the question period when stated, otherwise empty. due_day is an exact ISO day only when a specific date is stated in the source or A’s explicit check description; otherwise empty. '
         'date_basis says source_stated, analyst_check, or unknown; date_provenance copies the exact words supporting the date, or is empty. Do not turn an approximate month into an invented day. '
         'rungs are optional: return an empty array when useful mutually exclusive outcomes are not clear. For a directly yes/no question, two named yes/no outcomes are allowed. '
         'For a numerical question use five intervals only when a meaningful reference and boundaries are supported; never invent an article claim. '
         'Distinguish the article author from the original speaker; when it is the author’s own opinion, identify the author as the original speaker. For a fact report use fact, for a company forecast or explanation party_statement, '
         'for author analysis third_party_view, for an unconfirmed claim rumour; use unknown if attribution cannot be established. original_day is the ISO day when the original party said it, '
         'or empty when unknown. Do not invent dates or speakers. No dates, ladders or missing details are required to open a question.')
# The subject is chosen from the listed ids (code owns identity); the ladder and bounds sentences are the production role prompt's
# (role-v74i, "How to write a candidate thesis" and "Identity fields and numeric bounds"); the shared-quantity fields let code apply D197.
META_SYSTEM=('For the A answer, identify subject, attribution and optional details supported by the source or A answer. Describe every supplied ID; do not judge relevance or omit evidence. '
         'object is the id from [Subjects] whose own result the question asks about: a company\'s ticker when it asks about that company\'s revenue, profit, share, product progress or obligation, even when policy or macroeconomics drives it; '
         'a theme id when it asks what happens in the world, such as licensing, interest rates or aggregate spending. Use new only when no listed subject fits; then name the company or the matter (not the question) in new_subject and give new_subject_kind; otherwise new_subject is empty and new_subject_kind is none. '
         'shared_measure: for a question about one quantity shared by many companies and summed over a calendar year (the combined spending of named companies, total capacity added, a market\'s size), the kind of quantity; none otherwise, including prices, rates and growth rates. unit is the unit of the question\'s figure; n/a for an event. '
         'year is the question period when stated, otherwise empty. due_day is an exact ISO day only when a specific date is stated in the source or A’s explicit check description; otherwise empty. '
         'date_basis says source_stated, analyst_check, or unknown; date_provenance copies the exact words supporting the date, or is empty. Do not turn an approximate month into an invented day. '
         'rungs: use five rungs; only a yes/no question about an event has two. A five-rung ladder on a company\'s own result runs from Strongly bullish through Bullish, Neutral and Bearish to Strongly bearish, meaning good or bad for the business. '
         'A theme ladder runs between two ends of an outcome range; label the outcomes, without assigning business sentiment. Conditions must not overlap or leave gaps: exactly one must hold when resolved. '
         'State the neutral comparison in its condition: the reference the source or evidence gives, such as guidance, a consensus or analyst estimate, the last reported figure or a stated target; when it gives only a quarter\'s or part of the year\'s figure, the full-year pace that figure implies is the reference, and the condition says so. The ranges around the reference are your analyst\'s choice. '
         'Each numeric rung has an inclusive lower bound lo and exclusive upper bound hi, in the stated unit. Money amounts are written in full (12000000000, not 12 billion); percentages use 73, not 0.73. The lowest numeric range has lo null, the highest hi null. Both bounds are null for yes/no outcomes. '
         'Return an empty rungs array only when a numerical question has no reference in the source or evidence; never invent a reference figure. '
         'Distinguish the article author from the original speaker; when it is the author’s own opinion, identify the author as the original speaker. For a fact report use fact, for a company forecast or explanation party_statement, '
         'for author analysis third_party_view, for an unconfirmed claim rumour; use unknown if attribution cannot be established. original_day is the ISO day when the original party said it, '
         'or empty when unknown. Do not invent dates or speakers. No dates or missing details are required to open a question.')

def subject_list(uni):
 """Every subject a question can be filed under: covered companies, themes and research subjects written earlier in this run."""
 rows=[(k,v['name'],'company') for k,v in uni.companies.items()]+[(k,v['name'],'theme') for k,v in uni.themes.items()]
 return rows

def metadata_request(item,answer,uni=None):
 positions=[];idx=0
 for ci,q in enumerate(answer['questions'],1):
  for e in q['evidence']:
   idx+=1;positions.append({'id':'e'+str(idx),'original_speaker':e['original_speaker'],'quote':e['quote'],'summary':e['what_it_shows']})
 questions=json.dumps([{'id':'c'+str(i),'question':q['question'],'why_it_matters':q['why_it_matters'],'how_and_when_to_check':q['how_and_when_to_check']} for i,q in enumerate(answer['questions'],1)],ensure_ascii=False)
 body='[Article]\n'+item['text'][:extraction.MAX_TEXT_CHARS]+'\n\n[Questions]\n'+questions+'\n\n[Evidence]\n'+json.dumps(positions,ensure_ascii=False)
 if uni is None:
  return LEGACY_META_SYSTEM,body,meta_schema(len(answer['questions']),len(positions)),'record_preparation'
 subjects=subject_list(uni)
 head='[Subjects]\n'+'\n'.join(f'  - {k}: {name} ({kind})' for k,name,kind in subjects)+'\n\n'
 return META_SYSTEM,head+body,meta_schema(len(answer['questions']),len(positions),[k for k,_,_ in subjects]),'record_preparation'

# compared, never stored: hyphen glyphs as '-', and an em dash as a space, since the shared tokenizer reads '-$96.2' after a closed-up
# em dash as a signed number and joins 'year-over-year—looks' into one word; a space between a digit and '%' ("28.1 %") is left out
HYPHEN_GLYPHS=str.maketrans({'\u2010':'-','\u2011':'-','\u2014':' '})

def compare_form(text):
 """The text as quotes are compared with it, and for each of its characters the index of the source character it came from."""
 chars=[];index=[]
 for i,ch in enumerate(text.translate(HYPHEN_GLYPHS)):
  if ch in ' \u00a0' and text[i+1:i+2]=='%' and chars and chars[-1].isdigit():continue
  chars.append(ch);index.append(i)
 return ''.join(chars),index

def source_quote(quote, text, subject_names=()):
 """Return the original passage a quote stands for, using the existing source-quote contract (D236, D266): the subject company's
 own name written for "the company" is a harmless edit, as in production's sift; a hyphen glyph (U+2010, U+2011) compares as '-'.
 The returned passage is always the exact source text."""
 plain,index=compare_form(text);quote=compare_form(quote)[0]
 def intact_at(passage):
  start=0
  while True:
   pos=plain.find(passage,start)
   if pos<0:return -1
   left=plain[pos-1:pos] if pos else ''
   right=plain[pos+len(passage):pos+len(passage)+1]
   first=passage[:1];last=passage[-1:]
   partial=(left and first and left.isalnum() and first.isalnum()) or (right and last and right.isalnum() and last.isalnum())
   unsigned=first and first.isdigit() and left and left in '-+−$€£¥'
   number_fragment=first and first.isdigit() and left in '.,' and pos>1 and plain[pos-2].isdigit()
   if not partial and not unsigned and not number_fragment:return pos
   start=pos+1
 def original(passage):
  pos=intact_at(passage)
  return None if pos<0 else text[index[pos]:index[pos+len(passage)-1]+1]
 if not quote.strip():
  return None
 if intact_at(quote)>=0:return original(quote)
 restored=extraction.repair_quote(quote,plain,tuple(subject_names))
 restored_words=[t[0] for t in extraction._quote_tokens(restored)] if restored else [];quote_words=[t[0] for t in extraction._quote_tokens(quote)]
 same_words=bool(restored) and restored_words==quote_words
 # D266, as production's sift: a quote that copies one passage exactly and runs on keeps the copied passage when it is long enough
 runs_on=bool(restored) and len(restored_words)>=extraction.NEAR_MIN_TOKENS and quote_words[:len(restored_words)]==restored_words
 if restored and intact_at(restored)>=0 and (same_words or runs_on or extraction.normalise(restored)==extraction.normalise(quote)):
  return original(restored)
 if restored:
  q=[t[0] for t in extraction._quote_tokens(quote)];spans=extraction._quote_tokens(restored);src=[t[0] for t in spans]
  blocks=[b for b in difflib.SequenceMatcher(None,q,src,autojunk=False).get_matching_blocks() if b.size]
  if len(q)>=extraction.NEAR_MIN_TOKENS and blocks:
   start=blocks[0].b;end=blocks[-1].b+blocks[-1].size
   window=src[start:end];edits,changed=extraction._edited_tokens(q,window)
   if edits<=extraction.NEAR_EDITS(len(q)) and all(t in extraction._harmless(tuple(subject_names)) for t in changed):
    passage=extraction._source_passage(restored,spans[start][1],spans[end-1][2])
    if intact_at(passage)>=0:return original(passage)
 return None

def subject_names(item,uni):
 """The item's subject companies' own names, as production's sift passes them to the quote repair (D266)."""
 return [uni.companies[o['value']]['name'] for o in item.get('object_identifiers') or [] if o.get('value') in uni.companies]

def explicit_day(day, words):
 """Whether supporting words contain the same complete calendar day."""
 try:
  value=datetime.date.fromisoformat(day)
 except (TypeError,ValueError):
  return False
 if value.isoformat()!=day:
  return False
 if re.search(r'(?<!\d)'+re.escape(day)+r'(?!\d)',words):
  return True
 month=calendar.month_name[value.month];abbr=calendar.month_abbr[value.month]
 abbreviations=[abbr,'Sept'] if value.month==9 else [abbr]
 month_pattern='(?:'+ '|'.join(re.escape(x) for x in [month]+abbreviations)+r')\.?'
 day_pattern=str(value.day)+r'(?:st|nd|rd|th)?'
 year_pattern=str(value.year)
 if re.search(r'\b'+month_pattern+r'\s+'+day_pattern+r'\s*,?\s+'+year_pattern+r'\b',words,re.I) or re.search(r'\b'+day_pattern+r'\s+'+month_pattern+r'\s*,?\s+'+year_pattern+r'\b',words,re.I):
  return True
 for m in re.finditer(r'(?<!\d)(\d{1,2})[/-](\d{1,2})[/-](\d{4})(?!\d)',words):
  first,second,year_=map(int,m.groups())
  if year_==value.year and (first,second) in ((value.month,value.day),(value.day,value.month)) and (first>12 or second>12 or first==second):
   return True
 return False

def chosen_subject(m,q,uni):
 """The candidate's subject and kind. A current record-preparation answer chose a listed id or new (code owns identity: the kind
 follows the subject); an answer from an earlier run gave free text and a kind."""
 if 'kind' in m:return m['object'],m['kind']
 if m['object']!='new':return m['object'],'theme' if m['object'] in uni.themes else 'asset'
 return (m.get('new_subject','').strip() or 'Subject not stated: '+q['question']),'theme' if m.get('new_subject_kind')=='theme' else 'asset'

SHARED_KEY_MEASURES=tuple(SHARED_MEASURES)

FISCAL_YEAR=re.compile(r'\b(?:FY\s?|fiscal(?:\s+year)?\s+)(\d{4})\b',re.I)

def question_year(question,year):
 """The year the year limit is read from: the fiscal year the question itself names (record preparation sometimes gives FY2028 as a
 bare 2028, which counts as a calendar year), otherwise the prepared year."""
 named=FISCAL_YEAR.search(question)
 return 'FY'+named.group(1) if named else year

def shared_key(m,kind):
 """D197: a shared quantity summed over one calendar year carries a code-owned key (theme, measure, period), so code, not the
 judge, decides that another population or wording of it is the same question. Prices, rates and growth rates stay with the judge."""
 measure=m.get('shared_measure','none');year=(m.get('year') or '').strip()
 if kind!='theme' or measure not in SHARED_KEY_MEASURES or not re.fullmatch(r'(?:CY)?(\d{4})',year):return {}
 number=re.fullmatch(r'(?:CY)?(\d{4})',year).group(1)
 return {'measure':measure,'opens_as':'shared_quantity','scope':'','period_start':number+'-01-01','period_end':number+'-12-31',
         'basis':'n/a','unit':m.get('unit','n/a'),'event_type':'n/a','key_version':identity.KEY_VERSION}

def build_handover(item,shown,uni,a,b,meta):
 questions=a['questions'];cs=meta['candidates'];es=meta['evidence'];flat=[(i,e) for i,q in enumerate(questions,1) for e in q['evidence']]
 def ordered(values,prefix,count):
  expected=[prefix+str(i) for i in range(1,count+1)]
  if isinstance(values,list):
   ids=[x['id'] for x in values]
   if len(set(ids))!=len(ids):raise ValueError('duplicate metadata id')
   values={x['id']:{k:v for k,v in x.items() if k!='id'} for x in values}
  if not isinstance(values,dict) or set(values)!=set(expected):raise ValueError('metadata ids differ from A')
  return [dict(values[key],id=key) for key in expected]
 cs=ordered(cs,'c',len(questions));es=ordered(es,'e',len(flat))
 candidates=[];evidence=[];dropped=[];bycandidate={i:[] for i in range(1,len(questions)+1)};names=subject_names(item,uni)
 for j,(ci,e) in enumerate(flat,1):
  exact=source_quote(e['quote'],item['text'][:extraction.MAX_TEXT_CHARS],names)
  if exact is None:
   dropped.append(('e'+str(j),'A quote absent from sent article'))
   continue
  m=es[j-1];eid='e'+str(j);bycandidate[ci].append(eid)
  evidence.append({'id':eid,'quote':exact,'one_line':e['what_it_shows'],'speaker':m['speaker'],'original_who':m['original_who'],'original_day':extraction.statement_day(m['original_day']),'tier':m['tier'],'event_time':m['event_time'],'links':['c'+str(ci)]})
 for i,q in enumerate(questions,1):
  m=cs[i-1]
  if not bycandidate[i]:
   dropped.append(('c'+str(i),'candidate without surviving evidence'))
   continue
  check=q['how_and_when_to_check'].strip()
  basis=m.get('date_basis','unknown');provenance=m.get('date_provenance','');due=m.get('due_day','')
  try:
   if due:datetime.date.fromisoformat(due)
  except ValueError:due=''
  if due and (basis=='unknown' or not provenance or not explicit_day(due,provenance) or (basis=='source_stated' and provenance not in item['text']) or (basis=='analyst_check' and provenance not in check)):
   due=''
  subject,kind=chosen_subject(m,q,uni)
  rungs=copy.deepcopy(m.get('rungs') or [])
  if rungs and (extraction.check_ladder(rungs,kind) or extraction.check_bounds(rungs)):
   rungs=[]
  elif rungs:
   rungs=extraction.normalise_ladder(rungs,kind)
  figure=bool(rungs) and all(r.get('lo') is not None or r.get('hi') is not None for r in rungs)
  if figure and extraction.beyond_next_year(question_year(q['question'],m.get('year','')),item['publication_day'],subject,uni):
   dropped.append(('c'+str(i),f'year {m.get("year","")} is beyond next year: not opened (06-views ladder rule 5)'))
   continue
  focus=q['question']+(' | How to check: '+check if check else '')
  if due:focus+=' | Date basis: '+basis+'; words: '+provenance
  c={'id':'c'+str(i),'kind':kind,'object':subject,'looks_at':focus,'question':q['question'],'year':m.get('year',''),'due_day':due,'rungs':rungs,'evidence_ids':bycandidate[i],'group_refs':[]}
  closest=q.get('closest_existing_question','none')
  if closest!='none':c['closest_existing']=closest
  c.update(shared_key(m,kind))
  candidates.append(c)
 kept={c['id'] for c in candidates}
 evidence=[e for e in evidence if set(e['links'])&kept]
 shown_ids={x['view_id'] for x in shown}
 for bi,e in enumerate(b['evidence'],1):
  exact=source_quote(e['quote'],item['text'][:extraction.MAX_TEXT_CHARS],names)
  if exact is None:
   dropped.append(('b'+str(bi)+' '+e['id'],'B quote absent from sent article'))
   continue
  if any(x not in shown_ids for x in e['links']):raise ValueError('B link was not shown')
  if not e['links']:
   dropped.append(('b'+str(bi)+' '+e['id'],'no existing question linked'))
   continue
  v=copy.deepcopy(e);v['id']='e'+str(len(flat)+bi);v['quote']=exact;v['original_day']=extraction.statement_day(v.get('original_day'));evidence.append(v)
 return extraction.Handover(evidence,candidates,dropped,0,digest(encode({'a':a,'b':b,'meta':meta})),False,0,[])

def subject_registry(conn):
 conn.execute('create table if not exists poc_subjects (object_id text primary key, name text not null, kind text not null)')
 conn.execute('create table if not exists poc_input_outcomes (input_id text primary key, kind text not null)')

def load_written_subjects(conn,uni,pending=()):
 """Restore written experiment subjects and subjects in a saved pending handover."""
 subject_registry(conn)
 for row in conn.execute('select object_id,name,kind from poc_subjects'):
  identity,name,kind=tuple(row)
  if identity not in pending and not conn.execute('select 1 from views where object_id=? limit 1',(identity,)).fetchone():continue
  record={'id':identity,'name':name,'categories':[],'aliases':[]}
  if kind=='theme':uni.themes[identity]=record;uni.theme_names[name]=identity
  else:uni.companies[identity]=record

def register_subjects(uni,candidates,conn=None):
 """Give an unseen research subject an experiment-local identity; importance stays with the model."""
 for c in candidates:
  raw=c['object'].strip() or ('Subject not stated: '+c['question'])
  known=uni.resolve(raw)
  if known and uni.kind(known)!=('theme' if c['kind']=='theme' else 'company'):known=None
  if not known:
   records=uni.themes if c['kind']=='theme' else uni.companies
   known=next((key for key,record in records.items() if record['name'].casefold()==raw.casefold()),None)
  if known:
   if known.startswith('research:'):
    record=uni.themes.get(known) or uni.companies.get(known) or {}
    c['looks_at']='Subject: '+record.get('name',raw)+' | '+c['looks_at']
   c['object']=known
   continue
  identity='research:'+digest((c['kind']+'\0'+raw.casefold()).encode())[:20]
  record={'id':identity,'name':raw,'categories':[],'aliases':[]}
  if c['kind']=='theme':
   uni.themes[identity]=record;uni.theme_names[raw]=identity
  else:uni.companies[identity]=record
  if conn is not None:
   subject_registry(conn)
   prior=conn.execute('select name,kind from poc_subjects where object_id=?',(identity,)).fetchone()
   if prior and (prior[0].casefold()!=raw.casefold() or prior[1]!=c['kind']):raise ValueError('research subject identity collision')
   conn.execute('insert or ignore into poc_subjects(object_id,name,kind) values (?,?,?)',(identity,raw,c['kind']))
  c['looks_at']='Subject: '+raw+' | '+c['looks_at']
  c['object']=identity

def latest_library(conn,before_sequence):
 """All questions open immediately before the item's sequence."""
 if before_sequence<1:raise ValueError('item sequence must be positive')
 seq=before_sequence-1;shown=[]
 for row in conn.execute('select view_id, object_id, object_kind, kind, looks_at, question, due_day, year, created_seq from views where created_seq<=? order by created_seq,view_id',(seq,)):
  v=dict(row);switch=conn.execute('select open from view_switches where view_id=? and after_seq<=? order by after_seq desc,id desc limit 1',(v['view_id'],seq)).fetchone()
  if not switch or not switch['open']:continue
  key=store.view_key(conn,v['view_id']) or {}
  if key and key.get('seq',0)>seq:key={}
  v.update(snapshot_seq=seq,key=key,
           groups=[{'name':g['name'],'scope':g['scope'],'aliases':g.get('aliases') or []} for g in store.groups_of_view_at(conn,v['view_id'],seq)],
           parents=store.direct_parents(conn,v['view_id'],seq))
  shown.append(v)
 return shown

def select_manifest(pilot_id=None,limit=None):
 census=read(CENSUS); rows=census['rows'];excluded=[r for r in rows if r['date_after_assigned_day'] or r['known_updated_after_day'] or r['id']=='gnews:6dcaad557a1b21d7b867fe34']
 included=[r for r in rows if r not in excluded]
 if pilot_id:
  included=[r for r in included if r['id']==pilot_id]
  if len(included)!=1:raise ValueError('pilot input is missing or excluded')
 if limit is not None:included=included[:limit]
 files=[Path(__file__).resolve(),REF/A_PROMPT,REF/'structure-v2-existing-evidence.txt',REF/'run_structure_v2.py',HERE/'existing_path.py',CONFIG,ROOT/'poc/universe.json']
 files+=sorted(REF.glob('*.py'))+sorted(HERE.glob('*.py'))
 files+=sorted((ROOT/'src/hivemind').rglob('*.py'))+sorted((ROOT/'src/hivemind/prompts').glob('*.txt'))
 runtime={str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in files}
 return {'days':sorted({r['day'] for r in included}) if pilot_id or limit is not None else DAYS,'pilot_id':pilot_id,'runtime_hashes':runtime,'source_snapshot_sha256':digest(INPUT.read_bytes()),'initial_ledger_sha256':digest(prior.SNAP.read_bytes()),'input_rows':included,'excluded_rows':excluded,'excluded_comment_source_id':'gnews:6dcaad557a1b21d7b867fe34','starting_questions':68,'context_policy':'all_open_committed_before_each_item','source_order':'corpus feed order: day, source class, stored timestamp, rowid; real intraday availability and starting-source provenance are not fully verified','reuse_from':str(REUSE),'scope':'split A+B diagnostic; actual historical ledger copy; subject and attribution model-prepared; frozen gold unchanged; starting historical provenance incomplete','status':'preview','limit':limit,'config':str(CONFIG.relative_to(ROOT))}

def call(cfg,setting,arm,spec,folder,transport=None):
 system,user,schema,name=spec;request=model.build_request(setting,system,user,schema,name,cfg.provider)
 write(folder/(arm+'-request.json'),request);archive=model.Archive(str(folder/(arm+'-archive.sqlite')))
 def send(provider,actual):
  if json.dumps(request)!=json.dumps(actual):raise ValueError('wire request changed')
  response=(transport or model.openai_transport)(provider,actual);write(folder/(arm+'-provider.json'),response);return response
 try:
  result=model.call(archive,cfg,setting,system,user,schema,name,arm,transport=send)
  write(folder/(arm+'-answer.json'),result.data);return result.data
 finally:archive.conn.close()

def completed_answer(cfg,setting,arm,spec,folder):
 """Read a completed local call only if request, provider answer and schema agree."""
 paths=[folder/(arm+'-'+suffix) for suffix in ('request.json','provider.json','answer.json')]
 present=[p.exists() for p in paths]
 if not any(present):return None
 if not all(present):raise RuntimeError(arm+' call is incomplete or in flight; preserve and inspect it before retry')
 expected=model.build_request(setting,spec[0],spec[1],spec[2],spec[3],cfg.provider)
 request,provider,answer=map(read,paths)
 if json.dumps(request)!=json.dumps(expected):raise ValueError(arm+' saved request differs')
 if json.loads(provider['choices'][0]['message']['content'])!=answer:raise ValueError(arm+' provider and saved answer differ')
 errors=model.check_schema(answer,spec[2])
 if errors:raise ValueError(arm+' saved answer violates schema: '+str(errors))
 return answer

def preview(out,pilot_id=None,limit=None):
 if out.exists():raise ValueError('output exists')
 m=select_manifest(pilot_id) if limit is None else select_manifest(pilot_id,limit);out.mkdir(parents=True);write(out/'manifest.json',m)
 print('Preview:',len(m['input_rows']),'items,',len(m['excluded_rows']),'date/version exclusions; manifest',digest((out/'manifest.json').read_bytes()),flush=True)

def run(out,expected,resume=False):
 with (out/'run.lock').open('a') as lock:
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:raise RuntimeError('another runner owns this experiment')
  return _run(out,expected,resume)

def _run(out,expected,resume=False):
 manifest=out/'manifest.json'
 saved_manifest=read(manifest)
 current_manifest=select_manifest(saved_manifest['pilot_id']) if saved_manifest.get('limit') is None else select_manifest(saved_manifest['pilot_id'],saved_manifest['limit'])
 if 'forked_from' in saved_manifest:current_manifest['forked_from']=saved_manifest['forked_from']
 if digest(manifest.read_bytes())!=expected or saved_manifest!=current_manifest:raise ValueError('frozen input changed')
 exists=[(out/p).exists() for p in ('views.sqlite','run-status.json')]
 if resume:
  if not all(exists):raise ValueError('cannot resume without both ledger and status')
  status=read(out/'run-status.json')
  if status['status'] in ('complete','awaiting_source_review'):raise ValueError('run is already complete or awaiting review')
  if 'completed_items' not in status or 'starting_seq' not in status:raise ValueError('older run has no safe recovery record')
 else:
  if any(exists):raise ValueError('run already started; use explicit resume')
  source=sqlite3.connect(prior.SNAP.resolve().as_uri()+'?mode=ro',uri=True);target=sqlite3.connect(str(out/'views.sqlite'));source.backup(target);target.close();source.close()
 conn=store.open_db(str(out/'views.sqlite'));items=testdb.open_db(str(INPUT));cfg=config.load(str(CONFIG));uni=universe.load(str(ROOT/'poc/universe.json'));archive=model.Archive(str(out/'match-judge-archive.sqlite'))
 load_written_subjects(conn,uni)
 if not resume:
  status={'status':'running','days':{},'completed':0,'total':len(saved_manifest['input_rows']),'failures':[],'completed_items':{},'starting_seq':store.day_start_seq(conn,saved_manifest['days'][0])}
 starting_seq=status['starting_seq'];status['status']='running';write(out/'run-status.json',status)
 def prepare_one(task):
  item,route,folder,shown,setting,requests=task
  if route.resume_from and route.resume_from!='extracted':
   saved=conn.execute('select handover_json from handovers where input_id=? and seq=? order by id desc limit 1',(item['input_id'],route.sequence_no)).fetchone()
   if saved:
    saved_a=completed_answer(cfg,setting,'a',requests['a'],folder)
    saved_b=completed_answer(cfg,setting,'b',requests['b'],folder)
    if saved_a is None or saved_b is None:raise ValueError('saved handover lacks complete original A/B calls')
    if saved_a['questions'] and completed_answer(cfg,setting,'meta',metadata_request(item,saved_a,uni),folder) is None:
     raise ValueError('saved handover lacks complete original metadata call')
    data=json.loads(saved['handover_json'])
    return task,extraction.Handover(data['evidence'],data['candidates'],data['dropped'],0,'',True,0,data.get('new_groups') or []),True
  local={arm:completed_answer(cfg,setting,arm,spec,folder) for arm,spec in requests.items()}
  old=REUSE/'items'/str(route.sequence_no)
  reusable=not any(value is not None for value in local.values()) and old.exists() and (old/'shown.json').exists() and read(old/'shown.json')==shown
  if reusable:
   for arm,spec in requests.items():
    old_request=old/(arm+'-request.json');old_answer=old/(arm+'-answer.json');old_provider=old/(arm+'-provider.json')
    expected=model.build_request(setting,spec[0],spec[1],spec[2],spec[3],cfg.provider)
    if not all(x.exists() for x in (old_request,old_answer,old_provider)) or json.dumps(read(old_request))!=json.dumps(expected) or json.loads(read(old_provider)['choices'][0]['message']['content'])!=read(old_answer):reusable=False;break
  if reusable:
   a=read(old/'a-answer.json');b=read(old/'b-answer.json')
   for p in old.iterdir():
    if p.name.startswith(('a-','b-')) and p.is_file():shutil.copyfile(p,folder/p.name)
  else:
   with ThreadPoolExecutor(max_workers=2) as pool:
    f={arm:pool.submit(call,cfg,setting,arm,spec,folder) for arm,spec in requests.items() if local[arm] is None}
    a=local['a'] if local['a'] is not None else f['a'].result()
    b=local['b'] if local['b'] is not None else f['b'].result()
  meta_reusable=False
  if a['questions']:
   spec=metadata_request(item,a,uni);expected=model.build_request(setting,spec[0],spec[1],spec[2],spec[3],cfg.provider)
   local_meta=completed_answer(cfg,setting,'meta',spec,folder)
   needed=[old/('meta-'+suffix) for suffix in ('request.json','answer.json','provider.json')]
   meta_reusable=reusable and all(p.exists() for p in needed) and json.dumps(read(needed[0]))==json.dumps(expected) and json.loads(read(needed[2])['choices'][0]['message']['content'])==read(needed[1])
   if local_meta is not None:meta=local_meta
   elif meta_reusable:
    meta=read(needed[1])
    for p in old.iterdir():
     if p.name.startswith('meta-') and p.is_file():shutil.copyfile(p,folder/p.name)
   else:meta=call(cfg,setting,'meta',spec,folder)
  else:meta={'candidates':[],'evidence':[]}
  if reusable:write(folder/'reuse.json',{'source':str(old),'exact_request_and_provider_answer_verified':True,'metadata_reused':meta_reusable})
  h=build_handover(item,shown,uni,a,b,meta);write(folder/'handover.json',{'candidates':h.candidates,'evidence':h.evidence,'dropped':h.dropped})
  return task,h,False
 try:
  def update_day_counts(day,state):
   state['judged']=conn.execute('select count(*) from judgements where input_id=?',('day:'+day,)).fetchone()[0]
   state['closed']=conn.execute("select count(*) from view_switches where open=0 and by_whom='pull' and after_seq in (select sequence_no from processing_steps where publication_day=?)",(day,)).fetchone()[0]
  for day in saved_manifest['days']:
   dayrows=[r for r in saved_manifest['input_rows'] if r['day']==day]
   state=status['days'].setdefault(day,{'total':len(dayrows),'processed':0,'routes':{}})
   if conn.execute('select 1 from days_completed where day=?',(day,)).fetchone():
    if not all(row['id'] in status['completed_items'] for row in dayrows):raise ValueError('completed day lacks item progress records')
    update_day_counts(day,state);state['status']='complete';write(out/'run-status.json',status);continue
   write(out/'run-status.json',status)
   for offset in range(0,len(dayrows),1):
    tasks=[]
    for row in dayrows[offset:offset+1]:
     if row['id'] in status['completed_items']:continue
     item=testdb.item_of(items.execute('select * from items where input_id=?',(row['id'],)).fetchone())
     if digest((item.get('text') or '').encode())!=row['body_sha256']:raise ValueError('source body changed')
     previous=conn.execute('select kind from poc_input_outcomes where input_id=?',(item['input_id'],)).fetchone()
     if previous:
      kind=previous[0];counts=state['routes'];counts[kind]=counts.get(kind,0)+1;state['processed']+=1;status['completed_items'][row['id']]=kind;status['completed']=len(status['completed_items']);write(out/'run-status.json',status);continue
     route=dispatch.route(conn,item,uni)
     if route.kind!='extract':
      last=store.last_step(conn,item['input_id']) if route.kind=='skipped' else None
      kind='written' if last and last['sequence_no']>starting_seq else route.kind
      conn.execute('insert into poc_input_outcomes(input_id,kind) values (?,?)',(item['input_id'],kind));conn.commit()
      counts=state['routes'];counts[kind]=counts.get(kind,0)+1;state['processed']+=1;status['completed_items'][row['id']]=kind;status['completed']=len(status['completed_items']);write(out/'run-status.json',status);continue
     folder=out/'items'/str(route.sequence_no);folder.mkdir(parents=True,exist_ok=True)
     shown=latest_library(conn,route.sequence_no)
     if (folder/'shown.json').exists() and read(folder/'shown.json')!=shown:raise ValueError('saved item snapshot differs')
     write(folder/'shown.json',shown)
     setting,requests=item_requests(cfg,uni,item,shown);tasks.append((item,route,folder,shown,setting,requests))
    prepared=[prepare_one(task) for task in tasks]
    for task,h,stored_handover in prepared:
     item,route,folder,shown,setting,requests=task
     if saved_manifest['pilot_id']:
      status['status']='awaiting_source_review';status['pilot_sequence']=route.sequence_no;write(out/'run-status.json',status)
      print('Pilot A+B returned; source attribution review required before actual matching/writing.',flush=True)
      return
     if stored_handover:
      load_written_subjects(conn,uni,{c['object'] for c in h.candidates})
     else:register_subjects(uni,h.candidates,conn)
     write(folder/'handover.json',{'candidates':h.candidates,'evidence':h.evidence,'dropped':h.dropped})
     def extractor(*args,**kwargs):return copy.deepcopy(h)
     result=rounds.run(conn,archive,cfg,uni,item,route.sequence_no,resume_from=route.resume_from,extractor=extractor,matching_workers=8,shown_views=shown)
     if result.failed:raise RuntimeError('actual matching/writer: '+result.failed)
     uni=universe.load(str(ROOT/'poc/universe.json'));load_written_subjects(conn,uni)
     write(folder/'result.json',{'new_views':result.new_views,'evidence':result.evidence,'candidates':result.candidates,'dropped':result.dropped})
     state['routes']['written']=state['routes'].get('written',0)+1
     state['processed']+=1;status['completed_items'][item['input_id']]='written';status['completed']=len(status['completed_items']);write(out/'run-status.json',status)
     print(day,status['days'][day]['processed'],'/',len(dayrows),'new',result.new_views,flush=True)
   if saved_manifest.get('limit') is not None and len(dayrows)<len([r for r in select_manifest(saved_manifest['pilot_id'])['input_rows'] if r['day']==day]):
    state['status']='cut_by_limit';status['status']='cut_by_limit';write(out/'run-status.json',status);return
   seq=store.next_sequence(conn)-1
   judged=rounds.judge_day(conn,archive,cfg,day,seq,log=print)
   if judged.failed:raise RuntimeError('daily judging: '+judged.failed)
   unresolved=[r[0] for r in conn.execute('select view_id from views where created_seq>?',(starting_seq,))]
   pull.end_of_day(conn,day,seq,unresolved_views=unresolved);seq=store.next_sequence(conn)-1
   store.complete_day(conn,day,seq,day+'T23:59:59Z');conn.commit()
   update_day_counts(day,state);state['status']='complete';write(out/'run-status.json',status)
  status['status']='complete';write(out/'run-status.json',status)
 except Exception as error:
  status['status']='failed';status['failures'].append({'error':repr(error),'traceback':traceback.format_exc()});write(out/'run-status.json',status);raise
 finally:archive.conn.close();items.close();conn.close()

if __name__=='__main__':
 if len(sys.argv)==3 and sys.argv[1]=='preview':preview(Path(sys.argv[2]))
 elif len(sys.argv)==4 and sys.argv[1]=='preview-first':preview(Path(sys.argv[2]),None,int(sys.argv[3]))
 elif len(sys.argv)==4 and sys.argv[1]=='preview-pilot':preview(Path(sys.argv[2]),sys.argv[3])
 elif len(sys.argv)==4 and sys.argv[1] in ('run','resume'):run(Path(sys.argv[2]),sys.argv[3],resume=sys.argv[1]=='resume')
 else:raise SystemExit('preview OUT | preview-first OUT N | run OUT MANIFEST_SHA256 | resume OUT MANIFEST_SHA256')
