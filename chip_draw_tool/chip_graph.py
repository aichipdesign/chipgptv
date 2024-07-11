from typing import List, Tuple, Set, Optional
from graphviz import Digraph

class Node:
    def __init__(self, name: str):
        self.name: str = name
        self.ports: List[Tuple[str, int, int]] = []  # List of tuples, each tuple is (port_name, width, type) type 0: input, 1: output
        self._connected_ports: Set[str] = set()  # Set of port names that are connected
        self.signal_connected_ports: Set[Tuple[str, int]] = set()  # Set of port names that are connected to signals

    def add_port(self, port_name: str, width: int, port_type: int) -> int:
        """Add a port to the node."""
        if not self.find_port(port_name):
            self.ports.append((port_name, width, port_type))
            return 0
        else:
            return -1

    def connect_port(self, port_name: str) -> None:
        """Mark a port as connected."""
        if port_name not in self._connected_ports:
            self._connected_ports.add(port_name)
    
    def connect_signal_port(self, port_name: str, signal_name: str) -> None:
        """Mark a port as connected to a signal."""
        self.signal_connected_ports.add((port_name, signal_name))
        self._connected_ports.add(port_name)

    def disconnect_port(self, port_name: str) -> None:
        """Mark a port as disconnected."""
        if port_name in self._connected_ports:
            self._connected_ports.remove(port_name)
        # just use port_name to find if there is such a port in signal_connected_ports
        for port in self.signal_connected_ports:
            if port[0] == port_name:
                self.signal_connected_ports.remove(port)

    def is_port_connected(self, port_name: str) -> bool:
        """Check if a port is connected."""
        return port_name in self._connected_ports
    
    def find_port(self, port_name: str) -> Optional[Tuple[str, int]]:
        """Find a port by name and return the port tuple."""
        for port in self.ports:
            if port[0] == port_name:
                return port
        return None


class Graph:
    def __init__(self, name: str):
        self.name: str = name  # Design name
        self.nodes: List[Node] = []  # List of Node objects
        self.edges: List[Tuple[Node, Node, str, str]] = []  # List of edges

    def add_node(self, node: Node) -> None:
        if node not in self.nodes:
            self.nodes.append(node)

    def add_edge(self, nodeA: Node, nodeB: Node, portA: str, portB: str) -> int:
        # Find ports and verify if their widths match
        port_tuple_A = nodeA.find_port(portA)
        port_tuple_B = nodeB.find_port(portB)

        if port_tuple_A and port_tuple_B and port_tuple_A[1] == port_tuple_B[1] and port_tuple_A[2] != port_tuple_B[2]:
            self.edges.append((nodeA, nodeB, portA, portB))
            # Mark ports as connected in each node
            nodeA.connect_port(portA)
            nodeB.connect_port(portB)
            return 0
        else:
            return -1
    
    def add_signal_edge(self, node: Node, port: str, signal_name: str) -> None:
        port_tuple = node.find_port(port)
        if port_tuple:
            node.connect_signal_port(port, signal_name)
        else:
            print("Port does not exist.")

    def delete_node(self, node: Node) -> None:
        self.nodes.remove(node)
        # Remove edges associated with this node
        self.edges = [edge for edge in self.edges if node not in edge[:2]]

    def delete_edge(self, nodeA: Node, nodeB: Node, portA: str, portB: str) -> None:
        edge_to_delete = (nodeA, nodeB, portA, portB)
        if edge_to_delete in self.edges:
            self.edges.remove(edge_to_delete)
            # Disconnect ports
            nodeA.disconnect_port(portA)
            nodeB.disconnect_port(portB)

    def find_node(self, name: str) -> Node:
        """Find a node by name."""
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def all_ports_connected(self):
        for node in self.nodes:
            return len(node.ports) == len(node._connected_ports)
    

    def visualize(self):
        dot = Digraph('G', filename=f'{self.name}.gv', engine='dot')
        dot.attr('node', shape='plaintext')
        dot.attr(rankdir='LR')  # Graph will be left to right
        dot.attr(newrank='true')  # Use new rank model

        # Create nodes with ports using HTML-like labels
        for node in self.nodes:
            inputs = '<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">'
            outputs = '<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">'
            for port_name, port_width, port_type in node.ports:
                port_label = f'<FONT POINT-SIZE="10">{port_name} ({port_width})</FONT>'
                if port_type == 0:  # input port
                    inputs += f'<TR><TD PORT="{port_name}" ALIGN="LEFT">{port_label}</TD></TR>'
                elif port_type == 1:  # output port
                    outputs += f'<TR><TD PORT="{port_name}" ALIGN="RIGHT">{port_label}</TD></TR>'
            inputs += '</TABLE>'
            outputs += '</TABLE>'

            label = f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0">'
            label += f'<TR><TD ALIGN="LEFT" BORDER="0">{inputs}</TD>'
            label += f'<TD>{node.name}</TD>'
            label += f'<TD ALIGN="RIGHT" BORDER="0">{outputs}</TD></TR>'
            label += '</TABLE>>'
            dot.node(node.name, label=label)

        # Create edges for node connections, specifying ports
        for edge in self.edges:
            nodeA, nodeB, portA, portB = edge
            portA_tuple = nodeA.find_port(portA)
            portB_tuple = nodeB.find_port(portB)
            width = portA_tuple[1] if portA_tuple and portB_tuple else ''
            
            # Specify the ports to avoid overlap
            tailport = 'e' if portA_tuple[2] == 1 else 'w'  # Output port should connect on the east, input on the west
            headport = 'w' if portB_tuple[2] == 0 else 'e'  # Input port should connect on the west, output on the east
            
            dot.edge(f'{nodeA.name}:{portA}:{tailport}', f'{nodeB.name}:{portB}:{headport}', label=str(width), dir='none')

        # Visualize signal connections, specifying ports
        for node in self.nodes:
            for port, signal in node.signal_connected_ports:
                signal_id = f'signal_{signal}'
                dot.node(signal, '', width='.1', height='.1', shape='point', style='invis')
                # Determine the appropriate port to connect the signal
                port_tuple = node.find_port(port)
                signal_port = 'w' if port_tuple[2] == 0 else 'e'
                dot.edge(signal_id, f'{node.name}:{port}:{signal_port}', dir='none')

        dot.render(view=True)

# Continue with the rest of your classes and main function logic

def tool_interface():
    print("Welcome to the chip draw tool.")
    print("What's the design name of your chip?")
    design_name = input("Design name: ")
    graph = Graph(design_name)
    while True:
        print("\n1. Add submodule")
        print("2. Add connections between submodules")
        print("3. Connect signal to a port")
        print("4. Done")

        choice = input("Choose an option: ")
        if choice == '1':
            name = input("Submodule name: ")
            if graph.find_node(name):
                print("Submodule already exists.")
                continue
            node = Node(name)
            while True:
                port_name = input("Port name, type -1 to stop: ")
                if port_name == '-1':
                    if len(node.ports) == 0:
                        print("At least one port is required.")
                        continue
                    break
                width = int(input("Port width: "))
                port_type = int(input("Port type (0: input, 1: output): "))
                success = node.add_port(port_name, width, port_type)
                if success == -1:
                    print("Add port failed")
                    continue
            graph.add_node(node)

        elif choice == '2':
            name1 = input("Submodule name 1: ")
            name2 = input("Submodule name 2: ")
            nodeA = graph.find_node(name1)
            nodeB = graph.find_node(name2)
            if not nodeA or not nodeB:
                print("One of the submodules does not exist.")
                continue
            portA = input(f"Port in {name1}: ")
            portB = input(f"Port in {name2}: ")
            try:
                success = graph.add_edge(nodeA, nodeB, portA, portB)
                if success == -1:
                    print("Add edge failed")
                    continue
            except ValueError as e:
                print(e)

        elif choice == '3':
            name = input("Submodule name: ")
            node = graph.find_node(name)
            if not node:
                print("Submodule does not exist.")
                continue
            port_name = input("Port name: ")
            signal_name = input("Signal name: ")
            if node.find_port(port_name):
                node.connect_signal_port(port_name, signal_name)
            else:
                print("Port does not exist.")

        elif choice == '4':
            if graph.all_ports_connected():
                print("All ports are properly connected.")
                # You can add visualization or more details here.
                graph.visualize()
                break
            else:
                print("Not all ports are connected. Check your configuration.")

if __name__ == "__main__":
    tool_interface()