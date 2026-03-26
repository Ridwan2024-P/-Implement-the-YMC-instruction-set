def encode_instruction(inst):
    parts = inst.split()
    op = parts[0]

    if op == 'mov':
        r, val = parts[1].replace(',', ''), parts[2]
        return f"{opcode[op]} {reg_code[r]} {val}"

    elif op in ['add', 'sub']:
        r = parts[1].replace(',', '')
        r1 = parts[2].replace(',', '')
        r2 = parts[3]

        # ✅ check: r2 register নাকি number
        if r2 in reg_code:
            return f"{opcode[op]} {reg_code[r]} {reg_code[r1]} {reg_code[r2]}"
        else:
            return f"{opcode[op]} {reg_code[r]} {reg_code[r1]} {r2}"

    elif op == 'cmp':
        r, val = parts[1].replace(',', ''), parts[2]
        return f"{opcode[op]} {reg_code[r]} {val}"

    elif op in ['jmp', 'jg', 'jle']:
        return f"{opcode[op]} {parts[1]}"

    return "00"