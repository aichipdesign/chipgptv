from tqdm import tqdm
from llm_generate_code import llm_generate_code
from llm_complete_code import llm_complete_code
from llm_predict_token import llm_predict_token
import os
import argparse
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="gpt-4-vision-preview")
    parser.add_argument("--prompt_type", type=str, default="complex")
    parser.add_argument("--method", type=str, default="default")
    args = parser.parse_args()
    model_name = args.model_name
    prompt_type = args.prompt_type
    instance_list = [
        "arithmetic/accu",
        "arithmetic/adder_8bit",
        "arithmetic/adder_16bit",
        "arithmetic/adder_16bit_csa",
        "arithmetic/adder_32bit",
        "arithmetic/adder_64bit",
        "arithmetic/div_16bit",
        "arithmetic/multi_16bit",
        "arithmetic/multi_booth",
        "arithmetic/multi_pipe_4bit",
        "arithmetic/multi_pipe_8bit",
        "digital_circuit/alu",
        "digital_circuit/edge_detect",
        "digital_circuit/freq_div",
        "digital_circuit/Johnson_Counter",
        "digital_circuit/mux",
        "digital_circuit/parallel2serial",
        "digital_circuit/serial2parallel",
        "digital_circuit/pulse_detect",
        "digital_circuit/right_shifter",
        "digital_circuit/width_8to16",
        "advanced/fsm",
        "advanced/1x2nocpe",
        "advanced/1x4systolic",
        "advanced/2x2systolic",
        "advanced/3stagepipe",
        "advanced/3state_fsm",
        "advanced/4state_fsm",
        "advanced/4x4spatialacc",
        "advanced/5stagepipe",
        "advanced/5state_fsm",
        "advanced/macpe",
        "advanced/2state_fsm",
    ]


    iter = {"default": 5, "complete": 3, "predict": 3}

    for instance in tqdm(instance_list):
        for i in range(iter[args.method]):
            if args.method == "default":
                output = f"generated_code/{model_name}-{prompt_type}/{instance}_{i}.v"
                output_answer = f"generated_code/{model_name}-{prompt_type}/{instance}_{i}.txt"
                llm_generate_code(model_name, instance, output, output_answer, prompt_type)
            elif args.method == "complete":
                output = f"generated_code/{model_name}-complete-code/{instance}_{i}.v"
                output_answer = f"generated_code/{model_name}-complete-code/{instance}_{i}.txt"
                llm_complete_code(model_name, instance, output, output_answer, i+1)
            elif args.method == "predict":
                output = f"generated_code/{model_name}-predict/{instance}_{i}.v"
                output_answer = f"generated_code/{model_name}-predict/{instance}_{i}.txt"
                llm_predict_token(model_name, instance, output, output_answer, i+1)\
                

