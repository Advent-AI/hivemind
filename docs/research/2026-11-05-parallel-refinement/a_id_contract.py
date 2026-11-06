# -*- coding: utf-8 -*-
"""Isolated A-lane candidate identity boundary; never decides what is important."""
import copy,re
from hivemind import model
import run_poc
class IdentityRefusal(ValueError):pass

def experimental_schema(original):
 schema=copy.deepcopy(original)
 field=schema['properties']['candidates']['items']['properties']['id']
 if field!= {'type':'string'}:raise ValueError('candidate id schema changed')
 field['pattern']=r'^c[0-9]+$'
 return schema

def check_answer(data,schema):
 errors=model.check_schema(data,schema)
 if errors:raise IdentityRefusal('schema: '+'; '.join(errors[:5]))
 ids=[q['id'] for q in data['candidates']]
 if any(not re.fullmatch(r'c[0-9]+',i) for i in ids):raise IdentityRefusal('candidate id must be full ASCII c + digits')
 if len(ids)!=len(set(ids)):raise IdentityRefusal('duplicate candidate IDs')

def checked_handover(data,schema,request,uni,answer):
 # Apply even when the model archive returned a cache hit.
 check_answer(data,schema)
 return run_poc.handover(data,request,uni,answer)
