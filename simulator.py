from utils import registers, flags

def simulate(ymc_asm, machine_code):
    reg = {r:0 for r in registers}
    flags_state = {f:0 for f in flags}
    results = []

    for idx, instr in enumerate(ymc_asm):
        parts = instr.replace(',','').split()
        op = parts[0]
        modified_regs, modified_flags = [], []

        if op == 'mov':
            dst, src = parts[1], parts[2]
            if src.isdigit():
                reg[dst] = int(src)
            else:
                reg[dst] = reg[src]
            modified_regs.append(dst)
        elif op in ['add','sub','mult','div']:
            dst, src1, src2 = parts[1], parts[2], parts[3]
            if op == 'add':
                res = reg[src1] + reg[src2]
            elif op == 'sub':
                res = reg[src1] - reg[src2]
            elif op == 'mult':
                res = reg[src1] * reg[src2]
            elif op == 'div':
                res = reg[src1] // (reg[src2] if reg[src2]!=0 else 1)
            # overflow 8-bit
            res = res % 256
            reg[dst] = res
            modified_regs.append(dst)
            flags_state['ZF'] = int(res==0)
            flags_state['SF'] = int(res>=128)
            flags_state['OF'] = int(res>255)
        results.append({
            'HLC': instr,
            'Assembly': instr,
            'Machine': machine_code[idx],
            'Registers': reg.copy(),
            'Flags': flags_state.copy()
        })
    return results