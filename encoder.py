from utils import reg_codes, var_map, op_codes, registers

# Temp register assignment for more than 4 variables
temp_reg_idx = 0

def get_register(var):
    """
    Return the register mapped to a variable.
    If variable is new, assign it a temporary register.
    """
    global temp_reg_idx
    if var in var_map:
        return var_map[var]
    else:
        reg = registers[temp_reg_idx % len(registers)]
        var_map[var] = reg
        temp_reg_idx += 1
        return reg

def encode_ymc(ymc):
    """
    Encode YMC assembly instructions to machine code.
    Supports mov, add, sub, mult, div, cmp, jumps.
    Automatically assigns registers for new variables.
    """
    machine = []
    for instr in ymc:
        parts = instr.replace(',', '').split()
        op = parts[0]

        if op == 'mov':
            dst, src = get_register(parts[1]), parts[2]
            if src.isdigit():  # Immediate value
                code = f"{op_codes[op]}{reg_codes[dst]}{int(src):02X}"
            else:  # Register to register
                src = get_register(src)
                code = f"{op_codes[op]}{reg_codes[dst]}{reg_codes[src]}00"

        elif op in ['add','sub','mult','div']:
            dst = get_register(parts[1])
            a = get_register(parts[2])
            b = get_register(parts[3])
            code = f"{op_codes[op]}{reg_codes[dst]}{reg_codes[a]}{reg_codes[b]}"

        elif op == 'cmp':
            a = get_register(parts[1])
            b = get_register(parts[2])
            code = f"{op_codes[op]}{reg_codes[a]}{reg_codes[b]}"

        elif op in ['jmp','jg','jge','jl','jle','je','jne']:
            addr = int(parts[1])
            code = f"{op_codes[op]}{addr:02X}"

        else:
            raise ValueError(f"Unknown instruction: {instr}")

        machine.append(code)
    return machine