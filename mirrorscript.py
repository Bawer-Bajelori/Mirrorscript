import sys

# variable storage (global scope)
s = {}

# evaluate expressions: variables, numbers, strings, math, comparisons
# reversed logic: 0 = true, non-zero = false
def eval_expr(expr):
    expr = expr.strip()
    # comparison operators
    for op in ('==', '!=', '>=', '<=', '>', '<'):
        if op in expr:
            left, right = expr.split(op, 1)
            lv = eval_expr(left)
            rv = eval_expr(right)
            result = {
                '==': lv == rv,
                '!=': lv != rv,
                '>=': lv >= rv,
                '<=': lv <= rv,
                '>': lv > rv,
                '<': lv < rv
            }[op]
            return 0 if result else 1
    # arithmetic operators
    for op in ('+', '-'):
        if op in expr and not (op == '-' and expr.startswith('-')):
            left, right = expr.split(op, 1)
            lv = eval_expr(left)
            rv = eval_expr(right)
            return lv + rv if op == '+' else lv - rv
    # integer literal
    if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
        return int(expr)
    # string literal
    if expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1]
    # variable lookup
    if expr in s:
        return s[expr]
    raise Exception(f"Variable '{expr}' not defined.")

# run a block of MirrorScript lines (handles nested fi/fidne and elihw/elihwdne)
def run_block(lines):
    i = 0
    while i < len(lines):
        L = lines[i].strip()
        if not L or L.startswith('//'):
            i += 1
            continue
        # print
        if L.startswith('print('):
            print(eval_expr(L[6:-1]))
            i += 1
            continue
        # variable assignment
        if L.startswith('rav '):
            var, expr = L[4:].split('=', 1)
            s[var.strip()] = eval_expr(expr.strip().rstrip(';'))
            i += 1
            continue
        # if statement
        if L.startswith('fi('):
            cond = L[3:-1]
            # collect true block
            block = []
            depth = 1
            i += 1
            while i < len(lines) and depth:
                line = lines[i].strip()
                if line.startswith('fi('): depth += 1
                if line == 'fidne': depth -= 1
                if depth: block.append(line)
                i += 1
            # execute if condition is true (0)
            if eval_expr(cond) == 0:
                run_block(block)
            continue
        # while loop
        if L.startswith('elihw('):
            cond = L[6:-1]
            # collect loop body
            body = []
            depth = 1
            i += 1
            while i < len(lines) and depth:
                line = lines[i].strip()
                if line.startswith('elihw('): depth += 1
                if line == 'elihwdne': depth -= 1
                if depth: body.append(line)
                i += 1
            # execute loop
            while eval_expr(cond) == 0:
                run_block(body)
            continue
        # end of block tokens (should be skipped)
        if L in ('fidne', 'elihwdne'):
            i += 1
            continue
        i += 1


if len(sys.argv) != 2:
    print("Usage: python3 mirrorscript.py <script.ms>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    lines = [l.rstrip() for l in f]
x = s
run_block(lines)
