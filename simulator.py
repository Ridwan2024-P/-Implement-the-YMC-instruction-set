from utils import register_map, initialize_registers, update_flags

def simulate(ymc_lines, machine_code):
    reg = initialize_registers()
    flags = {"ZF":0, "SF":0, "OF":0, "CF":0}
    results = []
    
    for addr, line in enumerate(ymc_lines):
        parts = line.replace(",", "").split()
        modified_regs = {}
        modified_flags = {}
        if not parts or parts[0].startswith("#"):
            results.append([line, addr, line, machine_code[addr], modified_regs, modified_flags])
            continue
        instr = parts[0]
        if instr == "mov":
            if parts[2] in reg:
                reg[parts[1]] = reg[parts[2]]
            else:
                reg[parts[1]] = int(parts[2])
            modified_regs[parts[1]] = reg[parts[1]]
        elif instr == "add":
            reg[parts[1]] = (reg[parts[2]] + reg[parts[3]]) % 256
            modified_regs[parts[1]] = reg[parts[1]]
            update_flags(reg[parts[1]], flags)
        elif instr == "sub":
            reg[parts[1]] = (reg[parts[2]] - reg[parts[3]]) % 256
            modified_regs[parts[1]] = reg[parts[1]]
            update_flags(reg[parts[1]], flags)
        elif instr == "mult":
            reg[parts[1]] = (reg[parts[2]] * reg[parts[3]]) % 256
            modified_regs[parts[1]] = reg[parts[1]]
            update_flags(reg[parts[1]], flags)
        elif instr == "div":
            reg[parts[1]] = (reg[parts[2]] // reg[parts[3]]) % 256
            modified_regs[parts[1]] = reg[parts[1]]
            update_flags(reg[parts[1]], flags)
        results.append([line, addr, line, machine_code[addr], modified_regs.copy(), flags.copy()])
    return results