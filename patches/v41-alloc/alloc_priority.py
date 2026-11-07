"""inference/agent/alloc_priority.py (ours, v41, §337): the allocation form, env-gated, byte-identical when unset.

ARC3_ALLOC_STUCK_TOKENS=N  (default unset = off): a game whose CURRENT level is <= ARC3_ALLOC_STUCK_LEVEL (default 2)
and whose tokens on that level have reached N is PARKED: its slot priority becomes 1, the lowest band, so it is served
only when no other game wants the slot. Nothing else changes: the stock priority_value (or D' when ARC3_PRIORITY_FORM=1)
keeps ranking every other game. Read from capc (§335): games ending at <= 2 levels take 25% of the pool's tokens for 2%
of the RHAE; the park moves that budget to games that return nine times as much per token.
"""
from __future__ import annotations
import logging, os

log = logging.getLogger(__name__)
PARKED_PRIORITY = 1


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        raise ValueError(f"{name} must be a number, got {raw!r}") from None


def settings() -> tuple[float, int]:
    return _env_float("ARC3_ALLOC_STUCK_TOKENS", 0.0), int(_env_float("ARC3_ALLOC_STUCK_LEVEL", 2))


def make_alloc_priority(stock):
    stuck_tokens, stuck_level = settings()
    parked: set[int] = set()

    def alloc_priority(state, **kwargs) -> int:
        value = stock(state, **kwargs)
        if stuck_tokens > 0 and int(state.level) <= stuck_level and float(state.tokens) >= stuck_tokens:
            key = id(state)
            if key not in parked:
                parked.add(key)
                log.warning("alloc: parking a game at level %d after %.0f tokens on it (stock priority %d)",
                            int(state.level), float(state.tokens), value)
            return PARKED_PRIORITY
        return value
    alloc_priority.__wrapped__ = stock  # type: ignore[attr-defined]
    return alloc_priority


def install(tool_agent) -> bool:
    """Wrap tool_agent.priority_value. Returns False (no change) when the env is unset."""
    stuck_tokens, stuck_level = settings()
    if stuck_tokens <= 0:
        return False
    if not callable(getattr(tool_agent, "priority_value", None)):
        raise RuntimeError("tool_agent.priority_value missing: the upstream changed")
    tool_agent.priority_value = make_alloc_priority(tool_agent.priority_value)
    log.warning("allocation form installed: park at level <= %d after %.0f tokens on the level", stuck_level, stuck_tokens)
    return True
