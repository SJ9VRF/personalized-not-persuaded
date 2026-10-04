from pathlib import Path
import json, csv, html, statistics, sys
root=Path(__file__).resolve().parents[1]
summary=json.loads((root/'results/summary.json').read_text())
rm=json.loads((root/'results/reward_model_metrics.json').read_text())
with (root/'results/long_horizon.csv').open() as f: lh=list(csv.DictReader(f))
policies=list(summary)
metric_order=['overall','personalization','truthfulness','sycophancy','calibration','emotional_appropriateness','personality_consistency']
rows=''.join('<tr><td>'+html.escape(p)+'</td>'+''.join(f"<td>{summary[p][m]['mean']:.3f}</td>" for m in metric_order)+'</tr>' for p in policies)
# long horizon means
lmeans=[]
for p in policies:
  for h in [1,10,25,50,100,200]:
    vals=[float(r['drift']) for r in lh if r['policy']==p and int(r['horizon'])==h]
    lmeans.append((p,h,sum(vals)/len(vals)))
chart_data=json.dumps(lmeans)
html_doc=f"""<!doctype html><html><head><meta charset="utf-8"><title>Model Behavior Lab Dashboard</title><style>
body{{font-family:Inter,system-ui,sans-serif;margin:0;background:#0b0d12;color:#eef2f7}} .wrap{{max-width:1180px;margin:auto;padding:48px 24px}} h1{{font-size:52px;line-height:1.0;margin:0 0 12px}} .sub{{color:#aeb8c5;font-size:20px;max-width:850px}} .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:32px 0}} .card{{background:#141821;border:1px solid #262d39;border-radius:16px;padding:20px}} .num{{font-size:30px;font-weight:700}} table{{width:100%;border-collapse:collapse;background:#141821;border-radius:16px;overflow:hidden}} th,td{{padding:12px;border-bottom:1px solid #262d39;text-align:right}} th:first-child,td:first-child{{text-align:left}} .good{{color:#8de2b1}} .warn{{color:#ffcf7b}} canvas{{width:100%;height:320px;background:#141821;border-radius:16px;margin-top:20px}} .note{{color:#aeb8c5;font-size:14px;margin-top:14px}}</style></head><body><div class="wrap">
<h1>Model Behavior Lab</h1><div class="sub">Local, reproducible evaluation of personalization, truthfulness, sycophancy, emotional appropriateness, personality stability, and multi-objective reward modeling.</div>
<div class="grid"><div class="card"><div class="num">{sum(1 for _ in open(root/'datasets/behaviorbench/behaviorbench_v1.jsonl')):,}</div><div>Benchmark scenarios</div></div><div class="card"><div class="num">{rm['n_pairs']:,}</div><div>Preference pairs</div></div><div class="card"><div class="num">{rm['pairwise_preference_accuracy']:.3f}</div><div>Preference-model accuracy</div></div><div class="card"><div class="num">{rm['reward_regression_mae']:.4f}</div><div>Reward-model MAE</div></div></div>
<h2>Held-out benchmark</h2><table><thead><tr><th>Policy</th>{''.join('<th>'+m.replace('_',' ').title()+'</th>' for m in metric_order)}</tr></thead><tbody>{rows}</tbody></table>
<div class="note">Sycophancy is a harm metric: lower is better. All other displayed metrics are higher-is-better. Scores come from the local proxy evaluator; they are not human-study claims.</div>
<h2>Long-horizon personality drift</h2><canvas id="c" width="1100" height="340"></canvas><div class="note">Normalized L2 personality drift over simulated stress trajectories. Lower is better.</div>
<script>
const data={chart_data}; const c=document.getElementById('c'),x=c.getContext('2d'); const W=c.width,H=c.height,ml=55,mr=25,mt=25,mb=45; const hs=[1,10,25,50,100,200]; const ps=[...new Set(data.map(d=>d[0]))];
x.strokeStyle='#485366';x.fillStyle='#aeb8c5';x.font='13px sans-serif'; for(let i=0;i<=5;i++){{let y=mt+(H-mt-mb)*i/5;x.beginPath();x.moveTo(ml,y);x.lineTo(W-mr,y);x.stroke();x.fillText((0.3*(1-i/5)).toFixed(2),8,y+4)}}
hs.forEach((h,i)=>{{let xx=ml+(W-ml-mr)*i/(hs.length-1);x.fillText(h,xx-8,H-16)}}); const colors=['#7dd3fc','#f0abfc','#86efac']; ps.forEach((p,pi)=>{{let arr=data.filter(d=>d[0]===p);x.strokeStyle=colors[pi];x.lineWidth=3;x.beginPath();arr.forEach((d,i)=>{{let xx=ml+(W-ml-mr)*i/(arr.length-1), yy=mt+(H-mt-mb)*(1-d[2]/.3); if(i===0)x.moveTo(xx,yy);else x.lineTo(xx,yy)}});x.stroke();x.fillStyle=colors[pi];x.fillText(p,W-260,28+20*pi)}});
</script></div></body></html>"""
(root/'dashboard/index.html').write_text(html_doc)
print(root/'dashboard/index.html')
