from parser import parse_hlc
from compiler import compile_hlc_to_ymc
from encoder import encode_ymc
from simulator import simulate
from utils import save_csv

def main():
    with open("input.txt") as f:
        hlc_code = [line.strip() for line in f if line.strip()]
    
    # 1. Parse HLC
    hlc_lines = parse_hlc(hlc_code)
    
    # 2. Compile to YMC assembly
    ymc_asm = compile_hlc_to_ymc(hlc_lines)
    
    # 3. Encode YMC to machine code
    machine_code = encode_ymc(ymc_asm)
    
    # 4. Simulate
    sim_results = simulate(ymc_asm, machine_code)
    
    # 5. Save CSV
    save_csv(sim_results, "output.csv")
    print("✅ Simulation complete. Output saved to output.csv")

if __name__ == "__main__":
    main()