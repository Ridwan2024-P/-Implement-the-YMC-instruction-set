from utils import reg_codes, var_map, op_codes

def encode_ymc(ymc):
    machine = []

    for instr in ymc:
        parts = instr.replace(',','').split()
        op = parts[0]

        if op == 'mov':
            dst, src = parts[1], parts[2]
            dst = var_map.get(dst, dst)
            src = var_map.get(src, src)

            if src.isdigit():
                code = f"{op_codes[op]}{reg_codes[dst]}{int(src):02X}"
            else:
                code = f"{op_codes[op]}{reg_codes[dst]}{reg_codes[src]}00"

        elif op in ['add','sub','mult','div']:
            dst,a,b = parts[1],parts[2],parts[3]
            dst = var_map.get(dst,dst)
            a = var_map.get(a,a)
            b = var_map.get(b,b)

            code = f"{op_codes[op]}{reg_codes[dst]}{reg_codes[a]}{reg_codes[b]}"

        elif op == 'cmp':
            a,b = parts[1],parts[2]
            a = var_map.get(a,a)
            b = var_map.get(b,b)
            code = f"{op_codes[op]}{reg_codes[a]}{reg_codes[b]}"

        elif op in ['jmp','jg','jge','jl','jle','je','jne']:
            addr = int(parts[1])
            code = f"{op_codes[op]}{addr:02X}"

        machine.append(code)

    return machine