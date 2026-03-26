def simulate(assembly):
    registers = {
        'eax': 0,
        'ebx': 0,
        'ecx': 0,
        'edx': 0
    }

    flags = {
        'ZF': 0,
        'SF': 0,
        'OF': 0,
        'CF': 0
    }

    result = []

    for addr, inst in enumerate(assembly):
        parts = inst.split()
        op = parts[0]

        modified_reg = ""
        modified_flag = ""

        if op == 'mov':
            reg = parts[1].replace(',', '')
            val = int(parts[2])
            registers[reg] = val
            modified_reg = f"{reg}={val}"

        elif op == 'add':
            r, r1, r2 = parts[1].replace(',', ''), parts[2].replace(',', ''), parts[3]
            res = registers[r1] + registers[r2]
            registers[r] = res

            flags['ZF'] = int(res == 0)
            flags['SF'] = int(res < 0)

            modified_reg = f"{r}={res}"
            modified_flag = f"ZF={flags['ZF']} SF={flags['SF']}"

        elif op == 'sub':
            r, r1, r2 = parts[1].replace(',', ''), parts[2].replace(',', ''), parts[3]
            res = registers[r1] - registers[r2]
            registers[r] = res

            flags['ZF'] = int(res == 0)
            flags['SF'] = int(res < 0)

            modified_reg = f"{r}={res}"
            modified_flag = f"ZF={flags['ZF']} SF={flags['SF']}"

        result.append((addr, inst, modified_reg, modified_flag))

    return result