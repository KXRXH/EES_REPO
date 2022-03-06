import matplotlib as plt


fig, ax = plt.subplots(2, 1)
fig.set_figwidth(20)
fig.set_figheight(10)


def normalise_num_for_str(data):
    data = round(data, 2)
    if data >= 0:
        return '+' + str(data) + '₽'
    else:
        return str(data) + '₽'


def gen_Total():
    global Total
    global delta_Total

    delta_Total = delta_Auction + delta_Consumers + delta_Generators + delta_Power_System + delta_Overload + delta_Exchange
    Total = Auction + Consumers + Generators + Power_System + Overload + Exchange


def normalise_y_data(y1, y2, k=1):
    return [k * (y1[i] + k * (y2[i])) for i in range(0, len(y1))]


def max_value_data_graph():
    global max_energy_data

    positive_value = energy_solar_data[-1] + energy_wind_data[-1] + energy_accamulator_p_data[-1]
    positive_value += energy_diesel_data[-1] + energy_exchange_p_data[-1]
    negative_value = energy_hospital_data[-1] + energy_factory_data[-1] + energy_houseA_data[-1]
    negative_value += energy_houseB_data[-1] + energy_accamulator_n_data[-1] + energy_exchange_n_data[-1]

    if positive_value > max_energy_data: max_energy_data = positive_value
    if negative_value > max_energy_data: max_energy_data = negative_value

    return max_energy_data
