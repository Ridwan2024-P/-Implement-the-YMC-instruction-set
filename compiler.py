from utils import registers, reg_map, flags

def hlc_to_ymc(lines):
    ymc = []
    label_count = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Assignment: a = 5 or a = b
        if '=' in line and '(' not in line:
            dest, right = [x.strip() for x in line.split('=')]
            if right.isdigit():
                ymc.append(f"mov {dest}, {right}")
            elif right in registers:
                ymc.append(f"mov {dest}, {right}")
            continue

        # Arithmetic
        ops = ['+', '-', '*', '/']
        for op in ops:
            if op in line:
                # Support two-operand
                dest, expr = [x.strip() for x in line.split('=')]
                parts = expr.replace('(','').replace(')','').split(op)
                if len(parts) == 2:
                    left, right = parts[0].strip(), parts[1].strip()
                    if op == '+':
                        ymc.append(f"add {dest}, {left}, {right}")
                    elif op == '-':
                        ymc.append(f"sub {dest}, {left}, {right}")
                    elif op == '*':
                        ymc.append(f"mult {dest}, {left}, {right}")
                    elif op == '/':
                        ymc.append(f"div {dest}, {left}, {right}")
                elif len(parts) == 3:
                    l, m, r = parts
                    if op == '+':
                        ymc.append(f"addsub {dest}, {l.strip()}, {m.strip()}, {r.strip()}")
                    elif op == '-':
                        ymc.append(f"subadd {dest}, {l.strip()}, {m.strip()}, {r.strip()}")
                    elif op == '*':
                        ymc.append(f"multdiv {dest}, {l.strip()}, {m.strip()}, {r.strip()}")
                break

        # If/While simple: convert to cmp + jump
        if line.startswith("if ") or line.startswith("while "):
            cond = line[line.find(' ')+1:].strip()
            for rel in ['>=','<=','>','<','==','!=']:
                if rel in cond:
                    left, right = cond.split(rel)
                    left, right = left.strip(), right.strip()
                    ymc.append(f"cmp {left}, {right}")
                    # choose jump based on rel
                    if line.startswith("if "):
                        jmp_map = {'>':'jg','>=':'jge','<':'jl','<=':'jle','==':'je','!=':'jne'}
                        ymc.append(f"{jmp_map[rel]} LABEL_{label_count}")
                        label_count += 1
                    else:
                        jmp_map = {'>':'jg','>=':'jge','<':'jl','<=':'jle','==':'je','!=':'jne'}
                        ymc.append(f"{jmp_map[rel]} LOOP_{label_count}")
                        label_count += 1
                    break
    return ymc