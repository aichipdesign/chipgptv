import os
import random
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def process_design_folders(main_folders):
    for main_folder in main_folders:
        if os.path.exists(main_folder) and os.path.isdir(main_folder):
            for subfolder in os.listdir(main_folder):
                subfolder_path = os.path.join(main_folder, subfolder)
                if os.path.isdir(subfolder_path):
                    process_design(subfolder_path)

def process_design(folder_path):
    description_file_path = os.path.join(folder_path, 'medium_design_description.txt')
    if os.path.exists(description_file_path):
        with open(description_file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        
        # Modify 'Implement' to 'Complete' or add a sentence at the beginning
        if 'Implement' in data:
            data = data.replace('Implement', 'Complete')
        else:
            data = "Complete this verilog code." + data
        
        # Remove content after the third newline
        split_data = data.split('\n', 3)
        if len(split_data) > 3:
            data = '\n'.join(split_data[:3])

        # last_period_index = data.rfind('.')
        # second_last_period_index = data.rfind('.', 0, last_period_index)
        # if 'picture' in data[second_last_period_index:last_period_index]:
        #     data = data[:second_last_period_index+1] + data[last_period_index+1:]
        # elif 'diagram' in data[second_last_period_index:last_period_index]:
        #     data = data[:second_last_period_index+1] + data[last_period_index+1:]

        data = data + "Here's the imcomplete verilog code: \n ```verilog"
        # find the last '.' in data, and the second last '.' in the data, check if there is 'picture' or 'diagram' in between
        # if so, delete this sentence
        
        # Attempt to read from 'reference.v' or a file that begins with 'verified'
        verilog_code = get_verilog_code(folder_path)
        
        # Perform the content manipulation and save to files
        for i in range(1, 4):  # Generate three files
            modified_data = modify_and_append(data, verilog_code)
            modified_data = modified_data + f"\n```\nPlease complete the above verilog code."
            output_file_path = os.path.join(folder_path, f'code_completion_{i}.txt')
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(modified_data)

def get_verilog_code(folder_path):
    reference_path = os.path.join(folder_path, 'reference.v')
    if os.path.exists(reference_path):
        with open(reference_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        # Check for files starting with 'verified'
        for filename in os.listdir(folder_path):
            if filename.startswith('verified'):
                verified_path = os.path.join(folder_path, filename)
                with open(verified_path, 'r', encoding='utf-8') as file:
                    return file.read()
    return ''  # Return empty string if no file is found

def modify_and_append(data, verilog_code):
    if verilog_code:
        # Generate a random index in the range of the Verilog code length
        random_index = random.randint(0, len(verilog_code) - 1)

        # Find the next whitespace after the random index to ensure completeness of the last token
        if random_index < len(verilog_code) - 1:  # Check if not at the end of the string
            # Move the index forward to the end of the current token
            while random_index < len(verilog_code) and not verilog_code[random_index].isspace():
                random_index += 1
            # Now move to the end of the whitespace
            while random_index < len(verilog_code) and verilog_code[random_index].isspace():
                random_index += 1

        # Slice the Verilog code up to the adjusted index
        snippet = verilog_code[:random_index]
        data += '\n' + snippet
    return data
# Define your main folders here
main_folders = ['advanced', 'arithmetic', 'digital_circuit']

# Call the function
process_design_folders(main_folders)
