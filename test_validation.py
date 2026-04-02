from compiler import hlc_to_ymc
from encoder import encode_ymc
from simulator import simulate
from label_resolver import resolve_labels

def run_test(test_name, hlc_lines, expected_regs, expected_flags):
    ymc = hlc_to_ymc(hlc_lines)
    ymc = resolve_labels(ymc)
    machine = encode_ymc(ymc)
    results = simulate(ymc, machine)
    final = results[-1]
    got_regs = final['Registers']
    got_flags = final['Flags']
    if got_regs != expected_regs or got_flags != expected_flags:
        print(f"❌ Test Failed: {test_name}")
        print(f"Expected Registers: {expected_regs}, Got: {got_regs}")
        print(f"Expected Flags: {expected_flags}, Got: {got_flags}")
    else:
        print(f"✅ Test Passed: {test_name}")

if __name__ == "__main__":
    run_test("Simple Assignment & Addition", ["a=5","b=3","c=a+b"],
             {'eax':5,'ebx':3,'ecx':8,'edx':0},{'ZF':0,'SF':0,'OF':0,'CF':0})
    run_test("If Condition True", ["a=5","b=3","if a>b","x=10"],
             {'eax':10,'ebx':3,'ecx':0,'edx':0},{'ZF':0,'SF':0,'OF':0,'CF':0})
    run_test("While Loop", ["a=5","b=3","while a>b","a=a-b"],
             {'eax':2,'ebx':3,'ecx':0,'edx':0},{'ZF':0,'SF':0,'OF':0,'CF':0})
    run_test("Complex Arithmetic: addsub", ["a=5","b=3","c=a+b","d=c-a"],
             {'eax':5,'ebx':3,'ecx':8,'edx':5},{'ZF':0,'SF':0,'OF':0,'CF':0})
    run_test("Complex Arithmetic: multdiv", ["a=6","b=2","c=a*b","d=c/b"],
             {'eax':6,'ebx':2,'ecx':12,'edx':6},{'ZF':0,'SF':0,'OF':0,'CF':0})