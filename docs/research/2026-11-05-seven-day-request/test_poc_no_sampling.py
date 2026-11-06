"""Alex: active POC configuration and requests contain no temperature parameter."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT/'src'))
from hivemind import config,model

def main():
 path=ROOT/'poc/config/poc-v118.json';raw=json.loads(path.read_text())
 def walk(x):
  if isinstance(x,dict):
   assert 'temperature' not in x
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(raw)
 cfg=config.load(path);setting=cfg.extraction_setting('T7')
 for provider in ('openai','deepseek'):
  request=model.build_request(setting,'system','user',{'type':'object'},'test',provider)
  assert 'temperature' not in request
 print('PASS: active v118 configuration and both provider request shapes omit temperature.')
if __name__=='__main__':main()
