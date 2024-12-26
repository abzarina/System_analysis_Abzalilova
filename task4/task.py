import numpy as np
from math import log2

def calc_entropy(prob_array):
    entropy= 0
    for prob in np.nditer(prob_array):
        entropy -= prob * log2(prob)
    return entropy

def analyze_data(data_matrix):
    data_array = np.array(data_matrix)
    total_events = data_array.sum()

    joint_probability_matrix = data_array / total_events

    marginal_prob_rows = joint_probability_matrix.sum(axis=1)
    marginal_prob_cols = joint_probability_matrix.sum(axis=0)

    row_entropy = calc_entropy(marginal_prob_rows)
    col_entropy = calc_entropy(marginal_prob_cols)

    conditional_prob_matrix = np.copy(joint_probability_matrix)
    total_conditional_entropy = 0

    for i, row_prob in enumerate(marginal_prob_rows):
        conditional_prob_matrix[i] /= row_prob
        conditional_entropy = calc_entropy(conditional_prob_matrix[i])
        total_conditional_entropy += conditional_entropy * row_prob

    mutual_information = col_entropy - total_conditional_entropy
    derived_joint_entropy = row_entropy + total_conditional_entropy

    print(f"Количество информации: {round(mutual_information, 2)}")
    print(f"Энтропия совместных событий: {round(derived_joint_entropy, 2)}")

test_data = [[20, 15, 10, 5],
               [30, 20, 15, 10],
               [25, 25, 20, 15],
               [20, 20, 25, 20],
               [15, 15, 30, 25]]


def main():
    analyze_data(test_data)

if __name__ == "__main__":
    main()