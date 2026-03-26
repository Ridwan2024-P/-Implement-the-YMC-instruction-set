def simulate(assembly):
    regs = {'eax':0,'ebx':0,'ecx':0,'edx':0}
    flags = {'ZF':0,'SF':0}

    pc = 0
    output = []

    while pc < len(assembly):
        inst = assembly[pc]
        parts = inst.split()
        op = parts[0]

        reg_change = ""
        flag_change = ""

        if op == 'mov':
            r = parts[1].replace(',', '')
            val = int(parts[2])
            regs[r] = val
            reg_change = f"{r}={val}"

        elif op == 'add':
            r,r1,r2 = parts[1].replace(',', ''), parts[2].replace(',', ''), parts[3]
            res = regs[r1] + regs[r2]
            regs[r] = res
            flags['ZF'] = int(res==0)
            flags['SF'] = int(res<0)
            reg_change = f"{r}={res}"

        elif op == 'sub':
            r,r1,r2 = parts[1].replace(',', ''), parts[2].replace(',', ''), parts[3]
            res = regs[r1] - regs[r2]
            regs[r] = res
            flags['ZF'] = int(res==0)
            flags['SF'] = int(res<0)
            reg_change = f"{r}={res}"

        elif op == 'cmp':
            r = parts[1].replace(',', '')
            val = int(parts[2])
            res = regs[r] - val
            flags['ZF'] = int(res==0)
            flags['SF'] = int(res<0)

        elif op == 'jmp':
            pc = int(parts[1])
            continue

        elif op == 'jg':
            if flags['ZF']==0 and flags['SF']==0:
                pc = int(parts[1])
                continue

        elif op == 'jle':
            if flags['SF']==1 or flags['ZF']==1:
                pc = int(parts[1])
                continue

        output.append((pc, inst, reg_change, str(flags)))
        pc += 1

    return output