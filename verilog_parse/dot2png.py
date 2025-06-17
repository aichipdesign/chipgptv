import graphviz
import os

def dot_to_png(dot_text, output_file):
    # Create a Graphviz graph object
    graph = graphviz.Source(dot_text)
    
    # Render the graph to a PNG file
    graph.render(output_file, format='png', cleanup=True)
    

def main():
    # Example usage
    dot_text = """
    digraph G {
        A -> B;
        B -> C;
        C -> A;
    }
    """
    
    output_file = "output_graph"
    dot_to_png(dot_text, output_file)
    print(f"PNG file created: {output_file}.png")

if __name__ == "__main__":
    main()
