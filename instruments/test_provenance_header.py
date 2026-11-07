"""Fixture for v42: with ARC3_CROSS_GAME_PROVENANCE=foreign the block differs from stock ONLY in its header line."""
import os, sys, importlib
sys.path.insert(0, "runs/field/franzen-milestone2/tree/ARC3-Inference")
import inference.agent.cross_game as cg
src = open(cg.__file__).read()
patched = src.replace(
 '    header = ("Other games already played in this run (your own record from OTHER games; their mechanics often recur, "\n              "so treat these as hypotheses to check cheaply here, never as facts about this game):")\n',
 '    header = ("Other games already played in this run (your own record from OTHER games; their mechanics often recur, "\n              "so treat these as hypotheses to check cheaply here, never as facts about this game):")\n'
 '    if os.environ.get("ARC3_CROSS_GAME_PROVENANCE", "").strip().lower() == "foreign":\n'
 '        header = ("Games played earlier by a different agent in a previous run (not your record; their mechanics often recur, "\n'
 '                  "so treat these as hypotheses to check cheaply here, never as facts about this game):")\n', 1)
assert patched != src, "anchor not found in cross_game.py"
ns = {}; exec(compile(patched, cg.__file__, "exec"), ns)
cards = [{"key": "cn04-aaaa", "level": 1, "kind": "cleared", "rule": "GOAL: x", "actions": ["UP"], "n_actions": 1, "valid": None, "palette": [], "t": 1, "levels_total": 6},
         {"key": "lp85-bbbb", "level": 2, "kind": "cleared", "rule": "GOAL: y", "actions": ["CLICK"], "n_actions": 1, "valid": None, "palette": [], "t": 2, "levels_total": 8}]
os.environ.pop("ARC3_CROSS_GAME_PROVENANCE", None); a = ns["render_block"](cards)
os.environ["ARC3_CROSS_GAME_PROVENANCE"] = "foreign"; b = ns["render_block"](cards)
la, lb = a.split("\n"), b.split("\n")
assert la[0].startswith("Other games already played in this run (your own record") and lb[0].startswith("Games played earlier by a different agent"), (la[0], lb[0])
assert la[1:] == lb[1:], "card lines must be identical"
print("provenance fixture PASS: header differs,", len(la)-1, "card lines identical")
