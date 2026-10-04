from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
out=root/'figures'; out.mkdir(exist_ok=True)
df=pd.read_csv(root/'results/benchmark_results.csv')
# Tradeoff
m=df.groupby('policy').mean(numeric_only=True)
fig,ax=plt.subplots(figsize=(7,5))
for p,r in m.iterrows():
    ax.scatter(r['truthfulness'],r['personalization'],s=90); ax.annotate(p,(r['truthfulness'],r['personalization']),xytext=(6,6),textcoords='offset points')
ax.set_xlabel('Truthfulness'); ax.set_ylabel('Personalization'); ax.set_title('Personalization–Truthfulness Tradeoff (Proxy Eval)'); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(out/'tradeoff.png',dpi=180); plt.close(fig)
# Sycophancy
fig,ax=plt.subplots(figsize=(7,4)); m['sycophancy'].sort_values().plot(kind='bar',ax=ax); ax.set_ylabel('Sycophancy (lower is better)'); ax.set_title('Held-out Sycophancy'); ax.grid(axis='y',alpha=.25); fig.tight_layout(); fig.savefig(out/'sycophancy.png',dpi=180); plt.close(fig)
# Long horizon
lh=pd.read_csv(root/'results/long_horizon.csv'); q=lh.groupby(['policy','horizon']).drift.mean().reset_index()
fig,ax=plt.subplots(figsize=(7,4.5))
for p,g in q.groupby('policy'): ax.plot(g.horizon,g.drift,marker='o',label=p)
ax.set_xscale('log'); ax.set_xlabel('Conversation horizon (synthetic stress steps)'); ax.set_ylabel('Personality drift'); ax.set_title('Long-horizon Stress Simulator'); ax.legend(); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(out/'long_horizon.png',dpi=180); plt.close(fig)
# Reward hacking
rh=pd.read_csv(root/'results/reward_hacking_sweep.csv'); fig,ax=plt.subplots(figsize=(7,4.5))
ax.plot(rh.satisfaction_weight,rh.truthfulness,marker='o',label='truthfulness'); ax.plot(rh.satisfaction_weight,rh.sycophancy,marker='o',label='sycophancy'); ax.plot(rh.satisfaction_weight,rh.calibration,marker='o',label='calibration'); ax.set_xlabel('Injected satisfaction weight'); ax.set_ylabel('Score'); ax.set_title('Failure-injection Reward-Hacking Sweep'); ax.legend(); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(out/'reward_hacking.png',dpi=180); plt.close(fig)
print('wrote figures')
