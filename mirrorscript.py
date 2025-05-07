# Simple MirrorScript interpreter

import sys, re

s = {}

def eval_expr(expr):
    expr = expr.strip()
    # this si for the comparisons operations
    for op in ('==','!=','>=','<=','>','<'):
        if op in expr:
            L,R = expr.split(op,1)
            lv, rv = eval_expr(L), eval_expr(R)
            res = {
                '==': lv==rv, '!=': lv!=rv,
                '>=': lv>=rv, '<=': lv<=rv,
                '>':  lv>rv, '<':  lv<rv
            }[op]
            return 0 if res else 1
    # this is the multipication and modulo operators
    if '*' in expr:
        L,R = expr.split('*',1)
        return eval_expr(L) * eval_expr(R)
    if '%' in expr:
        L,R = expr.split('%',1)
        return eval_expr(L) % eval_expr(R)
    # this si the addition and subtraction operators
    for op in ('+','-'):
        if op in expr and not (op=='-' and expr.startswith('-')):
            L,R = expr.split(op,1)
            lv, rv = eval_expr(L), eval_expr(R)
            return (lv+rv) if op=='+' else (lv-rv)
    # for the integer
    if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
        return int(expr)
    # for the string
    if expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1]
    # for the variable
    if expr in s:
        return s[expr]
    raise Exception(f"Variable '{expr}' not defined.")

def run_block(lines):
    i = 0
    while i < len(lines):
        L = lines[i].strip()
        # skip blank or comments
        if not L or L.startswith('//'):
            i += 1
            continue

        # this is the print function
        if L.startswith('print('):
            # find last ')'
            end = L.rfind(')')
            inner = L[6:end]
            print(eval_expr(inner))
            i += 1
            continue

        # rav x = expr;
        if L.startswith('rav '):
            stmt = L[4:].rstrip(';')
            var, expr = stmt.split('=',1)
            s[var.strip()] = eval_expr(expr.strip())
            i += 1
            continue

        if L.endswith('{'):
            header = L[:-1].strip()

            # this is the fi function
            if header.startswith('fi(') and header.endswith(')'):
                cond = header[3:-1].strip()
                block, depth = [], 1
                i += 1
                while i < len(lines) and depth:
                    ln = lines[i].strip()
                    if ln.endswith('{'): depth += 1
                    if ln ==   '}':     depth -= 1
                    if depth: block.append(ln)
                    i += 1
                if eval_expr(cond) == 0:
                    run_block(block)
                continue

            # this is the elihw
            if header.startswith('elihw(') and header.endswith(')'):
                cond = header[6:-1].strip()
                body, depth = [], 1
                i += 1
                while i < len(lines) and depth:
                    ln = lines[i].strip()
                    if ln.endswith('{'): depth += 1
                    if ln ==   '}':     depth -= 1
                    if depth: body.append(ln)
                    i += 1
                while eval_expr(cond) == 0:
                    run_block(body)
                continue

        # closing brace
        if L == '}':
            i += 1
            continue

        # this is the  fallback assignment x = expr;
        if '=' in L:
            stmt = L.rstrip(';')
            var, expr = stmt.split('=',1)
            s[var.strip()] = eval_expr(expr.strip())

        i += 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 mirrorscript.py <script.ms>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        lines = [l.rstrip() for l in f]
    run_block(lines)
