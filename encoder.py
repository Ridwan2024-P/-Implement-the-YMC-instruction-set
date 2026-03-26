# encoder.py

# Register codes
reg_codes = {
    'eax': '00',
    'ebx': '01',
    'ecx': '02',
    'edx': '03'
}

# Variable mapping (HLC -> registers)
var_map = {
    'a': 'eax',
    'b': 'ebx',
    'c': 'ecx',
    'x': 'eax',
    'y': 'ebx',
    'z': 'ecx'
}

# Opcode mapping
op_codes = {
    'mov': '10',
    'add': '20',
    'sub': '21',
    'mult': '22',
    'div': '23',
    'addsub': '30',
    'subadd': '31',
    'multdiv': '32',
    'cmp': '40',
    'jmp': '50',
    'jg': '51',
    'jge': '52',
    'jl': '53',
    'jle': '54',
    'jne': '55',
    'je': '56'
}

def encode_ymc(ymc_asm):
    machine = []
    for instr in ymc_asm:
        parts = instr.replace(',','').split()
        op = parts[0]
        if op == 'mov':
            dst, src = parts[1], parts[2]
            if dst in var_map: dst = var_map[dst]
            if src in var_map: src = var_map[src]
            if src.isdigit():
                code = f"{op_codes[op]}{reg_codes[dst]}{int(src):02X}"
            else:
                code = f"{op_codes[op]}{reg_codes[dst]}{reg_codes[src]}00"
        elif op in ['add','sub','mult','div']:
            dst, src1, src2 = parts[1], parts[2], parts[3]
            if dst in var_map: dst = var_map[dst]
            if src1 in var_map: src1 = var_map[src1]
            if src2 in var_map: src2 = var_map[src2]
            code = f"{op_codes[op]}{reg_codes[dst]}{reg_codes[src1]}{reg_codes[src2]}"
        else:
            # For jumps/cmp (simplified)
            args = ''.join([reg_codes.get(p,var_map.get(p,p)) for p in parts[1:]])
            code = f"{op_codes[op]}{args}"
        machine.append(code)
    return machine