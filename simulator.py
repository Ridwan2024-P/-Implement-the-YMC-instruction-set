from utils import registers, flags
from compiler import get_register, memory_map, var_map

def simulate(ymc_asm, machine_code):
    reg = {r:0 for r in registers}
    flags_state = {f:0 for f in flags}
    results = []
    pc = 0
    while pc < len(ymc_asm):
        instr = ymc_asm[pc]
        parts = instr.replace(',','').split()
        op = parts[0]

        # handle spilled variable load
        for var in var_map:
            if var in memory_map:
                reg[var_map[var]] = memory_map[var]

        if op == 'mov':
            dst, src = parts[1], parts[2]
            dst_reg = get_register(dst)
            if src.isdigit():
                reg[dst_reg] = int(src)
            else:
                src_reg = get_register(src)
                reg[dst_reg] = reg[src_reg]

        elif op == 'cmp':
            a,b = parts[1],parts[2]
            a_reg = get_register(a)
            b_reg = get_register(b)
            res = reg[a_reg]-reg[b_reg]
            flags_state['ZF'] = int(res==0)
            flags_state['SF'] = int(res<0)

        elif op in ['jg','jge','jl','jle','je','jne']:
            addr = int(parts[1])
            jump = False
            if op=='jg' and flags_state['ZF']==0 and flags_state['SF']==0: jump=True
            elif op=='jge' and flags_state['SF']==0: jump=True
            elif op=='jl' and flags_state['SF']==1: jump=True
            elif op=='jle' and (flags_state['SF']==1 or flags_state['ZF']==1): jump=True
            elif op=='je' and flags_state['ZF']==1: jump=True
            elif op=='jne' and flags_state['ZF']==0: jump=True
            if jump: pc = addr; continue

        elif op == 'jmp':
            pc = int(parts[1]); continue

        elif op in ['add','sub','mult','div']:
            dst,a,b = parts[1],parts[2],parts[3]
            dst_reg = get_register(dst)
            a_reg = get_register(a)
            b_reg = get_register(b)
            if op=='add': reg[dst_reg]=reg[a_reg]+reg[b_reg]
            elif op=='sub': reg[dst_reg]=reg[a_reg]-reg[b_reg]
            elif op=='mult': reg[dst_reg]=reg[a_reg]*reg[b_reg]
            elif op=='div': reg[dst_reg]=reg[a_reg]//(reg[b_reg] if reg[b_reg]!=0 else 1)

        # store spilled variables
        for var in memory_map:
            memory_map[var] = reg[var_map[var]]

        results.append({
            'HLC': instr,
            'Assembly': instr,
            'Machine': machine_code[pc],
            'Registers': reg.copy(),
            'Flags': flags_state.copy()
        })
        pc += 1
    return results