from __future__ import annotations

import sqlite3

from config import DB_PATH
from src.schema import ToolResult


def _get_write_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def cancel_order(order_id: str) -> ToolResult:
    conn = _get_write_conn()
    row = conn.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchone()
    if not row:
        conn.close()
        return ToolResult(success=False, tool_name="cancel_order", error=f"Order {order_id} not found")

    if row["status"] == "cancelled":
        conn.close()
        return ToolResult(success=False, tool_name="cancel_order", error=f"Order {order_id} is already cancelled")

    if row["status"] == "delivered":
        conn.close()
        return ToolResult(success=False, tool_name="cancel_order", error=f"Order {order_id} is already delivered and cannot be cancelled")

    conn.execute("UPDATE orders SET status = 'cancelled' WHERE order_id = ?", (order_id,))
    conn.commit()
    conn.close()

    return ToolResult(
        success=True,
        tool_name="cancel_order",
        data={"order_id": order_id, "previous_status": row["status"], "new_status": "cancelled"},
    )


def process_refund(order_id: str) -> ToolResult:
    conn = _get_write_conn()
    row = conn.execute(
        "SELECT p.*, o.total_amount FROM payments p JOIN orders o ON p.order_id = o.order_id WHERE p.order_id = ?",
        (order_id,),
    ).fetchone()
    if not row:
        conn.close()
        return ToolResult(success=False, tool_name="process_refund", error=f"No payment found for order {order_id}")

    conn.execute("UPDATE payments SET status = 'refunded' WHERE order_id = ?", (order_id,))
    conn.commit()
    conn.close()

    return ToolResult(
        success=True,
        tool_name="process_refund",
        data={"order_id": order_id, "refund_amount": row["total_amount"], "payment_method": row["method"]},
    )


ORDER_API_TOOLS = {
    "cancel_order": cancel_order,
    "process_refund": process_refund,
}


def execute_order_api(tool_name: str, tool_args: dict) -> ToolResult:
    func = ORDER_API_TOOLS.get(tool_name)
    if not func:
        return ToolResult(success=False, tool_name=tool_name, error=f"Unknown order API tool: {tool_name}")
    return func(**tool_args)
