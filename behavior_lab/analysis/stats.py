from __future__ import annotations
import random, math

def mean(xs): return sum(xs)/len(xs) if xs else float('nan')

def bootstrap_ci(xs, n_boot=1000, seed=7, alpha=.05):
    if not xs: return (float('nan'),float('nan'))
    rng=random.Random(seed); n=len(xs); vals=[]
    for _ in range(n_boot): vals.append(mean([xs[rng.randrange(n)] for _ in range(n)]))
    vals.sort(); lo=int((alpha/2)*n_boot); hi=int((1-alpha/2)*n_boot)-1
    return vals[lo], vals[max(lo,hi)]

def paired_effect(a,b):
    ds=[x-y for x,y in zip(a,b)]
    m=mean(ds)
    if len(ds)<2: return m, float('nan')
    var=sum((d-m)**2 for d in ds)/(len(ds)-1)
    sd=math.sqrt(var)
    return m, (m/sd if sd else 0.0)
