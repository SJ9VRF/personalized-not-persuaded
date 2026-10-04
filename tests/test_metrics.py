from behavior_lab.metrics import incorrect_personalization_rate, personality_drift, repetition_concession_slope


def test_personality_drift_zero_for_identical_vectors():
    assert personality_drift([0.1, 0.8], [0.1, 0.8]) == 0.0


def test_incorrect_personalization_rate():
    assert incorrect_personalization_rate([True, False, True, False]) == 0.5


def test_repetition_concession_slope_positive():
    assert repetition_concession_slope([0.1, 0.2, 0.4, 0.7]) > 0
