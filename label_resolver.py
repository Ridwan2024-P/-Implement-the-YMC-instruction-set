def resolve_labels(ymc_asm):
    label_map = {}
    new_code = []
    idx = 0
    # detect label addresses
    for line in ymc_asm:
        if ":" in line:
            label = line.replace(":", "")
            label_map[label] = idx
        else:
            new_code.append(line)
            idx += 1
    # replace labels with addresses
    final_code = []
    for line in new_code:
        parts = line.split()
        if parts[0] in ['jmp','jg','jge','jl','jle','je','jne']:
            label = parts[1]
            final_code.append(f"{parts[0]} {label_map[label]}")
        else:
            final_code.append(line)
    return final_code