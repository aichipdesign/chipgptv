import json
import pprint

def extract_module_info(json_data, leaf_modules):
    modules = {}
    module_names = set(json_data['modules'].keys())

    for module_name, module_data in json_data['modules'].items():
        module_info = {
            'name': module_name,
            'ports': {},
            'submodules': [],
            'connections': {}
        }
        
        # Extract port information
        if 'ports' in module_data:
            for port_name, port_data in module_data['ports'].items():
                module_info['ports'][port_name] = {
                    'direction': port_data['direction'],
                    'width': len(port_data['bits'])
                }
        if module_name in leaf_modules:
            modules[module_name] = module_info
            continue

        # Extract netname information (but don't store it in the output)
        netnames = {}
        if 'netnames' in module_data:
            for net_name, net_data in module_data['netnames'].items():
                netnames[net_name] = net_data['bits']
        
        # Create a mapping of bit identifiers to signal names and ranges
        bit_to_signal = {}
        for net_name, bits in netnames.items():
            for i, bit in enumerate(bits):
                bit_to_signal[bit] = (net_name, i)
        
        # Extract submodule information and connections
        if 'cells' in module_data:
            for cell_name, cell_data in module_data['cells'].items():
                if cell_data['type'] in module_names:
                    module_info['submodules'].append(cell_data['type'])
                    connections = {}
                    for port, bits in cell_data['connections'].items():
                        if len(bits) == 1:
                            bit = bits[0]
                            if bit in bit_to_signal:
                                signal_name, bit_index = bit_to_signal[bit]
                                connections[port] = f"{signal_name}[{bit_index}]"
                            else:
                                connections[port] = f"{bit:b}"
                        else:
                            signal_ranges = {}
                            for bit in bits:
                                if bit in bit_to_signal:
                                    signal_name, bit_index = bit_to_signal[bit]
                                    if signal_name not in signal_ranges:
                                        signal_ranges[signal_name] = [bit_index, bit_index]
                                    else:
                                        signal_ranges[signal_name][0] = min(signal_ranges[signal_name][0], bit_index)
                                        signal_ranges[signal_name][1] = max(signal_ranges[signal_name][1], bit_index)
                                else:
                                    connections[port] = f"{bit:b}"
                            
                            if len(signal_ranges) == 1:
                                signal_name, (start, end) = next(iter(signal_ranges.items()))
                                if start == end:
                                    connections[port] = f"{signal_name}[{start}]"
                                else:
                                    connections[port] = f"{signal_name}[{end}:{start}]"
                            else:
                                signal_range = []
                                for signal_name, (start, end) in signal_ranges.items():
                                    if start == end:
                                        signal_range.append(f"{signal_name}[{start}]")
                                    else:
                                        signal_range.append(f"{signal_name}[{end}:{start}]")
                                connections[port] = f"{{{', '.join(signal_range)}}}"
                    module_info['connections'][cell_name] = connections
        
        modules[module_name] = module_info
    
    return modules

def main():
    # Read the JSON file
    with open('out.json', 'r') as f:
        json_data = json.load(f)
    
    # Extract module information
    modules = extract_module_info(json_data)
    
    # Pretty print the extracted information (for debugging)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(modules)
    
    # Store the extracted information in a new JSON file
    with open('module_hierarchy.json', 'w') as f:
        json.dump(modules, f, indent=2)

if __name__ == "__main__":
    main()
