from behavior_lab.generation.generate import generate

def test_generation_size_and_ids():
    rows=generate(n_per_combo=1)
    assert len(rows)==10*6*4
    assert len({r['scenario_id'] for r in rows})==len(rows)

def test_language_variants_share_split_cluster():
    rows=generate(n_per_combo=1)
    groups={}
    for r in rows:
        k=(r['category'], r['ground_truth']['claim'], r['metadata']['profile_condition'])
        groups.setdefault(k,set()).add(r['metadata']['split'])
    assert all(len(v)==1 for v in groups.values())
