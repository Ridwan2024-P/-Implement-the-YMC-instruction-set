"""
Parser module for handling variable declarations and type tracking
"""
from utils import unsigned_vars_allowed, signed_vars_allowed, var_types, var_initialized

def parse_declarations(lines):
    """Parse variable declarations from first lines"""
    remaining_lines = []
    declarations_found = 0
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            remaining_lines.append(line)
            continue
        
        # Check if this is a declaration line (comma-separated variable names, no operators)
        if ',' in line and '=' not in line and not any(op in line for op in ['+','-','*','/','if','while']):
            vars_list = [v.strip() for v in line.split(',')]
            
            # Check if all variables are valid
            all_unsigned = all(v in unsigned_vars_allowed for v in vars_list)
            all_signed = all(v in signed_vars_allowed for v in vars_list)
            
            if all_unsigned:
                for var in vars_list:
                    var_types[var] = 'unsigned'
                    var_initialized[var] = False
                declarations_found += 1
                continue
            elif all_signed:
                for var in vars_list:
                    var_types[var] = 'signed'
                    var_initialized[var] = False
                declarations_found += 1
                continue
            elif declarations_found < 2:
                # Mixed declaration - not allowed
                raise ValueError(f"Invalid declaration: Cannot mix unsigned and signed: {line}")
        
        remaining_lines.append(line)
    
    return remaining_lines

def get_var_type(var):
    """Get variable type"""
    if var in var_types:
        return var_types[var]
    
    # Auto-detect based on name
    if var in unsigned_vars_allowed:
        var_types[var] = 'unsigned'
        return 'unsigned'
    elif var in signed_vars_allowed:
        var_types[var] = 'signed'
        return 'signed'
    else:
        raise ValueError(f"Invalid variable: {var}. Use a,b,c (unsigned) or x,y,z (signed)")

def validate_variable(var):
    """Validate variable limits"""
    if var in unsigned_vars_allowed:
        used = [v for v in var_types if var_types.get(v) == 'unsigned']
        if var not in used and len(used) >= 3:
            raise ValueError(f"Max 3 unsigned vars. Using: {used}")
    elif var in signed_vars_allowed:
        used = [v for v in var_types if var_types.get(v) == 'signed']
        if var not in used and len(used) >= 3:
            raise ValueError(f"Max 3 signed vars. Using: {used}")
    return True