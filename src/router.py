from __future__ import annotations

import json

from src.llm import llm_json_call
from src.schema import RouteDecision, TOOL_REGISTRY

ROUTER_SYSTEM_PROMPT = """You are an intent router for a customer service AI assistant. Given a user query, decide which tool to use.

Available tools:
{tools_description}

Database tables available:
- customers(customer_id, name, email, phone, created_at, tier) — 20 customers, IDs: C001-C020
- orders(order_id, customer_id, order_date, total_amount, status, items_count) — 40 orders, IDs: O001-O040
- payments(payment_id, order_id, paid_at, amount, method, status) — 35 payments
- support_tickets(ticket_id, customer_id, issue, status, priority, created_at, resolved_at) — 15 tickets

Routing rules:
1. Questions about policies (refund, shipping, warranty, return, membership) → route: "rag_tool"
2. Questions needing database data (customer info, orders, revenue, tickets) → route: "sql_tool"
3. Math calculations → route: "calculator", tool_name: "calculate", tool_args: {{"expression": "..."}}
4. Destructive actions (cancel, refund, delete) → route: "human_review", risk_level: "high", need_human_review: true
5. If required parameters are missing (e.g., no customer_id when asking about a specific customer) → route: "clarification"
6. For SQL queries, pick the most specific tool_name from the available tools

Respond with ONLY a JSON object matching this schema:
{{
  "route": "rag_tool" | "sql_tool" | "calculator" | "clarification" | "human_review",
  "intent": "short description",
  "tool_name": "specific tool name or null",
  "tool_args": {{}},
  "confidence": 0.0-1.0,
  "missing_fields": [],
  "risk_level": "low" | "medium" | "high",
  "need_human_review": false,
  "reason": "why this route"
}}"""


def _build_tools_description() -> str:
    lines = []
    for name, info in TOOL_REGISTRY.items():
        args = ", ".join(info["required_args"]) if info["required_args"] else "none"
        lines.append(f"- {name}: {info['description']} (required args: {args}, risk: {info['risk']})")
    return "\n".join(lines)


def route_query(query: str) -> RouteDecision:
    tools_desc = _build_tools_description()
    system = ROUTER_SYSTEM_PROMPT.format(tools_description=tools_desc)

    result = llm_json_call(system, query)

    if result:
        try:
            return RouteDecision(**result)
        except Exception:
            pass

    return _fallback_route(query)


def _fallback_route(query: str) -> RouteDecision:
    q = query.lower()

    policy_keywords = ["policy", "refund", "return", "warranty", "shipping", "membership", "tier"]
    if any(kw in q for kw in policy_keywords):
        return RouteDecision(
            route="rag_tool", intent="policy_question", tool_name="rag_search",
            confidence=0.7, risk_level="low", need_human_review=False,
            reason="Query contains policy-related keywords, falling back to RAG",
        )

    cancel_keywords = ["cancel", "refund", "delete", "remove"]
    if any(kw in q for kw in cancel_keywords):
        return RouteDecision(
            route="human_review", intent="destructive_action", tool_name=None,
            confidence=0.6, risk_level="high", need_human_review=True,
            reason="Query contains destructive action keywords",
        )

    import re
    calc_match = re.search(r"[\d]+[\s]*[+\-*/][\s]*[\d]+", q)
    if calc_match or any(kw in q for kw in ["calculate", "compute", "what is", "how much is"]):
        nums = re.findall(r"[\d\.\+\-\*\/\(\)\%\s]+", q)
        expr = max(nums, key=len).strip() if nums else ""
        return RouteDecision(
            route="calculator", intent="calculation", tool_name="calculate",
            tool_args={"expression": expr} if expr else {},
            confidence=0.6, risk_level="low", need_human_review=False,
            reason="Query appears to be a calculation",
        )

    db_keywords = ["customer", "order", "revenue", "payment", "ticket", "how long", "total", "status"]
    if any(kw in q for kw in db_keywords):
        return RouteDecision(
            route="sql_tool", intent="database_query", tool_name=None,
            confidence=0.5, risk_level="low", need_human_review=False,
            reason="Query contains database-related keywords, but couldn't determine specific tool",
        )

    return RouteDecision(
        route="rag_tool", intent="general_question", tool_name="rag_search",
        confidence=0.4, risk_level="low", need_human_review=False,
        reason="Default fallback to RAG",
    )
