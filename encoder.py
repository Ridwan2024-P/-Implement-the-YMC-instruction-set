def encode_ymc(ymc_lines):
    code = []
    for i, line in enumerate(ymc_lines):
        parts = line.split()
        if not parts or parts[0].startswith("#"):
            code.append("00 00")
            continue
        instr = parts[0]
        if instr == "mov":
            code.append("10 00")
        elif instr == "add":
            code.append("20 00")
        elif instr == "sub":
            code.append("21 00")
        elif instr == "mult":
            code.append("22 00")
        elif instr == "div":
            code.append("23 00")
        else:
            code.append("00 00")
    return code