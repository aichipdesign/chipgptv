import os
import re  # Import the regex module

# Get access to the parent directory
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def remove_sentence_with_word(text, word):
    # This regular expression captures sentences that contain the specific word
    pattern = r'(?:[A-Z][^.!?]*?\s)?' + re.escape(word) + r'[^.!?]*[.!?]'
    # Remove the sentence containing the word
    modified_text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    # Clean up extra spaces and return the modified text
    return modified_text   

def generate_descriptions(main_folders):
    for main_folder in main_folders:
        # Check if the main folder exists
        if os.path.exists(main_folder) and os.path.isdir(main_folder):
            for subfolder in os.listdir(main_folder):
                subfolder_path = os.path.join(main_folder, subfolder)
                
                # Check if the current path is a directory (subfolder)
                if os.path.isdir(subfolder_path):
                    description_file_path = os.path.join(subfolder_path, 'intermediate_design_description.txt')
                    # Read the design_description.txt file
                    complete_description_file_path = os.path.join(subfolder_path, 'design_description.txt')
                    with open(complete_description_file_path, 'r', encoding='utf-8') as file:
                        description = file.read()
                    
                    # Find the index using the updated matching method
                    matches = re.search(r"\n", description, re.IGNORECASE)
                    if matches:
                        start_index = matches.start()
                        description = description[start_index:]
                    else:
                        description = "No module description found."
                    
                    # Write to medium_design_description.txt
                    with open(description_file_path, 'w', encoding='utf-8') as file:
                        file.write(description)


def generate_gpt4_medium_descriptions(main_folders):
    for main_folder in main_folders:
        # Check if the main folder exists
        if os.path.exists(main_folder) and os.path.isdir(main_folder):
            for subfolder in os.listdir(main_folder):
                subfolder_path = os.path.join(main_folder, subfolder)
                
                # Check if the current path is a directory (subfolder)
                if os.path.isdir(subfolder_path):
                    description_file_path = os.path.join(subfolder_path, 'gpt4_medium_design_description.txt')
                    # Read the design_description.txt file
                    complete_description_file_path = os.path.join(subfolder_path, 'medium_design_description.txt')
                    with open(complete_description_file_path, 'r', encoding='utf-8') as file:
                        description = file.read()
                    description = remove_sentence_with_word(description, 'picture')
                    with open(description_file_path, 'w', encoding='utf-8') as file:
                        file.write(description)

def generate_gpt4_simple_descriptions(main_folders):
    for main_folder in main_folders:
        # Check if the main folder exists
        if os.path.exists(main_folder) and os.path.isdir(main_folder):
            for subfolder in os.listdir(main_folder):
                subfolder_path = os.path.join(main_folder, subfolder)
                
                # Check if the current path is a directory (subfolder)
                if os.path.isdir(subfolder_path):
                    description_file_path = os.path.join(subfolder_path, 'gpt4_simple_design_description.txt')
                    # Read the design_description.txt file
                    complete_description_file_path = os.path.join(subfolder_path, 'simple_design_description.txt')
                    with open(complete_description_file_path, 'r', encoding='utf-8') as file:
                        description = file.read()
                    description = description.replace(" according to the function description in the image", ".")
                    with open(description_file_path, 'w', encoding='utf-8') as file:
                        file.write(description)
                    
                    

# Define your main folders here
main_folders = ['advanced', 'arithmetic', 'digital_circuit']

# Call the function
if __name__ == "__main__":
    generate_gpt4_simple_descriptions(main_folders)
