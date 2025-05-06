#!/usr/bin/env python3
import sys, random, re

# this is to load and strip comments
if len(sys.argv) != 2:
    print("Usage: python3 mirrorscript.py <script.ms>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    raw = [l.rstrip() for l in f]

lines = [
    re.sub(r'\bWagen\b', 'Wagon', l) 
    for l in raw
    if l.strip() and not l.lstrip().startswith('//')
]

# these are the initial game stats
env = {
    'coins':       100,
    'food':        75,
    'hunger':      100,
    'distance':    0,
    'destination': 400,
    'day':         0,
    'health':      100,
    'Wagon.condition': 100
}

# this is the expression evaluator
def eval_expr(expr):
    expr = expr.strip()
    # inline rand()
    while 'rand()' in expr:
        expr = expr.replace('rand()', str(random.randint(0,100)), 1)
    # this si the comparison operators
    for op in ('==','!=','>=','<=','>','<'):
        if op in expr:
            L, R = expr.split(op, 1)
            lv, rv = eval_expr(L), eval_expr(R)
            res = {
                '==': lv==rv,  '!=': lv!=rv,
                '>=': lv>=rv,  '<=': lv<=rv,
                '>':  lv>rv,   '<':  lv<rv
            }[op]
            return 0 if res else 1
    # also for *, %
    if '*' in expr:
        L, R = expr.split('*',1)
        return eval_expr(L) * eval_expr(R)
    if '%' in expr:
        L, R = expr.split('%',1)
        return eval_expr(L) % eval_expr(R)
    # for +, -. And also skis leading -
    for op in ('+','-'):
        if op in expr and not (op=='-' and expr.startswith('-')):
            L, R = expr.split(op,1)
            lv, rv = eval_expr(L), eval_expr(R)
            return (lv + rv) if op=='+' else (lv - rv)
    # string literal
    if expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1]
    # integer literal
    if re.fullmatch(r'-?\d+', expr):
        return int(expr)
    # variable lookup
    if expr in env:
        return env[expr]
    raise Exception(f"Undefined expr: {expr}")

# the is the print helper
def do_print(arg):
    parts = re.split(r'\s*\+\s*', arg)
    out = ''
    for p in parts:
        p = p.strip()
        if p.startswith('"') and p.endswith('"'):
            out += p[1:-1]
        else:
            out += str(eval_expr(p))
    print(out)

# built in method dispatch that is helps intepret the language into the game.
def builtin_call(name, args):
    if name == 'FoodHandler.buy':
        amt, price = args
        cost = amt * price
        if env['coins'] >= cost:
            env['coins'] -= cost
            env['food']   += amt
            print(f"Bought {amt} food for {cost} coins")

    elif name == 'FoodHandler.hunt':
        rate, = args
        if random.randint(0,99) <= rate:
            gained = rate // 2
            env['food'] += gained
            print(f"Hunting succeeded: +{gained} food")

    elif name == 'FoodHandler.forage':
        found = random.randint(0,5)
        env['food'] += found
        print(f"Foraged wild plants: +{found} food")

    elif name == 'HealthHandler.check':
        if env['health'] <= 30:
            print("Your health is low! Seek rest or medicine.")

    elif name == 'HealthHandler.heal':
        if env['food'] >= 15:
            env['food']   -= 15
            env['health'] += 10
            if env['health'] > 100:
                env['health'] = 100
            print("Healed 10 health at cost of 15 food")

    elif name == 'HungerHandler.eat':
        amt, = args
        if env['food'] >= amt:
            env['food']   -= amt
            env['hunger'] += amt
            # this clamps both food and hunger so it doesnt go under 0
            if env['food'] < 0:
                env['food'] = 0
            if env['hunger'] > 100:
                env['hunger'] = 100
            print(f"Ate {amt} food → +{amt} hunger")

    elif name == 'HungerHandler.check':
        if env['hunger'] == 0:
            print("You have starved! Game over.")
            env['destination'] = env['distance']

    elif name == 'FightHandler.encounter':
        chance = random.randint(0,99)
        if chance < 40:
            print("!!! Ambush! You are attacked by bandits !!!")
            dmg = random.randint(5,24)
            env['health'] -= dmg
            print(f"You took {dmg} damage!")
            stolen = random.randint(5,14)
            env['coins'] -= stolen
            print(f"They stole {stolen} coins!")
            if env['health'] < 0:
                env['health'] = 0
            if env['coins'] < 0:
                env['coins'] = 0
            builtin_call('HealthHandler.check', [])
            builtin_call('HungerHandler.check', [])

    elif name == 'Trader.sellFood':
        amt, rate = args
        if env['food'] >= amt:
            env['food']  -= amt
            env['coins'] += amt * rate
            print(f"Sold {amt} food for {amt*rate} coins")

    elif name == 'Wagon.damage':
        dmg, = args
        env['Wagon.condition'] -= dmg
        if env['Wagon.condition'] < 0:
            env['Wagon.condition'] = 0
        print(f"Wagon damaged: -{dmg}%")

    elif name == 'Wagon.repair':
        cost, = args
        effect = cost // 2
        if env['coins'] >= cost:
            env['coins'] -= cost
            env['Wagon.condition'] += effect
            if env['Wagon.condition'] > 100:
                env['Wagon.condition'] = 100
            print(f"Repaired wagon: +{effect}% condition")

    elif name == 'EventHandler.trigger':
        print(" ")
        print("----- Daily Event -----")
        r = random.randint(0,6)

        if   r == 0:
            env['food'] -= 20
            if env['food'] < 0: env['food'] = 0
            print("Flash flood: -20 food")

        elif r == 1:
            dam = random.randint(25,74)
            builtin_call('Wagon.damage', [dam])

        elif r == 2:
            loss = random.randint(10,24)
            env['hunger'] -= loss
            if env['hunger'] < 0: env['hunger'] = 0
            print(f"Sandstorm: -{loss} hunger")

        elif r == 3:
            sick = random.randint(10,29)
            env['health'] -= sick
            if env['health'] < 0: env['health'] = 0
            print(f"Disease outbreak: -{sick} health")

        elif r == 4:
            steal = random.randint(10,29)
            env['coins'] -= steal
            if env['coins'] < 0: env['coins'] = 0
            print(f"Bandit raid: -{steal} coins")

        elif r == 5:
            bonus = random.randint(0,9)
            env['coins'] += bonus
            print(f"Lucky find: +{bonus} coins")

        elif r == 6:
            print("Quiet day — nothing happens.")

        print("----- End Event -----")
        print(" ")

    else:
        raise Exception(f"Unknown builtin: {name}")

# this is the core interpreter
def run_block(lines):
    i = 0
    while i < len(lines):
        L = lines[i].strip()
        i += 1

        # this skips the class / function
        if L.startswith('ssalc ') or (' func ' in L and L.endswith('{')):
            depth = 1
            while i < len(lines) and depth:
                ln = lines[i].strip(); i += 1
                if ln.endswith('{') or ln == '{': depth += 1
                if ln == '}': depth -= 1
            continue

        # inline single‐statement for fi(...){}
        m = re.match(r'^fi\((.+)\)\s*\{\s*(.+);\s*\}$', L)
        if m:
            cond, stmt = m.groups()
            if eval_expr(cond) == 0:
                run_block([stmt + ';'])
            continue

        # to print and allow input on the same line: rav x = input("prompt");
        m = re.match(r'^rav\s+(\w+)\s*=\s*input\("([^"]*)"\);$', L)
        if m:
            var, prompt = m.groups()
            val = input(prompt)
            env[var] = int(val.strip())
            continue

        # rav x = input();
        m = re.match(r'^rav\s+(\w+)\s*=\s*input\(\);$', L)
        if m:
            var = m.group(1)
            val = input()
            env[var] = int(val.strip())
            continue

        # rav x = expr;
        m = re.match(r'^rav\s+(\w+)\s*=\s*(.+);$', L)
        if m:
            var, expr = m.groups()
            expr = expr.rstrip().rstrip('}').strip()
            env[var] = eval_expr(expr)
            continue

        # type x = expr;
        m = re.match(r'^(tni|taolf|gnirts|looB)\s+(\w+)\s*=\s*(.+);$', L)
        if m:
            _, var, expr = m.groups()
            expr = expr.rstrip().rstrip('}').strip()
            env[var] = eval_expr(expr)
            continue

        # print(...)
        m = re.match(r'^print\((.+)\);$', L)
        if m:
            do_print(m.group(1))
            continue

        # Class.method(...)
        m = re.match(r'^(\w+(?:\.\w+)*)\((.*)\);$', L)
        if m:
            name, args_str = m.groups()
            args = [eval_expr(a) for a in args_str.split(',') if a.strip()]
            builtin_call(name, args)
            continue

        # fi(cond) { ... }
        m = re.match(r'^fi\((.+)\)\s*\{$', L)
        if m:
            cond, block, depth = m.group(1), [], 1
            while i < len(lines) and depth:
                ln = lines[i].strip(); i += 1
                if ln.endswith('{') or ln == '{': depth += 1
                if ln == '}': depth -= 1
                if depth > 0: block.append(ln)
            if eval_expr(cond) == 0:
                run_block(block)
            continue

        # elihw(cond) { ... }
        m = re.match(r'^elihw\((.+)\)\s*\{$', L)
        if m:
            cond, body, depth = m.group(1), [], 1
            while i < len(lines) and depth:
                ln = lines[i].strip(); i += 1
                if ln.endswith('{') or ln == '{': depth += 1
                if ln == '}': depth -= 1
                if depth > 0: body.append(ln)
            while eval_expr(cond) == 0:
                run_block(body)
            continue

        # this is the fallback assignment function and clamps the variables at the bottom so it doesnt go below o.
        if '=' in L:
            var, expr = L.split('=',1)
            var = var.strip()
            expr = expr.rstrip().rstrip('}').strip().rstrip(';')
            if var not in ('fi','elihw'):
                env[var] = eval_expr(expr)
            if env.get('food',0) < 0:    env['food']    = 0
            if env.get('hunger',0) < 0:  env['hunger'] = 0
            continue

# Run the script
run_block(lines)
