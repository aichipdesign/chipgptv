# Natural language is not enough: Benchmarking multi-modal generative AI for Verilog generation


## File Structure

- benchmark
  - advanced
  - arithmetic
  - digital_circuit
- chip_draw_tool
- img
- src

## Benchmark
benchmark folder contains 3 kinds of design, arithmetic circuit, digital circuit, and advanced circuit repectively. Each design class folder several designs, and each design contains 3 level design descriptions: simple (simple_design_description.txt), medium (medium_design description.txt), and detailed (design_description.txt) respectively. In addition, each design folder contains the image of the design ([design_name].png), next token prediction prompts ([model_name]\_next_token_[idx].txt), the reference design code (reference.v), the testbench code (testbench.v). Overall, each design folder contains the following files.

- [design_name].png (design image)
- reference.v (reference Verilog code of design)
- testbench.v (testbench code of design)
- design_description.txt (default/complex design description for multi-modal models)
- medium_design_description.txt (medium design description for multi-modal models)
- simple_design_description.txt (simple design description for multi-modal models)
- gpt4_design_description.txt (default/complex design description for natural language only models)
- gpt4_medium_design_description.txt (medium design description for natural language only models)
- gpt4_simple_design_description.txt (simple design description for natural language only models)
- gptv_next_token_1.txt (first prompt of token prediction for multi-modal models)
- gptv_next_token_2.txt (second prompt of token prediction for multi-modal models)
- gptv_next_token_1.txt (third prompt of token prediction for multi-modal models)
- gpt4_next_token_1.txt (first prompt of token prediction for natural language only models)
- gpt4_next_token_2.txt (second prompt of token prediction for natural language only models)
- gpt4_next_token_1.txt (third prompt of token prediction for natural language only models)

- code_completion_1.txt (first prompt of code completion for multi-modal models)
- code_completion_2.txt (second prompt of code completion for multi-modal models)
- code_completion_3.txt (third prompt of code completion for multi-modal models)
- gpt4_code_completion_1.txt (first prompt of code completion for natural language only models)
- gpt4_code_completion_2.txt (second prompt of code completion for natural language only models)
- gpt4_code_completion_3.txt (third prompt of code completion for natural language only models)

## Enviroment establishment
1. Establish the python environment
```
pip install requirements.txt
```
2. You need to install `iverilog` package from [here](https://bleyer.org/icarus/) to establish the testing environment.
3. Use your own openai api keys in `src/llm_generate_code.py`, `src/llm_complete_code.py`, `src/llm_predict_token.py`. We recommend you use 2 api keys here to overcome the api limitations. 

## How to run the code
When you want to run the code, you can simply run
```
python src/main.py --model_name=<model> --prompt_type=<type> --method=<method>
```
args:
- model_name: gpt-4/gpt-4-vision-preview
- prompt_type: simple/medium/complex, three levels of the design_descriptions
- method: default/complete/predict, "default" means generate the whole verilog code, "complete" means complete the code with a snippet of the  verilog code, "predict" means predict the next token of the verilog code.

When you want to check the function correctness of the code, just run
```
python src/function_correctness.py
```

When you want to check the next token correctness, just run

```
python src/next_token_correctness.py
```

## Chip drawing tool
chip_draw_tool folder contains the tool code that can faciliate drawing the chip. When you want to the code, type
```
python chip_draw_tool/chip_graph.py
```

You will get the following menu:

```
Welcome to the chip draw tool.
What's the design name of your chip?
Design name: <design_name>

1. Add submodule
2. Add connections between submodules
3. Connect signal to a port
4. Done
```
In this tool, you can draw the chip diagram quickly, and you only need to define the submodules and the connections among the submodules. Then the tool can automatically draw the chip diagram for you.


