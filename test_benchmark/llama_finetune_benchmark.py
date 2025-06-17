# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

import os
import sys
import time
import argparse
import fire

import torch

from accelerate.utils import is_xpu_available
from llama_recipes.inference.model_utils import load_model, load_peft_model

from llama_recipes.inference.safety_utils import AgentType, get_safety_checker
from transformers import AutoTokenizer
import random
from tqdm import tqdm


folder_path = [
    "../benchmark/arithmetic",
    "../benchmark/digital_circuit", 
    "../benchmark/fsm",
    "../benchmark/multimodule",
    "../benchmark/testbench",
]

design_list = []
for folder in folder_path:
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            design_list.append(subfolder)

print(design_list)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True,
                      help="Path to base model")
    parser.add_argument("--peft_model", type=str, required=True,
                      help="Path to PEFT model") 
    parser.add_argument("--output_dir", type=str, required=True,
                      help="Directory to save output")
    parser.add_argument("--use_projector", type=bool, default=False,
                      help="Whether to use projector description")
    return parser.parse_args()

def llama_inference(
    model_name,
    peft_model: str = None,
    quantization: str = None, # Options: 4bit, 8bit
    max_new_tokens=2048,  # The maximum numbers of tokens to generate
    prompt_file: list[str] = None,
    seed: int = 42,  # seed value for reproducibility
    do_sample: bool = True,  # Whether or not to use sampling ; use greedy decoding otherwise.
    min_length: int = None,  # The minimum length of the sequence to be generated, input prompt + min_new_tokens
    use_cache: bool = True,  # [optional] Whether or not the model should use the past last key/values attentions Whether or not the model should use the past last key/values attentions (if applicable to the model) to speed up decoding.
    top_p: float = 1.0,  # [optional] If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation.
    temperature: float = 1.0,  # [optional] The value used to modulate the next token probabilities.
    top_k: int = 50,  # [optional] The number of highest probability vocabulary tokens to keep for top-k-filtering.
    repetition_penalty: float = 1.0,  # The parameter for repetition penalty. 1.0 means no penalty.
    length_penalty: int = 1,  # [optional] Exponential penalty to the length that is used with beam-based generation.
    enable_azure_content_safety: bool = False,  # Enable safety check with Azure content safety api
    enable_sensitive_topics: bool = False,  # Enable check for sensitive topics using AuditNLG APIs
    enable_salesforce_content_safety: bool = True,  # Enable safety check with Salesforce safety flan t5
    enable_llamaguard_content_safety: bool = False,
    max_padding_length: int = None,  # the max padding length to be used with tokenizer padding the prompts.
    use_fast_kernels: bool = False,  # Enable using SDPA from PyTroch Accelerated Transformers, make use Flash Attention and Xformer memory-efficient kernels
    share_gradio: bool = False,  # Enable endpoint creation for gradio.live
    **kwargs,
):
    args = parse_args()

    # Set the seeds for reproducibility
    if is_xpu_available():
        torch.xpu.manual_seed(seed)
    else:
        torch.cuda.manual_seed(seed)

    seed = random.randint(0, 1000000)
    torch.manual_seed(seed)

    model = load_model(args.model_name, quantization, use_fast_kernels, **kwargs)
    if args.peft_model:
        model = load_peft_model(model, args.peft_model)

    model.eval()

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    tokenizer.pad_token = tokenizer.eos_token

    def inference(
        user_prompt,
        temperature,
        top_p,
        top_k,
        max_new_tokens,
        **kwargs,
    ):
        batch = tokenizer(
            user_prompt,
            truncation=True,
            max_length=max_padding_length,
            return_tensors="pt",
        )
        if is_xpu_available():
            batch = {k: v.to("xpu") for k, v in batch.items()}
        else:
            batch = {k: v.to("cuda") for k, v in batch.items()}

        start = time.perf_counter()
        with torch.no_grad():
            outputs = model.generate(
                **batch,
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                top_p=top_p,
                temperature=temperature,
                min_length=min_length,
                use_cache=use_cache,
                top_k=top_k,
                repetition_penalty=repetition_penalty,
                length_penalty=length_penalty,
                **kwargs,
            )
        e2e_inference_time = (time.perf_counter() - start) * 1000
        output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return output_text

    file_list = []
    desc_file = "projector_description.txt" if args.use_projector else "gpt4_design_description.txt"
    for folder in folder_path:
        for subfolder in os.listdir(folder):
            subfolder_path = os.path.join(folder, subfolder)
            if os.path.isdir(subfolder_path):
                file_list.append(f"{folder}/{subfolder}/{desc_file}")
    
    for prompt_file in tqdm(file_list):
        if prompt_file is not None:
            assert os.path.exists(
                prompt_file
            ), f"Provided Prompt file does not exist {prompt_file}"
            with open(prompt_file, "r") as f:
                user_prompt = "\n".join(f.readlines())

            # Get folder and subfolder names from prompt_file path
            path_parts = prompt_file.split('/')
            folder = path_parts[2]
            subfolder = path_parts[3]
            for i in range(5):
                response = inference(user_prompt, temperature, top_p, top_k, max_new_tokens)
                
                # Create output directory structure
                output_base = os.path.join(args.output_dir, folder, subfolder)
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
        elif not sys.stdin.isatty():
            user_prompt = "\n".join(sys.stdin.readlines())
            inference(user_prompt, temperature, top_p, top_k, max_new_tokens)
        else:
            try:
                import gradio as gr
            except ImportError:
                raise ImportError("This part of the recipe requires gradio. Please run `pip install gradio`")
                
            gr.Interface(
                fn=inference,
                inputs=[
                    gr.components.Textbox(
                        lines=9,
                        label="User Prompt",
                        placeholder="none",
                    ),
                    gr.components.Slider(
                        minimum=0, maximum=1, value=1.0, label="Temperature"
                    ),
                    gr.components.Slider(minimum=0, maximum=1, value=1.0, label="Top p"),
                    gr.components.Slider(
                        minimum=0, maximum=100, step=1, value=50, label="Top k"
                    ),
                    gr.components.Slider(
                        minimum=1, maximum=2000, step=1, value=200, label="Max tokens"
                    ),
                ],
                outputs=[
                    gr.components.Textbox(
                        lines=5,
                        label="Output",
                    )
                ],
                title="Meta Llama3 Playground",
                description="https://github.com/meta-llama/llama-recipes",
            ).queue().launch(server_name="0.0.0.0", share=share_gradio)


if __name__ == "__main__":
    fire.Fire(llama_inference)