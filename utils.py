import csv

registers = ['eax','ebx','ecx','edx']

reg_codes = {
    'eax': '00',
    'ebx': '01',
    'ecx': '02',
    'edx': '03'
}

var_map = {
    'a':'eax',
    'b':'ebx',
    'c':'ecx',
    'd':'edx',
    'x':'eax',
    'y':'ebx',
    'z':'ecx'
}

op_codes = {
    'mov':'10',
    'add':'20',
    'sub':'21',
    'mult':'22',
    'div':'23',
    'cmp':'30',
    'jmp':'40',
    'jg':'41',
    'jge':'42',
    'jl':'43',
    'jle':'44',
    'je':'45',
    'jne':'46'
}

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