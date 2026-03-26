opcode = {
    'mov': '01',
    'add': '02',
    'sub': '03',
    'cmp': '04',
    'jmp': '05'
}

reg_code = {
    'eax': '00',
    'ebx': '01',
    'ecx': '02',
    'edx': '03'
}

def encode_instruction(inst):
    parts = inst.split()
    op = parts[0]

    if op == 'mov':
        r, val = parts[1].replace(',', ''), parts[2]
        return f"{opcode[op]} {reg_code[r]} {val}"

    elif op in ['add', 'sub']:
        r, r1, r2 = parts[1].replace(',', ''), parts[2].replace(',', ''), parts[3]
        return f"{opcode[op]} {reg_code[r]} {reg_code[r1]} {reg_code[r2]}"

    return "00"