from openai import OpenAI
import os
import random
from tqdm import tqdm
import argparse

folder_path = [
    "../benchmark/arithmetic",
    "../benchmark/digital_circuit",
    "../benchmark/fsm", 
    "../benchmark/multimodule",
    "../benchmark/testbench"
]

def gpt4_inference(api_key, output_dir, use_projector, use_table_projector, testbench_gen, use_time_projector):
    file_list = []
    for folder in folder_path:
        for subfolder in os.listdir(folder):
            subfolder_path = os.path.join(folder, subfolder)
            if os.path.isdir(subfolder_path):
                if testbench_gen:
                    if use_time_projector:
                        file_list.append(f"{folder}/{subfolder}/testbench_description_with_timeseries.txt")
                    else:
                        file_list.append(f"{folder}/{subfolder}/testbench_description.txt")
                elif use_projector:
                    file_list.append(f"{folder}/{subfolder}/projector_description.txt")
                elif use_table_projector:
                    file_list.append(f"{folder}/{subfolder}/gpt4_design_description.txt")
                else:
                    file_list.append(f"{folder}/{subfolder}/design_description_no_table.txt")

    for prompt_file in tqdm(file_list):
        if prompt_file is not None:
            with open(prompt_file, "r") as f:
                prompt = "\n".join(f.readlines())

            path_parts = prompt_file.split('/')
            folder = path_parts[2]  # This is the category (arithmetic, digital_circuit, etc.)
            subfolder = path_parts[3]  # This is the actual design name

            for i in range(5):
                try:
                    client = OpenAI(base_url="https://jeniya.top/v1", api_key=api_key)
                    
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {
                                "role": "user", 
                                "content": prompt
                            }
                        ]
                    )
                    
                    answer = response.choices[0].message.content
                    
                    # Create output directory structure
                    output_base = os.path.join(output_dir, folder, subfolder)
                    os.makedirs(output_base, exist_ok=True)
                    
                    # Save full response
                    response_file_path = os.path.join(output_base, f"response_{i}.txt")
                    with open(response_file_path, "w") as response_file:
                        response_file.write(answer)
                        
                    # Parse and save Verilog code
                    verilog_code = ""
                    in_verilog_block = False
                    find_code = False
                    
                    for line in answer.split("\n"):
                        if "```verilog" in line:
                            in_verilog_block = True
                            find_code = True
                        elif "```" in line and in_verilog_block:
                            in_verilog_block = False
                        elif in_verilog_block:
                            verilog_code += line + "\n"
                            
                    if not find_code:
                        # Find first module...( and last endmodule
                        lines = answer.split("\n")
                        start_idx = -1
                        end_idx = -1
                        for j, line in enumerate(lines):
                            if start_idx == -1 and "module" in line and "(" in line:
                                module_pos = line.find("module")
                                paren_pos = line.find("(")
                                if paren_pos > module_pos:
                                    start_idx = j
                            if "endmodule" in line:
                                end_idx = j
                        if start_idx != -1 and end_idx != -1:
                            verilog_code = "\n".join(lines[start_idx:end_idx+1]) + "\n"
                            find_code = True
                            
                    # Save Verilog code
                    verilog_file_path = os.path.join(output_base, f"{subfolder}_{i}.v")
                    with open(verilog_file_path, "w") as verilog_file:
                        verilog_file.write(verilog_code)

                except Exception as e:
                    print(f"API call failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', type=str, required=True, help='OpenAI API key')
    parser.add_argument('--output_dir', type=str, default="generated_code/gpt4", help='Directory to save generated code')
    parser.add_argument('--use_projector', type=bool, default=False, help='Whether to use projector description')
    parser.add_argument('--use_table_projector', action='store_true', help='Whether to use table projector description')
    parser.add_argument('--testbench_gen', action='store_true', help='Whether to generate testbench')
    parser.add_argument('--use_time_projector', action='store_true', help='Whether to use time projector for testbench')
    args = parser.parse_args()
    gpt4_inference(args.api_key, args.output_dir, args.use_projector, args.use_table_projector, args.testbench_gen, args.use_time_projector)
