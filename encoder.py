from utils import reg_codes, var_map, op_codes
from compiler import get_register

def encode_ymc(ymc):
    machine = []
    for instr in ymc:
        parts = instr.replace(',','').split()
        op = parts[0]
        if op == 'mov':
            dst, src = parts[1], parts[2]
            dst_reg = get_register(dst)
            if src.isdigit():
                code = f"{op_codes[op]}{reg_codes[dst_reg]}{int(src):02X}"
            else:
                src_reg = get_register(src)
                code = f"{op_codes[op]}{reg_codes[dst_reg]}{reg_codes[src_reg]}00"
        elif op in ['add','sub','mult','div']:
            dst,a,b = parts[1],parts[2],parts[3]
            dst_reg = get_register(dst)
            a_reg = get_register(a)
            b_reg = get_register(b)
            code = f"{op_codes[op]}{reg_codes[dst_reg]}{reg_codes[a_reg]}{reg_codes[b_reg]}"
        elif op == 'cmp':
            a,b = parts[1],parts[2]
            a_reg = get_register(a)
            b_reg = get_register(b)
            code = f"{op_codes[op]}{reg_codes[a_reg]}{reg_codes[b_reg]}"
        elif op in ['jmp','jg','jge','jl','jle','je','jne']:
            addr = int(parts[1])
            code = f"{op_codes[op]}{addr:02X}"
        machine.append(code)
    return machine