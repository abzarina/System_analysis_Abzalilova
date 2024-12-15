import math
import json

def main(adj_list):
    vertex_degrees = {vertex: len(neighbors) for vertex, neighbors in adj_list.items()}
    total_edges_count = sum(vertex_degrees.values())
    
    if total_edges_count == 0:
        return 0
    entropy_value = 0
    for _, degree in vertex_degrees.items():
        if degree > 0:
            probability = degree / total_edges_count
            entropy_value -= probability * math.log2(probability)
    
    return entropy_value

with open('example.json') as example:
    example_graph = json.load(example)

entropy_of_graph = main(example_graph)
print(f"Graph entropy: {entropy_of_graph}")