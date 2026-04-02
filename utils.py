import csv

registers = ['eax','ebx','ecx','edx']
reg_codes = { 'eax': '00', 'ebx': '01', 'ecx': '02', 'edx': '03' }


var_map = {}  
var_types = {}  
var_initialized = {} 


unsigned_vars_allowed = {'a', 'b', 'c'}
signed_vars_allowed = {'x', 'y', 'z'}

op_codes = {
    'mov':'10', 'add':'20', 'sub':'21', 'mult':'22', 'div':'23',
    'cmp':'30', 'jmp':'40', 'jg':'41', 'jge':'42', 'jl':'43', 'jle':'44', 'je':'45', 'jne':'46'
}

flags = ['ZF','SF','OF','CF']

memory_map = {}
memory_counter = 0
data_memory = {}
data_memory_counter = 0x100

def write_csv(data, filename):
    with open(filename,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['HLC','Assembly','Machine','Registers','Flags','MemoryAddr'])
        for row in data:
            writer.writerow([
                row['HLC'], row['Assembly'], row['Machine'],
                row['Registers'], row['Flags'], row['MemoryAddr']
            ])

def reset_state():
    global var_map, var_types, var_initialized, memory_map, memory_counter, data_memory, data_memory_counter
    var_map = {}
    var_types = {}
    var_initialized = {}
    memory_map = {}
    memory_counter = 0
    data_memory = {}
    data_memory_counter = 0x100