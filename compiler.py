from utils import register_map

def compile_hlc_to_ymc(hlc_lines):
    ymc = []
    label_count = 0
    for line in hlc_lines:
        line = line.strip()
        if "=" in line:
            dest, expr = map(str.strip, line.split("=", 1))
            # Two-operand arithmetic
            if '+' in expr:
                left, right = map(str.strip, expr.split('+'))
                if '*' in right:
                    r1, r2 = map(str.strip, right.split('*'))
                    ymc.append(f"mult {dest}, {left}, {r1}")
                else:
                    ymc.append(f"add {dest}, {left}, {right}")
            elif '*' in expr:
                r1, r2 = map(str.strip, expr.split('*'))
                ymc.append(f"mult {dest}, {r1}, {r2}")
            elif '/' in expr:
                r1, r2 = map(str.strip, expr.split('/'))
                ymc.append(f"div {dest}, {r1}, {r2}")
            else:
                # mov immediate or reg
                if expr in register_map:
                    ymc.append(f"mov {dest}, {expr}")
                else:
                    ymc.append(f"mov {dest}, {expr}")
        elif line.startswith("if") or line.startswith("while"):
            ymc.append(f"# {line}")
        elif line.startswith("print"):
            ymc.append(f"# {line}")
        else:
            ymc.append(f"# {line}")
    return ymc