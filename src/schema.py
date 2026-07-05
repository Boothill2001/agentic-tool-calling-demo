from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class RouteDecision(BaseModel):
    route: Literal["rag_tool", "sql_tool", "calculator", "clarification", "human_review"]
    intent: str = Field(description="Short description of what the user wants")
    tool_name: str | None = Field(default=None, description="Specific tool function to call")
    tool_args: dict = Field(default_factory=dict, description="Arguments for the tool")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the routing decision")
    missing_fields: list[str] = Field(default_factory=list, description="Required fields not provided by user")
    risk_level: Literal["low", "medium", "high"] = "low"
    need_human_review: bool = False
    reason: str = Field(description="Why this route was chosen")


class ToolResult(BaseModel):
    success: bool
    tool_name: str
    data: dict | list | str | None = None
    error: str | None = None


class ExecutionTrace(BaseModel):
    query: str
    route_decision: RouteDecision
    validation_passed: bool
    validation_errors: list[str] = Field(default_factory=list)
    permission_check: str = "approved"
    tool_result: ToolResult | None = None
    final_answer: str = ""


TOOL_REGISTRY = {
    "get_customer_info": {
        "description": "Get customer details by customer_id",
        "required_args": ["customer_id"],
        "route": "sql_tool",
        "risk": "low",
    },
    "get_customer_orders": {
        "description": "List all orders for a customer",
        "required_args": ["customer_id"],
        "route": "sql_tool",
        "risk": "low",
    },
    "get_order_details": {
        "description": "Get order details including payment info",
        "required_args": ["order_id"],
        "route": "sql_tool",
        "risk": "low",
    },
    "get_revenue_summary": {
        "description": "Get total revenue, optionally filtered by month or quarter",
        "required_args": [],
        "optional_args": ["month", "quarter", "year"],
        "route": "sql_tool",
        "risk": "low",
    },
    "get_open_tickets": {
        "description": "List open support tickets, optionally for a specific customer",
        "required_args": [],
        "optional_args": ["customer_id"],
        "route": "sql_tool",
        "risk": "low",
    },
    "get_customer_purchase_duration": {
        "description": "Calculate how long a customer has been purchasing from us",
        "required_args": ["customer_id"],
        "route": "sql_tool",
        "risk": "low",
    },
    "cancel_order": {
        "description": "Cancel a pending or shipped order",
        "required_args": ["order_id"],
        "route": "human_review",
        "risk": "high",
    },
    "process_refund": {
        "description": "Process a refund for an order",
        "required_args": ["order_id"],
        "route": "human_review",
        "risk": "high",
    },
    "calculate": {
        "description": "Perform a mathematical calculation",
        "required_args": ["expression"],
        "route": "calculator",
        "risk": "low",
    },
}
