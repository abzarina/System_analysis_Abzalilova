import json
import numpy as np

def get_matrix(filepath: str): 
    try:
        with open(filepath, 'r') as file: 
            clusters = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка чтения JSON файла: {e}")
        return None

    clusters = [c if isinstance(c, list) else [c] for c in clusters] 
    n = sum(len(cluster) for cluster in clusters)
    
    matrix = [[1] * n for _ in range(n)]
    
    processed_elements = [] 
    for cluster in clusters:
        for processed_element in processed_elements:
            for element in cluster:
                matrix[element - 1][processed_element - 1] = 0 
        for element in cluster:
            processed_elements.append(int(element))
    
    return np.array(matrix)
 
def find_clusters(matrix): 
    conflict_core = [] 
    
    for i in range(len(matrix)): 
        for j in range(i + 1, len(matrix)): 
            if matrix[i][j] == 0 and matrix[j][i] == 0: 
                conflict_pair = sorted([i + 1, j + 1]) 
                if conflict_pair not in conflict_core: 
                    conflict_core.append(conflict_pair)
    
    return conflict_core

def main(file_path1, file_path2):
    matrix1 = get_matrix(file_path1)
    matrix2 = get_matrix(file_path2)
    
    if matrix1 is None or matrix2 is None:
        print("Не менее 1 файла пустой")
        return
    
    matrix_and = np.multiply(matrix1, matrix2)
    matrix_and_t = np.multiply(np.transpose(matrix1), np.transpose(matrix2))
    matrix_or = np.maximum(matrix_and, matrix_and_t)
    
    clusters = find_clusters(matrix_or)
    print("Conflicting clusters or pairs:", clusters)

#main("example1.json", "example2.json")