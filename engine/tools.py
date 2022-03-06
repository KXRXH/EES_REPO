
# Данные по энергии
def get_received_energy():  # получено
    global energy_solar_data
    global energy_wind_data
    global energy_accamulator_p_data
    global energy_diesel_data

    energy_solar = 0
    energy_wind = 0
    energy_storage = 0

    energy_accamulator = 0
    energy_diesel = 0

    for itr in range(0, qty_solar):
        energy_solar += min(value_solar * koaf_solar_gen[itr], max_power_solar)

    for itr in range(0, qty_wind):
        if value_wind ** 3 * koaf_wind_gen[itr] > max_power_wind * 100 / max_power_percent:
            online_wind[itr] = False
        if value_wind ** 3 * koaf_wind_gen[itr] < max_power_wind * min_percent_for_resume / max_power_percent:
            online_wind[itr] = True

        if online_wind[itr]:
            energy_wind += min(value_wind ** 3 * koaf_wind_gen[itr], max_power_wind)

    for itr, mode in enumerate(delta_storage):
        if mode < 0:
            energy_storage += mode
            delta_storage[itr] = 0

    for itr, delta in enumerate(delta_accamulator):
        if delta < 0:
            energy_accamulator += delta
            delta_accamulator[itr] = 0

    for mode in power_diesel:
        energy_diesel += mode

    energy_solar_data.append(energy_solar)
    energy_wind_data.append(energy_wind)
    energy_accamulator_p_data.append(energy_storage + energy_accamulator)
    energy_diesel_data.append(energy_diesel)

    all_energy = energy_solar + energy_wind + energy_storage + energy_accamulator + energy_diesel

    return all_energy


def get_spent_energy():  # потрачено
    global energy_hospital_data
    global energy_factory_data
    global energy_houseA_data
    global energy_houseB_data
    global energy_accamulator_n_data

    energy_hospital = 0
    energy_factory = 0
    energy_houseA = 0
    energy_houseB = 0

    energy_storage = 0
    energy_accamulator = 0

    for _ in range(0, qty_hospital):
        energy_hospital += value_hospital

    for _ in range(0, qty_factory):
        energy_factory += value_factory

    for _ in range(0, qty_houseA):
        energy_houseA += value_houseA

    for _ in range(0, qty_houseB):
        energy_houseB += value_houseB

    for itr, mode in enumerate(delta_storage):
        if mode > 0:
            energy_storage += mode
            delta_storage[itr] = 0

    for itr, delta in enumerate(delta_accamulator):
        if delta > 0:
            energy_accamulator += delta
            delta_accamulator[itr] = 0

    energy_hospital_data.append(energy_hospital)
    energy_factory_data.append(energy_factory)
    energy_houseA_data.append(energy_houseA)
    energy_houseB_data.append(energy_houseB)
    energy_accamulator_n_data.append(energy_storage + energy_accamulator)

    all_spent_energy = energy_hospital + energy_factory + energy_houseA
    all_spent_energy += energy_houseB + energy_storage + energy_accamulator

    return all_spent_energy


# Оплата за генераторы
def get_money_generators():
    global delta_Generators
    global Generators
    global Power_System
    global delta_Power_System

    spent_mini_substationB = 0
    spent_mini_substationA = 0

    spent_storage = 0
    spent_solar = 0
    spent_wind = 0

    spent_diesel = 0
    spent_accamulator = 0

    if online_mini_substationB[0]:
        spent_mini_substationB += contract_mini_substationB[0]

    for cost in contract_mini_substationA:
        spent_mini_substationA += cost

    for cost in contract_storage:
        spent_storage += cost

    for cost in contract_solar:
        spent_solar += cost

    for cost in contract_wind:
        spent_wind += cost

    for connect in connected_accamulator:
        if not connect is None:
            spent_accamulator += cost_accamulator

    for itr, connect in enumerate(connected_diesel):
        if not connect is None:
            spent_diesel += cost_diesel
            spent_diesel += power_diesel[itr] * cost_MW_diesel

    all_spent_money = spent_storage + spent_solar + spent_wind

    delta_Generators = -all_spent_money
    Generators -= all_spent_money

    all_spent_money += spent_mini_substationB + spent_mini_substationA + spent_diesel + spent_accamulator

    delta_Power_System = - all_spent_money - delta_Generators
    Power_System += delta_Power_System

    return all_spent_money


# Биржа энергии между игроками
def get_bidding_players():
    return None, None


# если энергии все еще не хватает, то покупаем из внешней сети
def get_money_remains():
    global Exchange
    global delta_Exchange
    global energy_exchange_p_data
    global energy_exchange_n_data

    cost_power_instant = 0
    _balance_energy = balance_energy

    if _balance_energy < 0:
        if get_crash():
            cost_power_instant += max(0, abs(_balance_energy) - 10) * received_power_instant
        cost_power_instant += abs(_balance_energy) * received_power_instant
        energy_exchange_p_data.append(abs(_balance_energy))
        energy_exchange_n_data.append(0)
        k = -1
    else:
        if get_crash():
            cost_power_instant += max(0, abs(_balance_energy) - 10) * received_power_instant
        cost_power_instant += abs(_balance_energy) * spent_power_instant
        energy_exchange_n_data.append(abs(_balance_energy))
        energy_exchange_p_data.append(0)
        k = 1

    delta_Exchange = cost_power_instant * k
    Exchange += cost_power_instant * k

    return cost_power_instant


# Прибыль
def get_received_consumer():
    global Consumers
    global delta_Consumers

    profit_hospital = 0
    profit_factory = 0
    profit_houseA = 0
    profit_houseB = 0

    for money in contract_hospital:
        profit_hospital += money * value_hospital

    for money in contract_factory:
        profit_factory += money * value_factory

    for money in contract_houseA:
        profit_houseA += money * value_houseA

    for money in contract_houseB:
        profit_houseB += money * value_houseB

    all_profit = profit_hospital + profit_factory + profit_houseA + profit_houseB

    delta_Consumers = all_profit
    Consumers += all_profit

    return all_profit


def reset_var():
    global all_spent_money
    global all_received_money

    all_spent_money = 0  # потрачено всего за тик рублей
    all_received_money = 0  # получено всего за тик рублей
