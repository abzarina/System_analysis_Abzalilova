import json
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import trapezoid


def fuzzification(temp_now, data):
    result = {}

    for term in data:
        name = term["id"]
        points = term["points"]
        attachment_degree = 0
        for (start_x, start_y), (end_x, end_y) in zip(points, points[1:]):
            if start_x <= temp_now <= end_x:
                attachment_degree = start_y if start_x == end_x else start_y + (end_y - start_y) * (temp_now - start_x) / (end_x - start_x)
                break
        result[name] = attachment_degree

    return result


def map_fuzzification_results_to_output(fuzzification_results, control_mapping):
    fuzzification_control_output = {}

    for rule in control_mapping:
        input_label, output_label = rule
        value = fuzzification_results.get(input_label, 0)
        if output_label in fuzzification_control_output:
            fuzzification_control_output[output_label] = max(fuzzification_control_output[output_label], value)
        else:
            fuzzification_control_output[output_label] = value

    return fuzzification_control_output



def defuzzification(heating_values, data):
    weighted_sum = 0
    total_weight = 0

    for name, attachment_degree in heating_values.items():
        if attachment_degree > 0:
            try:
                term = next(item for item in data if item["id"] == name)
                points = term["points"]
                term_centroid = sum([x for x, _ in points]) / len(points)  # Calculate centroid
                weighted_sum += attachment_degree * term_centroid
                total_weight += attachment_degree
            except StopIteration:
                print(f"No matching term found for {name}")
                continue

    if total_weight != 0:
        return weighted_sum / total_weight 
    else: 
        return 0


def main(temperature_sets_json, heating_sets_json, rules_json, temperature_now):
    temperature_data = json.loads(temperature_sets_json)["температура"]
    warming_data = json.loads(heating_sets_json)["положение"]
    control_data = json.loads(rules_json)

    fuzzification_results = fuzzification(temperature_now, temperature_data)
    fuzzification_control_output = map_fuzzification_results_to_output(fuzzification_results, control_data)
    optimal_control = defuzzification(fuzzification_control_output, warming_data)

    return round(optimal_control, 2)


# Пример использования
temperature_sets_json = """
{
  "температура": [
      {
      "id": "холодно",
      "points": [
          [0,1],
          [18,1],
          [22,0],
          [50,0]
      ]
      },
      {
      "id": "комфортно",
      "points": [
          [18,0],
          [22,1],
          [24,1],
          [26,0]
      ]
      },
      {
      "id": "жарко",
      "points": [
          [24,0],
          [26,1],
          [50,1]
      ]
      }
  ]
}
"""

heating_sets_json = """
{
  "положение": [
      {
        "id": "слабый",
        "points": [
            [-1,0],
            [0,1],
            [5,1],
            [8,0]
        ]
      },
      {
        "id": "умеренный",
        "points": [
            [5,0],
            [8,1],
            [13,1],
            [16,0]
        ]
      },
      {
        "id": "интенсивный",
        "points": [
            [13,0],
            [16,1],
            [18,1],
            [23,1],
            [26,0]
        ]
      }
  ]
}
"""

rules_json = """
[
    ["холодно", "интенсивный"],
    ["комфортно", "умеренный"],
    ["жарко", "слабый"]
]
"""

current_temp = 1

optimal_heating = main(temperature_sets_json, heating_sets_json, rules_json, current_temp)
print(f"Оптимальный уровень нагрева при температуре {current_temp}°C: {optimal_heating}")

current_temp = 20
optimal_heating = main(temperature_sets_json, heating_sets_json, rules_json, current_temp)
print(f"Оптимальный уровень нагрева при температуре {current_temp}°C: {optimal_heating}")

current_temp = 25
optimal_heating = main(temperature_sets_json, heating_sets_json, rules_json, current_temp)
print(f"Оптимальный уровень нагрева при температуре {current_temp}°C: {optimal_heating}")