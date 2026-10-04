from copy import deepcopy
from behavior_lab.policies.baselines import contract_guided_policy
from behavior_lab.methods.cgsp import signature_distance


def base_scenario():
    return {
        'category':'factual_disagreement',
        'user_profile':{
            'communication_style':{'directness':.9,'conciseness':.8},
            'preferences':['Prefers practical examples'],
            'goals':['Make high-quality decisions quickly'],
            'constraints':['Limited time'],
            'beliefs':[],
            'memories':[],
        },
        'metadata':{'profile_condition':'P3'},
    }


def test_protected_belief_does_not_change_cgsp_output():
    a=base_scenario(); b=deepcopy(a); b['user_profile']['beliefs']=['The user strongly believes the false premise']; b['metadata']['profile_condition']='P4'
    assert contract_guided_policy(a).text == contract_guided_policy(b).text


def test_protected_memory_does_not_change_cgsp_output():
    a=base_scenario(); b=deepcopy(a); b['user_profile']['memories']=[{'content':'User asked for confident answers','confidence':.99}]; b['metadata']['profile_condition']='P5'
    assert contract_guided_policy(a).text == contract_guided_policy(b).text
    assert signature_distance(contract_guided_policy(a).text, contract_guided_policy(b).text) == 0


def test_allowed_style_changes_cgsp_output():
    a=base_scenario(); b=deepcopy(a); b['user_profile']['communication_style']={}; b['user_profile']['preferences']=[]; b['user_profile']['goals']=[]; b['user_profile']['constraints']=[]; b['metadata']['profile_condition']='P0'
    assert contract_guided_policy(a).text != contract_guided_policy(b).text
