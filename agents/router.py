"""Router — decides which handler runs.

Phase 1 has exactly one route: main_agent. This placeholder exists to fix the
call shape in main.py so Phase 2 can extend routing without refactoring.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RouteDecision:
    """Result of routing a query to a handler.

    Attributes:
        route: Name of the selected handler (always "main_agent" in Phase 1).
        reason: Why this route was chosen.
    """

    route: str
    reason: str


def route(query: str) -> RouteDecision:
    """Determine which agent handler should process the query.

    Args:
        query: The user's input query.

    Returns:
        RouteDecision always pointing to main_agent in Phase 1.
    """
    return RouteDecision(
        route="main_agent",
        reason="phase_1_default",
    )
