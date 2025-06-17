import os
import subprocess
# get access the parent directory
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the directories for the designs and generated codes
design_dirs = ['advanced', 'arithmetic', 'digital_circuit']
generated_code_dir = 'generated_code'

# Function to compile and run the testbench with the generated code
def test_design(testbench, design_file):
    # Create the command to compile and run with iverilog
    try:
        # Run the command
        cmd = f"iverilog -o test.vvp {testbench} {design_file} && vvp test.vvp"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=2,  start_new_session=True)
        # Check if the test passed
        if 'pass' in result.stdout.lower():
            return True
    except Exception as e:
        print(f"Error running test: {e}")
    return False

# Loop through each situation in the generated_code folder
for situation in os.listdir(generated_code_dir):
    if situation != 'gpt-4-vision-preview-medium':
        continue
    situation_path = os.path.join(generated_code_dir, situation)
    print(f"Testing situation: {situation}")

    # File to store the correctness results
    correctness_file = open('function_correctness.txt', 'a')
    correctness_file.write(f"Results for situation {situation}:\n")

    # Test each type of design directory
    for design_dir in design_dirs:
        design_base_path = design_dir
        generated_design_path = os.path.join(situation_path, design_dir)

        # Loop through each design testbench in the design directory
        for design in os.listdir(design_base_path):
            design_path = os.path.join(design_base_path, design)
            design_path = os.path.join("benchmark", design_path)
            testbench = os.path.join(design_path, 'testbench.v')
            correct_count = 0
            total_tests = 0
            # Test each generated design file
            for file in os.listdir(generated_design_path):
                if file.startswith(design) and file.endswith('.v'):
                    design_file = os.path.join(generated_design_path, file)
                    if test_design(testbench, design_file):
                        correct_count += 1
                    total_tests += 1


            if total_tests > 0:
                correctness_rate = (correct_count / total_tests) * 100
                correctness_file.write(f"{design}: {correctness_rate}% correct\n")

    correctness_file.write("\n")
    correctness_file.close()

print("Testing completed.")
