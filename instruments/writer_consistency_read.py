#!/usr/bin/env python3
"""writer_consistency_read.py — the writer measured without ground truth (register row writer-consistency, book §388/§390).

  python3 runs/lib/writer_consistency_read.py MIRROR [MIRROR ...] [--baseline MIRROR ...] [--boot 2000] [--seed 1]

Each MIRROR holds cross_game_cards.jsonl. Cleared-level notes are grouped by (game, level). A SAME-LEVEL pair is two
notes for the same game-level from DIFFERENT sources (different mirrors, or different passes inside one mirror); a
DIFFERENT-LEVEL pair takes the first note against a note for the same game at another level. The read is the ratio of
mean similarities (Jaccard on content words; tf-idf cosine), with a bootstrap band over the pair set.
--baseline: extra mirrors used only to print the same read for comparison (e.g. the thinking-off four-pass mirrors).
"""
import argparse, collections, itertools, json, math, os, random, re, statistics as st, sys

STOP = set("the a an of to and or in on at is are was were it its this that with by for from as be not no one two three into onto when then you your each only".split())

def words(t): return set(w for w in re.findall(r"[a-z]+", t.lower()) if w not in STOP and len(w) > 2)

def load(mirrors):
    cards = []
    for m in mirrors:
        f = os.path.join(m, "cross_game_cards.jsonl")
        if not os.path.exists(f):
            print(f"no cards file in {m}", file=sys.stderr); continue
        for i, l in enumerate(open(f, errors="ignore")):
            try: r = json.loads(l)
            except Exception: continue
            if r.get("rule") and r.get("kind", "cleared") == "cleared" and "GOAL" in r["rule"] and "excerpt" not in r["rule"][:40].lower():  # §391: a note, never an excerpt fallback
                # source = mirror + pass index when the file carries one, else the mirror (then same-level pairs need >1 mirror)
                src = f"{m}#{r.get('pass', r.get('p', ''))}" if r.get("pass") is not None or r.get("p") is not None else m
                cards.append(dict(game=str(r["key"])[:4], level=int(r.get("level", 0) or 0), rule=r["rule"], src=src, t=float(r.get("t", i))))
    return cards

def pairs(cards, per=6, rng=random):
    by = collections.defaultdict(list)
    for c in cards: by[(c["game"], c["level"])].append(c)
    W, B = [], []
    for (g, lv), cs in by.items():
        srcs = collections.defaultdict(list)
        for c in cs: srcs[c["src"]].append(c)
        ss = list(srcs)
        if len(ss) < 2:
            # one source only: treat each note as its own write when there are >=2 notes (passes without a pass field)
            if len(cs) < 2: continue
            ss = list(range(len(cs))); srcs = {i: [cs[i]] for i in ss}
        for a, b in itertools.combinations(rng.sample(ss, min(per, len(ss))), 2):
            ca, cb = rng.choice(srcs[a]), rng.choice(srcs[b])
            others = [c for (g2, l2), cs2 in by.items() if g2 == g and l2 != lv for c in cs2]
            if not others: continue
            co = rng.choice(others)
            W.append((ca, cb)); B.append((ca, co))
    return W, B, len(by)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("mirrors", nargs="+"); ap.add_argument("--baseline", nargs="*", default=[])
    ap.add_argument("--boot", type=int, default=2000); ap.add_argument("--seed", type=int, default=1); a = ap.parse_args()
    rng = random.Random(a.seed)
    def read(label, cards):
        if not cards: print(f"{label}: no cleared notes"); return
        docs = [words(c["rule"]) for c in cards]; df = collections.Counter(w for d in docs for w in d); N = len(docs)
        def vec(ws): return {w: math.log(N / (1 + df[w])) for w in ws}
        def cos(x, y):
            vx, vy = vec(x), vec(y); num = sum(vx[w] * vy[w] for w in vx if w in vy)
            den = math.sqrt(sum(v * v for v in vx.values())) * math.sqrt(sum(v * v for v in vy.values())); return num / den if den else 0.0
        W, B, nlev = pairs(cards, rng=rng)
        if not W: print(f"{label}: no same-level pairs (one note per level?)"); return
        def sims(P, f): return [f(words(x["rule"]), words(y["rule"])) for x, y in P]
        jac = lambda x, y: len(x & y) / max(1, len(x | y))
        for name, f in (("jaccard", jac), ("tf-idf cosine", cos)):
            w, b = sims(W, f), sims(B, f); r = st.mean(w) / st.mean(b)
            rs = []
            for _ in range(a.boot):
                idx = [rng.randrange(len(w)) for _ in range(len(w))]
                rs.append(st.mean(w[i] for i in idx) / st.mean(b[i] for i in idx))
            rs.sort(); lo, hi = rs[int(0.05 * a.boot)], rs[int(0.95 * a.boot)]
            print(f"{label:34s} {name:14s} ratio {r:.2f} [90% {lo:.2f}, {hi:.2f}]  within {st.mean(w):.2f} between {st.mean(b):.2f}  pairs {len(w)}  levels {nlev}  notes {len(cards)}")
    read("ARM (" + ", ".join(os.path.basename(m.rstrip('/')) for m in a.mirrors) + ")", load(a.mirrors))
    if a.baseline: read("BASELINE (" + ", ".join(os.path.basename(m.rstrip('/')) for m in a.baseline) + ")", load(a.baseline))
    print("bars (writer-thinking-consistency): ratio >= 1.6 with the 90% band above 1.3 = the writer's budget was the gap; <= 1.3 with the band below 1.6 = the writer fails below the line, confound removed; else unresolved.")

if __name__ == "__main__": main()
