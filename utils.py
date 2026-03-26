import csv

register_map = {"eax":"eax", "ebx":"ebx", "ecx":"ecx", "edx":"edx"}

def initialize_registers():
    return {reg:0 for reg in register_map}

def update_flags(value, flags):
    flags["ZF"] = int(value == 0)
    flags["SF"] = int(value & 0x80 > 0)
    flags["OF"] = 0
    flags["CF"] = 0

def save_csv(sim_results, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["HLC", "Address", "YMC Assembly", "Machine Code", "Registers", "Flags"])
        for row in sim_results:
            writer.writerow(row)