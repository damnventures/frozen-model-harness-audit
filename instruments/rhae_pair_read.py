#!/usr/bin/env python3
"""rhae_pair_read.py ARM_MIRROR CONTROL_MIRROR [--tokens]
The score Kaggle computes, read from benchmark.json final_score per game (RHAE: per-level efficiency min(1.15,(h/a)^2),
levels weighted by index, capped at the completed weight share), paired per game with a standard error, beside the
levels count. §335: RHAE is the primary read of every pair from 2026-10-26; levels are secondary.
"""
import json, glob, os, sys, math, statistics as st
def games(M):
    """One record per game. Multi-pass mirrors (n_passes > 1) are reduced to per-game MEANS over passes (final_score and
    levels_completed), so a four-pass pair reads per-game four-pass means (§363); single-pass mirrors are unchanged."""
    d = json.load(open(os.path.join(M, 'benchmark.json'))); by = {}
    for x in d['game_runs']: by.setdefault(x['game_id'][:4], []).append(x)
    out = {}
    for g, xs in by.items():
        if len(xs) == 1: out[g] = xs[0]; continue
        r = dict(xs[-1]); r['final_score'] = sum(float(x.get('final_score') or 0) for x in xs) / len(xs)
        r['levels_completed'] = sum(x.get('levels_completed', 0) for x in xs) / len(xs); r['passes'] = len(xs); out[g] = r
    return out
def tokens(M):
    out = {}
    for f in glob.glob(os.path.join(M, '*_requests.jsonl')):
        g = os.path.basename(f)[:4]; t = 0
        for l in open(f):
            try: r = json.loads(l)
            except Exception: continue
            u = r.get('usage') or (r.get('response') or {}).get('usage') or {}
            t += u.get('completion_tokens', 0) or 0
        out[g] = out.get(g, 0) + t
    return out
def main(a):
    A, C = games(a[0]), games(a[1]); common = [g for g in A if g in C]
    dS = [(A[g].get('final_score') or 0) - (C[g].get('final_score') or 0) for g in common]
    dL = [A[g]['levels_completed'] - C[g]['levels_completed'] for g in common]
    SA = sum((A[g].get('final_score') or 0) for g in common) / len(common); SC = sum((C[g].get('final_score') or 0) for g in common) / len(common)
    se = st.stdev(dS) / math.sqrt(len(dS)) if len(dS) > 1 else float('nan')
    up = sum(1 for d in dS if d > 0.5); dn = sum(1 for d in dS if d < -0.5)
    print(f"RHAE arm {SA:.2f} vs control {SC:.2f} = {st.mean(dS):+.2f} ± {se:.2f} s.e. over {len(common)} games (up {up} / down {dn} / tied {len(common)-up-dn}) | levels {sum(A[g]['levels_completed'] for g in common)} vs {sum(C[g]['levels_completed'] for g in common)} ({sum(dL):+.0f})")
    deep = [(g, A[g]['levels_completed'], C[g]['levels_completed'], round((A[g].get('final_score') or 0) - (C[g].get('final_score') or 0), 1)) for g in common]
    deep.sort(key=lambda r: -abs(r[3])); print("largest per-game RHAE moves:", deep[:6])
    if '--tokens' in a:
        TA, TC = tokens(a[0]), tokens(a[1])
        print(f"tokens/game median arm {st.median([TA.get(g,0) for g in common])/1000:.0f}K vs control {st.median([TC.get(g,0) for g in common])/1000:.0f}K")
    bar = 4.0
    print(f"VERDICT §335 (bar +{bar:.0f} RHAE paired AND diff > 1 s.e.): {'CONVERTS' if st.mean(dS) >= bar and st.mean(dS) > se else 'MISS'}")
if __name__ == '__main__': main([x for x in sys.argv[1:] if not x.startswith('--')] + [x for x in sys.argv[1:] if x.startswith('--')])
