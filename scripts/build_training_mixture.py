from pathlib import Path
import sys, json, random
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from behavior_lab.post_training.curriculum import build_training_example

SEED = 17
rng = random.Random(SEED)
df = pd.read_csv(ROOT / 'results/provenancebench_predictions.csv')
rows = df.to_dict(orient='records')
corrections=[]; anchors=[]
for r in rows:
    ex=build_training_example(r, method='hybrid')
    if ex is not None:
        ex['mixture_role']='failure_correction'; corrections.append(ex)
    else:
        anchors.append({
            'example_id': f"ANCHOR-{r['case_id']}", 'source_case_id': str(r['case_id']),
            'split': str(r.get('split_eval', r.get('split','unknown'))), 'mixture_role':'stability_anchor',
            'priority': 1.0,
            'input': {k:(bool(r[k]) if k in ['current','relevant'] else float(r[k]) if k=='confidence' else r[k]) for k in ['task_kind','signal_content','scope','provenance','confidence','current','relevant']},
            'observed_licenses': {c:int(r[f'hybrid_{c}_license']) for c in ['presentation','personalization','evidence']},
            'target_licenses': {c:int(r[f'{c}_license']) for c in ['presentation','personalization','evidence']},
            'training_target': {'type':'stability_anchor','supervision':{c:int(r[f'{c}_license']) for c in ['presentation','personalization','evidence']}, 'rationale':'Preserve a currently correct licensing decision while correcting nearby failures.'}
        })
# Use an equal number of anchors so the mixture does not teach only error correction.
rng.shuffle(anchors)
anchors=anchors[:len(corrections)]
mixture=corrections+anchors
rng.shuffle(mixture)
out=ROOT/'datasets/post_training/training_mixture.jsonl'; out.parent.mkdir(parents=True,exist_ok=True)
out.write_text('\n'.join(json.dumps(x,sort_keys=True) for x in mixture)+'\n')
manifest={'seed':SEED,'n_total':len(mixture),'n_failure_corrections':len(corrections),'n_stability_anchors':len(anchors),
          'intended_use':'SFT/preference-data seed for a real post-training experiment; not evidence that training has been run.',
          'design':'Balanced failure corrections with stability anchors to reduce regression risk.'}
(ROOT/'results/training_mixture_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps(manifest,indent=2))
