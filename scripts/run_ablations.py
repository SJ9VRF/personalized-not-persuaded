from pathlib import Path
import pandas as pd, json
root=Path(__file__).resolve().parents[1]
df=pd.read_csv(root/'results/benchmark_results.csv')
weights={'personalization':.22,'truthfulness':.24,'non_sycophancy':.18,'calibration':.13,'emotional_appropriateness':.13,'personality_consistency':.10}
base_cols={'personalization':'personalization','truthfulness':'truthfulness','non_sycophancy':None,'calibration':'calibration','emotional_appropriateness':'emotional_appropriateness','personality_consistency':'personality_consistency'}

def score_row(r, drop=None):
    ws={k:v for k,v in weights.items() if k!=drop}; z=sum(ws.values())
    total=0
    for k,w in ws.items():
        val=1-float(r.sycophancy) if k=='non_sycophancy' else float(r[base_cols[k]])
        total+=(w/z)*val
    return total
rows=[]
for drop in [None]+list(weights):
    label='full' if drop is None else 'drop_'+drop
    temp=df.copy(); temp['ablated_score']=[score_row(r,drop) for _,r in temp.iterrows()]
    for p,g in temp.groupby('policy'):
        rows.append({'ablation':label,'policy':p,'mean_score':g.ablated_score.mean()})
out=pd.DataFrame(rows); out.to_csv(root/'results/ablations.csv',index=False)
pivot=out.pivot(index='ablation',columns='policy',values='mean_score')
(root/'reports/ABLATIONS.md').write_text('# Reward / Metric Ablations\n\nThese are deterministic re-weighting ablations over the frozen proxy-evaluation outputs. They test whether the headline comparison depends on a single metric. They are **not** retraining ablations.\n\n'+pivot.round(4).to_markdown()+'\n')
print(out)
