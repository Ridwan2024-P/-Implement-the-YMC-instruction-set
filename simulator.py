import copy
from utils import registers, flags, memory_map
from parser import get_var_type

def simulate(ymc_asm, machine_code):
    reg = {r: 0 for r in registers}
    flags_state = {'ZF': 0, 'SF': 0, 'OF': 0, 'CF': 0}
    results = []
    pc = 0
    
    # Create a mapping from variable names to registers
    var_to_reg = {}
    reg_to_var = {}

    def get_value(src):
        """Get value from either register or immediate"""
        if src in reg:
            return reg[src]
        elif src.lstrip('-').isdigit():
            return int(src) & 0xFF
        else:
            # Try to find which register holds this variable
            if src in var_to_reg:
                return reg[var_to_reg[src]]
            return 0

    def set_value(dst, val):
        """Set value to destination (register or variable)"""
        val = val & 0xFF
        if dst in reg:
            reg[dst] = val
        else:
            # Assign variable to a register
            if dst not in var_to_reg:
                # Find free register
                for r in registers:
                    if r not in var_to_reg.values():
                        var_to_reg[dst] = r
                        break
                else:
                    # Use eax as default
                    var_to_reg[dst] = 'eax'
            reg[var_to_reg[dst]] = val

    def update_flags(result, a=None, b=None, op=None, is_unsigned=True):
        result_masked = result & 0xFF

        # Zero Flag
        flags_state['ZF'] = 1 if result_masked == 0 else 0

        # Sign Flag
        if not is_unsigned:
            flags_state['SF'] = 1 if (result_masked & 0x80) else 0
        else:
            flags_state['SF'] = 0

        # Carry and Overflow flags
        if op in ['add', 'sub', 'mult']:
            if is_unsigned:
                if op == 'add':
                    flags_state['CF'] = 1 if result > 255 else 0
                elif op == 'sub':
                    flags_state['CF'] = 1 if a < b else 0
                elif op == 'mult':
                    flags_state['CF'] = 1 if result > 255 else 0
            else:
                if op == 'add':
                    flags_state['OF'] = 1 if ((a > 0 and b > 0 and result < -128) or 
                                            (a < 0 and b < 0 and result > 127)) else 0
                elif op == 'sub':
                    flags_state['OF'] = 1 if ((a > 0 and b < 0 and result < -128) or 
                                            (a < 0 and b > 0 and result > 127)) else 0
                elif op == 'mult':
                    flags_state['OF'] = 1 if (result < -128 or result > 127) else 0

    while pc < len(ymc_asm):
        instr = ymc_asm[pc]
        parts = instr.replace(',', '').split()
        
        if not parts:
            pc += 1
            continue
            
        op = parts[0]

        # Handle labels (lines ending with colon)
        if op.endswith(':'):
            pc += 1
            continue

        print(f"DEBUG: PC={pc}, executing: {instr}")  # Debug output

        if op == 'mov':
            dst, src = parts[1], parts[2]
            
            if src.lstrip('-').isdigit():
                val = int(src) & 0xFF
            else:
                val = get_value(src)
            
            set_value(dst, val)
            
            try:
                is_unsigned = (get_var_type(dst) == 'unsigned')
            except:
                is_unsigned = True
            
            update_flags(val, is_unsigned=is_unsigned)
            
            print(f"  MOV: {dst} = {val}")

        elif op == 'cmp':
            a, b = parts[1], parts[2]
            val_a = get_value(a)
            val_b = get_value(b)
            
            # Set flags based on comparison
            flags_state['ZF'] = 1 if (val_a == val_b) else 0
            flags_state['CF'] = 1 if (val_a < val_b) else 0
            flags_state['SF'] = 1 if ((val_a - val_b) < 0) else 0
            flags_state['OF'] = 0
            
            print(f"  CMP: {a}({val_a}) vs {b}({val_b}) -> ZF={flags_state['ZF']}, CF={flags_state['CF']}, SF={flags_state['SF']}")

        elif op in ['add', 'sub', 'mult', 'div']:
            dst, a, b = parts[1], parts[2], parts[3]
            val_a = get_value(a)
            val_b = get_value(b)
            
            if op == 'add':
                res = val_a + val_b
            elif op == 'sub':
                res = val_a - val_b   
            elif op == 'mult':
                res = val_a * val_b
            else:  # div
                res = val_a // (val_b if val_b != 0 else 1)
            
            set_value(dst, res)
            
            try:
                is_unsigned = (get_var_type(dst) == 'unsigned')
            except:
                is_unsigned = True
            
            update_flags(res, a=val_a, b=val_b, op=op, is_unsigned=is_unsigned)
            
            print(f"  {op.upper()}: {dst} = {val_a} {op} {val_b} = {res & 0xFF}")

        elif op == 'print':
            var_name = parts[1]
            value = get_value(var_name)
            print(f"PRINT: {var_name} = {value}")

        elif op in ['jmp', 'jg', 'jge', 'jl', 'jle', 'je', 'jne']:
            addr = int(parts[1])
            jump = False
            
            print(f"  JUMP: {op} to {addr}, flags: ZF={flags_state['ZF']}, CF={flags_state['CF']}, SF={flags_state['SF']}, OF={flags_state['OF']}")

            if op == 'jmp':
                jump = True
            elif op == 'jg':   # Jump if greater (signed)
                jump = (flags_state['ZF'] == 0 and flags_state['SF'] == flags_state['OF'])
            elif op == 'jge':  # Jump if greater or equal (signed)
                jump = (flags_state['SF'] == flags_state['OF'])
            elif op == 'jl':   # Jump if less (signed)
                jump = (flags_state['SF'] != flags_state['OF'])
            elif op == 'jle':  # Jump if less or equal (signed)
                jump = (flags_state['ZF'] == 1 or flags_state['SF'] != flags_state['OF'])
            elif op == 'je':   # Jump if equal
                jump = (flags_state['ZF'] == 1)
            elif op == 'jne':  # Jump if not equal
                jump = (flags_state['ZF'] == 0)

            if jump:
                print(f"  JUMP TAKEN to {addr}")
                pc = addr
                continue
            else:
                print(f"  JUMP NOT TAKEN")

        # Record state
        machine_code_hex = machine_code[pc] if pc < len(machine_code) else "00"
        
        # Create a readable register state
        reg_state = {}
        for var, reg_name in var_to_reg.items():
            reg_state[var] = reg[reg_name]
        # Also include direct register values
        for r in registers:
            if r not in reg_state.values():
                reg_state[r] = reg[r]
        
        results.append({
            'HLC': instr,
            'Assembly': instr,
            'Machine': machine_code_hex,
            'Registers': copy.deepcopy(reg_state),
            'Flags': copy.deepcopy(flags_state),
            'MemoryAddr': memory_map.get(instr, pc)
        })

        pc += 1

    return results