from pathlib import Path
import csv, random, sys, math
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from behavior_lab.policies.baselines import POLICIES
from behavior_lab.metrics.core import personality_drift

root=Path(__file__).resolve().parents[1]
rng=random.Random(11)
target=[.90,.55,.80,.75,.25,.45,.80,.85]  # directness,warmth,concision,confidence,humor,formality,empathy,humility
horizons=[1,10,25,50,100,200]
# Explicitly a stress simulator: it injects bounded perturbations that grow with horizon. It is not a
# substitute for stateful real-model conversations; it makes long-horizon analysis code executable locally.
base_noise={'generic':.060,'naive_personalized':.095,'behavior_trained_proxy':.035,'cgsp':.030}
rows=[]
for name in POLICIES:
  for h in horizons:
    for run in range(40):
      scale=base_noise[name]*(1+math.log10(max(h,1)))
      obs=[min(1,max(0,v+rng.uniform(-scale,scale))) for v in target]
      rows.append({'policy':name,'horizon':h,'run':run,'drift':round(personality_drift(target,obs),4),'simulation':'bounded_stress_v1'})
with (root/'results/long_horizon.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} synthetic long-horizon stress measurements")
