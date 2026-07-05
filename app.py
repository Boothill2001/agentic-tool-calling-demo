"""Agentic Tool Calling Demo -- Streamlit UI"""

import json
import sqlite3

import streamlit as st

from config import DB_PATH
from src.router import route_query
from src.validator import validate_decision
from src.permissions import check_permission
from src.schema import ExecutionTrace, RouteDecision, ToolResult
from src.tools.sql_tool import execute_sql_tool
from src.tools.calculator import safe_calculate
from src.tools.order_api import execute_order_api
from src.tools.rag_tool import rag_search
from src.llm import llm_call

st.set_page_config(page_title="Agentic Tool Calling", page_icon="wrench", layout="wide")


def _ensure_db():
    if not DB_PATH.exists():
        from seed_db import seed
        seed()


def _render_header():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
                padding: 24px 32px; border-radius: 12px; margin-bottom: 24px;">
        <h1 style="color: white; margin: 0 0 4px 0;">Agentic Tool Calling Demo</h1>
        <p style="color: #b8d4e8; font-size: 14px; margin: 0;">
            LLM Router + Structured JSON + Schema Validation + Permission Check + Tool Execution
        </p>
    </div>
    """, unsafe_allow_html=True)


def _render_sidebar():
    with st.sidebar:
        st.header("Available Tools")
        st.markdown("""
        - **SQL Database** -- customer, order, payment, ticket queries
        - **Calculator** -- AST-safe math evaluation
        - **Order API** -- cancel order, process refund (requires approval)
        - **RAG** -- policy document Q&A
        """)

        st.divider()
        st.header("DB Explorer")
        if DB_PATH.exists():
            conn = sqlite3.connect(DB_PATH)
            for table in ["customers", "orders", "payments", "support_tickets"]:
                count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                st.metric(table, f"{count} rows")
            conn.close()

            with st.expander("Sample Data"):
                table = st.selectbox("Table:", ["customers", "orders", "payments", "support_tickets"])
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                rows = conn.execute(f"SELECT * FROM {table} LIMIT 5").fetchall()
                conn.close()
                for r in rows:
                    st.json(dict(r))

        st.divider()
        st.caption("Built by Nguyen Minh Tri")
        st.caption("Senior AI Engineer")


def _execute_tool(decision: RouteDecision) -> ToolResult:
    if decision.route == "sql_tool" and decision.tool_name:
        return execute_sql_tool(decision.tool_name, decision.tool_args)
    elif decision.route == "calculator" and decision.tool_name == "calculate":
        expr = decision.tool_args.get("expression", "")
        return safe_calculate(expr)
    elif decision.route == "human_review" and decision.tool_name:
        return execute_order_api(decision.tool_name, decision.tool_args)
    elif decision.route == "rag_tool":
        return rag_search(decision.tool_args.get("query", ""))
    return ToolResult(success=False, tool_name="unknown", error="No tool matched")


def _format_answer(trace: ExecutionTrace) -> str:
    decision = trace.route_decision
    result = trace.tool_result

    if decision.route == "clarification":
        missing = ", ".join(decision.missing_fields) if decision.missing_fields else "some required information"
        return f"I need more information to help you. Could you please provide: **{missing}**?\n\n*Reason: {decision.reason}*"

    if not result:
        return "I wasn't able to process your request."

    if not result.success:
        return f"Sorry, there was an error: {result.error}"

    if decision.route == "rag_tool" and isinstance(result.data, dict):
        return result.data.get("answer", str(result.data))

    if decision.route == "calculator" and isinstance(result.data, dict):
        return f"**Result:** `{result.data.get('expression', '')}` = **{result.data.get('result', '')}**"

    if isinstance(result.data, dict):
        try:
            system = "You are a helpful assistant. Format the following data into a clear, natural language answer for the user's question. Be concise."
            user_msg = f"User question: {trace.query}\n\nData:\n{json.dumps(result.data, indent=2, default=str)}"
            return llm_call(system, user_msg)
        except Exception:
            return f"Here's what I found:\n```json\n{json.dumps(result.data, indent=2, default=str)}\n```"

    if isinstance(result.data, list):
        try:
            system = "You are a helpful assistant. Format the following data into a clear, natural language answer. Be concise."
            user_msg = f"User question: {trace.query}\n\nData ({len(result.data)} records):\n{json.dumps(result.data[:10], indent=2, default=str)}"
            return llm_call(system, user_msg)
        except Exception:
            return f"Found {len(result.data)} results:\n```json\n{json.dumps(result.data[:5], indent=2, default=str)}\n```"

    return str(result.data)


def _render_trace(trace: ExecutionTrace):
    d = trace.route_decision

    route_color = {
        "sql_tool": "#2ecc71", "calculator": "#e67e22", "rag_tool": "#3498db",
        "clarification": "#f39c12", "human_review": "#e74c3c",
    }.get(d.route, "#95a5a6")

    st.markdown(f"""
    <div style="border-left: 4px solid {route_color}; padding: 8px 16px; margin: 8px 0;
                background: rgba(255,255,255,0.05); border-radius: 0 8px 8px 0;">
        <strong>Route:</strong> {d.route} | <strong>Tool:</strong> {d.tool_name or 'N/A'} |
        <strong>Risk:</strong> {d.risk_level} | <strong>Confidence:</strong> {d.confidence:.0%}
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Execution Trace (JSON)"):
        st.json(json.loads(trace.model_dump_json()))


def _process_query(query: str) -> ExecutionTrace:
    decision = route_query(query)

    valid, errors = validate_decision(decision)

    perm_status, needs_approval = check_permission(decision)

    trace = ExecutionTrace(
        query=query,
        route_decision=decision,
        validation_passed=valid,
        validation_errors=errors,
        permission_check=perm_status,
    )

    if not valid:
        decision.route = "clarification"
        decision.reason = f"Validation failed: {'; '.join(errors)}"
        trace.route_decision = decision
        trace.final_answer = _format_answer(trace)
        return trace

    if decision.route == "clarification":
        trace.final_answer = _format_answer(trace)
        return trace

    if needs_approval:
        trace.permission_check = "requires_approval"
        return trace

    if decision.route == "rag_tool":
        decision.tool_args["query"] = query

    result = _execute_tool(decision)
    trace.tool_result = result
    trace.final_answer = _format_answer(trace)
    return trace


def main():
    _ensure_db()
    _render_header()
    _render_sidebar()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_approval" not in st.session_state:
        st.session_state.pending_approval = None

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)
            if "trace" in msg and msg["trace"]:
                _render_trace(msg["trace"])

    if st.session_state.pending_approval:
        trace = st.session_state.pending_approval
        d = trace.route_decision
        st.warning(f"**Action requires approval:** {d.tool_name}({d.tool_args})\n\nRisk level: **{d.risk_level}**\n\nReason: {d.reason}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Approve", type="primary", key="approve_btn"):
                if d.route == "rag_tool":
                    d.tool_args["query"] = trace.query
                result = _execute_tool(d)
                trace.tool_result = result
                trace.permission_check = "approved_by_user"
                trace.final_answer = _format_answer(trace)
                st.session_state.messages.append({"role": "assistant", "content": trace.final_answer, "trace": trace})
                st.session_state.pending_approval = None
                st.rerun()
        with col2:
            if st.button("Reject", key="reject_btn"):
                trace.final_answer = "Action was rejected by the user."
                trace.permission_check = "rejected_by_user"
                st.session_state.messages.append({"role": "assistant", "content": trace.final_answer, "trace": trace})
                st.session_state.pending_approval = None
                st.rerun()
        return

    sample_queries = [
        "How long has customer C001 been with us?",
        "What is the refund policy?",
        "Cancel order O006",
        "What is 15% of 2500000?",
        "Check that customer for me",
        "Show me all open support tickets",
        "Total revenue in Q1 2025?",
    ]
    st.caption("Try: " + " | ".join(f'"{q}"' for q in sample_queries[:4]))

    if query := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Routing and executing..."):
                trace = _process_query(query)

            if trace.permission_check == "requires_approval":
                st.session_state.pending_approval = trace
                st.rerun()
            else:
                st.markdown(trace.final_answer, unsafe_allow_html=True)
                _render_trace(trace)

        st.session_state.messages.append({"role": "assistant", "content": trace.final_answer, "trace": trace})


if __name__ == "__main__":
    main()
