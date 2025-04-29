import sys

# this is the variable storage
s = {}

def eval_expr(expr):
    expr = expr.strip()
    # handle integer literals first so “-1” doesn’t get split wrongly
    if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
        return int(expr)
    # this is handling addition: it will split on '+' and add the two parts
    if '+' in expr:
        left, right = expr.split('+', 1)
        return eval_expr(left) + eval_expr(right)
    # this is handling subtraction: it will split on '-' and subtract the two parts
    if '-' in expr and not expr.startswith('-'):
        left, right = expr.split('-', 1)
        return eval_expr(left) - eval_expr(right)
    # handle string literal: this will remove surrounding quotes and reverse the text
    if expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1][::-1]
    # handle variables: return stored value if exists
    if expr in s:
        return s[expr]
    # if nothing matches, we don't know this expression. it will display error message
    raise Exception(f"Variable '{expr}' not defined.")

# Interpreter loop (top-level of loop)
# make sure user gave a script filename
if len(sys.argv) != 2:
    print("Usage: python3 mirrorscript.py <script.ms>")
    sys.exit(1)

# this will open the file and read lines, stripping blanks and comments
with open(sys.argv[1]) as f:
    lines = [
        line.strip()
        for line in f
        if line.strip() and not line.lstrip().startswith('//')
    ]

i = 0

# we will be going through each line in the script with this function
while i < len(lines):
    L = lines[i]

    # skip standalone end-tokens so they don't hit assignment
    # if the line is just 'endwhile' or 'endif', then this will skip it
    if L in ('endwhile', 'endif'):
        i += 1
        continue

    # 2) print statement function: print(...)
    elif L.startswith('print('):
        # extract what's inside the parentheses
        val = L[6:-1].strip()
        print(eval_expr(val))
        i += 1
        continue

    # 3) if statement function: if(...)
    elif L.startswith('if('):
        # get condition expression inside if
        cond = L[3:-1].strip()
        # 0 means true, non-zero means false
        # skip block when cond == 0 (true)
        if eval_expr(cond) == 0:
            i += 1
            while i < len(lines) and lines[i] != 'endif':
                i += 1
        i += 1
        continue

    # while loop function: while(...)
    elif L.startswith('while('):
        # get condition inside while
        cond_expr = L[6:-1].strip()
        body = []
        i += 1
        # collect loop body until 'endwhile'
        while i < len(lines) and lines[i] != 'endwhile':
            body.append(lines[i])
            i += 1

        # repeat until cond becomes true: loop while eval_expr != 0
        while eval_expr(cond_expr) != 0:
            for B in body:
                if B.startswith('print('):
                    val = B[6:-1].strip()
                    print(eval_expr(val))
                elif '=' in B:
                    var, expr = B.split('=', 1)
                    expr = expr.strip().rstrip(';')
                    if expr:
                        s[var.strip()] = eval_expr(expr)
            # automatically re-check condition
        
        # this will skip past the 'endwhile' line and go onto the next loop
        i += 1
        continue

    elif '=' in L:
        # split on '=', left is var name, right is expression
        var, expr = L.split('=', 1)
        # this will strip the whitespace and remove any trailing semicolon
        expr = expr.strip().rstrip(';')
        if expr:
            s[var.strip()] = eval_expr(expr)
        i += 1
        continue

    else:
        # anything else, just move on
        i += 1
