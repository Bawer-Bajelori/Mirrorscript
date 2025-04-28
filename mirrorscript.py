import sys

s = {}  # Variable storage

def eval_expr(expr):
    expr = expr.strip()
    if '+' in expr:
        left, right = expr.split('+', 1)
        return eval_expr(left) + eval_expr(right)
    if '-' in expr:
        left, right = expr.split('-', 1)
        return eval_expr(left) - eval_expr(right)
    if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
        return int(expr)
    if expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1][::-1]
    if expr in s:
        return s[expr]
    raise Exception(f"Variable '{expr}' not defined.")

arg_file = sys.argv[1]
with open(arg_file) as f:
    lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('//')]

i = 0
while i < len(lines):
    L = lines[i]

    if L.startswith('print('):
        val = L[6:-1].strip()
        print(eval_expr(val))

    elif L.startswith('if('):
        cond = L[3:-1].strip()
        if eval_expr(cond) != 0:  # MirrorScript: 0 = true, anything else = false
            i += 1
            while i < len(lines) and not lines[i].startswith('endif'):
                i += 1

    elif L.startswith('while('):
        cond_expr = L[6:-1].strip()
        body = []
        i += 1
        while i < len(lines) and not lines[i].startswith('endwhile'):
            body.append(lines[i])
            i += 1
        # NEW: Now we re-evaluate fresh every time
        while eval_expr(cond_expr) == 0:
            for B in body:
                if B.startswith('print('):
                    val = B[6:-1].strip()
                    print(eval_expr(val))
                elif '=' in B:
                    var, expr = B.split('=', 1)
                    s[var.strip()] = eval_expr(expr.strip().rstrip(';'))
            # RE-EVALUATE condition after body
            # because maybe x changed inside body
            # (like x = x + -1)
            # so check cond_expr again fresh

    elif '=' in L:
        var, expr = L.split('=', 1)
        s[var.strip()] = eval_expr(expr.strip().rstrip(';'))

    i += 1
