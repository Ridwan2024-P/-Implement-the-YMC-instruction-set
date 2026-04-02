from utils import registers, var_map, op_codes

def hlc_to_ymc(lines):
    ymc = []
    label_count = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # --- Complex Arithmetic ---
        if 'addsub' in line:
            dest, expr = [x.strip() for x in line.split('=')]
            args = expr[7:-1].split(',')
            b, c = args[0].strip(), args[1].strip()
            ymc.append(f"add {dest}, {b}, {c}")
            ymc.append(f"sub {dest}, {dest}, {b}")
            continue

        if 'subadd' in line:
            dest, expr = [x.strip() for x in line.split('=')]
            args = expr[7:-1].split(',')
            b, c = args[0].strip(), args[1].strip()
            ymc.append(f"sub {dest}, {b}, {c}")
            ymc.append(f"add {dest}, {dest}, {b}")
            continue

        if 'multdiv' in line:
            dest, expr = [x.strip() for x in line.split('=')]
            args = expr[8:-1].split(',')
            b, c = args[0].strip(), args[1].strip()
            ymc.append(f"mult {dest}, {b}, {c}")
            ymc.append(f"div {dest}, {dest}, {b}")
            continue

        # --- Simple assignment ---
        if '=' in line and not any(op in line for op in ['+','-','*','/']):
            dest, right = [x.strip() for x in line.split('=')]
            ymc.append(f"mov {dest}, {right}")
            continue

        # --- Arithmetic ---
        for op in ['+','-','*','/']:
            if op in line:
                dest, expr = [x.strip() for x in line.split('=')]
                left, right = expr.split(op)
                if op == '+': ymc.append(f"add {dest}, {left.strip()}, {right.strip()}")
                elif op == '-': ymc.append(f"sub {dest}, {left.strip()}, {right.strip()}")
                elif op == '*': ymc.append(f"mult {dest}, {left.strip()}, {right.strip()}")
                elif op == '/': ymc.append(f"div {dest}, {left.strip()}, {right.strip()}")
                break

        # --- Conditional ---
        if line.startswith("if "):
            cond = line[3:].strip()
            for rel in ['>=','<=','>','<','==','!=']:
                if rel in cond:
                    left, right = cond.split(rel)
                    ymc.append(f"cmp {left.strip()}, {right.strip()}")
                    jmp_map = { '>':'jg','>=':'jge','<':'jl', '<=':'jle','==':'je','!=':'jne' }
                    ymc.append(f"{jmp_map[rel]} LABEL_{label_count}")
                    ymc.append(f"LABEL_{label_count}:")
                    label_count += 1
                    break

        # --- Loops ---
        if line.startswith("while "):
            cond = line[6:].strip()
            start = f"LOOP_{label_count}"
            end = f"END_{label_count}"
            label_count += 1
            ymc.append(f"{start}:")
            for rel in ['>=','<=','>','<','==','!=']:
                if rel in cond:
                    left, right = cond.split(rel)
                    ymc.append(f"cmp {left.strip()}, {right.strip()}")
                    jmp_map = { '>':'jg','>=':'jge','<':'jl', '<=':'jle','==':'je','!=':'jne' }
                    ymc.append(f"{jmp_map[rel]} {end}")
                    break
            ymc.append(f"jmp {start}")
            ymc.append(f"{end}:")
    return ymc