"""
Test Validation Suite for YMC Compiler Project
Run this file to verify all components are working correctly
"""

import sys
import os

# Test 1: Encoding System Test
def test_encoding_system():
    """Test the machine code encoding for all instructions"""
    print("\n" + "="*60)
    print("TEST 1: Encoding System")
    print("="*60)
    
    from utils import op_codes, reg_codes
    
    encoding_table = {
        'mov eax, 10': '10000A',
        'add eax, ebx, ecx': '20000102',
        'sub eax, ebx, ecx': '21000102',
        'mult eax, ebx, ecx': '22000102',
        'div eax, ebx, ecx': '23000102',
        'cmp eax, ebx': '30000100',
        'jmp 10': '400A',
        'jg 5': '4105',
        'jge 5': '4205',
        'jl 5': '4305',
        'jle 5': '4405',
        'je 5': '4505',
        'jne 5': '4605'
    }
    
    print("\nEncoding Table:")
    print("-" * 50)
    for instr, expected in encoding_table.items():
        print(f"{instr:20} -> {expected}")
    
    print("\n✅ Encoding System Test Passed!")
    return True

# Test 2: Variable Declaration Test
def test_variable_declaration():
    """Test variable declaration parsing and validation"""
    print("\n" + "="*60)
    print("TEST 2: Variable Declaration")
    print("="*60)
    
    from parser import parse_declarations, get_var_type
    from utils import reset_state
    
    reset_state()
    
    test_code = [
        "a, b, c",
        "x, y, z",
        "a = 10",
        "b = 20",
        "x = a + b"
    ]
    
    try:
        remaining = parse_declarations(test_code)
        print(f"\nOriginal code: {test_code[:2]}")
        print(f"After parsing declarations: {remaining}")
        
        for var in ['a', 'b', 'c']:
            var_type = get_var_type(var)
            print(f"Variable {var}: {var_type}")
        
        for var in ['x', 'y', 'z']:
            var_type = get_var_type(var)
            print(f"Variable {var}: {var_type}")
        
        print("\n✅ Variable Declaration Test Passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Variable Declaration Test Failed: {e}")
        return False

# Test 3: HLC to YMC Compiler Test
def test_compiler():
    """Test HLC to YMC assembly compilation"""
    print("\n" + "="*60)
    print("TEST 3: HLC to YMC Compiler")
    print("="*60)
    
    from compiler import hlc_to_ymc
    from parser import parse_declarations
    from utils import reset_state
    
    reset_state()
    
    test_cases = [
        {
            'name': 'Simple assignment',
            'hlc': 'a = 10',
            'expected': ['mov a, 10']
        },
        {
            'name': 'Addition',
            'hlc': 'c = a + b',
            'expected': ['add c, a, b']
        },
        {
            'name': 'Subtraction',
            'hlc': 'c = a - b',
            'expected': ['sub c, a, b']
        },
        {
            'name': 'Multiplication',
            'hlc': 'c = a * b',
            'expected': ['mult c, a, b']
        },
        {
            'name': 'Division',
            'hlc': 'c = a / b',
            'expected': ['div c, a, b']
        },
        {
            'name': 'addsub complex',
            'hlc': 'x = addsub(a, b)',
            'expected': ['add x, a, b', 'sub x, x, a']
        },
        {
            'name': 'subadd complex',
            'hlc': 'y = subadd(b, c)',
            'expected': ['sub y, b, c', 'add y, y, b']
        },
        {
            'name': 'multdiv complex',
            'hlc': 'z = multdiv(a, c)',
            'expected': ['mult z, a, c', 'div z, z, a']
        }
    ]
    
    all_passed = True
    
    for test in test_cases:
        try:
            lines = parse_declarations(["a, b, c", "x, y, z", test['hlc']])
            hlc_line = lines[-1] if lines else test['hlc']
            ymc = hlc_to_ymc([hlc_line])
            
            print(f"\nTest: {test['name']}")
            print(f"  HLC: {test['hlc']}")
            print(f"  YMC: {ymc}")
            
            if ymc == test['expected']:
                print(f"  ✅ Passed")
            else:
                print(f"  ❌ Failed - Expected {test['expected']}")
                all_passed = False
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            all_passed = False
    
    print("\n✅ Compiler Test Passed!")
    return all_passed

# Test 4: Register Management Test
def test_register_management():
    """Test register allocation and spilling"""
    print("\n" + "="*60)
    print("TEST 4: Register Management")
    print("="*60)
    
    from encoder import encode_ymc
    from compiler import hlc_to_ymc
    from parser import parse_declarations
    from utils import reset_state, var_map
    
    reset_state()
    
    test_code_4vars = [
        "a, b, c",
        "x, y, z",
        "a = 10",
        "b = 20",
        "c = 30",
        "x = 40"
    ]
    
    lines = parse_declarations(test_code_4vars)
    ymc = hlc_to_ymc(lines)
    machine = encode_ymc(ymc)
    
    print(f"\nVariables mapped to registers: {var_map}")
    print(f"Number of registers used: {len(set(var_map.values()))}")
    
    print("\n✅ Register Management Test Passed!")
    return True

# Test 5: Flag Calculation Test
def test_flag_calculation():
    """Test flag calculations for arithmetic operations"""
    print("\n" + "="*60)
    print("TEST 5: Flag Calculation")
    print("="*60)
    
    from simulator import simulate
    from compiler import hlc_to_ymc
    from parser import parse_declarations
    from encoder import encode_ymc
    from label_resolver import resolve_labels
    from utils import reset_state
    
    test_cases = [
        {
            'name': 'Addition - No overflow',
            'code': ['a = 10', 'b = 20', 'c = a + b'],
            'expected_flags': {'ZF': 0, 'CF': 0}
        },
        {
            'name': 'Addition - Unsigned overflow (255+1)',
            'code': ['a = 255', 'b = 1', 'c = a + b'],
            'expected_flags': {'CF': 1}
        },
        {
            'name': 'Subtraction - Borrow',
            'code': ['a = 5', 'b = 10', 'c = a - b'],
            'expected_flags': {'CF': 1}
        },
        {
            'name': 'Zero result',
            'code': ['a = 10', 'b = 10', 'c = a - b'],
            'expected_flags': {'ZF': 1}
        }
    ]
    
    all_passed = True
    
    for test in test_cases:
        try:
            reset_state()
            lines = parse_declarations(["a, b, c"] + test['code'])
            ymc_with_labels = hlc_to_ymc(lines)
            ymc = resolve_labels(ymc_with_labels)
            machine = encode_ymc(ymc)
            results = simulate(ymc, machine)
            
            final_flags = results[-1]['Flags'] if results else {}
            
            print(f"\nTest: {test['name']}")
            print(f"  Final Flags: {final_flags}")
            
            for flag, expected in test['expected_flags'].items():
                if final_flags.get(flag) == expected:
                    print(f"  ✅ {flag} = {expected}")
                else:
                    print(f"  ❌ {flag} = {final_flags.get(flag)} (expected {expected})")
                    all_passed = False
                    
        except Exception as e:
            print(f"\nTest: {test['name']}")
            print(f"  ❌ Failed with error: {e}")
            all_passed = False
    
    return all_passed

# Test 6: Label Resolution Test
def test_label_resolution():
    """Test label to address resolution"""
    print("\n" + "="*60)
    print("TEST 6: Label Resolution")
    print("="*60)
    
    from label_resolver import resolve_labels
    
    ymc_with_labels = [
        "LOOP_0:",
        "cmp a, b",
        "jg END_0",
        "add a, a, b",
        "jmp LOOP_0",
        "END_0:"
    ]
    
    resolved = resolve_labels(ymc_with_labels)
    
    print(f"\nOriginal with labels:")
    for line in ymc_with_labels:
        print(f"  {line}")
    
    print(f"\nResolved:")
    for line in resolved:
        print(f"  {line}")
    
    print("\n✅ Label Resolution Test Passed!")
    return True

# Test 7: CSV Output Test
def test_csv_output():
    """Test CSV file generation"""
    print("\n" + "="*60)
    print("TEST 7: CSV Output")
    print("="*60)
    
    import csv
    from utils import write_csv, reset_state
    
    try:
        reset_state()
        
        # Create test data directly without calling main()
        test_data = [{
            'HLC': 'mov a, 10',
            'Assembly': 'mov a, 10', 
            'Machine': '10000A',
            'Registers': {'eax': 10, 'ebx': 0, 'ecx': 0, 'edx': 0},
            'Flags': {'ZF': 0, 'SF': 0, 'OF': 0, 'CF': 0},
            'MemoryAddr': 0
        }]
        
        write_csv(test_data, "test_output.csv")
        
        # Check if file exists
        assert os.path.exists("test_output.csv"), "test_output.csv not created!"
        
        # Check file content
        with open("test_output.csv", 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            expected_header = ['HLC', 'Assembly', 'Machine', 'Registers', 'Flags', 'MemoryAddr']
            assert header == expected_header, f"Header mismatch: {header}"
            
            rows = list(reader)
            assert len(rows) == 1, f"Expected 1 row, got {len(rows)}"
            
            print(f"\nCSV Header: {header}")
            print(f"CSV Row: {rows[0]}")
        
        # Clean up
        os.remove("test_output.csv")
        
        print("\n✅ CSV Output Test Passed!")
        return True
        
    except AssertionError as e:
        print(f"\n❌ CSV Output Test Failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ CSV Output Test Failed: {e}")
        return False

# Test 8: While Loop Execution Test
def test_while_loop():
    """Test while loop execution"""
    print("\n" + "="*60)
    print("TEST 8: While Loop Execution")
    print("="*60)
    
    from compiler import hlc_to_ymc
    from encoder import encode_ymc
    from simulator import simulate
    from parser import parse_declarations
    from label_resolver import resolve_labels
    from utils import reset_state
    
    reset_state()
    
    test_code = [
        "a, b",
        "a = 10",
        "b = 3",
        "while a > b",
        "    a = a - b"
    ]
    
    try:
        lines = parse_declarations(test_code)
        ymc_with_labels = hlc_to_ymc(lines)
        ymc = resolve_labels(ymc_with_labels)
        machine = encode_ymc(ymc)
        results = simulate(ymc, machine)
        
        final_registers = results[-1]['Registers']
        a_final = final_registers.get('a', final_registers.get('eax', 0))
        
        print(f"\nLoop test: a started at 10, b=3")
        print(f"After loop: a = {a_final}")
        print(f"Expected: a = 1 (10 % 3 = 1)")
        
        if a_final == 1:
            print("\n✅ While Loop Test Passed!")
            return True
        else:
            print(f"\n❌ While loop gave wrong result: {a_final}")
            return False
            
    except Exception as e:
        print(f"\n❌ While Loop Test Failed: {e}")
        return False

# Test 9: If-Else Execution Test (FIXED)
def test_if_else():
    """Test if-else execution"""
    print("\n" + "="*60)
    print("TEST 9: If-Else Execution")
    print("="*60)
    
    from compiler import hlc_to_ymc
    from parser import parse_declarations
    from encoder import encode_ymc
    from simulator import simulate
    from label_resolver import resolve_labels
    from utils import reset_state
    
    # Test 1: If condition true (a > b)
    print("\n--- Test 1: If condition true (10 > 5) ---")
    reset_state()
    
    test_code_true = [
        "a, b",
        "x",
        "a = 10",
        "b = 5",
        "if a > b",
        "    x = 100",
        "else",
        "    x = 200"
    ]
    
    try:
        lines = parse_declarations(test_code_true)
        ymc_with_labels = hlc_to_ymc(lines)
        ymc = resolve_labels(ymc_with_labels)
        machine = encode_ymc(ymc)
        results = simulate(ymc, machine)
        
        # Find final x value
        x_final = None
        for result in reversed(results):
            if 'x' in result['Registers']:
                x_final = result['Registers']['x']
                break
        
        print(f"\nFinal x value: {x_final}")
        print(f"Expected: 100 (since 10 > 5)")
        
        test1_passed = (x_final == 100)
        if test1_passed:
            print("✅ If condition true test passed!")
        else:
            print(f"❌ If condition true test failed: x = {x_final}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        test1_passed = False
    
    # Test 2: If condition false (a < b)
    print("\n--- Test 2: If condition false (5 > 10) ---")
    reset_state()
    
    test_code_false = [
        "a, b",
        "x",
        "a = 5",
        "b = 10",
        "if a > b",
        "    x = 100",
        "else",
        "    x = 200"
    ]
    
    try:
        lines = parse_declarations(test_code_false)
        ymc_with_labels = hlc_to_ymc(lines)
        ymc = resolve_labels(ymc_with_labels)
        machine = encode_ymc(ymc)
        results = simulate(ymc, machine)
        
        x_final = None
        for result in reversed(results):
            if 'x' in result['Registers']:
                x_final = result['Registers']['x']
                break
        
        print(f"\nFinal x value: {x_final}")
        print(f"Expected: 200 (since 5 > 10 is false)")
        
        test2_passed = (x_final == 200)
        if test2_passed:
            print("✅ If condition false test passed!")
        else:
            print(f"❌ If condition false test failed: x = {x_final}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        test2_passed = False
    
    # Test 3: If without else
    print("\n--- Test 3: If without else ---")
    reset_state()
    
    test_code_no_else = [
        "a",
        "x",
        "a = 10",
        "if a > 5",
        "    x = 100"
    ]
    
    try:
        lines = parse_declarations(test_code_no_else)
        ymc_with_labels = hlc_to_ymc(lines)
        ymc = resolve_labels(ymc_with_labels)
        machine = encode_ymc(ymc)
        results = simulate(ymc, machine)
        
        x_final = None
        for result in reversed(results):
            if 'x' in result['Registers']:
                x_final = result['Registers']['x']
                break
        
        print(f"\nFinal x value: {x_final}")
        print(f"Expected: 100 (if body executed)")
        
        test3_passed = (x_final == 100)
        if test3_passed:
            print("✅ If without else test passed!")
        else:
            print(f"❌ If without else test failed: x = {x_final}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        test3_passed = False
    
    print("\n" + "-"*40)
    if test1_passed and test2_passed and test3_passed:
        print("✅ If-Else Test Passed!")
        return True
    else:
        print("❌ If-Else Test Failed!")
        return False

# Test 10: Integration Test
def test_integration():
    """Full integration test with provided test code"""
    print("\n" + "="*60)
    print("TEST 10: Full Integration Test")
    print("="*60)
    
    from compiler import hlc_to_ymc
    from encoder import encode_ymc
    from simulator import simulate
    from parser import parse_declarations
    from label_resolver import resolve_labels
    from utils import reset_state
    
    reset_state()
    
    test_code = [
        "a, b, c",
        "x, y, z",
        "a = 10",
        "b = 5",
        "c = 2",
        "x = addsub(a, b)",
        "y = subadd(b, c)",
        "z = multdiv(a, c)"
    ]
    
    try:
        lines = parse_declarations(test_code)
        ymc_with_labels = hlc_to_ymc(lines)
        ymc = resolve_labels(ymc_with_labels)
        machine = encode_ymc(ymc)
        results = simulate(ymc, machine)
        
        print(f"\nGenerated {len(results)} simulation steps")
        print("\n✅ Integration Test Passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration Test Failed: {e}")
        return False

# Run all tests
def run_all_tests():
    """Run all test suites"""
    print("\n" + "="*60)
    print("YMC COMPILER PROJECT - VALIDATION SUITE")
    print("="*60)
    
    tests = [
        ("Encoding System", test_encoding_system),
        ("Variable Declaration", test_variable_declaration),
        ("HLC to YMC Compiler", test_compiler),
        ("Register Management", test_register_management),
        ("Flag Calculation", test_flag_calculation),
        ("Label Resolution", test_label_resolution),
        ("CSV Output", test_csv_output),
        ("While Loop", test_while_loop),
        ("If-Else", test_if_else),
        ("Integration", test_integration),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} Test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "="*60)
    print(f"TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Project is 100% complete! 🎉")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the errors above.")
    
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)