import csv
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: task1 % python task.py <path_to_json> <row_numer> <col_number>")
        return

    file_path = sys.argv[1]
    row_numer = int(sys.argv[2])
    col_number = int(sys.argv[3])

    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    
    if (row_numer > len(data)) or (col_number > len(data[0])):
        return "Out of range"
    print(data[row_numer - 1][col_number - 1])

# file_path = 'example.csv'

main()