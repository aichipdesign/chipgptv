import argparse
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM
import torch
import os
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True,
                      help="Path to pretrained model or model identifier from huggingface.co/models")
    parser.add_argument("--output_dir", type=str, default="generated_code/rtlcoder_ft",
                      help="Directory to save generated code")
    parser.add_argument("--use_projector", type=bool, default=True,
                      help="Whether to use projector description")
    return parser.parse_args()

def load_model(model):
    config = AutoConfig.from_pretrained(model)
    tokenizer = AutoTokenizer.from_pretrained(model, padding_side="left")
    model = AutoModelForCausalLM.from_pretrained(model, torch_dtype=torch.float16, device_map="auto")
    model.eval()
    return tokenizer, model

def generate_code(prompt, tokenizer, model, temperature=0.2):
    inputs = tokenizer([prompt], return_tensors="pt", padding='longest').to(model.device)
    outputs = model.generate(
        inputs=inputs.input_ids,
        max_length=len(inputs[0]) + 2048,
        do_sample=True,
        temperature=temperature,
        top_p=0.95,
        attention_mask=inputs.attention_mask
    )
    
    s_full = tokenizer.decode(outputs[0][len(inputs[0]):].cpu().squeeze(), skip_special_tokens=True)
    
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
        
    return s, s_full

def main():
    args = parse_args()
    
    folder_path = [
        "../benchmark/testbench",
        "../benchmark/fsm", 
        "../benchmark/multimodule",
        "../benchmark/digital_circuit",
        "../benchmark/arithmetic"
    ]

    # Load model
    tokenizer, model = load_model(args.model)

    file_list = []
    for folder in folder_path:
        for subfolder in os.listdir(folder):
            subfolder_path = os.path.join(folder, subfolder)
            if os.path.isdir(subfolder_path):
                if args.use_projector:
                    file_list.append(f"{folder}/{subfolder}/projector_description.txt")
                else:
                    file_list.append(f"{folder}/{subfolder}/gpt4_design_description.txt")

    for prompt_file in tqdm(file_list):
        if prompt_file is not None:
            assert os.path.exists(prompt_file), f"Provided Prompt file does not exist {prompt_file}"
            with open(prompt_file, "r") as f:
                prompt = "\n".join(f.readlines())

            # Get folder and subfolder names from prompt_file path
            path_parts = prompt_file.split('/')
            folder = path_parts[1]
            subfolder = path_parts[2]

            for i in range(5):
                generated_code, response = generate_code(prompt, tokenizer, model)

                # Create output directory structure
                output_base = os.path.join(args.output_dir, folder, subfolder)
                os.makedirs(output_base, exist_ok=True)

                # Save Verilog code
                verilog_file_path = os.path.join(output_base, f"{subfolder}_{i}.v")
                response_file_path = os.path.join(output_base, f"response_{i}.txt")
                with open(verilog_file_path, "w") as f:
                    f.write(generated_code)
                with open(response_file_path, "w") as f:
                    f.write(response)

if __name__ == "__main__":
    main()
