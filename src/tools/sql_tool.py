from __future__ import annotations

import sqlite3
from datetime import datetime

from config import DB_PATH
from src.schema import ToolResult


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def get_customer_info(customer_id: str) -> ToolResult:
    conn = _get_conn()
    row = conn.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,)).fetchone()
    conn.close()
    if not row:
        return ToolResult(success=False, tool_name="get_customer_info", error=f"Customer {customer_id} not found")
    return ToolResult(success=True, tool_name="get_customer_info", data=dict(row))


def get_customer_orders(customer_id: str) -> ToolResult:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM orders WHERE customer_id = ? ORDER BY order_date DESC", (customer_id,)
    ).fetchall()
    conn.close()
    return ToolResult(success=True, tool_name="get_customer_orders", data=[dict(r) for r in rows])


def get_order_details(order_id: str) -> ToolResult:
    conn = _get_conn()
    row = conn.execute(
        """SELECT o.*, p.payment_id, p.paid_at, p.method AS payment_method, p.status AS payment_status
           FROM orders o LEFT JOIN payments p ON o.order_id = p.order_id
           WHERE o.order_id = ?""",
        (order_id,),
    ).fetchone()
    conn.close()
    if not row:
        return ToolResult(success=False, tool_name="get_order_details", error=f"Order {order_id} not found")
    return ToolResult(success=True, tool_name="get_order_details", data=dict(row))


def get_revenue_summary(**kwargs) -> ToolResult:
    conn = _get_conn()
    query = """SELECT strftime('%Y-%m', order_date) AS month,
                      COUNT(*) AS order_count,
                      SUM(total_amount) AS total_revenue
               FROM orders WHERE status != 'cancelled'"""
    params: list = []

    if "month" in kwargs and kwargs["month"]:
        query += " AND strftime('%Y-%m', order_date) = ?"
        params.append(kwargs["month"])
    elif "quarter" in kwargs and kwargs["quarter"]:
        q = kwargs["quarter"]
        year = kwargs.get("year", "2025")
        quarter_map = {"Q1": ("01", "03"), "Q2": ("04", "06"), "Q3": ("07", "09"), "Q4": ("10", "12")}
        if q.upper() in quarter_map:
            start, end = quarter_map[q.upper()]
            query += " AND order_date >= ? AND order_date < ?"
            params.extend([f"{year}-{start}-01", f"{year}-{end}-31"])

    query += " GROUP BY month ORDER BY month"
    rows = conn.execute(query, params).fetchall()
    conn.close()

    total = sum(r["total_revenue"] for r in rows)
    return ToolResult(
        success=True,
        tool_name="get_revenue_summary",
        data={"months": [dict(r) for r in rows], "grand_total": total},
    )


def get_open_tickets(**kwargs) -> ToolResult:
    conn = _get_conn()
    query = "SELECT * FROM support_tickets WHERE status IN ('open', 'in_progress')"
    params: list = []
    if "customer_id" in kwargs and kwargs["customer_id"]:
        query += " AND customer_id = ?"
        params.append(kwargs["customer_id"])
    query += " ORDER BY priority DESC, created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return ToolResult(success=True, tool_name="get_open_tickets", data=[dict(r) for r in rows])


def get_customer_purchase_duration(customer_id: str) -> ToolResult:
    conn = _get_conn()
    row = conn.execute("SELECT created_at FROM customers WHERE customer_id = ?", (customer_id,)).fetchone()
    conn.close()
    if not row:
        return ToolResult(success=False, tool_name="get_customer_purchase_duration", error=f"Customer {customer_id} not found")

    created = datetime.strptime(row["created_at"], "%Y-%m-%d")
    now = datetime.now()
    delta = now - created
    years = delta.days // 365
    months = (delta.days % 365) // 30
    return ToolResult(
        success=True,
        tool_name="get_customer_purchase_duration",
        data={"customer_id": customer_id, "created_at": row["created_at"], "years": years, "months": months, "total_days": delta.days},
    )


SQL_TOOLS = {
    "get_customer_info": get_customer_info,
    "get_customer_orders": get_customer_orders,
    "get_order_details": get_order_details,
    "get_revenue_summary": get_revenue_summary,
    "get_open_tickets": get_open_tickets,
    "get_customer_purchase_duration": get_customer_purchase_duration,
}


def execute_sql_tool(tool_name: str, tool_args: dict) -> ToolResult:
    func = SQL_TOOLS.get(tool_name)
    if not func:
        return ToolResult(success=False, tool_name=tool_name, error=f"Unknown SQL tool: {tool_name}")
    return func(**tool_args)
