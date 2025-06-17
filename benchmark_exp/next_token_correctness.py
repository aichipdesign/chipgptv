import os
import re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def extract_snippet(code):
    """Extracts a verilog code snippet enclosed in triple backticks."""
    pattern = r"```verilog(.*?)```"
    match = re.search(pattern, code, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def get_next_token_from_reference(reference_path, token_length):
    """Gets the token at a specific position from the reference code."""
    with open(reference_path, 'r', encoding='utf-8') as file:
        reference_code = file.read()
    tokens = reference_code.split()
    if (token_length == len(tokens)):
        print("reference file path: ", reference_path)
        return None
    if tokens[token_length] == '\n':
        token_length += 1
    if token_length < len(tokens):
        return tokens[token_length]
    return None

def find_reference_file(folder_path):
    """Finds the reference file in the given folder."""
    for filename in os.listdir(folder_path):
        if filename == 'reference.v' or filename.startswith('verified_'):
            return os.path.join(folder_path, filename)
    return None

def process_folder(folder_path):
    """Processes each folder and compares GPT generated tokens with the reference."""
    gptv_correct_num = 0
    gpt4_correct_num = 0
    path_list = folder_path.split(os.sep)
    for iter_num in range(1, 4):
        gpt_files = [f"gptv_next_token_{iter_num}.txt", f"gpt4_next_token_{iter_num}.txt"]
        for gpt_file in gpt_files:
            file_path = os.path.join(folder_path, gpt_file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                snippet = extract_snippet(content)
                tokens = snippet.split()
                token_length = len(tokens)
                reference_file_path = find_reference_file(folder_path)
                if reference_file_path:
                    next_token = get_next_token_from_reference(reference_file_path, token_length)
                    print(f"Next token in {path_list[1]} after {token_length} tokens is: {next_token}")

                    # Check output in the corresponding prediction file
                    output_dir = 'generated_code/gpt-4-vision-preview-predict' if 'gptv' in gpt_file else 'generated_code/gpt-4-predict'

                    prediction_file_path = os.path.join(output_dir, path_list[0], f"{path_list[1]}_{iter_num-1}.v") if 'gptv' in gpt_file else os.path.join(output_dir, path_list[0], f"{path_list[1]}_{iter_num-1}.txt")
                    if os.path.exists(prediction_file_path):
                        with open(prediction_file_path, 'r', encoding='utf-8') as pred_file:
                            predicted_token = pred_file.read().strip()
                            while (len(predicted_token) > 0 and predicted_token[0] == '\n'):
                                predicted_token = predicted_token[1:]
                            if len(predicted_token) == 0:
                                continue
                            # get the first token from the predicted code
                            predicted_token = predicted_token.split()[0]
                            print(f"Predicted token: {predicted_token}")

                        if predicted_token == next_token:
                            if 'gptv' in gpt_file:
                                gptv_correct_num += 1
                            else:
                                gpt4_correct_num += 1
    with open("next_token_correctness.csv", 'a') as file:
        # keep only 2 digits after the decimal point
        file.write(f"{path_list[1]},{gptv_correct_num * 100 / 3:.2f}%,{gpt4_correct_num * 100 / 3:.2f}%\n")
    

                        

def process_all_folders(main_folders):
    """Processes all design folders under the base path."""
    for folder in main_folders:
        for sub_folder in os.listdir(folder):
            folder_path = os.path.join(folder, sub_folder)
            if os.path.isdir(folder_path):
                process_folder(folder_path)

# Example call
if __name__ == '__main__':
    # Define your main folders here
    main_folders = ['advanced', 'arithmetic', 'digital_circuit']
    # clear the output file
    with open("next_token_correctness.csv", 'w') as file:
        file.write("Design, GPT-4 Vision Preview, GPT-4\n")
    process_all_folders(main_folders)
