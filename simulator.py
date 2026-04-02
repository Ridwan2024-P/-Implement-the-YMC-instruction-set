from utils import registers, flags

def simulate(ymc_asm, machine_code):
    reg = {r:0 for r in registers}
    flags_state = {f:0 for f in flags}
    results = []

    pc = 0

    while pc < len(ymc_asm):
        instr = ymc_asm[pc]
        parts = instr.replace(',','').split()
        op = parts[0]

        if op == 'mov':
            dst, src = parts[1], parts[2]
            reg[dst] = int(src) if src.isdigit() else reg[src]

        elif op == 'cmp':
            a,b = parts[1],parts[2]
            res = reg[a] - reg[b]
            flags_state['ZF'] = int(res == 0)
            flags_state['SF'] = int(res < 0)

        elif op in ['jg','jge','jl','jle','je','jne']:
            addr = int(parts[1])
            jump = False

            if op=='jg' and flags_state['ZF']==0 and flags_state['SF']==0:
                jump=True
            elif op=='jge' and flags_state['SF']==0:
                jump=True
            elif op=='jl' and flags_state['SF']==1:
                jump=True
            elif op=='jle' and (flags_state['SF']==1 or flags_state['ZF']==1):
                jump=True
            elif op=='je' and flags_state['ZF']==1:
                jump=True
            elif op=='jne' and flags_state['ZF']==0:
                jump=True

            if jump:
                pc = addr
                continue

        elif op == 'jmp':
            pc = int(parts[1])
            continue

        elif op in ['add','sub','mult','div']:
            dst,a,b = parts[1],parts[2],parts[3]

            if op=='add':
                reg[dst]=reg[a]+reg[b]
            elif op=='sub':
                reg[dst]=reg[a]-reg[b]
            elif op=='mult':
                reg[dst]=reg[a]*reg[b]
            elif op=='div':
                reg[dst]=reg[a]//(reg[b] if reg[b]!=0 else 1)

        results.append({
            'HLC': instr,
            'Assembly': instr,
            'Machine': machine_code[pc],
            'Registers': reg.copy(),
            'Flags': flags_state.copy()
        })

        pc += 1

    return results