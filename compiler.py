from utils import registers, var_map, op_codes
from parser import get_var_type, validate_variable

class Compiler:
    def __init__(self):
        self.ymc = []
        self.label_count = 0
        self.loop_stack = []
        self.if_stack = []
        self.indent_stack = []
        
    def get_indent(self, line):
        return len(line) - len(line.lstrip())
    
    def new_label(self, prefix):
        label = f"{prefix}_{self.label_count}"
        self.label_count += 1
        return label
    
    def compile_line(self, line):
        line = line.strip()
        if not line or line.startswith('#'):
            return
        
        # Print command - ignore
        if line.startswith('print'):
            return
        
        # Variable validation
        import re
        vars_in_line = re.findall(r'[a-z][a-z0-9]*', line)
        for var in vars_in_line:
            if var not in ['if', 'while', 'else', 'print', 'addsub', 'subadd', 'multdiv']:
                try:
                    validate_variable(var)
                    get_var_type(var)
                except ValueError as e:
                    raise ValueError(f"Error in line '{line}': {e}")
        
        # Complex arithmetic
        if 'addsub' in line:
            dest, expr = [x.strip() for x in line.split('=')]
            args = expr[7:-1].split(',')
            b, c = args[0].strip(), args[1].strip()
            self.ymc.append(f"add {dest}, {b}, {c}")
            self.ymc.append(f"sub {dest}, {dest}, {b}")
            return
        
        if 'subadd' in line:
            dest, expr = [x.strip() for x in line.split('=')]
            args = expr[7:-1].split(',')
            b, c = args[0].strip(), args[1].strip()
            self.ymc.append(f"sub {dest}, {b}, {c}")
            self.ymc.append(f"add {dest}, {dest}, {b}")
            return
        
        if 'multdiv' in line:
            dest, expr = [x.strip() for x in line.split('=')]
            args = expr[8:-1].split(',')
            b, c = args[0].strip(), args[1].strip()
            self.ymc.append(f"mult {dest}, {b}, {c}")
            self.ymc.append(f"div {dest}, {dest}, {b}")
            return
        
        # Simple assignment
        if '=' in line and not any(op in line for op in ['+','-','*','/']):
            dest, right = [x.strip() for x in line.split('=')]
            self.ymc.append(f"mov {dest}, {right}")
            return
        
        # Arithmetic operations
        for op in ['+','-','*','/']:
            if op in line and 'addsub' not in line and 'subadd' not in line and 'multdiv' not in line:
                dest, expr = [x.strip() for x in line.split('=')]
                left, right = expr.split(op)
                if op == '+':
                    self.ymc.append(f"add {dest}, {left.strip()}, {right.strip()}")
                elif op == '-':
                    self.ymc.append(f"sub {dest}, {left.strip()}, {right.strip()}")
                elif op == '*':
                    self.ymc.append(f"mult {dest}, {left.strip()}, {right.strip()}")
                elif op == '/':
                    self.ymc.append(f"div {dest}, {left.strip()}, {right.strip()}")
                return
        
        # If statement
        if line.startswith('if '):
            cond = line[3:].strip()
            else_label = self.new_label("ELSE")
            end_label = self.new_label("ENDIF")
            
            self._emit_condition(cond, else_label)
            self.if_stack.append(('if', else_label, end_label))
            return
        
        # Else statement
        if line.startswith('else'):
            if not self.if_stack or self.if_stack[-1][0] != 'if':
                raise ValueError("else without if")
            _, else_label, end_label = self.if_stack[-1]
            self.if_stack[-1] = ('else', else_label, end_label)
            self.ymc.append(f"jmp {end_label}")
            self.ymc.append(f"{else_label}:")
            return
        
        # While loop
        if line.startswith('while '):
            cond = line[6:].strip()
            start_label = self.new_label("LOOP")
            end_label = self.new_label("END")
            
            self.ymc.append(f"{start_label}:")
            self._emit_condition_opposite(cond, end_label)
            self.loop_stack.append((start_label, end_label))
            return
    
    def _emit_condition(self, cond, target_label):
        """Emit condition check that jumps to target if true"""
        for rel in ['>=','<=','>','<','==','!=']:
            if rel in cond:
                left, right = cond.split(rel)
                self.ymc.append(f"cmp {left.strip()}, {right.strip()}")
                jmp_map = {'>':'jg', '>=':'jge', '<':'jl', '<=':'jle', '==':'je', '!=':'jne'}
                self.ymc.append(f"{jmp_map[rel]} {target_label}")
                return
    
    def _emit_condition_opposite(self, cond, target_label):
        """Emit condition check that jumps to target if false (for while loops)"""
        for rel in ['>=','<=','>','<','==','!=']:
            if rel in cond:
                left, right = cond.split(rel)
                self.ymc.append(f"cmp {left.strip()}, {right.strip()}")
                # Opposite jump for while loop exit
                opp_map = {'>':'jle', '>=':'jl', '<':'jge', '<=':'jg', '==':'jne', '!=':'je'}
                self.ymc.append(f"{opp_map[rel]} {target_label}")
                return
    
    def close_block(self):
        """Close current block (loop or if)"""
        if self.loop_stack:
            start_label, end_label = self.loop_stack.pop()
            self.ymc.append(f"jmp {start_label}")
            self.ymc.append(f"{end_label}:")
        elif self.if_stack and self.if_stack[-1][0] == 'else':
            _, else_label, end_label = self.if_stack.pop()
            self.ymc.append(f"{end_label}:")
        elif self.if_stack and self.if_stack[-1][0] == 'if':
            _, else_label, end_label = self.if_stack.pop()
            self.ymc.append(f"{else_label}:")
            self.ymc.append(f"{end_label}:")
    
    def compile(self, lines):
        """Compile HLC to YMC with indentation handling"""
        self.ymc = []
        self.label_count = 0
        self.loop_stack = []
        self.if_stack = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            indent = self.get_indent(line)
            
            # Check if we need to close blocks
            while self.indent_stack and indent <= self.indent_stack[-1]:
                self.indent_stack.pop()
                self.close_block()
            
            # Compile the line
            self.compile_line(line)
            
            # Look ahead to next line to determine if we need to open a block
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                next_indent = self.get_indent(next_line)
                if next_indent > indent and (line.strip().startswith('if ') or line.strip().startswith('while ')):
                    self.indent_stack.append(indent)
            
            i += 1
        
        # Close any remaining blocks
        while self.indent_stack:
            self.indent_stack.pop()
            self.close_block()
        while self.loop_stack:
            self.close_block()
        while self.if_stack:
            self.close_block()
        
        return self.ymc

def hlc_to_ymc(lines):
    compiler = Compiler()
    return compiler.compile(lines)