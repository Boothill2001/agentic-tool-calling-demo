from __future__ import annotations

from src.schema import RouteDecision, TOOL_REGISTRY


def validate_decision(decision: RouteDecision) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if decision.route == "clarification":
        return True, []

    if decision.route == "rag_tool":
        return True, []

    if decision.tool_name and decision.tool_name not in TOOL_REGISTRY and decision.tool_name != "rag_search":
        errors.append(f"Unknown tool: {decision.tool_name}")

    if decision.tool_name and decision.tool_name in TOOL_REGISTRY:
        registry = TOOL_REGISTRY[decision.tool_name]
        for req_arg in registry["required_args"]:
            if req_arg not in decision.tool_args or not decision.tool_args[req_arg]:
                errors.append(f"Missing required argument: {req_arg}")

    if decision.missing_fields:
        if decision.route != "clarification":
            decision.route = "clarification"

    return len(errors) == 0, errors
