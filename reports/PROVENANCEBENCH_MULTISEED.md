# ProvenanceBench — multi-seed stability

Ten logistic-router fits use different solver random states; validation threshold selection is repeated per fit.

```
                                    exact_license_match      evidence_uptake      unsupported_leakage     
                                                   mean  std            mean  std                mean  std
split                   method                                                                            
compositional_test      hybrid_plp             0.800000  0.0             0.5  0.0            0.000000  0.0
                        learned_plp            0.400000  0.0             0.5  0.0            0.666667  0.0
ood_test                hybrid_plp             0.947368  0.0             0.8  0.0            0.000000  0.0
                        learned_plp            0.842105  0.0             0.8  0.0            0.142857  0.0
provenance_intervention hybrid_plp             0.750000  0.0             0.5  0.0            0.000000  0.0
                        learned_plp            0.750000  0.0             0.5  0.0            0.000000  0.0
test                    hybrid_plp             1.000000  0.0             1.0  0.0            0.000000  0.0
                        learned_plp            1.000000  0.0             1.0  0.0            0.000000  0.0
```

This does not substitute for multi-seed neural-model training, but it checks whether the reported linear-router result is an initialization artifact.