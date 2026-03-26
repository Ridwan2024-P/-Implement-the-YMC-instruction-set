import csv

registers = ['eax','ebx','ecx','edx']
reg_map = {r:i for i,r in enumerate(registers)}
flags = ['ZF','SF','OF','CF']

def write_csv(data, filename):
    with open(filename,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['HLC','Assembly','Machine','Registers','Flags'])
        for row in data:
            writer.writerow([
                row['HLC'],
                row['Assembly'],
                row['Machine'],
                row['Registers'],
                row['Flags']
            ])