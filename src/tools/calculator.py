from __future__ import annotations

import ast
import math
import operator

from src.schema import ToolResult

SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
}

SAFE_FUNCS = {"sqrt": math.sqrt, "round": round, "abs": abs}


def _safe_eval(node):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant: {node.value}")
    if isinstance(node, ast.BinOp):
        op = SAFE_OPS.get(type(node.op))
        if not op:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op(_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        op = SAFE_OPS.get(type(node.op))
        if not op:
            raise ValueError(f"Unsupported unary: {type(node.op).__name__}")
        return op(_safe_eval(node.operand))
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in SAFE_FUNCS:
            args = [_safe_eval(a) for a in node.args]
            return SAFE_FUNCS[node.func.id](*args)
        raise ValueError(f"Unsupported function: {ast.dump(node.func)}")
    raise ValueError(f"Unsupported expression: {type(node).__name__}")


def safe_calculate(expression: str) -> ToolResult:
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _safe_eval(tree)
        return ToolResult(
            success=True,
            tool_name="calculate",
            data={"expression": expression, "result": result},
        )
    except Exception as e:
        return ToolResult(success=False, tool_name="calculate", error=str(e))
