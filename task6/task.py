import json
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import trapezoid

def main(temperature_sets_json, heating_sets_json, rules_json, current_temperature):
    try:
        temperature_sets = json.loads(temperature_sets_json)
        heating_sets = json.loads(heating_sets_json)
        rules = json.loads(rules_json)
    except json.JSONDecodeError:
        return "Ошибка: Неверный формат JSON-строки."


    def create_interp_function(points):
        x = np.array([point[0] for point in points])
        y = np.array([point[1] for point in points])

        #Handle duplicate x-values by averaging y-values for those x's
        unique_x, index, counts = np.unique(x, return_index=True, return_counts=True)
        averaged_y = np.array([np.mean(y[i:i+c]) for i,c in zip(index, counts)])

        return interp1d(unique_x, averaged_y, kind='linear', fill_value="extrapolate")



    # Функции принадлежности для температуры
    temp_functions = {}
    for term in temperature_sets["температура"]:
        temp_functions[term["id"]] = create_interp_function(term["points"])

    # Функции принадлежности для уровня нагрева
    heating_functions = {}
    for term in heating_sets["температура"]:
        heating_functions[term["id"]] = create_interp_function(term["points"])

    # Определение степеней принадлежности текущей температуры к нечетким множествам
    membership_degrees = {term_id: temp_functions[term_id](current_temperature) for term_id in temp_functions}

    # Применение правил нечеткого вывода
    heating_membership = {}
    for rule in rules:
        temp_term, heating_term = rule
        degree = min(membership_degrees[temp_term], 1) #  Убираем ограничение на 1
        if heating_term in heating_membership:
            heating_membership[heating_term] = max(heating_membership[heating_term], degree)
        else:
            heating_membership[heating_term] = degree

    # Дефаззификация (метод центра тяжести)
    numerator = 0
    denominator = 0
    for term_id, degree in heating_membership.items():
        x = np.linspace(0,26,100) # Диапазон значений для уровня нагрева
        y = heating_functions[term_id](x)
        centroid = trapezoid(x * y, x) / trapezoid(y, x)
        numerator += centroid * degree
        denominator += degree

    if denominator == 0:
        return 0 # Обработка случая, когда знаменатель равен нулю

    optimal_heating = numerator / denominator

    return round(optimal_heating, 2)


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
  "температура": [
      {
        "id": "слабый",
        "points": [
            [0,0],
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

current_temp = -24.00

optimal_heating = main(temperature_sets_json, heating_sets_json, rules_json, current_temp)
print(f"Оптимальный уровень нагрева при температуре {current_temp}°C: {optimal_heating}")

current_temp = 23
optimal_heating = main(temperature_sets_json, heating_sets_json, rules_json, current_temp)
print(f"Оптимальный уровень нагрева при температуре {current_temp}°C: {optimal_heating}")