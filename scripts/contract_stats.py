from pathlib import Path
import numpy as np, pandas as pd
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'results/counterfactual_contract_pairs.csv')
METRICS=['allowed_personalization_gain','protected_epistemic_drift','contract_score','contract_pass']
rng=np.random.default_rng(20260923)
rows=[]
for policy,g in df.groupby('policy'):
    n=len(g)
    for m in METRICS:
        vals=g[m].to_numpy(float)
        boots=np.empty(5000)
        for i in range(len(boots)):
            boots[i]=vals[rng.integers(0,n,n)].mean()
        rows.append({'policy':policy,'metric':m,'mean':vals.mean(),'ci_low':np.quantile(boots,.025),'ci_high':np.quantile(boots,.975),'n_contracts':n})
out=pd.DataFrame(rows)
out.to_csv(ROOT/'results/contract_bootstrap_ci.csv',index=False)
# Paired differences against CGSP on exact contract IDs.
base=df[df.policy=='cgsp'].set_index('contract_id')
pairs=[]
for policy in sorted(set(df.policy)-{'cgsp'}):
    other=df[df.policy==policy].set_index('contract_id').loc[base.index]
    for m in ['allowed_personalization_gain','protected_epistemic_drift','contract_score','contract_pass']:
        d=(base[m]-other[m]).to_numpy(float); n=len(d)
        boots=np.empty(5000)
        for i in range(len(boots)):
            boots[i]=d[rng.integers(0,n,n)].mean()
        sd=d.std(ddof=1)
        pairs.append({'comparison':f'cgsp - {policy}','metric':m,'mean_difference':d.mean(),'ci_low':np.quantile(boots,.025),'ci_high':np.quantile(boots,.975),'paired_d':(d.mean()/sd if sd>0 else float('inf')),'n_pairs':n})
pd.DataFrame(pairs).to_csv(ROOT/'results/contract_paired_effects.csv',index=False)
lines=['# Contract Statistical Analysis','',
'Bootstrap confidence intervals use 5,000 resamples over the 820 exact matched contracts. Pairwise comparisons preserve contract identity.','',
'## 95% bootstrap confidence intervals','',
'| Policy | Metric | Mean | 95% CI | N |','|---|---|---:|---:|---:|']
for _,r in out.iterrows():
    lines.append(f"| {r.policy} | {r.metric} | {r['mean']:.4f} | [{r.ci_low:.4f}, {r.ci_high:.4f}] | {int(r.n_contracts)} |")
pe=pd.read_csv(ROOT/'results/contract_paired_effects.csv')
lines += ['', '## Paired CGSP effects','', '| Comparison | Metric | Mean Δ | 95% CI | Paired d |','|---|---|---:|---:|---:|']
for _,r in pe.iterrows():
    d='∞' if np.isinf(r.paired_d) else f'{r.paired_d:.3f}'
    lines.append(f"| {r.comparison} | {r.metric} | {r.mean_difference:.4f} | [{r.ci_low:.4f}, {r.ci_high:.4f}] | {d} |")
lines += ['', 'These intervals characterize the deterministic proxy fixture under contract resampling; they do not substitute for model-seed variance or human-rater uncertainty.']
(ROOT/'reports/CONTRACT_STATISTICS.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print(out.to_string(index=False,float_format=lambda x:f'{x:.4f}'))
