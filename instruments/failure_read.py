#!/usr/bin/env python
"""The failure read: where a Franzen-form run loses its levels, one class per game-run, from the events it leaves.

  ops/ledger-venv/bin/python runs/lib/failure_read.py OUTDIR [OUTDIR ...] [--json PATH] [--hard-list runs/ledger/public-25.txt]

Classes (assigned by code; a 20% manual audit of the stuck level's last turns is part of every read):
  WON            every level cleared
  CUT            still progressing: the last level-up fell inside the final 20% of the game's turns (the clock, not the model)
  NEVER-OPENED   0 levels; sub a/b/c as below
  STALLED-k      stuck at level k >= 1 for >= 20% of the turns; sub:
     a  exploring: no action list of >= 3 fired on the stuck level, single-action batches dominate -> mechanic never found
     b  executing: >= 2 lists of >= 3 actions fired on the stuck level, no level-up -> found, not executed (wrong rule or plan)
     c  dying: >= 2 game_over events on the stuck level
     d  starved: fewer than 6 analyzer turns on the stuck level (the scheduler gave it little; read with the turn count)
The same sub-classes apply to NEVER-OPENED (stuck level = level 1).
Features per game: levels/n, turns, actions, deaths, and on the stuck level: turns, actions, list batches, single batches,
deaths, share of analysis-only turns. The hidden set is harder than the public 25; report the games our old form never
opened (the 'hard' list) as a separate line, they are the closest public proxies for hidden never-opens.
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import sys


def truthy(v) -> bool:
    return v is True or (isinstance(v, str) and v.strip().lower() == "true")


def read_game(path: str, n_levels: int | None) -> dict:
    ev = []
    for line in open(path, errors="ignore"):
        try:
            ev.append(json.loads(line))
        except ValueError:
            pass
    acts = [e for e in ev if e.get("type") == "action" and str(e.get("action_display") or e.get("action_name")) != "RESET"]
    ana = [e for e in ev if e.get("type") == "analysis"]
    ups = [i for i, e in enumerate(acts) if truthy(e.get("level_completed")) or truthy(e.get("run_complete"))]
    levels = len(ups)
    deaths = sum(1 for e in acts if truthy(e.get("game_over")))
    steps = [a.get("analysis_step") for a in ana]
    total_turns = len(ana)
    tail = acts[(ups[-1] + 1) if ups else 0:]
    # turns on the stuck level: analyzer steps after the last level-up's step
    up_step = acts[ups[-1]].get("analysis_step") if ups else -1
    tail_turns = sum(1 for s in steps if s is not None and up_step is not None and s > up_step) if ups else total_turns
    batches = collections.Counter(e.get("analysis_step") for e in tail)
    lists = sum(1 for c in batches.values() if c >= 3)
    singles = sum(1 for c in batches.values() if c == 1)
    tail_deaths = sum(1 for e in tail if truthy(e.get("game_over")))
    acting_steps = set(batches)
    analysis_only = tail_turns - len([s for s in steps if s in acting_steps and (up_step is None or s > up_step)]) if tail_turns else 0
    n = n_levels or (max(int(e.get("level") or 0) for e in ev) if ev else 0)
    # class
    if n and levels >= n:
        cls, sub = "WON", ""
    elif ups and (total_turns - (steps.index(up_step) + 1 if up_step in steps else total_turns)) <= max(2, 0.2 * total_turns):
        cls, sub = "CUT", ""
    else:
        cls = "NEVER-OPENED" if levels == 0 else f"STALLED-{levels}"
        if tail_turns < 6:
            sub = "d"
        elif tail_deaths >= 2:
            sub = "c"
        elif lists >= 2:
            sub = "b"
        elif lists == 0 and singles >= max(1, 0.6 * max(1, len(batches))):
            sub = "a"
        else:
            sub = "a" if lists == 0 else "b"
    return dict(levels=levels, n=n, turns=total_turns, actions=len(acts), deaths=deaths, stuck_turns=tail_turns,
                stuck_actions=len(tail), stuck_lists=lists, stuck_singles=singles, stuck_deaths=tail_deaths,
                stuck_analysis_only=max(0, analysis_only), cls=cls, sub=sub)


def n_levels_map() -> dict:
    import sqlite3
    db = os.path.join(os.path.dirname(__file__), "..", "ledger", "arc.sqlite")
    try:
        con = sqlite3.connect(f"file:{os.path.abspath(db)}?mode=ro", uri=True)
        m = {g: int(n) for g, n in con.execute("SELECT substr(game,1,4), max(n_levels) FROM attempts WHERE n_levels IS NOT NULL GROUP BY 1")}
        con.close()
        return m
    except Exception:
        return {}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("outdirs", nargs="+")
    ap.add_argument("--json", default=None)
    ap.add_argument("--hard", default="r11l,tn36,g50t,sk48,sp80", help="public games our old form never opened")
    a = ap.parse_args(argv)
    nmap = n_levels_map()
    hard = set(a.hard.split(","))
    allrows = {}
    for d in a.outdirs:
        rows = {}
        truth = {}
        bj = os.path.join(d, "benchmark.json")
        if os.path.exists(bj):
            for gr in json.load(open(bj)).get("game_runs", []):
                truth[gr["game_id"][:4]] = (gr["levels_completed"], gr["number_of_levels"])
        for f in sorted(glob.glob(os.path.join(d, "artifacts", "*_events.jsonl")) or glob.glob(os.path.join(d, "*_events.jsonl"))):
            g = os.path.basename(f)[:4]
            rows[g] = read_game(f, nmap.get(g))
            if g in truth:
                # the final level's completion is a run_complete, not a level_completed event: events undercount wins
                lv, n = truth[g]
                rows[g]["levels"], rows[g]["n"] = lv, n
                if lv >= n:
                    rows[g]["cls"], rows[g]["sub"] = "WON", ""
        allrows[d] = rows
        print(f"\n{d}")
        print(f"  {'game':5s} {'lv':>5s} {'turns':>5s} {'acts':>5s} {'dth':>3s} | stuck: {'turns':>5s} {'acts':>4s} {'lists':>5s} {'singles':>7s} {'dth':>3s} {'ana-only':>8s} | class")
        for g, r in rows.items():
            print(f"  {g:5s} {r['levels']:>2d}/{r['n']:<2d} {r['turns']:>5d} {r['actions']:>5d} {r['deaths']:>3d} | "
                  f"{r['stuck_turns']:>12d} {r['stuck_actions']:>4d} {r['stuck_lists']:>5d} {r['stuck_singles']:>7d} {r['stuck_deaths']:>3d} {r['stuck_analysis_only']:>8d} | {r['cls']}{r['sub']}")
        cls = collections.Counter((r["cls"].split("-")[0] + ("" if r["cls"] in ("WON", "CUT") else "-" + r["sub"])) for r in rows.values())
        print("  classes:", dict(cls), "| hard games:", {g: rows[g]["cls"] + rows[g]["sub"] for g in rows if g in hard})
    if a.json:
        json.dump(allrows, open(a.json, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
