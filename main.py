from parser import parse_hlc
from compiler import compile_to_ymc
from label_resolver import resolve_labels
from encoder import encode_instruction
from simulator import simulate
from utils import write_csv

def main():
    hlc = parse_hlc("input.txt")

    assembly = compile_to_ymc(hlc)
    resolved = resolve_labels(assembly)

    print("\n=== Assembly ===")
    for i in resolved:
        print(i)

    print("\n=== Machine Code ===")
    for i in resolved:
        print(encode_instruction(i))

    sim = simulate(resolved)
    write_csv(sim)

    print("\n🔥 DONE (Advanced Version)")

if __name__ == "__main__":
    main()