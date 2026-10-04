"""Frozen adapter harness for real-model generation experiments.

An adapter module must expose:
    generate(example: dict, licenses: dict) -> str

This script intentionally does not contain provider credentials. It produces a
JSONL of model outputs that can be blindly human-scored or passed to a separately
calibrated grader. This keeps generation compliance distinct from license-routing
accuracy.
"""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def load_adapter(path):
    spec=importlib.util.spec_from_file_location('pnp_adapter',path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    if not hasattr(mod,'generate'): raise ValueError('adapter must expose generate(example, licenses)')
    return mod.generate

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('adapter'); ap.add_argument('--split',default='test'); ap.add_argument('--limit',type=int,default=0); ap.add_argument('--out',default='results/generation_outputs.jsonl'); args=ap.parse_args()
    df=pd.read_csv(ROOT/'datasets/provenance/provenancebench.csv'); df=df[df.split==args.split].copy()
    if args.limit: df=df.head(args.limit)
    gen=load_adapter(args.adapter); out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w') as f:
        for _,r in df.iterrows():
            licenses={k:int(r[k]) for k in ['presentation_license','personalization_license','evidence_license']}
            response=gen(r.to_dict(),licenses)
            f.write(json.dumps({'case_id':r.case_id,'split':args.split,'licenses':licenses,'response':response},ensure_ascii=False)+'\n')
    print(f'wrote {len(df)} outputs to {out}')
if __name__=='__main__': main()
