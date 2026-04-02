from utils import reg_codes, var_map, op_codes, registers, memory_map, memory_counter, data_memory, data_memory_counter
from parser import get_var_type

temp_reg_idx = 0
spill_memory = {}

def get_register(var):
    global temp_reg_idx, spill_memory, data_memory_counter
    if var in var_map:
        return var_map[var]
    else:
        if temp_reg_idx < len(registers):
            reg = registers[temp_reg_idx]
            var_map[var] = reg
            temp_reg_idx += 1
            return reg
        else:
            spill_addr = data_memory_counter
            data_memory[spill_addr] = 0
            data_memory_counter += 1
            spill_memory[var] = spill_addr
            return None

def get_immediate_value(value, var_type='unsigned'):
    val = int(value)
    if var_type == 'unsigned':
        val = val & 0xFF
    else:
        if val < 0:
            val = 256 + val
        val = val & 0xFF
    return f"{val:02X}"

def encode_ymc(ymc):
    global memory_counter
    machine = []
    
    for instr in ymc:
        addr = memory_counter
        memory_map[instr] = addr
        memory_counter += 1

        if instr.startswith('#'):
            machine.append("00")
            continue

        parts = instr.replace(',', '').split()
        op = parts[0]

        if op == 'mov':
            dst, src = parts[1], parts[2]
            dst_reg = get_register(dst)
            
            if src.isdigit() or (src.startswith('-') and src[1:].isdigit()):
                try:
                    var_type = get_var_type(dst)
                except:
                    var_type = 'unsigned'
                code = f"{op_codes[op]}{reg_codes.get(dst_reg,'00')}{get_immediate_value(src, var_type)}"
            else:
                src_reg = get_register(src)
                code = f"{op_codes[op]}{reg_codes.get(dst_reg,'00')}{reg_codes.get(src_reg,'00')}00"

        elif op in ['add','sub','mult','div']:
            dst = get_register(parts[1])
            a = get_register(parts[2])
            b = get_register(parts[3])
            code = f"{op_codes[op]}{reg_codes.get(dst,'00')}{reg_codes.get(a,'00')}{reg_codes.get(b,'00')}"

        elif op == 'cmp':
            a = get_register(parts[1])
            b = get_register(parts[2])
            code = f"{op_codes[op]}{reg_codes.get(a,'00')}{reg_codes.get(b,'00')}00"

        elif op in ['jmp','jg','jge','jl','jle','je','jne']:
            addr_val = int(parts[1])
            code = f"{op_codes[op]}{addr_val:02X}"

        else:
            raise ValueError(f"Unknown instruction: {instr}")

        machine.append(code)
    return machine