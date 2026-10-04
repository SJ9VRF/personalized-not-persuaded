from __future__ import annotations
from pathlib import Path
import json, pickle, random, re
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, accuracy_score, roc_auc_score

CAT_COLS=['category','language','profile']
CUES={
 'agreement':['yes','you\'re right','conclusion makes sense','definitely','exactly what happened'],
 'uncertainty':['not enough evidence','does not support','isn\'t established','can\'t give a guarantee','main risks','evidence'],
 'personalization':['your preference','what i know about you','prior views','current instruction','standing preference','adapting to your'],
 'empathy':['sounds difficult','genuinely hard','annoying','feeling is real','without minimizing'],
 'grounding':['evidence','criteria','reasoning','risks','next steps'],
 'directness':['direct','concise','specifically','not quite'],
}

def lexical_features(text: str):
    t=str(text).lower()
    feats={f'lex_{k}':sum(t.count(c) for c in vals) for k,vals in CUES.items()}
    feats.update({'lex_len':min(len(t)/300.0,2.0),'lex_hedge':sum(t.count(c) for c in ['might','may','could','probably'])})
    return feats

LEX_COLS=[f'lex_{k}' for k in CUES]+['lex_len','lex_hedge']


def _group_split(df: pd.DataFrame, frac=.8, seed=19):
    ids=list(df['scenario_id'].unique())
    rng=random.Random(seed); rng.shuffle(ids)
    cut=max(1,int(len(ids)*frac)); train_ids=set(ids[:cut])
    return df[df.scenario_id.isin(train_ids)].copy(), df[~df.scenario_id.isin(train_ids)].copy()


def _reward_pipeline():
    pre=ColumnTransformer([
        ('text', TfidfVectorizer(ngram_range=(1,2), min_df=1, max_features=4000), 'response'),
        ('cat', OneHotEncoder(handle_unknown='ignore'), CAT_COLS),
    ])
    return Pipeline([('pre',pre),('model',Ridge(alpha=2.0))])


def _pair_pipeline():
    pre=ColumnTransformer([
        ('cat',OneHotEncoder(handle_unknown='ignore'),CAT_COLS),
        ('num',StandardScaler(),LEX_COLS),
    ])
    return Pipeline([('pre',pre),('model',LogisticRegression(max_iter=2000,C=1.0))])


def train_reward_models(root: Path):
    df=pd.read_csv(root/'results/benchmark_results.csv')
    train,test=_group_split(df,.8,19)
    pipe=_reward_pipeline(); pipe.fit(train,train['overall'])
    pred=pipe.predict(test); mae=float(mean_absolute_error(test['overall'],pred))

    pairs=[]; rng=random.Random(5)
    for sid,g in df.groupby('scenario_id'):
        rs=g.to_dict('records')
        if len(rs)<2: continue
        for _ in range(min(2,len(rs))):
            a,b=rng.sample(rs,2)
            if abs(float(a['overall'])-float(b['overall'])) < 1e-9: continue
            fa,fb=lexical_features(a['response']),lexical_features(b['response'])
            row={'scenario_id':sid,'category':a['category'],'language':a['language'],'profile':a['profile'],
                 'response_a':a['response'],'response_b':b['response'],'label':int(float(a['overall'])>float(b['overall'])),
                 'margin':round(float(a['overall'])-float(b['overall']),6)}
            for c in LEX_COLS: row[c]=fa[c]-fb[c]
            pairs.append(row)
    pdf=pd.DataFrame(pairs)
    ptrain,ptest=_group_split(pdf,.8,3)
    clf=_pair_pipeline(); clf.fit(ptrain,ptrain['label'])
    ppred=clf.predict(ptest); acc=float(accuracy_score(ptest['label'],ppred))
    try: auc=float(roc_auc_score(ptest['label'],clf.predict_proba(ptest)[:,1]))
    except Exception: auc=float('nan')

    metrics={
        'reward_regression_mae':mae,'pairwise_preference_accuracy':acc,'pairwise_preference_auc':auc,
        'n_candidates':int(len(df)),'n_pairs':int(len(pdf)),
        'reward_train_scenarios':int(train.scenario_id.nunique()),'reward_test_scenarios':int(test.scenario_id.nunique()),
        'note':'Reward model consumes response text + scenario metadata. Pairwise model consumes only differences in auditable lexical cues + metadata; no rubric component scores are used as features.'
    }
    (root/'results/reward_model_metrics.json').write_text(json.dumps(metrics,indent=2))
    with (root/'results/reward_model.pkl').open('wb') as f: pickle.dump(pipe,f)
    with (root/'results/preference_model.pkl').open('wb') as f: pickle.dump(clf,f)
    pdf.to_csv(root/'datasets/preferences/pairwise_preferences.csv',index=False)
    return metrics

if __name__=='__main__':
    root=Path(__file__).resolve().parents[2]
    print(train_reward_models(root))
