from openai import OpenAI
import argparse
import os

# get access the parent directory
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

api_keys = ['API_KEY1', "API_KEY2"]

def llm_complete_code(model_name, instance, output, output_answer, iter):


    # Function to rotate the API keys
    def rotate_keys():
        api_keys.append(api_keys.pop(0))



    # Try each API key until successful
    for _ in range(len(api_keys)):
        try:
            client = OpenAI(api_key=api_keys[0])

            # get the prompt
            with open("benchmark/" + f"{instance}/code_completion_{iter}.txt", "r", encoding='utf-8') as f:
                gpt4v_prompt = f.read()

            
            with open("benchmark/" + f"{instance}/gpt4_code_completion_{iter}.txt", "r", encoding='utf-8') as f:
                gpt4_prompt = f.read()
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



