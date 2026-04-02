from utils import reg_pool, var_map, memory_map

def get_register(var):
    """Get a register for a variable (spill if needed)"""
    if var in var_map:
        return var_map[var]
    # free register available
    if reg_pool:
        reg = reg_pool.pop(0)
        var_map[var] = reg
        return reg
    # spill: pick a var from var_map
    spill_var, spill_reg = next(iter(var_map.items()))
    memory_map[spill_var] = spill_reg
    del var_map[spill_var]
    var_map[var] = spill_reg
    return spill_reg

def hlc_to_ymc(lines):
    ymc = []
    label_count = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # assignment
        if '=' in line and not any(op in line for op in ['+','-','*','/']):
            dest, right = [x.strip() for x in line.split('=')]
            ymc.append(f"mov {dest}, {right}")
            continue

        # arithmetic
        for op in ['+','-','*','/']:
            if op in line:
                dest, expr = [x.strip() for x in line.split('=')]
                left, right = expr.split(op)
                if op == '+': ymc.append(f"add {dest}, {left.strip()}, {right.strip()}")
                elif op == '-': ymc.append(f"sub {dest}, {left.strip()}, {right.strip()}")
                elif op == '*': ymc.append(f"mult {dest}, {left.strip()}, {right.strip()}")
                elif op == '/': ymc.append(f"div {dest}, {left.strip()}, {right.strip()}")
                break

        # IF condition
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

        # WHILE loop
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