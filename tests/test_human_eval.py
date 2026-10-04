import numpy as np
from scripts.aggregate_human_eval import krippendorff_alpha_nominal

def test_alpha_perfect_agreement():
    m=np.array([[0,0,0],[1,1,1],[0,0,0],[1,1,1]])
    assert krippendorff_alpha_nominal(m)==1.0

def test_alpha_finite_with_disagreement():
    m=np.array([[0,0,1],[1,1,1],[0,1,0],[1,0,1]])
    a=krippendorff_alpha_nominal(m)
    assert -1.0 <= a <= 1.0
