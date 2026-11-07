#!/usr/bin/env python3
"""pair_cap_read — the §253 rung-1/rung-4 read of a paired pod run at the operating point (composer, 2026-10-19).

  python3 runs/lib/pair_cap_read.py ARM_MIRROR CONTROL_MIRROR [--heldout ka59,lf52,ls20,r11l,sp80] [--cap 158000]

Reads benchmark.json in each mirror (the harness's own per-game fields: levels_completed, final_generated_tokens,
history length = actions). Prints, verbatim for the book:
  PAIR levels arm A vs control C = diff D over N games (up U / down W / tied T) | held-out A' vs C'
  ECONOMY generated tokens per level arm X vs control Y (ratio R) | tokens per action arm P vs control Q
  CAP: games over 1.05x cap (must be 0 in both arms: the cap was in force) | games binding at 0.9-1.05x
  VERDICT per §253 rung 1/4: CONVERTS (diff >= +4 on 5 games / +6 on 25) | ECONOMY (diff >= 0 and R <= 0.6) | MISS
No fixture file: the dry run is solc vs nulla (known: 29 vs 22, diff -7; both UNCAPPED, so the CAP line must show 5/5 over in both arms)."""
import argparse, glob, json, os, statistics as st

def load(d):
    ps = glob.glob(os.path.join(d, '**', 'benchmark.json'), recursive=True)
    if not ps: raise SystemExit(f"no benchmark.json under {d}")
    per = {}
    for p in ps:
        for g in json.load(open(p)).get('game_runs', []):
            k = g['game_id'][:4]
            r = per.setdefault(k, {'levels': 0, 'tokens': 0, 'actions': 0, 'runs': 0})
            r['levels'] += g.get('levels_completed', 0); r['tokens'] += g.get('final_generated_tokens') or 0
            r['actions'] += len(g.get('history', [])); r['runs'] += 1
    # the harness's final_generated_tokens is unset on our pod mirrors: fall back to the request logs' usage rows
    if sum(r['tokens'] for r in per.values()) == 0:
        for f in glob.glob(os.path.join(d, '**', '*_p*_requests.jsonl'), recursive=True):
            k = os.path.basename(f)[:4]
            if k not in per: continue
            for line in open(f, errors='ignore'):
                try: u = json.loads(line).get('usage')
                except Exception: continue
                if u: per[k]['tokens'] += u.get('completion_tokens', 0)
    return per

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('arm'); ap.add_argument('control')
    ap.add_argument('--heldout', default='ka59,lf52,ls20,r11l,sp80'); ap.add_argument('--cap', type=int, default=158000)
    a = ap.parse_args(); A = load(a.arm); C = load(a.control)
    common = sorted(set(A) & set(C)); held = [g for g in a.heldout.split(',') if g in common]
    d = [A[g]['levels'] - C[g]['levels'] for g in common]
    la, lc = sum(A[g]['levels'] for g in common), sum(C[g]['levels'] for g in common)
    ha, hc = sum(A[g]['levels'] for g in held), sum(C[g]['levels'] for g in held)
    ta, tc = sum(A[g]['tokens'] for g in common), sum(C[g]['tokens'] for g in common)
    aa, ac = sum(A[g]['actions'] for g in common), sum(C[g]['actions'] for g in common)
    tpl_a = ta / max(la, 1); tpl_c = tc / max(lc, 1); ratio = tpl_a / tpl_c if tpl_c else float('nan')
    runs_a = max(A[g]['runs'] for g in common); runs_c = max(C[g]['runs'] for g in common)
    over_a = sum(1 for g in common if A[g]['tokens'] / A[g]['runs'] > 1.05 * a.cap)
    over_c = sum(1 for g in common if C[g]['tokens'] / C[g]['runs'] > 1.05 * a.cap)
    cap_a = sum(1 for g in common if 0.9 * a.cap <= A[g]['tokens'] / A[g]['runs'] <= 1.05 * a.cap)
    cap_c = sum(1 for g in common if 0.9 * a.cap <= C[g]['tokens'] / C[g]['runs'] <= 1.05 * a.cap)
    n = len(common); bar = 4 if n <= 10 else 6
    print(f"PAIR levels arm {la} vs control {lc} = diff {la-lc:+d} over {n} games (up {sum(x>0 for x in d)} / down {sum(x<0 for x in d)} / tied {sum(x==0 for x in d)}) | held-out {ha} vs {hc} ({len(held)} games) | passes arm {runs_a} control {runs_c}")
    print(f"ECONOMY generated tokens per level arm {tpl_a:,.0f} vs control {tpl_c:,.0f} (ratio {ratio:.2f}) | tokens per action arm {ta/max(aa,1):,.0f} vs control {tc/max(ac,1):,.0f}")
    print(f"CAP {a.cap:,} per game-pass: over the cap arm {over_a}/{n} control {over_c}/{n} (must be 0/0: the cap was in force) | binding (0.9-1.05x) arm {cap_a}/{n} control {cap_c}/{n}")
    print("PER-GAME " + " ".join(f"{g}:{A[g]['levels']}/{C[g]['levels']}" for g in common))
    v = 'CONVERTS' if la - lc >= bar else ('ECONOMY' if la - lc >= 0 and ratio <= 0.6 else 'MISS')
    print(f"VERDICT per §253 (bar {bar:+d} on {n} games; economy = diff >= 0 and ratio <= 0.6): {v}")
main()
