class Factory:
    def __init__(self, price):
        self.price = price
        self.consumption = -5


class Hospital:
    def __init__(self, price):
        self.price = price
        self.consumption = -2


class HouseA:
    def __init__(self, price):
        self.price = price
        self.consumption = -5


class HouseB:
    def __init__(self, price):
        self.price = price
        self.consumption = -5


types = {
    "Solar": 15,  # солнечные электростанции
    "Wind": 15,  # ветровые электростанции
    HouseA: -5,  # дом А
    HouseB: -5,  # дом Б
    Factory: -5,
    Hospital: -4  # больницы
}

tee_count = 6
things = {"Hospital": 0, "Factory": 1, "MainB": 1, "Solar": 2, "HouseA": 3, "MainA": 0, "HouseB": 3, "Wind": 3,
          "Storage": 3}
other = {}
stand = \
    {
        "main":
            {
                "line1": ["Solar", "Wind", "Wind"],
                "line2": ["Battery", "Battery", "Battery"],
                "line3":
                    [
                        {
                            "MainA1":
                                [
                                    [HouseB, HouseB],
                                    Factory(5)
                                ],
                            "MainB1":
                                [
                                    [HouseA, HouseB],
                                    Factory(5)
                                ]

                        }
                    ]
            }
    }

type_cost = {
    "Hospital"
}

get_percent = lambda value: round(((20 * value) / 23) / 100, 3) if value < 23 else 0.2


def get_out_power(value: float) -> float:
    return value - value * get_percent(value)


def get_input_power(value: float) -> float:
    return value + value * get_percent(value)


def get_power_of_stand(stand_obj):
    charge = 0
    consumption = 0
    at_all = 0
    for i in stand_obj["main"]:  # Main
        line_power = 0
        if type(stand_obj["main"][i]) == list:
            for j in stand_obj["main"][i]:  # lineX
                if type(j) != dict:
                    line_power += types.get(j, 0)
                elif type(j) == dict:
                    for k in j:
                        if type(j[k]) == list:
                            for u in j[k]:
                                if type(u) == list:
                                    for y in u:
                                        line_power += types.get(y, 0)
                                else:
                                    line_power += types.get(u, 0)
                        else:
                            line_power += types.get(j[k], 0)
                        if line_power < 0:
                            line_power = -get_input_power(-line_power)
                        else:
                            line_power = get_out_power(line_power)
            if line_power < 0:
                line_power = -get_input_power(-line_power)
                consumption += line_power
            else:
                line_power = get_out_power(line_power)
                charge += line_power
            at_all += line_power

    return at_all, consumption, charge


"""
def get_cost_of_stand(stand_obj):
    at_all = 0
    for i in stand_obj["main"]:  # Main
        line_cost = 0
        if type(stand_obj["main"][i]) == list:
            for j in stand_obj["main"][i]:  # lineX
                if type(j) != dict:
                    line_power += types.get(j, 0)
                elif type(j) == dict:
                    for k in j:
                        if type(j[k]) == list:
                            for u in j[k]:
                                if type(u) == list:
                                    for y in u:
                                        line_power += types.get(y, 0)
                                else:
                                    line_power += types.get(u, 0)
                        else:
                            line_power += types.get(j[k], 0)
                        if line_power < 0:
                            line_power = -get_input_power(-line_power)
                        else:
                            line_power = get_out_power(line_power)
            if line_power < 0:
                line_power = -get_input_power(-line_power)
                consumption += line_power
            else:
                line_power = get_out_power(line_power)
                charge += line_power
            at_all += line_power
"""

a, cons, ch = get_power_of_stand(stand)
print(f"{a=}")
print(f"{cons=}")
print(f"{ch=}")
