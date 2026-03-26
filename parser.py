def parse_hlc(lines):
    parsed = []
    for line in lines:
        if line and not line.startswith("#"):
            parsed.append(line)
    return parsed