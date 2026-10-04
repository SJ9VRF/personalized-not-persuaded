from pathlib import Path
import json, csv, sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from behavior_lab.policies.baselines import POLICIES
from behavior_lab.eval.scorer import score

ROOT=Path(__file__).resolve().parents[1]
rows=[json.loads(x) for x in (ROOT/'datasets/contracts/counterfactual_personalization_contracts_v1.jsonl').read_text(encoding='utf8').splitlines() if x.strip()]
results=[]
for s in rows:
    for name,fn in POLICIES.items():
        out=fn(s); sc=score(s,out)
        results.append({'scenario_id':s['scenario_id'],'contract_id':s['contract_id'],'category':s['category'],
                        'language':s['metadata']['language'],'pressure':s['metadata']['pressure'],
                        'profile':s['metadata']['profile_condition'],'policy':name,'response':out.text,**sc})
out=ROOT/'results/contract_benchmark_results.csv'
with out.open('w',newline='',encoding='utf8') as f:
    w=csv.DictWriter(f,fieldnames=results[0].keys()); w.writeheader(); w.writerows(results)
print(f'wrote {len(results)} policy responses -> {out}')
