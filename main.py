from parser import parse_hlc
from compiler import compile_to_ymc
from encoder import encode_instruction
from simulator import simulate
from utils import write_csv

def main():
    hlc = parse_hlc("input.txt")

    ymc = compile_to_ymc(hlc)

    print("=== YMC Assembly ===")
    for i in ymc:
        print(i)

    print("\n=== Machine Code ===")
    for i in ymc:
        print(encode_instruction(i))

    sim = simulate(ymc)

    write_csv(sim)

    print("\n✅ CSV Generated: output.csv")

if __name__ == "__main__":
    main()