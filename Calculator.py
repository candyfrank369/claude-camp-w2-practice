import ast
import operator
import re

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.Pow: operator.pow,
       ast.USub: operator.neg, ast.UAdd: operator.pos}


def safe_eval(node):
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](safe_eval(node.left), safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](safe_eval(node.operand))
    raise ValueError("Unsupported expression")


def normalize(expr):
    expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**")
    return re.sub(r"(\d+\.?\d*)\s*%", r"(\1/100)", expr)


def main():
    print("=== Safe Calculator === (type 'quit' to exit)\n"
          "Supports: + - × ÷ ^ % (percent) and parentheses\n"
          "Example: 12 + 72 ÷ 8 × 6 - 4 + 10 × 2%")
    while True:
        expr = input("\n> ").strip()
        if expr.lower() == "quit":
            print("Goodbye!")
            break
        if not expr:
            continue
        try:
            result = safe_eval(ast.parse(normalize(expr), mode="eval"))
            print(f"= {result}")
        except ZeroDivisionError:
            print("Error: Cannot divide by zero.")
        except (SyntaxError, ValueError):
            print("Error: Invalid expression.")
        except OverflowError:
            print("Error: Result too large.")


if __name__ == "__main__":
    main()
