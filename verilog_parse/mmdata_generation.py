import concurrent.futures
import json
import os
import argparse
from yosys_script import run_yosys_script
from verilog_parser import extract_module_info
from dot2png import dot_to_png
from tqdm import tqdm

def process_json_file(input_file, output_file):
    # Read the input JSON file
    err_case = []
    correct_cnt = 0
    error_cnt = 0
    with open(input_file, 'r') as f:
        data = json.load(f)

    augmented_data = []

    for idx, item in tqdm(list(enumerate(data))):
        instruction = item['Instruction']
        response = item['Response'][0]

        # Generate Verilog file
        verilog_file = f"metadata/response_{idx}.v"
        with open(verilog_file, 'w') as f:
            f.write(response)

        # Run Yosys script
        output_json = "metadata/out.json"
        output_dot = "metadata/out"

        try:
            top_module, leaf_modules = run_yosys_script(verilog_file, output_json, output_dot)
        except Exception as e:
            print(f"Error: {e}")
            err_case.append(idx)
            error_cnt += 1
            continue

        # Read the output_dot file
        with open(output_dot + ".dot", 'r') as f:
            dot_content = f.read()
        # Split the content into separate digraph objects
        digraphs = dot_content.split('digraph')

        for i, digraph in enumerate(digraphs[1:], 1):  # Skip the first empty split
            digraph_text = f'digraph{digraph}'
            digraph_name = digraph_text.split('{')[0].strip().split()[1]
            digraph_name = digraph_name.replace('"', '')
            if digraph_name in leaf_modules:
                continue
            png_file_path = f"chip_image/design_{idx}/{digraph_name}"
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(png_file_path), exist_ok=True)
            
            # Convert the digraph to PNG
            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(dot_to_png, digraph_text, png_file_path)
                    future.result(timeout=120)  # Set your desired timeout in seconds
            except concurrent.futures.TimeoutError:
                print(f"Error: dot_to_png timed out for index {idx}")
            except Exception as e:
                print(f"Error: {e}")
        # Process the JSON output
        with open(output_json, 'r') as f:
            json_data = json.load(f)
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(extract_module_info, json_data, leaf_modules)
                module_info = future.result(timeout=120)  # Set your desired timeout in seconds
        except concurrent.futures.TimeoutError:
            print(f"Error: extract_module_info timed out for index {idx}")
            err_case.append(idx)
            error_cnt += 1
            continue
        except Exception as e:
            print(f"Error: {e}")
            err_case.append(idx)
            error_cnt += 1
            continue
        module_info_json = json.dumps(module_info, indent=2)

        # Store module_info_json in chip_image_projection/design_{idx}.json
        os.makedirs("chip_image_projection", exist_ok=True)
        design_json_path = f"chip_image_projection/design_{idx}.json"
        with open(design_json_path, 'w') as f:
            f.write(module_info_json)
        # Append module info to instruction
        augmented_instruction = f"{instruction}\nImage information:\n{module_info_json}"

        # Store augmented data
        augmented_item = {
            "instruction": augmented_instruction,
            "output": response,
            "input": ""
        }
        augmented_data.append(augmented_item)

    # Save augmented data
    correct_cnt = len(augmented_data)
    print(f"Correct count: {correct_cnt}")
    print(f"Error count: {error_cnt}")

    with open(output_file, 'w') as f:
        json.dump(augmented_data, f, indent=2)

def process_verilog_file(input_folder, output_folder):
    # Read benchmark folder
    file_list = []
    for file in os.listdir(input_folder):
        if file.endswith(".v"):
            verilog_file = os.path.join(input_folder, file)
            file_list.append(verilog_file)
    
    os.makedirs(output_folder, exist_ok=True)
    
    for file in file_list:
        # open the file and read the content
        file_name = file.split("/")[-1].split(".")[0]
        with open(file, 'r') as f:
            content = f.read()
        # run the yosys script
        output_json = "metadata/out.json"
        output_dot = "metadata/out"
        try:
            top_module, leaf_modules = run_yosys_script(file, output_json, output_dot)
        except Exception as e:
            print(f"Error: {e}")
            continue

        
        with open(output_json, 'r') as f:
            json_data = json.load(f)

        module_info = extract_module_info(json_data, leaf_modules)
        module_info_json = json.dumps(module_info, indent=2)
        # save the module_info_json to the file
        output_path = os.path.join(output_folder, f"{file_name}.txt")
        with open(output_path, 'w') as f:
            f.write(module_info_json)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help='Input file/folder path')
    parser.add_argument('--output', type=str, required=True, help='Output file/folder path')
    args = parser.parse_args()

    if args.input.endswith('.json'):
        process_json_file(args.input, args.output)
    else:
        process_verilog_file(args.input, args.output)