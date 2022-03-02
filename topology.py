objects = {"hA": 0, "hB": 1, "ss": 1, "ws": 0, "hosp": 0, "manuf": 0}  # кол-во объектов
get_percent = lambda value: round(((20 * value) / 23) / 100, 3) if value < 23 else 0.2
# Макс кол-во подстанций типа Б: 3
# 15 МВт - Макс выход ЭС
# 23 МВт - Макс мощность подстанции


def get_out_power(value: float) -> float:
    return value - value * get_percent(value)

def get_input_power(value: float) -> float:
    return value + value * get_percent(value)


def get_max_diesel_power(value: float):
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