import subprocess
import os
import json

def run_yosys_script(verilog_file, output_json, output_dot):
    try:
        # Step 1: List all modules
        script_list_modules = f"""
        read_verilog -sv {verilog_file};
        design -save top_design;
        log;
        """
        result = subprocess.run(['yosys', '-p', script_list_modules], capture_output=True, text=True, check=True, timeout=60)
        modules = []
        leaf_modules = []
        for line in result.stdout.splitlines():
            if line.startswith("Generating RTLIL representation for module `\\"):
                module_name = line.split('`\\')[1].rstrip("'.")
                modules.append(module_name)
        
        # Step 2: Find the top module
        top_module = None
        max_modules_count = 0
        if len(modules) > 1:
            for module in modules:
                script_check_top = f"""
                read_verilog {verilog_file};
                hierarchy -check -top {module};
                proc; opt; fsm; opt; memory; opt;
                techmap; opt;
                write_json metadata/temp.json;
                """
                subprocess.run(['yosys', '-p', script_check_top], capture_output=True, text=True, check=True, timeout=60)
                with open('metadata/temp.json') as f:
                    data = json.load(f)
                    modules_count = len(data.get('modules', {}))
                    if modules_count == 1:
                        leaf_modules.append(module)
                    if modules_count > max_modules_count:
                        max_modules_count = modules_count
                        top_module = module
        else:
            top_module = modules[0]
            leaf_modules.append(top_module)
        
        # Step 3: Generate final output with the top module
        script_final = f"""
        read_verilog {verilog_file};
        hierarchy -check -top {top_module};
        proc; opt; fsm; opt; memory; opt;
        techmap; opt;
        write_json {output_json};
        show -format dot -prefix {output_dot} -notitle;
        """
        result = subprocess.run(['yosys', '-p', script_final], capture_output=True, text=True, check=True, timeout=60)

    except subprocess.TimeoutExpired:
        print("Error: Yosys script execution timed out after 60 seconds.")
        raise
    except subprocess.CalledProcessError as e:
        print("Error executing Yosys script:")
        print(e.stderr)
        raise

    return top_module, leaf_modules

def main():
    verilog_file = "test/adder_16bit.v"
    output_json = "metadata/out.json"
    output_dot = "metadata/out"
    
    if not os.path.exists(verilog_file):
        print(f"Error: Verilog file '{verilog_file}' not found.")
        return
    
    run_yosys_script(verilog_file, output_json, output_dot)
    
    if os.path.exists(output_json):
        print(f"JSON output generated: {output_json}")
    else:
        print(f"Error: JSON output file '{output_json}' was not generated.")
    
    dot_file = f"{output_dot}.dot"
    if os.path.exists(dot_file):
        print(f"DOT file generated: {dot_file}")
    else:
        print(f"Error: DOT file '{dot_file}' was not generated.")

if __name__ == "__main__":
    main()