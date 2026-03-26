register_map = {
    'a': 'eax',
    'b': 'ebx',
    'c': 'ecx',
    'x': 'edx',
    'y': 'eax',
    'z': 'ebx'
}

def compile_to_ymc(hlc_lines):
    ymc = []

    for line in hlc_lines:
        if '=' in line:
            left, right = line.split('=')
            left = left.strip()
            right = right.strip()

            dest = register_map[left]

            # number assignment
            if right.isdigit():
                ymc.append(f"mov {dest}, {right}")

            # addition
            elif '+' in right:
                op1, op2 = right.split('+')
                op1 = register_map.get(op1.strip(), op1.strip())
                op2 = register_map.get(op2.strip(), op2.strip())
                ymc.append(f"add {dest}, {op1}, {op2}")

            # subtraction
            elif '-' in right:
                op1, op2 = right.split('-')
                op1 = register_map.get(op1.strip(), op1.strip())
                op2 = register_map.get(op2.strip(), op2.strip())
                ymc.append(f"sub {dest}, {op1}, {op2}")

    return ymc