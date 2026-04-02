import copy
from utils import registers, flags, memory_map
from parser import get_var_type

def simulate(ymc_asm, machine_code):
    reg = {r: 0 for r in registers}
    flags_state = {f: 0 for f in flags}
    results = []
    pc = 0

    def update_flags(result, a=None, b=None, op=None, is_unsigned=True):
        # Mask to 8-bit
        result_masked = result & 0xFF
        
        flags_state['ZF'] = int(result_masked == 0)
        
        if not is_unsigned:
            # Signed: check if negative (bit 7 set)
            flags_state['SF'] = int(result_masked > 127)
        else:
            flags_state['SF'] = 0
        
        if op in ['add', 'sub', 'mult']:
            if is_unsigned:
                # CF for unsigned
                if op == 'add':
                    flags_state['CF'] = int(result > 255)
                elif op == 'sub':
                    flags_state['CF'] = int(a < b)
                elif op == 'mult':
                    flags_state['CF'] = int(result > 255)
            else:
                # OF for signed overflow
                if op == 'add':
                    flags_state['OF'] = int((a > 0 and b > 0 and result < -128) or 
                                            (a < 0 and b < 0 and result > 127))
                elif op == 'sub':
                    flags_state['OF'] = int((a > 0 and b < 0 and result < -128) or 
                                            (a < 0 and b > 0 and result > 127))
                elif op == 'mult':
                    flags_state['OF'] = int(result < -128 or result > 127)
        elif op == 'cmp':
            if is_unsigned:
                flags_state['CF'] = int(a < b)
            else:
                result_signed = result
                if result_signed > 127:
                    result_signed = result_signed - 256
                flags_state['SF'] = int(result_signed < 0)
                flags_state['OF'] = 0

    while pc < len(ymc_asm):
        instr = ymc_asm[pc]
        
        if instr.startswith('#'):
            results.append({
                'HLC': instr,
                'Assembly': instr,
                'Machine': machine_code[pc] if pc < len(machine_code) else "00",
                'Registers': copy.deepcopy(reg),
                'Flags': copy.deepcopy(flags_state),
                'MemoryAddr': memory_map.get(instr, pc)
            })
            pc += 1
            continue

        parts = instr.replace(',', '').split()
        op = parts[0]

        if op == 'mov':
            dst, src = parts[1], parts[2]
            if src.isdigit() or (src.startswith('-') and src[1:].isdigit()):
                val = int(src)
                try:
                    var_type = get_var_type(dst)
                    if var_type == 'unsigned':
                        val = val & 0xFF
                    else:
                        if val < 0:
                            val = 256 + val
                        val = val & 0xFF
                except:
                    val = val & 0xFF
            else:
                val = reg.get(src, 0)
            reg[dst] = val
            try:
                is_unsigned = (get_var_type(dst) == 'unsigned')
            except:
                is_unsigned = True
            update_flags(val, is_unsigned=is_unsigned)

        elif op == 'cmp':
            a, b = parts[1], parts[2]
            val_a = reg.get(a, 0)
            val_b = reg.get(b, 0)
            result = val_a - val_b
            try:
                is_unsigned = (get_var_type(a) == 'unsigned')
            except:
                is_unsigned = True
            update_flags(result, a=val_a, b=val_b, op='cmp', is_unsigned=is_unsigned)

        elif op in ['add', 'sub', 'mult', 'div']:
            dst, a, b = parts[1], parts[2], parts[3]
            val_a = reg.get(a, 0)
            val_b = reg.get(b, 0)
            
            try:
                is_unsigned = (get_var_type(dst) == 'unsigned')
            except:
                is_unsigned = True
            
            if op == 'add':
                res = val_a + val_b
            elif op == 'sub':
                res = val_a - val_b
            elif op == 'mult':
                res = val_a * val_b
            else:  # div
                res = val_a // (val_b if val_b != 0 else 1)
            
            if is_unsigned:
                reg[dst] = res & 0xFF
            else:
                reg[dst] = res & 0xFF
            
            update_flags(res, a=val_a, b=val_b, op=op, is_unsigned=is_unsigned)

        elif op in ['jmp', 'jg', 'jge', 'jl', 'jle', 'je', 'jne']:
            addr = int(parts[1])
            jump = False
            if op == 'jmp':
                jump = True
            elif op == 'jg' and flags_state['ZF'] == 0 and flags_state['SF'] == 0:
                jump = True
            elif op == 'jge' and flags_state['SF'] == 0:
                jump = True
            elif op == 'jl' and flags_state['SF'] == 1:
                jump = True
            elif op == 'jle' and (flags_state['SF'] == 1 or flags_state['ZF'] == 1):
                jump = True
            elif op == 'je' and flags_state['ZF'] == 1:
                jump = True
            elif op == 'jne' and flags_state['ZF'] == 0:
                jump = True
            
            if jump:
                pc = addr
                continue

        results.append({
            'HLC': instr,
            'Assembly': instr,
            'Machine': machine_code[pc] if pc < len(machine_code) else "00",
            'Registers': copy.deepcopy(reg),
            'Flags': copy.deepcopy(flags_state),
            'MemoryAddr': memory_map.get(instr, pc)
        })
        pc += 1
    
    return results