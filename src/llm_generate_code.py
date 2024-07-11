from openai import OpenAI
import argparse
import os

# get access the parent directory
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

api_keys = ['API_KEY1', "API_KEY2"]

def llm_generate_code(model_name, instance, output, output_answer, prompt_type):


    # Function to rotate the API keys
    def rotate_keys():
        api_keys.append(api_keys.pop(0))



    # Try each API key until successful
    for _ in range(len(api_keys)):
        try:
            client = OpenAI(api_key=api_keys[0])

            # get the prompt
            with open("benchmark/" + f"{instance}/simple_design_description.txt", "r", encoding='utf-8') as f:
                simple_prompt = f.read()

            with open("benchmark/" + f"{instance}/medium_design_description.txt", "r", encoding='utf-8') as f:
                medium_prompt = f.read()
            
            with open("benchmark/" + f"{instance}/design_description.txt", "r", encoding='utf-8') as f:
                complex_prompt = f.read()

            with open("benchmark/" + f"{instance}/gpt4_design_description.txt", "r", encoding='utf-8') as f:
                gpt4_complex_prompt = f.read()
            with open("benchmark/" + f"{instance}/gpt4_medium_design_description.txt", "r", encoding='utf-8') as f:
                gpt4_medium_prompt = f.read()
            with open("benchmark/" + f"{instance}/gpt4_simple_design_description.txt", "r", encoding='utf-8') as f:
                gpt4_simple_prompt = f.read()
            
            if prompt_type == "simple":
                gpt4v_prompt = simple_prompt
                gpt4_prompt = gpt4_simple_prompt
            elif prompt_type == "medium":
                gpt4v_prompt = medium_prompt
                gpt4_prompt = gpt4_medium_prompt
            elif prompt_type == "complex":
                gpt4v_prompt = complex_prompt
                gpt4_prompt = gpt4_complex_prompt
            else:
                raise ValueError("prompt should be simple, medium or complex")
            

            # get the image url
            img_url = f"https://raw.githubusercontent.com/rong-hash/chipgptv_img/main/{instance}.png"
            if model_name == "gpt-4-vision-preview":
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": gpt4v_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": img_url,
                                },
                            ],
                        }
                    ],
                    max_tokens=3000,
                )
            elif model_name == "gpt-4":
                # need to create the prompt for gpt-4
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": gpt4_prompt
                        }
                    ],
                    max_tokens=3000,
                )
            else :
                raise ValueError("model_name should be gpt-4-vision-preview or gpt-4")
            # parse the answer of verilog.
            # get the text after ```verilog\n and before \n```
            # if there are multiple ```verilog\n, merge all the generated code together
            answer = response.choices[0].message.content
            with open(output_answer, "w") as f:
                f.write(answer)
            # cast the code
            begin = answer.find("```verilog\n")
            end = answer.find("\n```")
            # clear the file first
            with open(output, "w") as f:
                f.write("")
            while begin != -1 and end != -1:
                with open(output, "a") as f:
                    f.write(answer[begin + 10:end])
                begin = answer.find("```verilog\n", end)
                end = answer.find("\n```", begin)
            return  

        except Exception as e:
            print(f"API call failed with key {api_keys[0]}: {e}")
            rotate_keys()  # Move the used key to the end

    raise Exception("All API calls failed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--model", type=str, default="gpt-4-vision-preview", help="The model name")
    parser.add_argument("--instance", type=str, default="arithmetic/adder_8bit", help="The instance name")
    parser.add_argument("--output", type=str, default="generated_code/gpt4v/adder_8bit_1.v", help="The output file name")
    parser.add_argument("--output_answer", type=str, default="generated_code/gpt4v/adder_8bit_1.txt", help="The output file name")
    parser.add_argument("--prompt_type", type=str, default="complex", help="The prompt length")
    model_name = parser.parse_args().model
    instance = parser.parse_args().instance
    output = parser.parse_args().output
    output_answer = parser.parse_args().output_answer
    prompt_type = parser.parse_args().prompt_type
    llm_generate_code(model_name, instance, output, output_answer, prompt_type)


