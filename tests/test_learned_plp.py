import pandas as pd
from behavior_lab.methods.learned_plp import PLPRouter, LICENSE_COLS, metric_bundle

def tiny():
    rows=[]
    provs=['explicit_user','tool_verified','inferred','external_verified']
    scopes=['preference','world_claim','personal_state','style']
    for i in range(80):
        p=provs[i%4]; s=scopes[i%4]
        evidence=int(p in ['tool_verified','external_verified'] and s in ['world_claim','personal_state'])
        rows.append(dict(signal_content=f'signal {p} {s} {i%7}',scope=s,provenance=p,task_kind='factual_world' if s=='world_claim' else 'planning',domain='x',tier='controlled',confidence=0.95,current=1,relevant=1,presentation_license=int(s=='style'),personalization_license=int(s in ['style','preference','personal_state']),evidence_license=evidence))
    return pd.DataFrame(rows)

def test_router_trains_and_predicts():
    d=tiny(); tr=d.iloc[:56]; va=d.iloc[56:68]; te=d.iloc[68:]
    r=PLPRouter().fit(tr,va)
    p=r.predict(te,hybrid=True)
    assert list(p.columns)==LICENSE_COLS
    assert metric_bundle(te,p)['exact_license_match'] >= .5

def test_hybrid_invalidates_stale_context():
    d=tiny(); tr=d.iloc[:56]; va=d.iloc[56:68]; te=d.iloc[68:].copy()
    r=PLPRouter().fit(tr,va)
    te.loc[te.index[0],'current']=0
    p=r.predict(te,hybrid=True)
    assert p.loc[te.index[0],LICENSE_COLS].sum()==0
