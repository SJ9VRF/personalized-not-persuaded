from behavior_lab.policies.baselines import POLICIES
from behavior_lab.eval.scorer import score
from behavior_lab.generation.generate import generate

def test_behavior_proxy_avoids_sycophancy_on_factual_cases():
    s=next(r for r in generate(n_per_combo=1) if r['category']=='factual_disagreement' and r['metadata']['profile_condition']=='P5')
    naive=score(s,POLICIES['naive_personalized'](s))
    good=score(s,POLICIES['behavior_trained_proxy'](s))
    assert good['truthfulness']>naive['truthfulness']
    assert good['sycophancy']<naive['sycophancy']
