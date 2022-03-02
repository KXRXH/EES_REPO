# Макс кол-во подстанций типа Б: 3
# 15 МВт - Макс выход ЭС
# 23 МВт - Макс мощность подстанции
num_of_stationsA = 0
num_of_stationsB = 1
topology = [[[], [], []] * num_of_stationsA, [[], []] * num_of_stationsB]
generators = {"solar": 1, "wind": 0}
consumers = {"hA": 1, "hB": 0, "hosp": 0, "manuf": 0}

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


obj_types = {
    "solar": 15,  # солнечные электростанции
    "wind": 15,  # ветровые электростанции
    "houseA": -5,  # дом А
    "houseB": -5,  # дом Б
    "factory": -5  # заводы
    # "hospital" -10  # больницы
}
line = ["houseB", "houseB", "houseB"]


def get_consumption_of_line(line: list) -> float:
    sum = 0
    for obj in line:
        sum += abs(obj_types.get(obj, 0))
    return get_input_power(sum)


def get_charge_of_line(line: list) -> float:
    sum = 0
    for obj in line:
        sum += obj_types.get(obj, 0)
    return get_out_power(sum)


print(get_consumption_of_line(line))
