import os
import subprocess
import argparse
# get access the parent directory
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the directories for the designs and generated codes
design_dirs = ['arithmetic', 'fsm', 'multimodule', 'digital_circuit']

# Function to compile and run the testbench with the generated code
def test_design(testbench, design_file):
    # Create the command to compile and run with iverilog
    try:
        # Run the command
        cmd = f"iverilog -o test.vvp {testbench} {design_file} && vvp test.vvp"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=2,  start_new_session=True)
        if result.returncode != 0:
            return False, False
        # Save error log
        design_name = os.path.basename(design_file).rsplit('_', 1)[0]
        with open('function_correctness.log', 'a') as f:
            f.write(f"{design_name}: {result.stdout.lower()}\n")
        # Check if the test passed
        if 'pass' in result.stdout.lower():
            return True, True
        return True, False
    except Exception as e:
        print(f"Error running test: {e}")
    return False, False

parser = argparse.ArgumentParser()
parser.add_argument('--generated_code_dir', type=str, required=True, help='Directory containing generated code')
parser.add_argument('--test_mode', type=str, required=True, choices=['design', 'testbench'], help='Testing mode: "design" to test generated designs, or "testbench" to test generated testbenches.')
args = parser.parse_args()

# Files to store the correctness results
correctness_file = open('function_correctness.txt', 'a')
syntax_file = open('syntax_correctness.txt', 'a')
correctness_file.write(f"Results for situation {args.generated_code_dir}:\n")
syntax_file.write(f"Results for situation {args.generated_code_dir}:\n")

# Test each type of design directory
for design_dir in design_dirs:

    design_base_path = design_dir
    generated_design_path = os.path.join(args.generated_code_dir, design_dir)

    # Loop through each design testbench in the design directory
    for design in os.listdir(os.path.join("benchmark", design_base_path)):

        design_path = os.path.join(design_base_path, design)
        design_path = os.path.join("benchmark", design_path)

        if args.test_mode == 'design':
            fixed_file = os.path.join(design_path, 'testbench.v')
        else:  # test_mode == 'testbench'
            try:
                # Find the design.v file, which is the .v file that is not 'testbench.v'
                design_v_file = [f for f in os.listdir(design_path) if f.endswith('.v') and f != 'testbench.v'][0]
                fixed_file = os.path.join(design_path, design_v_file)
            except IndexError:
                print(f"Warning: Could not find a design file in {design_path}. Skipping.")
                continue

        correct_count = 0
        syntax_count = 0
        total_tests = 0
        # Test each generated design file
        for file in os.listdir(generated_design_path):
            if file == design:
                for i in range(5):
                    generated_file = os.path.join(generated_design_path, file, f"{file}_{i}.v")
                    
                    if not os.path.exists(generated_file):
                        continue

                    if args.test_mode == 'design':
                        syntax_pass, func_pass = test_design(testbench=fixed_file, design_file=generated_file)
                    else:  # test_mode == 'testbench'
                        syntax_pass, func_pass = test_design(testbench=generated_file, design_file=fixed_file)
                        
                    if syntax_pass:
                        syntax_count += 1
                    if func_pass:
                        correct_count += 1
                    total_tests += 1

        if total_tests > 0:
            if correct_count > 0:
                correctness_rate = "100%"
            else:
                correctness_rate = "0%"
            syntax_rate = f"{(syntax_count/total_tests)*100:.0f}%"
            correctness_file.write(f"{design}: {correctness_rate}\n")
            syntax_file.write(f"{design}: {syntax_rate}\n")

correctness_file.write("\n")
syntax_file.write("\n")
correctness_file.close()
syntax_file.close()

print("Testing completed.")
