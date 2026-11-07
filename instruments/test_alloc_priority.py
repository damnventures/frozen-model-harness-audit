"""Fixture for the v41 allocation form: identical to stock when unset; parks only level<=2 past the token cutoff."""
import importlib.util, os, sys, types
TREE = "runs/field/franzen-milestone2/tree/ARC3-Inference"
sys.path.insert(0, TREE)
from inference.agent.priority_scheduler import PrioritySnapshot, priority_value  # noqa: E402
spec = importlib.util.spec_from_file_location("alloc_priority", "runs/field/ours/deploy/patches/v41-alloc/alloc_priority.py")
alloc = importlib.util.module_from_spec(spec); spec.loader.exec_module(alloc)
def fake_agent():
    m = types.SimpleNamespace(); m.priority_value = priority_value; return m
cases = [PrioritySnapshot(level=1, actions=50, tokens=90_000, total_levels=9),
         PrioritySnapshot(level=2, actions=40, tokens=80_000, total_levels=6),
         PrioritySnapshot(level=1, actions=10, tokens=20_000, total_levels=9),
         PrioritySnapshot(level=3, actions=60, tokens=150_000, total_levels=9),
         PrioritySnapshot(level=6, actions=30, tokens=90_000, total_levels=9)]
os.environ.pop("ARC3_ALLOC_STUCK_TOKENS", None); m = fake_agent(); assert alloc.install(m) is False
assert all(m.priority_value(c) == priority_value(c) for c in cases), "unset must be byte-identical"
os.environ["ARC3_ALLOC_STUCK_TOKENS"] = "80000"; m = fake_agent(); assert alloc.install(m) is True
got = [m.priority_value(c) for c in cases]; stock = [priority_value(c) for c in cases]
assert got[0] == 1 and got[1] == 1, f"level<=2 past 80K must park: {got[:2]}"
assert got[2] == stock[2] and got[3] == stock[3] and got[4] == stock[4], f"others unchanged: {got} vs {stock}"
assert all(s > 1 for s in stock), stock
print("alloc fixture PASS:", {"parked": got[:2], "unchanged": got[2:], "stock": stock})
