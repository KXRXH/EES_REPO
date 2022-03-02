# Макс кол-во подстанций типа Б: 3
# 15 МВт - Макс выход ЭС
# 23 МВт - Макс мощность подстанции
# 28.7 МВт - Макс выроботка на 1 подстанцию (22.96 МВт с потерями)
# 19.6 МВт - Макс потребление на 1 подстанцию (22.93 МВт с потерями)
# num_of_stationsA = 0
# num_of_stationsB = 1
# topology = [[[], [], []] * num_of_stationsA, [[], []] * num_of_stationsB]

from obj_types import types

get_percent = lambda value: round(((20 * value) / 23) / 100, 3) if value < 23 else 0.2


def get_out_power(value: float) -> float:
    return value - value * get_percent(value)


def get_input_power(value: float) -> float:
    return value + value * get_percent(value)


def get_max_diesel_power(value: float) -> float:
    max_value = 0
    for i in range(5, 0, -1):
        if get_out_power(value + i) <= 23:
            max_value = i
            break
    if max_value < 5:
        for i in [round(max_value + x * 0.01, 2) for x in range(0, 100)][::-1]:
            if get_out_power(i + value) <= 23:
                return i
    return max_value


"""
# Max consumption of the line
def get_consumption_of_line(line: list) -> float:
    consumption = 0
    for obj in line:
        consumption += abs(types.get(obj, 0))
    return get_input_power(consumption)


# Max charge of the line
def get_charge_of_line(line: list) -> float:
    charge = 0
    for obj in line:
        charge += types.get(obj, 0)
    return get_out_power(charge)
"""

line1 = ["solar", "factory1", 'factory1', 'factory1', ]


# Max power of line
def get_mixed_power_of_line(line: list) -> float:
    power = 0
    for obj in line:
        power += types.get(obj, 0)
    if power > 0:
        return get_out_power(power)
    return -get_input_power(-power)


max_cons = get_mixed_power_of_line(["houseB", "houseB", "houseB", "factory2", "factory2"])
print(max_cons)