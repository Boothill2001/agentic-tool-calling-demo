from __future__ import annotations

from config import HIGH_RISK_TOOLS
from src.schema import RouteDecision


def check_permission(decision: RouteDecision) -> tuple[str, bool]:
    if decision.tool_name in HIGH_RISK_TOOLS or decision.risk_level == "high":
        return "requires_approval", True

    return "approved", False
