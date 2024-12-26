#!/bin/python

from collections import defaultdict
import csv

def task(csv_str: str):
    children = defaultdict(list)
    parents = defaultdict(list)

    reader = csv.reader(csv_str.splitlines(), delimiter=',')

    for line in reader:
        if not line:
            continue

        a, b = line
        children[a].append(b)
        parents[b].append(a)

        if a not in parents:
            parents[a] = []

        if b not in children:
            children[b] = []

    root = next(key for key in parents if not parents[key])
    leaves = [key for key in children if not children[key]]

    certain_ans = {key: {'r1': set(children[key]),
                         'r2': set(parents[key]),
                         'r3': set(),
                         'r4': set(),
                         'r5': set()}
                   for key in parents}


    stack = [root]
    while stack:
        cur_node = stack.pop()
        for child in children[cur_node]:
            certain_ans[child]['r4'] |= certain_ans[cur_node]['r2'] | certain_ans[cur_node]['r4']
            certain_ans[child]['r5'] |= certain_ans[cur_node]['r1'] - {child, }
            stack.append(child)


    stack = list(leaves)
    while stack:
        cur_node = stack.pop()
        for parent in parents[cur_node]:
            certain_ans[parent]['r3'] |= certain_ans[cur_node]['r1'] | certain_ans[cur_node]['r3']
            if parent not in stack:
                stack.append(parent)

    fields = ('r1', 'r2', 'r3', 'r4', 'r5')
    csv_output = '\n'.join([','.join([str(len(certain_ans[node][field])) for field in fields]) for node in sorted(certain_ans)]) + '\n'

    return csv_output

if __name__ == '__main__':
    input_data = "1,2\n1,3\n3,4\n3,5\n"
    print(task(input_data))