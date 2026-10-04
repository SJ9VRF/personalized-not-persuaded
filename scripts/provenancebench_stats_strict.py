from pathlib import Path
import math
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
from sys import path; path.insert(0,str(ROOT))
from behavior_lab.methods.learned_plp import PLPRouter, LICENSE_COLS, baseline_predictions

def exact(g,p): return (g[LICENSE_COLS].to_numpy()==p[LICENSE_COLS].to_numpy()).all(1)
def boot(x,reps=5000,seed=11):
    x=np.asarray(x,float); rng=np.random.default_rng(seed)
    vals=np.array([rng.choice(x,len(x),replace=True).mean() for _ in range(reps)])
    return x.mean(),np.quantile(vals,.025),np.quantile(vals,.975)
def binom_two_sided(k,n):
    # exact two-sided for p=.5; stable for modest n using log-gamma
    if n==0:return 1.0
    probs=[]
    def pmf(i): return math.exp(math.lgamma(n+1)-math.lgamma(i+1)-math.lgamma(n-i+1)-n*math.log(2))
    pk=pmf(k)
    return min(1.0,sum(pmf(i) for i in range(n+1) if pmf(i)<=pk+1e-15))
def ece(y,p,bins=10):
    edges=np.linspace(0,1,bins+1); out=0.0
    for i in range(bins):
        m=(p>=edges[i]) & ((p<edges[i+1]) if i<bins-1 else (p<=edges[i+1]))
        if m.any(): out += m.mean()*abs(p[m].mean()-y[m].mean())
    return float(out)

df=pd.read_csv(ROOT/'datasets/provenance/provenancebench.csv')
tr=df[df.split=='train']; va=df[df.split=='val']; router=PLPRouter().fit(tr,va)
sets={s:df[df.split==s].copy() for s in ['test','ood_test','compositional_test']}
pi=ROOT/'datasets/provenance/provenance_intervention_test.csv'
if pi.exists(): sets['provenance_intervention']=pd.read_csv(pi)
rows=[]; text=['# ProvenanceBench — strict statistical report','', 'All intervals are 5,000-resample item bootstraps. Paired exact tests compare Hybrid PLP with the provenance-only baseline. These quantify benchmark-item uncertainty, not model-seed or human-rater uncertainty.','']
for s,d in sets.items():
    hy=router.predict(d,hybrid=True); pr=baseline_predictions(d,'provenance_only'); le=router.predict(d,hybrid=False); probs=router.predict_proba(d)
    g=d[LICENSE_COLS].astype(int)
    eh=exact(g,hy); ep=exact(g,pr); el=exact(g,le)
    m,lo,hi=boot(eh)
    a=int((eh & ~ep).sum()); b=int((ep & ~eh).sum()); p=binom_two_sided(a,a+b)
    e_ece=ece(d.evidence_license.astype(int).to_numpy(),probs.evidence_license_prob.to_numpy())
    rows.append({'split':s,'hybrid_exact':m,'hybrid_ci_low':lo,'hybrid_ci_high':hi,'learned_exact':el.mean(),'provenance_only_exact':ep.mean(),'hybrid_only_correct':a,'baseline_only_correct':b,'paired_exact_p':p,'evidence_head_ece':e_ece})
    text += [f'## {s}','',f'- Hybrid exact: **{m:.3f}** (95% CI {lo:.3f}–{hi:.3f})',f'- Learned exact: **{el.mean():.3f}**',f'- Provenance-only exact: **{ep.mean():.3f}**',f'- Paired discordant cases (Hybrid-only / baseline-only): **{a} / {b}**, exact p={p:.3g}',f'- Evidence-head ECE: **{e_ece:.3f}**','']
pd.DataFrame(rows).to_csv(ROOT/'results/provenancebench_strict_stats.csv',index=False)
(ROOT/'reports/PROVENANCEBENCH_STRICT_STATS.md').write_text('\n'.join(text))
print(pd.DataFrame(rows).to_string(index=False))
