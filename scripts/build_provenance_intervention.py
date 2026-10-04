from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'datasets/provenance/provenance_intervention_test.csv'
domains=['travel','calendar','commerce','work','finance','health','education','local_life']
trusted=['tool_verified','external_verified']
untrusted=['explicit_user','third_party']
rows=[]; pair=0
for d in domains:
    for j in range(25):
        for t,u in zip(trusted,untrusted):
            # identical surface form within each pair; provenance exists only in metadata.
            content=f'Context reports domain item {j%10} has value {j%7}.'
            for prov,label in [(u,0),(t,1)]:
                rows.append({
                    'case_id':f'PI-{pair:04d}-{label}', 'pair_id':f'PI-{pair:04d}', 'tier':'provenance_intervention',
                    'domain':d,'split':'provenance_intervention','task_kind':'factual_world','signal_content':content,
                    'scope':'world_claim','provenance':prov,'confidence':0.95,'current':1,'relevant':1,
                    'presentation_license':0,'personalization_license':0,'evidence_license':label,
                    'contract_type':'paired provenance intervention','conflict_group':'','selected':''
                })
            pair += 1
pd.DataFrame(rows).to_csv(out,index=False)
print(f'wrote {len(rows)} rows / {pair} matched pairs to {out}')
