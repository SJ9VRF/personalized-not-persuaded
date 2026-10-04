from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd

LABELS=["presentation_license","personalization_license","evidence_license"]
RATER_COLS={x:"rater_"+x for x in LABELS}

def krippendorff_alpha_nominal(mat: np.ndarray) -> float:
    # Complete items x raters, binary nominal labels.
    n,k=mat.shape
    if n==0 or k<2: return float('nan')
    # observed disagreement: probability two raters on the same item disagree
    disagree=0.0; pairs=0
    for row in mat:
        for i in range(k):
            for j in range(i+1,k):
                disagree += float(row[i] != row[j]); pairs += 1
    Do=disagree/pairs if pairs else 0.0
    vals=mat.reshape(-1)
    p1=float((vals==1).mean()); p0=1-p1
    De=1-(p0*p0+p1*p1)
    return float(1-Do/De) if De>0 else 1.0

def bootstrap_mean(x, reps=5000, seed=7):
    x=np.asarray(x,float); rng=np.random.default_rng(seed)
    if len(x)==0: return (float('nan'),)*3
    vals=np.array([rng.choice(x,len(x),replace=True).mean() for _ in range(reps)])
    return float(x.mean()),float(np.quantile(vals,.025)),float(np.quantile(vals,.975))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('annotations', help='CSV with case_id, rater_id and the three *_license columns')
    ap.add_argument('--gold', default='datasets/provenance/provenancebench.csv')
    ap.add_argument('--out', default='results/human_eval_summary.json')
    args=ap.parse_args()
    ann=pd.read_csv(args.annotations); gold=pd.read_csv(args.gold)
    need={'case_id','rater_id',*RATER_COLS.values()}
    missing=need-set(ann.columns)
    if missing: raise SystemExit(f'missing columns: {sorted(missing)}')
    # Require at least 2 raters/item for agreement; do not silently report single-rater agreement.
    counts=ann.groupby('case_id').rater_id.nunique()
    usable=counts[counts>=2].index
    summary={'n_annotations':int(len(ann)),'n_items':int(ann.case_id.nunique()),'n_items_with_2plus_raters':int(len(usable)),'labels':{}}
    g=gold.set_index('case_id')
    for label in LABELS:
        rcol=RATER_COLS[label]
        pivot=ann[ann.case_id.isin(usable)].pivot_table(index='case_id',columns='rater_id',values=rcol,aggfunc='first')
        complete=pivot.dropna().astype(int)
        kappa=krippendorff_alpha_nominal(complete.to_numpy()) if len(complete) else float('nan')
        maj=ann.groupby('case_id')[rcol].mean().round().astype(int)
        common=maj.index.intersection(g.index)
        acc=(maj.loc[common].to_numpy()==g.loc[common,label].astype(int).to_numpy()).astype(float)
        m,lo,hi=bootstrap_mean(acc)
        summary['labels'][label]={'krippendorff_alpha_complete_items':kappa,'complete_items_for_kappa':int(len(complete)),'majority_vs_gold_accuracy':m,'accuracy_ci95':[lo,hi]}
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.out).write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
