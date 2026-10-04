"""Evaluate a user-supplied ModelAdapter module against the frozen test split.
Usage: python scripts/evaluate_adapter.py my_adapter.py
The module must define `adapter`, an object with generate(scenario)->PolicyOutput.
"""
from pathlib import Path
import importlib.util, json, csv, sys, time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from behavior_lab.eval.scorer import score
root=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2: raise SystemExit('usage: python scripts/evaluate_adapter.py path/to/adapter.py')
path=Path(sys.argv[1]).resolve(); spec=importlib.util.spec_from_file_location('external_adapter',path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
adapter=mod.adapter
rows=[json.loads(x) for x in (root/'datasets/behaviorbench/test.jsonl').read_text().splitlines() if x.strip()]
out=[]
for s in rows:
    t=time.perf_counter(); r=adapter.generate(s); latency=time.perf_counter()-t
    out.append({'scenario_id':s['scenario_id'],'category':s['category'],'language':s['metadata']['language'],'profile':s['metadata']['profile_condition'],'response':r.text,'latency_s':round(latency,5),**score(s,r)})
name=path.stem; dest=root/'results'/f'external_{name}.csv'
with dest.open('w',newline='',encoding='utf8') as f:
    w=csv.DictWriter(f,fieldnames=out[0].keys()); w.writeheader(); w.writerows(out)
print(dest)
