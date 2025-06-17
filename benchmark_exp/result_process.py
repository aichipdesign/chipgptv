import pandas as pd
import os 
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def process_data(file_path):
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Prepare data structure
    data = {}
    current_situation = None

    # Process each line
    for line in lines:
        line = line.strip()
        if line.startswith('Results for situation'):
            # New situation type
            current_situation = line.split(':')[1].strip()
            data[current_situation] = {}
        elif line and current_situation:
            # Design data
            parts = line.split(':')
            design = parts[0].strip()
            correctness = float(parts[1].replace('% correct', '').strip())
            if design in data[current_situation]:
                data[current_situation][design].append(correctness)
            else:
                data[current_situation][design] = correctness

    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict({(i,j): data[i][j] 
                                 for i in data.keys() 
                                 for j in data[i].keys()},
                                orient='index')
    # Clean up DataFrame structure
    df.index = pd.MultiIndex.from_tuples(df.index)
    df = df.unstack(level=0)
    df.columns = df.columns.droplevel(0)
    df = df.reset_index()
    df.rename(columns={'index': 'design'}, inplace=True)

    # Save to CSV
    output_path = file_path.replace('.txt', '.csv')
    df.to_csv(output_path, index=False)
    print(f"Data processed and saved to {output_path}")

# Example usage
process_data('function_correctness.txt')
