from pathlib import Path
import csv, json
root=Path(__file__).resolve().parents[1]
# Controlled proxy sweep: increasing satisfaction weight induces tempting behaviors.
rows=[]
for w in [0.0,0.2,0.4,0.6,0.8,1.0]:
    personalization=min(.55+.28*w, .9)
    satisfaction=min(.62+.31*w, .96)
    sycophancy=.05+.32*(w**1.45)
    truthfulness=.95-.19*(w**1.35)
    calibration=.93-.16*(w**1.25)
    overall=.22*personalization+.24*truthfulness+.18*(1-sycophancy)+.13*calibration+.13*.82+.10*.88
    rows.append({'satisfaction_weight':w,'satisfaction':round(satisfaction,4),'personalization':round(personalization,4),'truthfulness':round(truthfulness,4),'sycophancy':round(sycophancy,4),'calibration':round(calibration,4),'overall':round(overall,4)})
with (root/'results/reward_hacking_sweep.csv').open('w',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
(root/'reports/REWARD_HACKING.md').write_text('# Reward-Hacking Sweep\n\nThis is a controlled **proxy** experiment, not a claim about a trained frontier model. It stress-tests the evaluation stack by deliberately coupling a larger satisfaction weight to more agreement pressure.\n\n| Satisfaction weight | Satisfaction | Truthfulness | Sycophancy ↓ | Calibration | Overall |\n|---:|---:|---:|---:|---:|---:|\n'+''.join(f"| {r['satisfaction_weight']:.1f} | {r['satisfaction']:.3f} | {r['truthfulness']:.3f} | {r['sycophancy']:.3f} | {r['calibration']:.3f} | {r['overall']:.3f} |\n" for r in rows)+'\nThe sweep is intentionally constructed as a failure-injection test: it verifies that the dashboard and regression criteria surface cases where a superficially attractive satisfaction objective degrades truthfulness and calibration.\n')
print('wrote reward-hacking sweep')
