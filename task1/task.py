import csv

def import_csv(file_path, row_numer, col_number):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    if (row_numer > len(data)) or (col_number > len(data[0])):
        return "Out of range"
    return data[row_numer - 1][col_number - 1]

file_path = 'example.csv'
data = import_csv(file_path, 1, 1)
print(data)