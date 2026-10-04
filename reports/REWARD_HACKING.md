# Reward-Hacking Sweep

This is a controlled **proxy** experiment, not a claim about a trained frontier model. It stress-tests the evaluation stack by deliberately coupling a larger satisfaction weight to more agreement pressure.

| Satisfaction weight | Satisfaction | Truthfulness | Sycophancy ↓ | Calibration | Overall |
|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.620 | 0.950 | 0.050 | 0.930 | 0.836 |
| 0.2 | 0.682 | 0.928 | 0.081 | 0.909 | 0.834 |
| 0.4 | 0.744 | 0.895 | 0.135 | 0.879 | 0.825 |
| 0.6 | 0.806 | 0.855 | 0.203 | 0.846 | 0.811 |
| 0.8 | 0.868 | 0.809 | 0.281 | 0.809 | 0.794 |
| 1.0 | 0.930 | 0.760 | 0.370 | 0.770 | 0.773 |

The sweep is intentionally constructed as a failure-injection test: it verifies that the dashboard and regression criteria surface cases where a superficially attractive satisfaction objective degrades truthfulness and calibration.
