from objects import Consumer, PowerPlant

loss = lambda value: round(((25 * value) / 30) / 100, 3) if value < 30 else 0.25
get_out_power = lambda value: value - value * loss(value)
get_input_power = lambda value: value + value * loss(value)
charge_power, discharge_power = [], []
stand = \
    {
        "main":
            {
                "line1": [{
                    "MainB1": [[PowerPlant.Battery, PowerPlant.Battery],
                               [PowerPlant.Solar, PowerPlant.Wind, PowerPlant.Solar], Consumer.Factory]
                }],
                "line2":
                    [
                        {
                            "MainA1":
                                [
                                    [Consumer.HouseA, Consumer.HouseB, Consumer.HouseB],
                                    Consumer.Factory
                                ]

                        }
                    ]
            }
    }


def get_power_of_stand(stand_obj):
    global charge_power, discharge_power
    charge = 0
    consumption = 0
    at_all = 0
    for i in stand_obj["main"]:  # Main
        line_power = 0
        if type(stand_obj["main"][i]) == list:
            for j in stand_obj["main"][i]:  # lineX
                if type(j) != dict:
                    line_power += j.charge
                elif type(j) == dict:
                    for k in j:
                        if type(j[k]) == list:
                            for u in j[k]:
                                if type(u) == list:
                                    for y in u:
                                        line_power += y.charge
                                else:
                                    line_power += u.charge
                        else:
                            line_power += j[k].charge
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


a, cons, ch = get_power_of_stand(stand)
print(f"Энергия сети: {a} МВт")
print(f"Потребление: {cons} МВт")
print(f"Зарядка: {ch} МВт")

print(get_input_power(5.5 + 5 + 5 + 5))

# 2
