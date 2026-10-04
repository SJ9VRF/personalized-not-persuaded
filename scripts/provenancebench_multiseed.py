from pathlib import Path
import sys, numpy as np, pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from behavior_lab.methods.learned_plp import PLPRouter, metric_bundle

df=pd.read_csv(ROOT/'datasets/provenance/provenancebench.csv')
tr=df[df.split=='train']; va=df[df.split=='val']
sets={s:df[df.split==s] for s in ['test','ood_test','compositional_test']}
pi=ROOT/'datasets/provenance/provenance_intervention_test.csv'
if pi.exists(): sets['provenance_intervention']=pd.read_csv(pi)
rows=[]
for seed in range(10):
    r=PLPRouter(random_state=seed).fit(tr,va)
    for split,d in sets.items():
        for hybrid in [False,True]:
            m=metric_bundle(d,r.predict(d,hybrid=hybrid)); rows.append({'seed':seed,'split':split,'method':'hybrid_plp' if hybrid else 'learned_plp',**m})
out=pd.DataFrame(rows); out.to_csv(ROOT/'results/provenancebench_multiseed.csv',index=False)
summary=out.groupby(['split','method']).agg(['mean','std'])[['exact_license_match','evidence_uptake','unsupported_leakage']]
lines=['# ProvenanceBench — multi-seed stability','', 'Ten logistic-router fits use different solver random states; validation threshold selection is repeated per fit.','', '```',summary.to_string(),'```','', 'This does not substitute for multi-seed neural-model training, but it checks whether the reported linear-router result is an initialization artifact.']
(ROOT/'reports/PROVENANCEBENCH_MULTISEED.md').write_text('\n'.join(lines))
print(summary)
