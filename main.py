from compiler import hlc_to_ymc
from encoder import encode_ymc
from simulator import simulate
from utils import write_csv
from label_resolver import resolve_labels

def main():
    with open("input.txt") as f:
        hlc_code = f.read().splitlines()

    ymc_asm = hlc_to_ymc(hlc_code)
    ymc_asm = resolve_labels(ymc_asm)
    machine_code = encode_ymc(ymc_asm)
    sim_results = simulate(ymc_asm, machine_code)
    write_csv(sim_results, "output.csv")
    print("Simulation complete. CSV saved as output.csv")

if __name__ == "__main__":
    main()