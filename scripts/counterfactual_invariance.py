from pathlib import Path
import json
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
rows=[]
for p in (ROOT/'datasets/behaviorbench').glob('*.jsonl'):
    for line in p.read_text().splitlines():
        if not line.strip(): continue
        x=json.loads(line)
        rows.append({
            'scenario_id':x['scenario_id'],
            'template_cluster':x['metadata']['template_cluster'],
            'pressure':x['metadata']['pressure'],
            'language':x['metadata']['language'],
            'profile':x['metadata']['profile_condition'],
            'category':x['category'],
        })
meta=pd.DataFrame(rows)
res=pd.read_csv(ROOT/'results/benchmark_results.csv')
df=res.merge(meta,on=['scenario_id','category','language','profile'],how='left')
key=['policy','template_cluster','pressure','language']
base=df[df.profile=='P0'][key+['personalization','truthfulness','sycophancy','calibration']].copy()
base=base.rename(columns={c:f'{c}_P0' for c in ['personalization','truthfulness','sycophancy','calibration']})
rich=df[df.profile.isin(['P4','P5'])].merge(base,on=key,how='inner')
rich['personalization_gain']=rich.personalization-rich.personalization_P0
rich['truthfulness_drift']=(rich.truthfulness-rich.truthfulness_P0).abs()
rich['calibration_drift']=(rich.calibration-rich.calibration_P0).abs()
rich['sycophancy_regression']=(rich.sycophancy-rich.sycophancy_P0).clip(lower=0)
rich['epistemic_drift']=(rich.truthfulness_drift+rich.calibration_drift+rich.sycophancy_regression)/3
rich['counterfactual_epistemic_invariance']=(1-rich.epistemic_drift).clip(0,1)
rich['selective_adaptation']=rich.personalization_gain-rich.epistemic_drift
summary=(rich.groupby('policy',as_index=False)
         .agg(pairs=('scenario_id','count'),
              personalization_gain=('personalization_gain','mean'),
              epistemic_drift=('epistemic_drift','mean'),
              counterfactual_epistemic_invariance=('counterfactual_epistemic_invariance','mean'),
              selective_adaptation=('selective_adaptation','mean'),
              truthfulness_drift=('truthfulness_drift','mean'),
              sycophancy_regression=('sycophancy_regression','mean'),
              calibration_drift=('calibration_drift','mean')))
summary.to_csv(ROOT/'results/counterfactual_invariance_summary.csv',index=False)
rich.to_csv(ROOT/'results/counterfactual_invariance_pairs.csv',index=False)
print(summary.to_string(index=False,float_format=lambda x:f'{x:.4f}'))
