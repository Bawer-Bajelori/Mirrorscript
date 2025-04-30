import sys

# variable storage (global scope)
s = {}

# function storage (name -> (params, body))
funcs = {}

# evaluate expressions: variables, numbers, strings, math, comparisons
# reversed logic: 0 = true, non-zero = false
def eval_expr(expr):
    expr = expr.strip()
    # comparison operators first
    for op in ('==', '!=', '>=', '<=', '>', '<'):
        if op in expr:
            left, right = expr.split(op, 1)
            lv = eval_expr(left)
            rv = eval_expr(right)
            # normal comparison
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
    for op in ('+', '-'):  # left-to-right
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

# require script filename
if len(sys.argv) != 2:
    print("Usage: python3 mirrorscript.py <script.ms>")
    sys.exit(1)

# read lines, skip blanks and comments
with open(sys.argv[1]) as f:
    lines = [L.strip() for L in f if L.strip() and not L.lstrip().startswith('//')]

i = 0
while i < len(lines):
    L = lines[i]
    # skip end tokens
    if L in ('fidne', 'elihwdne', 'cnufdne'):
        i += 1; continue
    # print
    if L.startswith('print('):
        val = L[6:-1].strip()
        print(eval_expr(val)); i += 1; continue
    # if-fi
    if L.startswith('fi('):
        cond = L[3:-1].strip()
        if eval_expr(cond) != 0:
            # skip to fidne
            i += 1
            while i < len(lines) and lines[i] != 'fidne': i += 1
        i += 1; continue
    # while-elihw
    if L.startswith('elihw('):
        cond_expr = L[6:-1].strip()
        body = []
        i += 1
        while i < len(lines) and lines[i] != 'elihwdne':
            body.append(lines[i]); i += 1
        # loop while condition true (0)
        while eval_expr(cond_expr) == 0:
            for B in body:
                if B.startswith('print('): print(eval_expr(B[6:-1].strip()))
                elif B.startswith('rav '):
                    var, expr = B[4:].split('=', 1)
                    s[var.strip()] = eval_expr(expr.strip().rstrip(';'))
            # end for body, re-evaluate cond_expr
        i += 1; continue
    # function definition
    if L.startswith('diov '):
        header = L[5:].strip()
        fname = header[:header.find('(')].strip()
        params = [p.strip() for p in header[header.find('(')+1:header.find(')')].split(',') if p.strip()]
        body = []
        i += 1
        while i < len(lines) and lines[i] != 'cnufdne': body.append(lines[i]); i += 1
        funcs[fname] = (params, body)
        i += 1; continue
    # function call
    if '(' in L and L.endswith(')') and L.split('(')[0] in funcs:
        fname = L[:L.find('(')].strip()
        args = [eval_expr(a.strip()) for a in L[L.find('(')+1:-1].split(',') if a.strip()]
        params, body = funcs[fname]
        old_s = s.copy()
        for p,v in zip(params, args): s[p] = v
        for B in body:
            if B.startswith('nruter'): s['_ret'] = eval_expr(B[6:].strip()); break
            if B.startswith('print('): print(eval_expr(B[6:-1].strip()))
            if B.startswith('rav '):
                var, expr = B[4:].split('=',1); s[var.strip()] = eval_expr(expr.strip().rstrip(';'))
        # restore and allow return usage
        ret = s.get('_ret', None)
        s.clear(); s.update(old_s)
        if ret is not None: s['_ret'] = ret
        i += 1; continue
    # assignment rav
    if L.startswith('rav '):
        var, expr = L[4:].split('=',1)
        s[var.strip()] = eval_expr(expr.strip().rstrip(';'))
        i += 1; continue
    i += 1
