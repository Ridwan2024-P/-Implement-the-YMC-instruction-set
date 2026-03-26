def parse_hlc(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        line = line.strip()
        if line:
            cleaned.append(line)

    return cleaned