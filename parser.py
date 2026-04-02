from utils import var_types, var_initialized, unsigned_vars_allowed, signed_vars_allowed

def parse_declarations(lines):
    """Parse variable declarations and remove them from code"""
    result = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a declaration line (contains commas and no operators)
        if ',' in line and not any(op in line for op in ['=', 'if', 'while', 'print']):
            # Parse variable declaration line like "a, b, c" or "x, y, z"
            vars_list = [v.strip() for v in line.split(',')]
            for var in vars_list:
                # Determine type based on variable name
                if var in unsigned_vars_allowed:
                    var_types[var] = 'unsigned'
                elif var in signed_vars_allowed:
                    var_types[var] = 'signed'
                elif var in ['a', 'b', 'c']:
                    var_types[var] = 'unsigned'
                elif var in ['x', 'y', 'z']:
                    var_types[var] = 'signed'
                else:
                    # Default based on first letter
                    if var.startswith(('a', 'b', 'c')):
                        var_types[var] = 'unsigned'
                    else:
                        var_types[var] = 'signed'
                var_initialized[var] = 0
            # Don't add declaration line to result
        else:
            result.append(line)
    return result

def get_var_type(var_name):
    """Get variable type (signed/unsigned)"""
    if var_name in var_types:
        return var_types[var_name]
    # Default based on naming convention
    if var_name in ['a', 'b', 'c'] or (var_name and var_name[0] in ['a', 'b', 'c']):
        return 'unsigned'
    elif var_name in ['x', 'y', 'z'] or (var_name and var_name[0] in ['x', 'y', 'z']):
        return 'signed'
    return 'unsigned'

def validate_variable(var_name):
    """Validate if variable is declared"""
    # Skip keywords
    keywords = ['if', 'while', 'else', 'print', 'addsub', 'subadd', 'multdiv']
    if var_name in keywords:
        return True
    # Check if it's a valid variable name
    if var_name not in var_types:
        # Auto-declare if it's a standard variable
        if var_name in ['a', 'b', 'c', 'x', 'y', 'z']:
            if var_name in unsigned_vars_allowed or var_name in ['a', 'b', 'c']:
                var_types[var_name] = 'unsigned'
            else:
                var_types[var_name] = 'signed'
            var_initialized[var_name] = 0
        else:
            raise ValueError(f"Undeclared variable: {var_name}")
    return True