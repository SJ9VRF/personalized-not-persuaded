from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def test_contract_dataset_is_exactly_paired():
    p=ROOT/'datasets/contracts/counterfactual_personalization_contracts_v1.jsonl'
    assert p.exists()
    rows=[json.loads(x) for x in p.read_text(encoding='utf8').splitlines() if x.strip()]
    groups={}
    for r in rows:
        groups.setdefault(r['contract_id'], set()).add(r['metadata']['profile_condition'])
    assert len(groups) >= 800
    assert all(v == {'P0','P1','P2','P3','P4','P5'} for v in groups.values())

def test_contract_summary_exists_and_has_policies():
    import pandas as pd
    p=ROOT/'results/counterfactual_contract_summary.csv'
    assert p.exists()
    df=pd.read_csv(p)
    assert {'generic','naive_personalized','behavior_trained_proxy','cgsp'} <= set(df.policy)
    assert {'allowed_personalization_gain','protected_epistemic_drift','cross_channel_interference','contract_pass_rate'} <= set(df.columns)
