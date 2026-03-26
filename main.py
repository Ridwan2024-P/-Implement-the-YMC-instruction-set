from compiler import hlc_to_ymc
from encoder import encode_ymc
from simulator import simulate
from utils import write_csv

def main():
    # Input HLC file
    with open("input.txt") as f:
        hlc_code = f.read().splitlines()

    # HLC -> YMC assembly
    ymc_asm = hlc_to_ymc(hlc_code)

    # YMC assembly -> machine code
    machine_code = encode_ymc(ymc_asm)

    # Simulate processor execution
    sim_results = simulate(ymc_asm, machine_code)

    # Output CSV
    write_csv(sim_results, "output.csv")
    print("✅ Simulation complete. CSV saved as output.csv")

if __name__ == "__main__":
    main()