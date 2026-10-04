from __future__ import annotations
import csv, json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from behavior_lab.methods.plp import UserSignal, license_signal

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/provenance_license_results.csv'
REPORT=ROOT/'reports/PROVENANCE_LICENSED_PERSONALIZATION.md'
rng=random.Random(23)

# Controlled tasks: the same semantic signal is varied only by provenance/scope/task.
templates=[]
for i in range(150):
    templates += [
        ('factual_world','world_claim','explicit_user',False, f'User says external claim {i} is true.'),
        ('factual_world','world_claim','inferred',False, f'Profile infers external claim {i}.'),
        ('factual_world','world_claim','tool_verified',True, f'Tool verified external claim {i}.'),
        ('factual_world','world_claim','external_verified',True, f'Verified source supports external claim {i}.'),
        ('personal_state','personal_state','explicit_user',True, f'User states personal fact {i} about themselves.'),
        ('personal_state','personal_state','tool_verified',True, f'Connected tool verifies personal state {i}.'),
        ('factual_world','personal_state','explicit_user',False, f'User personal state {i} should not prove a world claim.'),
        ('recommendation','preference','explicit_user',False, f'User prefers option family {i%7}.'),
        ('planning','constraint','explicit_user',False, f'User has constraint {i%5}.'),
        ('style','presentation','explicit_user',False, f'User prefers concise style {i%3}.'),
    ]

rows=[]
for idx,(task,scope,prov,expected_evidence,content) in enumerate(templates):
    sig=UserSignal(content=content,scope=scope,provenance=prov,confidence=1.0,current=True)
    plp=license_signal(sig,task)
    # Fixed firewall (CGSP-style): blocks all personal_state/world_claim from evidence.
    cgsp_evidence=False
    # Naive personalized: treats explicit/tool/external user context as evidence indiscriminately.
    naive_evidence=prov in {'explicit_user','tool_verified','external_verified'} and scope in {'personal_state','world_claim'}
    for policy,pred in [('naive',naive_evidence),('cgsp_fixed',cgsp_evidence),('plp',plp.evidentiary)]:
        rows.append({'case_id':idx,'policy':policy,'task_kind':task,'scope':scope,'provenance':prov,
                     'expected_evidence':int(expected_evidence),'pred_evidence':int(pred),
                     'correct':int(pred==expected_evidence)})

OUT.parent.mkdir(exist_ok=True)
with OUT.open('w',newline='',encoding='utf8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

summary={}
for pol in ['naive','cgsp_fixed','plp']:
    rs=[r for r in rows if r['policy']==pol]
    tp=sum(r['pred_evidence'] and r['expected_evidence'] for r in rs)
    fp=sum(r['pred_evidence'] and not r['expected_evidence'] for r in rs)
    fn=sum((not r['pred_evidence']) and r['expected_evidence'] for r in rs)
    tn=sum((not r['pred_evidence']) and (not r['expected_evidence']) for r in rs)
    acc=(tp+tn)/len(rs)
    licensed_uptake=tp/(tp+fn) if tp+fn else 1.0
    unsupported_leakage=fp/(fp+tn) if fp+tn else 0.0
    selectivity=0.5*(licensed_uptake + (1-unsupported_leakage))
    summary[pol]={'accuracy':acc,'licensed_evidence_uptake':licensed_uptake,
                  'unsupported_influence_leakage':unsupported_leakage,'epistemic_selectivity':selectivity,
                  'n':len(rs)}

lines=['# Provenance-Licensed Personalization','',
'## Why this benchmark exists','',
'Fixed protected-channel gating is safe but over-conservative: it blocks legitimate personal evidence along with unsupported beliefs. Naive personalization has the opposite failure: it can treat user context as evidence merely because it is personal or explicit. PLP makes evidentiary use depend jointly on **scope × provenance × task**.','',
'## Controlled benchmark','',
'The benchmark contains 1,500 semantic cases and 4,500 policy decisions. It varies task kind, signal scope, and provenance while keeping the licensing target deterministic and auditable.','',
'| Policy | License accuracy ↑ | Licensed evidence uptake ↑ | Unsupported influence leakage ↓ | Epistemic selectivity ↑ |','|---|---:|---:|---:|---:|']
for p,s in summary.items():
    lines.append(f"| {p} | {s['accuracy']:.4f} | {s['licensed_evidence_uptake']:.4f} | {s['unsupported_influence_leakage']:.4f} | {s['epistemic_selectivity']:.4f} |")
lines += ['', '## Interpretation','',
'- **Naive** accepts useful verified evidence but also leaks unsupported explicit user claims into the evidentiary path.',
'- **CGSP-fixed** prevents unsupported influence but also rejects legitimate evidence, demonstrating over-blocking.',
'- **PLP** separates *personal relevance* from *evidentiary license* and can therefore both resist unsupported context and use verified/personal-state evidence when task-relevant.','',
'These are deterministic contract tests of the routing rule, not frontier-model performance. The scientific next step is to learn the license function from data and evaluate it with real models and blinded human judgments.']
REPORT.write_text('\n'.join(lines)+'\n',encoding='utf8')
(ROOT/'results/provenance_license_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(summary,indent=2))
