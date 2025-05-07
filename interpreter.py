#!/usr/bin/env python3
import sys
import random
import re
import random

def error(msg, lineno):
    """
    Report a syntax error at a given line and exit.
    """
    print(f"SyntaxError at line {lineno}: {msg}")
    sys.exit(1)

def translate_expr(expr, lineno):
    
    #Translate a TacticaLang expression into a valid Python expression.
   
    expr = expr.strip()
    # Support our helper for random minutes 1–45
    expr = expr.replace('randomStep()', 'random.randint(1,45)')
    # Split into string literals vs. code segments
    parts = re.split(r'(".*?")', expr)
    out = []
    for part in parts:
        if not part:
            continue
        # If it's a quoted literal, keep it verbatim
        if part.startswith('"') and part.endswith('"'):
            out.append(part)
        else:
            # Replace TacticaLang soccer ops with Python ops
            t = (part
                 .replace('crossBack', '/')
                 .replace('cross',    '*')
                 .replace('passBack', '-')
                 .replace('pass',     '+')
                 .replace('feint',    '%'))
            # Allow letters, digits, whitespace, math symbols, commas
            if not re.match(r'^[\w\s\+\-\*\/\%\(\)\.<>=!,\[\]]+$', t):
                error(f"Invalid characters in expression: {expr}", lineno)
            out.append(t)
    return ''.join(out)

def transpile(lines):
    """
    Convert a list of TacticaLang source lines into Python source code lines.
    
    Returns the full Python program as a single string.
    """
    py_lines     = []
    py_lines     = ['import random']
    indent       = 0             # current indentation level (in 4-space units)
    update_stack = []            # for holding loop-update statements
    i            = 0

    while i < len(lines):
        raw      = lines[i]
        lineno   = i + 1
        stripped = raw.strip()

        # Skip comments and blank lines
        if not stripped or stripped.startswith('#') or stripped.startswith('//'):
            i += 1
            continue

        # Handle multi-line commentatorSay(...)
        if stripped.startswith('commentatorSay('):
            stmt = stripped
            # Gather until the closing ');'
            while not stmt.rstrip().endswith(');'):
                i += 1
                stmt += ' ' + lines[i].strip()
            # Remove trailing semicolon
            stmt = stmt.rstrip(';')
            m = re.match(r'commentatorSay\((.+)\)', stmt)
            if not m:
                error(f"Invalid commentatorSay syntax: {stmt}", lineno)
            expr = m.group(1)
            # Split on our 'pass' operator to build print args
            parts = re.split(r'\bpass\b', expr)
            args  = [translate_expr(p.strip(), lineno) for p in parts if p.strip()]
            py_lines.append(' ' * (4*indent) +
                            f'print("🎙️  Commentator:", {", ".join(args)})')
            i += 1
            continue

        # Handle startMatch(); — pick formations & start stadium audio
        if stripped == 'startMatch();':
            # pick & announce formation
            py_lines.append('home_formation = random.choice(["4-3-3","4-4-2","5-3-2","3-5-2"])')
            py_lines.append('print(f"🏟️  Home Coach selects {home_formation} formation for today!")')
            # independently draw Away formation
            py_lines.append('away_formation = random.choice(["4-3-3","4-4-2","5-3-2","3-5-2"])')
            py_lines.append('print(f"🏟️  Away Coach selects {away_formation} formation for today!")')
           # fire off the MP3 in a separate app so it plays concurrently
            py_lines.append('import os')
            py_lines.append('os.startfile("cheerleaders-333433.mp3")')
            i += 1
            continue


        # Variable declaration: let x = expr;
        m = re.match(r'let\s+(\w+)\s*=\s*(.+);$', stripped)
        if m:
            var, expr = m.groups()
            py_expr = translate_expr(expr, lineno)
            py_lines.append(' ' * (4*indent) + f'{var} = {py_expr}')
            # Once we've seen awayGoals, generate the unique, sorted minute lists:
            if var == 'awayGoals':
             py_lines.append('homeMinutes = sorted(random.sample(range(1,91), homeGoals))')
             py_lines.append('awayMinutes = sorted(random.sample(range(1,91), awayGoals))')
            i += 1
            continue

        # Loop: kickoff(init; cond; update) {
        m = re.match(r'kickoff\s*\(\s*(.+?);\s*(.+?);\s*(.+?)\)\s*\{$', stripped)
        if m:
            init, cond, update = m.groups()
            # init
            ivar, iexpr = re.match(r'(\w+)\s*=\s*(.+)', init.strip()).groups()
            py_init = f'{ivar} = {translate_expr(iexpr, lineno)}'
            # condition
            py_cond = translate_expr(cond, lineno)
            # update (deferred until loop end)
            upd = update.strip()
            if upd.endswith('++'):
                py_update = f'{upd[:-2].strip()} += 1'
            elif upd.endswith('--'):
                py_update = f'{upd[:-2].strip()} -= 1'
            else:
                uvar, uexpr = re.match(r'(\w+)\s*=\s*(.+)', upd).groups()
                py_update = f'{uvar} = {translate_expr(uexpr, lineno)}'
            # Emit Python loop header
            py_lines.append(' ' * (4*indent) + py_init)
            py_lines.append(' ' * (4*indent) + f'while {py_cond}:')
            indent += 1
            update_stack.append((indent, py_update))
            i += 1
            continue

        # Closing brace: emit any deferred update then outdent
        if stripped == '}':
            if update_stack and update_stack[-1][0] == indent:
                _, code = update_stack.pop()
                py_lines.append(' ' * (4*indent) + code)
            indent -= 1
            i += 1
            continue

        # when(condition) {
        m = re.match(r'when\s*\(\s*(.+?)\s*\)\s*\{$', stripped)
        if m:
            py_cond = translate_expr(m.group(1), lineno)
            py_lines.append(' ' * (4*indent) + f'if {py_cond}:')
            indent += 1
            i += 1
            continue

        # otherwiseIf(condition) {
        m = re.match(r'otherwiseIf\s*\(\s*(.+?)\s*\)\s*\{$', stripped)
        if m:
            py_cond = translate_expr(m.group(1), lineno)
            py_lines.append(' ' * (4*indent) + f'elif {py_cond}:')
            indent += 1
            i += 1
            continue

        # otherwise {
        if stripped == 'otherwise {':
            py_lines.append(' ' * (4*indent) + 'else:')
            indent += 1
            i += 1
            continue

        # Unrecognized statement → syntax error
        error(f"Unknown statement: {stripped}", lineno)

    # Join all Python lines into one source block
    return '\n'.join(py_lines)

def interpret_file(filename):
    """
    Read a .tac file, transpile it to Python, and execute.
    """
    try:
        with open(filename, encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        sys.exit(1)

    py_code = transpile(lines)
    try:
        exec(py_code, {})
    except Exception as e:
        print(f"RuntimeError: {e}")

if __name__ == '__main__':
    # Expect exactly one .tac filename argument
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <program.tac>")
        sys.exit(1)
    interpret_file(sys.argv[1])
