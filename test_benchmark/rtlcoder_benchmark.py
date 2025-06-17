import argparse
from transformers import AutoTokenizer
import os
from tqdm import tqdm
# vLLM imports
from vllm import LLM, SamplingParams

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="/public_extends/historydata/model/rtlcoder",
                      help="Path to pretrained model")
    parser.add_argument("--output_dir", type=str, default="../generated_code/rtlcoder",
                      help="Directory to save generated code")
    parser.add_argument("--use_projector", action='store_true',
                      help="Whether to use projector description")
    parser.add_argument('--use_table_projector', action='store_true', help='Whether to use table projector description')
    parser.add_argument('--testbench_gen', action='store_true', help='Whether to generate testbench')
    parser.add_argument('--use_time_projector', action='store_true', help='Whether to use time projector for testbench')
    parser.add_argument('--gpu_id', type=int, default=0, help='GPU id to use for vLLM')
    parser.add_argument('--gpu_util', type=float, default=0.90, help='Fraction of GPU memory to use for vLLM (0-1)')
    return parser.parse_args()

def generate_code(prompt, llm, sampling_params):
    outputs = llm.generate([prompt], sampling_params)
    s_full = outputs[0].outputs[0].text
    if 'module testbench' in s_full:
        s = s_full.split('module testbench', 1)[1]
        s = s.split('endmodule', 1)[0]
        s = 'module testbench' + s + '\nendmodule'
    else:
        # Extract code section
        if len(s_full.split('endmodulemodule', 1)) == 2:
            s = s_full.split('endmodulemodule', 1)[0] + "\n" + "endmodule"
        else:
            s = s_full.rsplit('endmodule', 1)[0] + "\n" + "endmodule"
        if s.find('top_module') != -1:
            s = s.split('top_module', 1)[0]
            s = s.rsplit('endmodule', 1)[0] + "\n" + "endmodule"
        index = s.rfind('tb_module')
        if index == -1:
            index = s.find('testbench')
        if index != -1:
            s_tmp = s[:index]
            s = s_tmp.rsplit("endmodule", 1)[0] + "\n" + "endmodule"
    return s

def main():
    args = parse_args()
    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu_id)
    folder_path = [
        # "../benchmark/testbench",
        "../benchmark/fsm", 
        "../benchmark/multimodule",
        "../benchmark/digital_circuit",
        "../benchmark/arithmetic"
    ]

    # Load tokenizer for prompt formatting
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, padding_side="left")
    # Load vLLM model
    llm = LLM(model=args.model_path, tokenizer=args.model_path, dtype="auto", gpu_memory_utilization=args.gpu_util)

    file_list = []
    for folder in folder_path:
        for subfolder in os.listdir(folder):
            subfolder_path = os.path.join(folder, subfolder)
            if os.path.isdir(subfolder_path):
                if args.testbench_gen:
                    if args.use_time_projector:
                        file_list.append(f"{folder}/{subfolder}/testbench_description_with_timeseries.txt")
                    else:
                        file_list.append(f"{folder}/{subfolder}/testbench_description.txt")
                elif args.use_projector:
                    file_list.append(f"{folder}/{subfolder}/projector_description.txt")
                elif args.use_table_projector:
                    file_list.append(f"{folder}/{subfolder}/gpt4_design_description.txt")
                else:
                    file_list.append(f"{folder}/{subfolder}/design_description_no_table.txt")

    for prompt_file in tqdm(file_list):
        if prompt_file is not None:
            assert os.path.exists(prompt_file), f"Provided Prompt file does not exist {prompt_file}"
            with open(prompt_file, "r") as f:
                prompt = "\n".join(f.readlines())

            # Get folder and subfolder names from prompt_file path
            path_parts = prompt_file.split('/')
            folder = path_parts[2]
            subfolder = path_parts[3]

            for i in range(5):
                # Use tokenizer to format prompt if needed (optional, for chat models)
                # For plain LLM, just use prompt
                sampling_params = SamplingParams(max_tokens=2048)
                generated_code = generate_code(prompt, llm, sampling_params)

                # Create output directory structure
                output_base = os.path.join(args.output_dir, folder, subfolder)
                os.makedirs(output_base, exist_ok=True)

                # Save Verilog code
                verilog_file_path = os.path.join(output_base, f"{subfolder}_{i}.v")
                with open(verilog_file_path, "w") as f:
                    f.write(generated_code)

if __name__ == "__main__":
    main()
