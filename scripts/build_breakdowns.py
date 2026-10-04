from pathlib import Path
import pandas as pd
root=Path(__file__).resolve().parents[1]
df=pd.read_csv(root/'results/benchmark_results.csv')
metrics=['overall','personalization','truthfulness','sycophancy','calibration','emotional_appropriateness','personality_consistency']
for key in ['category','language','profile']:
    out=df.groupby(['policy',key])[metrics].mean().reset_index()
    out.to_csv(root/f'results/by_{key}.csv',index=False)
print('wrote category/language/profile breakdowns')
