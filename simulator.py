import copy
from utils import registers, flags

def simulate(ymc_asm, machine_code):
    reg = {r: 0 for r in registers}
    flags_state = {f: 0 for f in flags}
    results = []
    pc = 0

    def update_flags(result, a=None, b=None, op=None):
        """
        Update ZF, SF, CF, OF based on result and operation.
        """
        # Zero flag
        flags_state['ZF'] = int(result == 0)
        # Sign flag
        flags_state['SF'] = int(result < 0)
        # Carry flag for unsigned arithmetic
        if op in ['add','sub','mult','div']:
            if op == 'add':
                flags_state['CF'] = int(a + b > 255)
            elif op == 'sub':
                flags_state['CF'] = int(a < b)
            elif op == 'mult':
                flags_state['CF'] = int(a * b > 255)
            elif op == 'div':
                flags_state['CF'] = int(False)
        # Overflow flag for signed arithmetic (-128 to 127)
        if op in ['add','sub','mult']:
            if op == 'add':
                flags_state['OF'] = int((a > 0 and b > 0 and result < 0) or (a < 0 and b < 0 and result > 127))
            elif op == 'sub':
                flags_state['OF'] = int((a > 0 and b < 0 and result < 0) or (a < 0 and b > 0 and result > 127))
            elif op == 'mult':
                flags_state['OF'] = int(result < -128 or result > 127)

    while pc < len(ymc_asm):
        instr = ymc_asm[pc]
        parts = instr.replace(',', '').split()
        op = parts[0]

        if op == 'mov':
            dst, src = parts[1], parts[2]
            if src.isdigit():
                val = int(src)
            else:
                val = reg[src]
            reg[dst] = val % 256  # Wrap-around 0-255
            update_flags(reg[dst])

        elif op == 'cmp':
            a, b = parts[1], parts[2]
            result = reg[a] - reg[b]
            update_flags(result)

        elif op in ['add','sub','mult','div']:
            dst, a, b = parts[1], parts[2], parts[3]
            val_a = reg[a]
            val_b = reg[b]
            if op == 'add':
                res = (val_a + val_b) % 256
            elif op == 'sub':
                res = (val_a - val_b) % 256
            elif op == 'mult':
                res = (val_a * val_b) % 256
            elif op == 'div':
                res = val_a // (val_b if val_b != 0 else 1)
            reg[dst] = res
            update_flags(res, a=val_a, b=val_b, op=op)

        elif op in ['jmp','jg','jge','jl','jle','je','jne']:
            addr = int(parts[1])
            jump = False
            if op=='jmp':
                jump = True
            elif op=='jg' and flags_state['ZF']==0 and flags_state['SF']==0:
                jump = True
            elif op=='jge' and flags_state['SF']==0:
                jump = True
            elif op=='jl' and flags_state['SF']==1:
                jump = True
            elif op=='jle' and (flags_state['SF']==1 or flags_state['ZF']==1):
                jump = True
            elif op=='je' and flags_state['ZF']==1:
                jump = True
            elif op=='jne' and flags_state['ZF']==0:
                jump = True
            if jump:
                pc = addr
                continue

        # Record the state
        results.append({
            'HLC': instr,
            'Assembly': instr,
            'Machine': machine_code[pc],
            'Registers': copy.deepcopy(reg),
            'Flags': copy.deepcopy(flags_state)
        })
        pc += 1

    return results