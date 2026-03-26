register_map = {
    'a': 'eax',
    'b': 'ebx',
    'c': 'ecx',
    'x': 'edx',
    'y': 'eax',
    'z': 'ebx'
}

label_count = 0

def new_label():
    global label_count
    label = f"L{label_count}"
    label_count += 1
    return label

def compile_to_ymc(hlc_lines):
    ymc = []
    i = 0

    while i < len(hlc_lines):
        line = hlc_lines[i]

        # IF
        if line.startswith("if"):
            cond = line.replace("if", "").strip()
            var, op, val = cond.split()

            reg = register_map[var]
            label_true = new_label()
            label_end = new_label()

            ymc.append(f"cmp {reg}, {val}")
            ymc.append(f"jg {label_true}")
            ymc.append(f"jmp {label_end}")
            ymc.append(f"{label_true}:")

            i += 1
            while i < len(hlc_lines) and hlc_lines[i].startswith("    "):
                inner = hlc_lines[i].strip()
                ymc += compile_to_ymc([inner])
                i += 1

            ymc.append(f"{label_end}:")
            continue

        # WHILE
        elif line.startswith("while"):
            cond = line.replace("while", "").strip()
            var, op, val = cond.split()

            start = new_label()
            end = new_label()

            ymc.append(f"{start}:")
            ymc.append(f"cmp {register_map[var]}, {val}")
            ymc.append(f"jle {end}")

            i += 1
            while i < len(hlc_lines) and hlc_lines[i].startswith("    "):
                inner = hlc_lines[i].strip()
                ymc += compile_to_ymc([inner])
                i += 1

            ymc.append(f"jmp {start}")
            ymc.append(f"{end}:")
            continue

        # NORMAL ASSIGNMENT
        elif "=" in line:
            left, right = line.split("=")
            left = left.strip()
            right = right.strip()
            dest = register_map[left]

            if right.isdigit():
                ymc.append(f"mov {dest}, {right}")

            elif '+' in right:
                a, b = right.split('+')
                a = register_map.get(a.strip(), a.strip())
                b = register_map.get(b.strip(), b.strip())
                ymc.append(f"add {dest}, {a}, {b}")

            elif '-' in right:
                a, b = right.split('-')
                a = register_map.get(a.strip(), a.strip())
                b = register_map.get(b.strip(), b.strip())
                ymc.append(f"sub {dest}, {a}, {b}")

        i += 1

    return ymc