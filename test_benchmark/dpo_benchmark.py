import os
import sys
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import json
import re
from tqdm import tqdm
import argparse
from vllm import LLM, SamplingParams
import shutil
import tempfile

folder_path = [
    "../benchmark/arithmetic",
    "../benchmark/digital_circuit", 
    "../benchmark/fsm",
    "../benchmark/multimodule",
    # "../benchmark/testbench",
]

def dpo_inference(base_model_path, adapter_path, output_dir, use_projector, use_table_projector, testbench_gen, use_time_projector, gpu_id, gpu_memory_utilization):
    # Set CUDA device
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    # Merge adapter with base model and save to temp dir
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype="auto", 
        device_map="cpu"
    )
    model = PeftModel.from_pretrained(base_model, adapter_path)
    model = model.merge_and_unload()
    temp_dir = tempfile.mkdtemp()
    model.save_pretrained(temp_dir)
    # Save tokenizer files as well
    tokenizer = AutoTokenizer.from_pretrained(base_model_path)
    tokenizer.save_pretrained(temp_dir)

    # Load with vLLM
    llm = LLM(model=temp_dir, tokenizer=temp_dir, dtype="auto", gpu_memory_utilization=gpu_memory_utilization)

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
            assert os.path.exists(prompt_file), f"Provided Prompt file does not exist {prompt_file}"
            with open(prompt_file, "r") as f:
                user_prompt = "\n".join(f.readlines())

            # Get folder and subfolder names from prompt_file path
            path_parts = prompt_file.split('/')
            folder = path_parts[2]
            subfolder = path_parts[3]
            for i in range(5):
                messages = [
                    {"role": "system", "content":"You are a professional verilog coder. Please act as a professional verilog designer, try to understand the requirements below and reason how to solve the problem step by step. Based on your reasoning, complete the module with syntax correct Verilog code. Please note that your response should only include Verilog code."},
                    {"role": "user", "content": user_prompt}
                ]
                # Use HuggingFace tokenizer to build prompt
                text = tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
                sampling_params = SamplingParams(max_tokens=2000)
                start = time.perf_counter()
                outputs = llm.generate([text], sampling_params)
                response = outputs[0].outputs[0].text
                e2e_inference_time = (time.perf_counter() - start) * 1000

                # Create output directory structure
                output_base = os.path.join(output_dir, folder, subfolder)
                os.makedirs(output_base, exist_ok=True)
                # Save response
                response_file_path = os.path.join(output_base, f"response_{i}.txt")
                with open(response_file_path, "w") as response_file:
                    response_file.write(response)
                # Parse and save Verilog code
                verilog_code = ""
                in_verilog_block = False
                find_code = False
                for line in response.split("\n"):
                    if "```verilog" in line:
                        in_verilog_block = True
                        find_code = True
                    elif "```" in line and in_verilog_block:
                        in_verilog_block = False
                    elif in_verilog_block:
                        verilog_code += line + "\n"
                if find_code == False:
                    # Find first module...( and last endmodule
                    lines = response.split("\n")
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
    # Clean up temp dir
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_model_path', type=str, default="/public_extends/historydata/llama3_lora_sft", help='Path to the base model')
    parser.add_argument('--adapter_path', type=str, default="/public_extends/historydata/dpo_model/", help='Path to the DPO adapter')
    parser.add_argument('--output_dir', type=str, default="../generated_code/llama_dpo_model", help='Output directory for generated code')
    parser.add_argument('--use_projector', action='store_true', help='Use projector description instead of GPT-4 description')
    parser.add_argument('--use_table_projector', action='store_true', help='Whether to use table projector description')
    parser.add_argument('--testbench_gen', action='store_true', help='Whether to generate testbench')
    parser.add_argument('--use_time_projector', action='store_true', help='Whether to use time projector for testbench')
    parser.add_argument('--gpu_id', type=int, default=0, help='GPU id to use for vLLM')
    parser.add_argument('--gpu_memory_utilization', type=float, default=0.90, help='Fraction of GPU memory to use for vLLM (0-1)')
    args = parser.parse_args()
    dpo_inference(args.base_model_path, args.adapter_path, args.output_dir, args.use_projector, args.use_table_projector, args.testbench_gen, args.use_time_projector, args.gpu_id, args.gpu_memory_utilization)
