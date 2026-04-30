"""Tests for the router (agents/router.py)."""

from __future__ import annotations

from agents.router import RouteDecision, route


class TestRouteDecision:
    """RouteDecision dataclass."""

    def test_fields_are_populated(self) -> None:
        decision = RouteDecision(route="main_agent", reason="test")
        assert decision.route == "main_agent"
        assert decision.reason == "test"


class TestRoute:
    """Router function."""

    def test_always_returns_main_agent(self) -> None:
        decision = route("any query here")
        assert decision.route == "main_agent"

    def test_reason_is_phase_1_default(self) -> None:
        decision = route("hello")
        assert decision.reason == "phase_1_default"

    def test_route_ignores_query_content(self) -> None:
        d1 = route("capital of France")
        d2 = route("explain quantum physics")
        assert d1.route == d2.route
        assert d1.reason == d2.reason
