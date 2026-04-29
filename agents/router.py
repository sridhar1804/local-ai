"""Router — decides which handler runs. Phase 1 has exactly one route."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RouteDecision:
    route: str
    reason: str


def route(query: str) -> RouteDecision:
    return RouteDecision(route="main_agent", reason="phase_1_default")
