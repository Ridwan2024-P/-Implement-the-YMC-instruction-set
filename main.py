from compiler import hlc_to_ymc
from encoder import encode_ymc
from simulator import simulate
from utils import write_csv, reset_state
from label_resolver import resolve_labels
from parser import parse_declarations

def main():
    reset_state()
    
    with open("input.txt", "r") as f:
        hlc_code = f.read().splitlines()
    
    # Parse variable declarations
    hlc_code = parse_declarations(hlc_code)
    
    # Compile
    ymc_asm = hlc_to_ymc(hlc_code)
    
    # Resolve labels
    ymc_asm = resolve_labels(ymc_asm)
    
    # Encode to machine code
    machine_code = encode_ymc(ymc_asm)
    
    # Simulate
    sim_results = simulate(ymc_asm, machine_code)
    
    # Write output
    write_csv(sim_results, "output.csv")
    
    print("=" * 60)
    print("COMPILATION COMPLETE")
    print("=" * 60)
    print(f"YMC Instructions: {len(ymc_asm)}")
    print(f"Machine Code Bytes: {len(machine_code)}")
    print(f"Output saved to: output.csv")
    print("=" * 60)

if __name__ == "__main__":
    main()