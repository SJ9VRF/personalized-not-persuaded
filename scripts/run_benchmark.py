from pathlib import Path
import json, csv, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from behavior_lab.policies.baselines import POLICIES
from behavior_lab.eval.scorer import score
from behavior_lab.analysis.stats import bootstrap_ci, mean

root=Path(__file__).resolve().parents[1]
rows=[json.loads(x) for x in (root/'datasets/behaviorbench/test.jsonl').read_text().splitlines() if x.strip()]
results=[]
for s in rows:
  for name,fn in POLICIES.items():
    out=fn(s); sc=score(s,out)
    results.append({'scenario_id':s['scenario_id'],'category':s['category'],'language':s['metadata']['language'],'profile':s['metadata']['profile_condition'],'policy':name,'response':out.text,**sc})
out=root/'results/benchmark_results.csv'; out.parent.mkdir(exist_ok=True)
with out.open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=results[0].keys()); w.writeheader(); w.writerows(results)
metrics=['overall','personalization','truthfulness','sycophancy','calibration','emotional_appropriateness','personality_consistency']
summary={}
for p in POLICIES:
  subset=[r for r in results if r['policy']==p]
  summary[p]={}
  for m in metrics:
    vals=[float(r[m]) for r in subset]; ci=bootstrap_ci(vals)
    summary[p][m]={'mean':round(mean(vals),4),'ci95':[round(ci[0],4),round(ci[1],4)]}
(root/'results/summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
