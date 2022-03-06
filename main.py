
import random
from collections import defaultdict, namedtuple, UserList
from argparse import Namespace

import csv

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.style.use('seaborn-whitegrid')


# # Функции для констант игры

# In[2]:


def get_weather_data():
    if '.csv' in weather_data_file:
        weather_data, real_weather = get_file_weather_data()
    else:
        weather_data, real_weather = get_generated_weather_data()

    return weather_data, real_weather


def get_file_weather_data():
    first_line = True
    weather_data_array = defaultdict(set)
    real_weather_array = defaultdict(set)

    with open(weather_data_file, newline='', encoding="utf-8") as File:
        reader = csv.reader(File)
        for values_tick in reader:
            if first_line:
                first_line = False
                for _object in weather_objects:
                    weather_data_array[_object] = []
                    real_weather_array[_object] = []
                continue

            values_tick_valid = list(map(float, values_tick))
            for itr, _object in enumerate(weather_objects):
                data_tick_array = values_tick_valid[itr * count_weather_value:(itr + 1) * count_weather_value]
                real_value = data_tick_array[weather_way[itr] - 1]

                weather_data_array[_object].append(data_tick_array)
                real_weather_array[_object].append(real_value)

    return weather_data_array, real_weather_array


def get_generated_weather_data():
    return None, None


# # Константы для игры

# In[3]:


# Информация о тике
start_tick = 0
end_tick = 100
act_tick = start_tick

# Информация о погоде
weather_data_file = './630.forecasts.csv'  # файл с погодой
SEED = 1337  # затравка для генератораD)
count_weather_value = 8  # Количество разных путей данных погоды

weather_objects = ['solar', 'wind', 'hospital', 'factory', 'houseA', 'houseB']
weather_way = [random.randint(1, count_weather_value) for i in weather_objects]

print(weather_way)

weather_data, real_weather = get_weather_data()
value_wind = 0

# Информация об авариях
crash_tick = [[15, 25], [40, 60], [65, 85]]

# Бюджет
balance_money = 0  # баланс

# Работа с энергией
# Главная подстанция +
qty_substation = 1
prefix_address_substation = 'M'
contract_substation = [0]
line_substation = [[]]
path_substation = [[]]
score_then_substation = [[]]
power_then_substation = [[]]
online_substation = [True]

# Мини подстанция Б +
qty_mini_substationB = 1
prefix_address_mini_substationB = 'm'
contract_mini_substationB = [2]
line_mini_substationB = [[1]]
path_mini_substationB = [[["main", 1]]]
score_then_mini_substationB = [[]]
power_then_mini_substationB = [[]]
online_mini_substationB = [True]

# Мини подстанция А +
qty_mini_substationA = 1
prefix_address_mini_substationA = 'e'
contract_mini_substationA = [5]
line_mini_substationA = [[1]]
path_mini_substationA = [[["main", 1]]]
score_then_mini_substationA = [[]]
power_then_mini_substationA = [[]]
online_mini_substationA = [True]

# Дизель +
qty_diesel = 2
power_diesel = [0, 0]
connected_diesel = ['M1', 'm1']
max_power_diesel = 5
cost_diesel = 1
cost_MW_diesel = 4  # руб/МВт

# Аккамулятор +
qty_accamulator = 2
delta_accamulator = [0, 0]  # -x - разрядка, 0 - хранение, x - зарядка
charge_accamulator = [0, 0]  # Заряд аккамуляторов
connected_accamulator = ['M1', 'M1']
max_power_accamulator = 50
max_exchange_power_accamulator = 10  # МВт/тик
cost_accamulator = 5

# Накопитель +
qty_storage = 1
charge_storage = [0]
delta_storage = [0]
prefix_address_storage = 't'
contract_storage = [5]
line_storage = [[1]]
path_storage = [[["main", 1]]]
score_then_storage = [[]]
power_then_storage = [[]]
charge_then_storage = [[]]
online_storage = [True]
max_power_storage = 100
max_exchange_power_storage = 15  # МВт/тик

# Солнечка +
qty_solar = 1
prefix_address_solar = 's'
contract_solar = [10]
line_solar = [[1]]
path_solar = [[["main", 1]]]

score_then_solar = [[] for _ in range(0, qty_solar)]
power_then_solar = [[] for _ in range(0, qty_solar)]
online_solar = [True for _ in range(0, qty_solar)]
max_power_solar = 15
koaf_solar_gen = [0.7 + random.uniform(-0.1, 0.1) for _ in range(0, qty_solar)]

# Ветряк +
qty_wind = 1
prefix_address_wind = 'a'
contract_wind = [5]
line_wind = [[1]]
path_wind = [[["main", 1]]]

score_then_wind = [[] for _ in range(0, qty_wind)]
power_then_wind = [[] for _ in range(0, qty_wind)]
online_wind = [True for _ in range(0, qty_wind)]
max_power_wind = 15
max_power_percent = 75  # процент от ветра, с которого на ветряке 15МВт
min_percent_for_resume = 62.5  # процент от ветра, с которого ветряк выходит из режима защиты
koaf_wind_gen = [0.011 + random.uniform(-0.004, 0.004) for _ in range(0, qty_wind)]

from set_clients import *


# Рынок мгновенной мощности
spent_power_instant = 1  # руб/МВт
received_power_instant = 10  # руб/МВт

# Рынок игроков
trade_players = 0

# Графики
Auction = -100
Consumers = 0
Generators = 0
Power_System = 0
Overload = 0
Exchange = 0
Total = 0

delta_Auction = 0
delta_Consumers = 0
delta_Generators = 0
delta_Power_System = 0
delta_Overload = 0
delta_Exchange = 0
delta_Total = 0

data_actions = []

energy_solar_data = [0]
energy_wind_data = [0]
energy_accamulator_p_data = [0]
energy_diesel_data = [0]

energy_hospital_data = [0]
energy_factory_data = [0]
energy_houseA_data = [0]
energy_houseB_data = [0]
energy_accamulator_n_data = [0]

energy_exchange_p_data = [0]
energy_exchange_n_data = [0]

max_energy_data = 0.01

# Var for core_Game
value_solar = 0
value_wind = 0
value_hospital = 0
value_factory = 0
value_houseA = 0
value_houseB = 0
flag_crash = 0
received_energy = 0
spent_energy = 0
balance_energy = 0
spent_money_generators = 0
energy_player = 0
money_player = 0
all_spent_money = 0
all_received_money = 0

### Контракты


# # Анимация графиков

# In[4]:


fig, ax = plt.subplots(2, 1)
fig.set_figwidth(20)
fig.set_figheight(10)


def normalise_num_for_str(data):
    data = round(data, 2)
    if data >= 0:
        return '+' + str(data) + 'Р'
    else:
        return str(data) + 'Р'


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


# # Функции для ядра

# In[5]:


# Погода
def get_solar():
    value_solar = real_weather['solar'][act_tick]
    return value_solar


def get_wind():
    value_wind = real_weather['wind'][act_tick]
    return value_wind


def get_hospital():
    value_hospital = real_weather['hospital'][act_tick]
    return value_hospital


def get_factory():
    value_factory = real_weather['factory'][act_tick]
    return value_factory


def get_houseA():
    value_houseA = real_weather['houseA'][act_tick]
    return value_houseA


def get_houseB():
    value_houseB = real_weather['houseB'][act_tick]
    return value_houseB


# Авария
def get_crash():
    value_crash = False
    for start_crash, end_crash in crash_tick:
        if start_crash <= act_tick < end_crash:
            value_crash = True

    return value_crash


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


# # Функции для действий игрока

# In[6]:


def get_objects():
    global score_then_substation
    global power_then_substation
    global score_then_mini_substationB
    global power_then_mini_substationB
    global score_then_mini_substationA
    global power_then_mini_substationA
    global score_then_storage
    global power_then_storage
    global charge_then_storage
    global score_then_solar
    global power_then_solar
    global score_then_wind
    global power_then_wind
    global score_then_hospital
    global power_then_hospital
    global score_then_factory
    global power_then_factory
    global score_then_houseA
    global power_then_houseA
    global score_then_houseB
    global power_then_houseB

    data_obj = []
    id_itr = 1

    # Главная подстанция
    address_itr = 1
    for itr in range(0, qty_substation):
        address = prefix_address_substation + hex(address_itr)[2:]
        contract = contract_substation[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        modules = []

        for itr_accamulator, connect in enumerate(connected_accamulator):
            if address == connect:
                score_now_loss += cost_accamulator
                modules.append(
                    {"delta": delta_accamulator[itr_accamulator], "charge": charge_accamulator[itr_accamulator],
                     "type": "cell"})

        for itr_diesel, connect in enumerate(connected_diesel):
            if address == connect:
                score_now_loss += cost_diesel
                score_now_loss += power_diesel[itr_diesel] * cost_MW_diesel
                power_now_generated += power_diesel[itr_diesel]
                modules.append({"power": power_diesel[itr_diesel], "type": "diesel"})

        data_obj.append(
            {
                "id": ["main", id_itr],
                "address": address,
                "contract": contract,
                "line": line_substation[itr],
                "path": path_substation[itr],
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_substation[itr].copy()},
                "power": {"now": {"online": online_substation[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_substation[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "main"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_substation[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_substation[itr].append(
            {"online": online_substation[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Мини подстанция Б
    address_itr = 1
    for itr in range(0, qty_mini_substationB):
        address = prefix_address_mini_substationB + hex(address_itr)[2:]
        contract = contract_mini_substationB[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_mini_substationB[itr])):
            path.append([{"line": line_mini_substationB[itr][itr_line], "id": path_mini_substationB[itr][itr_line]}])

        score_now_loss += contract

        for itr_accamulator, connect in enumerate(connected_accamulator):
            if address == connect:
                score_now_loss += cost_accamulator
                modules.append(
                    {"delta": delta_accamulator[itr_accamulator], "charge": charge_accamulator[itr_accamulator],
                     "type": "cell"})

        for itr_diesel, connect in enumerate(connected_diesel):
            if address == connect:
                score_now_loss += cost_diesel
                score_now_loss += power_diesel[itr_diesel] * cost_MW_diesel
                power_now_generated += power_diesel[itr_diesel]
                modules.append({"power": power_diesel[itr_diesel], "type": "diesel"})

        data_obj.append(
            {
                "id": ["miniB", id_itr],
                "address": address,
                "contract": contract,
                "line": line_mini_substationB[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_mini_substationB[itr].copy()},
                "power": {"now": {"online": online_mini_substationB[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_mini_substationB[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "miniB"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_mini_substationB[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_mini_substationB[itr].append(
            {"online": online_mini_substationB[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Мини подстанция А
    address_itr = 1
    for itr in range(0, qty_mini_substationA):
        address = prefix_address_mini_substationA + hex(address_itr)[2:]
        contract = contract_mini_substationA[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_mini_substationA[itr])):
            path.append([{"line": line_mini_substationA[itr][itr_line], "id": path_mini_substationA[itr][itr_line]}])

        score_now_loss += contract

        for itr_accamulator, connect in enumerate(connected_accamulator):
            if address == connect:
                score_now_loss += cost_accamulator
                modules.append(
                    {"delta": delta_accamulator[itr_accamulator], "charge": charge_accamulator[itr_accamulator],
                     "type": "cell"})

        for itr_diesel, connect in enumerate(connected_diesel):
            if address == connect:
                score_now_loss += cost_diesel
                score_now_loss += power_diesel[itr_diesel] * cost_MW_diesel
                power_now_generated += power_diesel[itr_diesel]
                modules.append({"power": power_diesel[itr_diesel], "type": "diesel"})

        data_obj.append(
            {
                "id": ["miniA", id_itr],
                "address": address,
                "contract": contract,
                "line": line_mini_substationA[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_mini_substationA[itr].copy()},
                "power": {"now": {"online": online_mini_substationA[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_mini_substationA[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "miniA"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_mini_substationA[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_mini_substationA[itr].append(
            {"online": online_mini_substationA[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Накопитель
    address_itr = 1
    for itr in range(0, qty_storage):
        address = prefix_address_storage + hex(address_itr)[2:]
        contract = contract_storage[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_storage[itr])):
            path.append([{"line": line_storage[itr][itr_line], "id": path_storage[itr][itr_line]}])

        score_now_loss += contract

        if delta_storage[itr] < 0:
            power_now_generated += delta_storage[itr]

        if delta_storage[itr] > 0:
            power_now_consumed += delta_storage[itr]

        data_obj.append(
            {
                "id": ["storage", id_itr],
                "address": address,
                "contract": contract,
                "line": line_storage[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_storage[itr].copy()},
                "power": {"now": {"online": online_storage[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_storage[itr].copy()},
                "charge": {"now": charge_storage[itr],
                           "then": charge_then_storage[itr].copy()},
                "modules": modules,
                "class": "storage"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_storage[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_storage[itr].append(
            {"online": online_storage[itr], "consumed": power_now_consumed, "generated": power_now_generated})
        charge_then_storage[itr].append(charge_storage[itr])

    # Солнечка
    address_itr = 1
    for itr in range(0, qty_solar):
        address = prefix_address_solar + hex(address_itr)[2:]
        contract = contract_solar[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_solar[itr])):
            path.append([{"line": line_solar[itr][itr_line], "id": path_solar[itr][itr_line]}])

        score_now_loss += contract

        power_now_generated += min(value_solar * koaf_solar_gen[itr], max_power_solar)

        data_obj.append(
            {
                "id": ["solar", id_itr],
                "address": address,
                "contract": contract,
                "line": line_solar[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_solar[itr].copy()},
                "power": {"now": {"online": online_solar[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_solar[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "solar"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_solar[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_solar[itr].append(
            {"online": online_solar[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Ветряк
    address_itr = 1
    for itr in range(0, qty_wind):
        address = prefix_address_wind + hex(address_itr)[2:]
        contract = contract_wind[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_wind[itr])):
            path.append([{"line": line_wind[itr][itr_line], "id": path_wind[itr][itr_line]}])

        score_now_loss += contract

        if online_wind[itr]:
            power_now_generated += min(value_wind ** 3 * koaf_wind_gen[itr], max_power_wind)

        data_obj.append(
            {
                "id": ["wind", id_itr],
                "address": address,
                "contract": contract,
                "line": line_wind[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_wind[itr].copy()},
                "power": {"now": {"online": online_wind[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_wind[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "wind"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_wind[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_wind[itr].append(
            {"online": online_wind[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Больницы
    address_itr = 1
    for itr in range(0, qty_hospital):
        address = prefix_address_hospital + hex(address_itr)[2:]
        contract = contract_hospital[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_hospital[itr])):
            path.append([{"line": line_hospital[itr][itr_line], "id": path_hospital[itr][itr_line]}])

        power_now_consumed += value_hospital

        score_now_income += contract_hospital[itr] * value_hospital

        data_obj.append(
            {
                "id": ["hospital", id_itr],
                "address": address,
                "contract": contract,
                "line": line_hospital[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_hospital[itr].copy()},
                "power": {"now": {"online": online_hospital[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_hospital[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "hospital"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_hospital[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_hospital[itr].append(
            {"online": online_hospital[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Заводы
    address_itr = 1
    for itr in range(0, qty_factory):
        address = prefix_address_factory + hex(address_itr)[2:]
        contract = contract_factory[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_factory[itr])):
            path.append([{"line": line_factory[itr][itr_line], "id": path_factory[itr][itr_line]}])

        power_now_consumed += value_factory

        score_now_income += contract_factory[itr] * value_factory

        data_obj.append(
            {
                "id": ["factory", id_itr],
                "address": address,
                "contract": contract,
                "line": line_factory[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_factory[itr].copy()},
                "power": {"now": {"online": online_factory[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_factory[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "factory"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_factory[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_factory[itr].append(
            {"online": online_factory[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Дом А
    address_itr = 1
    for itr in range(0, qty_houseA):
        address = prefix_address_houseA + hex(address_itr)[2:]
        contract = contract_houseA[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_houseA[itr])):
            path.append([{"line": line_houseA[itr][itr_line], "id": path_houseA[itr][itr_line]}])

        power_now_consumed += value_houseA

        score_now_income += contract_houseA[itr] * value_houseA

        data_obj.append(
            {
                "id": ["houseA", id_itr],
                "address": address,
                "contract": contract,
                "line": line_houseA[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_houseA[itr].copy()},
                "power": {"now": {"online": online_houseA[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_houseA[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "houseA"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_houseA[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_houseA[itr].append(
            {"online": online_houseA[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Дом Б
    address_itr = 1
    for itr in range(0, qty_houseB):
        address = prefix_address_houseB + hex(address_itr)[2:]
        contract = contract_houseB[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_houseB[itr])):
            path.append([{"line": line_houseB[itr][itr_line], "id": path_houseB[itr][itr_line]}])

        power_now_consumed += value_houseB

        score_now_income += contract_houseB[itr] * value_houseB

        data_obj.append(
            {
                "id": ["houseB", id_itr],
                "address": address,
                "contract": contract,
                "line": line_houseB[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_houseB[itr].copy()},
                "power": {"now": {"online": online_houseB[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_houseB[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "houseB"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_houseB[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_houseB[itr].append(
            {"online": online_houseB[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    return data_obj


# In[7]:


# act_tick = 26

__all__ = [
    "Powerstand", "Object", "Line", "Powerline",
    "Historic", "Receipt", "ExchangeReceipt",
    "Diesel", "Cell",
]

obj_types = [
    "main"  # подстанции
    "miniA",  # мини-подстанции А
    "miniB",  # мини-подстанции Б
    "solar",  # солнечные электростанции
    "wind",  # ветровые электростанции
    "houseA",  # дом А
    "houseB",  # дом Б
    "factory",  # больницы
    "hospital",  # заводы
    "storage",  # накопители
]

station_types = {"miniA", "miniB", "main"}
storage_types = {"miniA", "storage", "main"}

spent_obj = ['miniB', 'miniA', 'storage', 'solar', 'wind', 'main']

Historic = namedtuple("Historic", ("now", "then"))
Historic.__str__ = lambda self: f"{self.now} (было {safe_tail(self.then)})"

Receipt = namedtuple("Receipt", ("income", "loss"))
Receipt.__str__ = lambda self: f"(+{self.income} Р, -{self.loss} Р)"
Receipt.__add__ = lambda self, x: __add_receipt(self, x)


def __add_receipt(self, x):
    if isinstance(x, Receipt):
        return Receipt(self.income + x.income, self.loss + x.loss)
    raise TypeError(x)


Data_Weather = namedtuple("Data_Weather", ("sun", "wind", "hospital", "factory", "houseA", "houseB"))

Total_Power = namedtuple("Total_Power", ("generated", "consumed", "external", "losses"))

Object = namedtuple("Object", ("id", "type", "contract", "address", "path",
                               "score", "power", "charge", "modules"))
Object.__str__ = lambda self: f"{self.type} ({self.power.now}, {self.score.now})"

ExchangeReceipt = namedtuple("ExchangeReceipt", ("source", "flux", "price"))
ExchangeReceipt.__str__ = lambda \
    self: f"{pretty_source(self.source)} "                  f"({self.flux:.2f} МВт, {self.price:.2f} Р/МВт)"

Power = namedtuple("Line", ("generated", "consumed", "online"))
Power.__str__ = lambda \
    self: f"{pretty_bool(self.online)} "                              f"(+{self.generated} МВт⋅ч -{self.consumed} МВт⋅ч)"
Power.total = lambda self: self.generated - self.consumed

Line = namedtuple("Line", ("id", "line"))
Line.__str__ = lambda self: f"{self.id}-{self.line}"

Powerline = namedtuple("Powerline", ("location", "online", "upflow", "downflow", "losses"))
Powerline.__str__ = lambda self: f"{self.location} ({pretty_bool(self.online)})"

Diesel = namedtuple("Diesel", ("power",))
Diesel.__str__ = lambda self: f"Дизель ({self.power})"

Cell = namedtuple("Cell", ("charge", "delta"))
Cell.__str__ = lambda self: f"Аккумулятор ({self.charge})"


def pretty_bool(v):
    return 'вкл.' if v else 'выкл.'


def pretty_agent(ag):
    return f'{ag["place"]}.{ag["player"]}'


def pretty_source(ag):
    if ag == "exchange":
        return 'контракт c оператором'
    elif ag == 'overload':
        return 'штраф за перегрузку'
    return f'контракт с игроком {ag["place"]}.{ag["player"]}'


def unsource(src):
    tag = src["esType"]
    if tag == "player":
        return src["owner"]
    return tag


def safe_tail(data):
    if len(data):
        return None
    return data[-1]


def safe_head(data):
    if len(data):
        return None
    return data[0]


def make_module(m):
    if m["type"] == "cell":
        return Cell(m["charge"], m["delta"])
    if m["type"] == "diesel":
        return Diesel(m["power"])
    raise NotImplementedError("неизвестный модуль")


def make_historic(d, fn):
    return Historic(fn(**d["now"]), [fn(**x) for x in d["then"][::-1]])


def make_historic_(d, fn):
    return Historic(fn(d["now"]), [fn(x) for x in d["then"][::-1]])


def get_fails():
    fails = []
    for start_crash, end_crash in crash_tick + [[end_tick, end_tick]]:
        fails += [False] * (start_crash - len(fails))
        fails += [True] * (end_crash - start_crash)
    return fails


def make_object(d, stations, storages):
    obj = Object(
        id=d["id"],
        address=tuple(d["address"]),
        contract=d["contract"],
        path=tuple(tuple(Line(tuple(l["id"]), l["line"]) for l in a) for a in d["path"]),
        score=make_historic(d["score"], Receipt),
        power=make_historic(d["power"], Power),
        charge=make_historic_(d["charge"], float),
        modules=tuple(make_module(m) for m in d["modules"]),
        type=d["class"]
    )
    if obj.type in station_types:
        stations[obj.address] = obj.id
    if obj.type in storage_types:
        storages[obj.address] = obj.id
    return obj


def make_powerline(d):
    d["location"] = tuple(Line(tuple(l["id"]), l["line"]) for l in d["location"])
    del d["owner"]
    return Powerline(**d)


def from_chipping(d):
    return Historic(d["current"], d["done"][::-1])


def make_forecasts(d):
    arr = [[] for _ in range(0, len(d[0]))]
    for i in range(0, len(d)):
        for j in range(0, len(d[0])):
            arr[j].append(d[i][j])
    return arr


class Powerstand:
    GRAPH_COUNT = 4

    def __init__(self, data):

        self.__orders = orders = []
        self.__station_index = dict()
        self.__storage_index = dict()
        self.__user_data = [[] for _ in range(self.GRAPH_COUNT)]

        self.tick = act_tick
        self.gameLength = end_tick - start_tick
        self.scoreDelta = all_received_money - all_spent_money

        self.fails = get_fails()

        self.sun = Historic(real_weather['solar'][act_tick], real_weather['solar'][0:act_tick])
        self.wind = Historic(real_weather['wind'][act_tick], real_weather['wind'][0:act_tick])
        self.hospital = Historic(real_weather['hospital'][act_tick], real_weather['hospital'][0:act_tick])
        self.factory = Historic(real_weather['factory'][act_tick], real_weather['factory'][0:act_tick])
        self.houseA = Historic(real_weather['houseA'][act_tick], real_weather['houseA'][0:act_tick])
        self.houseB = Historic(real_weather['houseB'][act_tick], real_weather['houseB'][0:act_tick])

        self.forecasts = Data_Weather(make_forecasts(weather_data['solar']),
                                      make_forecasts(weather_data['wind']),
                                      make_forecasts(weather_data['hospital']),
                                      make_forecasts(weather_data['factory']),
                                      make_forecasts(weather_data['houseA']),
                                      make_forecasts(weather_data['houseB']))

        self.objs = get_objects()
        self.objects = [make_object(obj, self.__station_index, self.__storage_index)
                        for obj in self.objs]

        self.total_power = Total_Power(received_energy,
                                       spent_energy,
                                       energy_player,  # полученно с биржи
                                       0)  # потери

        self.orders = Namespace(
            diesel=lambda address, power: self.__set_diesel(address, power),
            charge=lambda address, power: self.__change_cell(address, power, True),
            discharge=lambda address, power: self.__change_cell(address, power, False),
            sell=lambda amount, price: self.__outstanding(amount, price, True),
            buy=lambda amount, price: self.__outstanding(amount, price, False),
            line_on=lambda address, line: self.__set_line(address, line, True),
            line_off=lambda address, line: self.__set_line(address, line, False),
            add_graph=lambda idx, values: self.__add_graph(idx, values),
            # debug functions
            get=lambda: orders.copy(),
            humanize=lambda: self.__humanize_orders(),
        )

    def __check_address(self, address):
        return address in self.__station_index

    def __set_diesel(self, address, power):
        try:
            power = float(power)
            if power < 0:
                raise ("Отрицательное значение энергии на дизеле. Приказ не принят.")
        except ValueError:
            raise ("Для приказа на дизель нужен float-совместимый тип. Приказ не принят.")
        if not self.__check_address(address):
            raise ("Такой подстанции не существует. Приказ не принят.")

        global power_diesel
        local_power = power
        for itr, connect in enumerate(connected_diesel):
            if address == tuple(connect):
                power_diesel[itr] = min(local_power, max_power_diesel)
                local_power -= power_diesel[itr]
        self.__orders.append({"orderT": "diesel", "address": ''.join(address), "power": power - local_power})

    def __change_cell(self, address, power, charge=True):
        try:
            power = float(power)
            if power < 0:
                raise ("Отрицательное значение энергии в приказе на аккумулятор. Приказ не принят.")
        except ValueError:
            raise ("Для приказа на аккумулятор нужен float-совместимый тип. Приказ не принят.")
        if address not in list(self.__storage_index):
            raise ("Такого накопителя/подстанции не существует. Приказ не принят.")

        order = "charge" if charge else "discharge"
        global delta_accamulator
        global charge_accamulator
        global delta_storage
        global charge_storage
        local_power = power
        if prefix_address_storage in address:
            itr = 0
            for obj in self.objects:
                if prefix_address_storage in obj.address: itr += 1
                if obj.address != address: continue
                itr -= 1
                if charge:
                    delta_storage[itr] = min(local_power, max_power_storage - charge_storage[itr],
                                             max_exchange_power_storage)
                    charge_storage[itr] += delta_storage[itr]
                    local_power -= delta_storage[itr]
                else:
                    delta_storage[itr] = -1 * min(local_power, charge_storage[itr], max_exchange_power_storage)
                    charge_storage[itr] += delta_storage[itr]
                    local_power -= -delta_storage[itr]
            if itr == len(self.objects): raise ("Такого накопителя/подстанции не существует. Приказ не принят.")
        else:
            for itr, connect in enumerate(connected_accamulator):
                if address == tuple(connect):
                    if charge:
                        delta_accamulator[itr] = min(local_power, max_power_accamulator - charge_accamulator[itr],
                                                     max_exchange_power_accamulator)
                        charge_accamulator[itr] += delta_accamulator[itr]
                        local_power -= delta_accamulator[itr]
                    else:
                        delta_accamulator[itr] = -1 * min(local_power, charge_accamulator[itr],
                                                          max_exchange_power_accamulator)
                        charge_accamulator[itr] += delta_accamulator[itr]
                        local_power -= -delta_accamulator[itr]
        self.__orders.append({"orderT": order, "address": ''.join(address), "power": power - local_power})

    def __outstanding(self, amount, price, sell=True):
        pass

    def __set_line(self, address, line, value=True):
        pass

    def __add_graph(self, idx, values):
        pass

    def get_orders(self):
        return self.__humanize_orders()

    def __humanize_orders(self):
        global data_actions
        data_actions = [self.humanize_order(o) for o in self.__orders]

        return data_actions

    @staticmethod
    def humanize_order(order):
        type = order["orderT"]
        if type == "lineOn":
            return f"включение линии {order['line']['line']} "                    f"на подстанции {order['address']}"
        if type == "lineOff":
            return f"выключение линии {order['line']['line']} "                    f"на подстанции {order['address']}"
        if type == "sell":
            return f"заявка на продажу {order['amount']:.2f} МВт⋅ч за {order['price']:.2f} Р"
        if type == "buy":
            return f"заявка на покупку {order['amount']:.2f} МВт⋅ч за {order['price']:.2f} Р"
        if type == "diesel":
            return f"установка мощности дизелей {order['address']} в {order['power']:.2f} МВт"
        if type == "charge":
            return f"зарядка аккумуляторов {order['address']} на {order['power']:.2f} МВт⋅ч"
        if type == "discharge":
            return f"разрядка аккумуляторов {order['address']} на {order['power']:.2f} МВт⋅ч"
        if type == "userData":
            return "отправить графики"
        else:
            return "неизвестный приказ"

    def save_and_exit(self):
        self.orders.humanize
        return 'Конец выполнения'

    def get_user_data(self):
        return 'Конец выполнения'

    class orders:
        def get(self):
            return 'Конец выполнения'

        def humanize(self):
            return 'Конец выполнения'


class ips():
    def init() -> Powerstand:
        return Powerstand(None)

    def init_test() -> Powerstand:
        return from_json(stub_input)

    def from_json(string) -> Powerstand:
        return Powerstand(None)

    def from_file(filename) -> Powerstand:
        return Powerstand(None)

    def from_log(filename, step) -> Powerstand:
        return Powerstand(None)


# # Код игрока

# In[8]:


flag_Sun = False
flag_Hospital = False
flag_Factory = False
flag_HouseA = False
flag_HouseB = False

waySun = -1
wayWind = -1
wayHospital = -1
wayFactory = -1
wayHouseA = -1
wayHouseB = -1

wind_way = list(range(0, 8))
sun_k = []


def player_actions():
    global flag_Sun
    global flag_Hospital
    global flag_Factory
    global flag_HouseA
    global flag_HouseB

    global waySun
    global wayWind
    global wayHospital
    global wayFactory
    global wayHouseA
    global wayHouseB

    global wind_way
    global sun_k

    from collections import defaultdict
    psm = ips.init()

    '''
    {
        waySun: 1,
        wayWind: [7],
        wayHospital: 2,
        wayFactory: 3,
        wayHouseA: 4,
        wayHouseB: 6
    }

    если у нас отключается верряк, то ставим дизель <--- нужно написать
    генерация ветра <--- написать
    записывать и читать переменные в файл
    продажа на бирже
    выгрузку из накопителей недостающей энергии
    '''

    if psm.tick != 0:
        with open('./vars', 'r') as f:
            input_data = eval(f.readline())

        flag_Sun = input_data['flag_Sun']
        flag_Hospital = input_data['flag_Hospital']
        flag_Factory = input_data['flag_Factory']
        flag_HouseA = input_data['flag_HouseA']
        flag_HouseB = input_data['flag_HouseB']

        waySun = input_data['waySun']
        wayWind = input_data['wayWind']
        wayHospital = input_data['wayHospital']
        wayFactory = input_data['wayFactory']
        wayHouseA = input_data['wayHouseA']
        wayHouseB = input_data['wayHouseB']

        wind_way = input_data['wind_way']
        wind_k = input_data['wind_k']
        sun_k = input_data['sun_k']
    else:
        flag_Sun = False
        flag_Hospital = False
        flag_Factory = False
        flag_HouseA = False
        flag_HouseB = False

        waySun = -1
        wayWind = -1
        wayHospital = -1
        wayFactory = -1
        wayHouseA = -1
        wayHouseB = -1

        wind_way = list(range(0, 8))
        wind_k = []
        sun_k = []

    loss = lambda power: power * 20 / 100 if power > 23 else power * (power * 20 / 23) / 100

    need_energy_next = 0
    need_energy_substation = defaultdict(set)

    gen_energy_next = 0
    gen_energy_substation = defaultdict(set)

    itr_sun = -1
    itr_wind = -1

    if psm.sun.now != 0 and not flag_Sun:
        for i in range(0, 8):
            if psm.forecasts.sun[i][psm.tick] == psm.sun.now:
                waySun = i
                flag_Sun = True
                break
        for obj in psm.objects:
            if obj.type == 'solar':
                sun_k.append(obj.power.now.generated / psm.sun.now)
    # gen_n = weather_s * sun_k[n]

    for i, way in enumerate(wind_way):
        if psm.forecasts.wind[way][psm.tick] != psm.wind.now:
            wind_way.pop(i)
    wayWind = wind_way[0]

    for obj in psm.objects:
        # потребление
        if obj.type == 'hospital':
            if not flag_Hospital:
                for i in range(0, 8):
                    if psm.forecasts.hospital[i][psm.tick] == obj.power.now.consumed:
                        wayHospital = i
                        flag_Hospital = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                need_energy_substation[path].append(psm.forecasts.hospital[wayHospital][psm.tick + 1] / len(obj.path))

        if obj.type == 'factory':
            if not flag_Factory:
                for i in range(0, 8):
                    if psm.forecasts.factory[i][psm.tick] == obj.power.now.consumed:
                        wayFactory = i
                        flag_Factory = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                need_energy_substation[path].append(psm.forecasts.factory[wayFactory][psm.tick + 1] / len(obj.path))

        if obj.type == 'houseA':
            if not flag_HouseA:
                for i in range(0, 8):
                    if psm.forecasts.houseA[i][psm.tick] == obj.power.now.consumed:
                        wayHouseA = i
                        flag_HouseA = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                need_energy_substation[path].append(psm.forecasts.houseA[wayHouseA][psm.tick + 1])

        if obj.type == 'houseB':
            if not flag_HouseB:
                for i in range(0, 8):
                    if psm.forecasts.houseB[i][psm.tick] == obj.power.now.consumed:
                        wayHouseB = i
                        flag_HouseB = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                need_energy_substation[path].append(psm.forecasts.houseB[wayHouseB][psm.tick + 1])

        # генерация
        if obj.type == 'solar':
            itr_sun += 1
            for path in obj.path:
                if not path in list(gen_energy_substation):
                    gen_energy_substation[path] = []
                if flag_Sun:
                    gen_energy_substation[path].append(sun_k[itr_sun] * psm.forecasts.sun[max(waySun, 0)][psm.tick + 1])

    #         if obj.type == 'wind':
    #             itr_wind += 1
    #             for path in obj.path:
    #                 if not path in list(gen_energy_substation):
    #                     gen_energy_substation[path] = []
    #                 gen_energy_substation[path].append( * psm.forecasts.wind[max(wayWind, 0)][psm.tick + 1])

    for address_powerarea in list(need_energy_substation):
        energy_powerarea = 0
        for power in need_energy_substation[address_powerarea]:
            energy_powerarea += power
        energy_powerarea += loss(energy_powerarea)
        need_energy_next += energy_powerarea + 3  # условно

    print(need_energy_next)

    '''
    написали:
    1) потребление зданий
    2) выработка солнца
    3) потери учитываем
    4) предсказали колонку погоды и потребеления
    5) открыли файлик)))
    '''

    output_data = {
        'flag_Sun': flag_Sun,
        'flag_Hospital': flag_Hospital,
        'flag_Factory': flag_Factory,
        'flag_HouseA': flag_HouseA,
        'flag_HouseB': flag_HouseB,

        'waySun': waySun,
        'wayWind': wayWind,
        'wayHospital': wayHospital,
        'wayFactory': wayFactory,
        'wayHouseA': wayHouseA,
        'wayHouseB': wayHouseB,

        'wind_way': wind_way,
        'wind_k': wind_k,
        'sun_k': sun_k
    }
    with open('./vars', 'w') as f:
        f.write(str(output_data))

    psm.save_and_exit()


# # Ядро игры

# In[9]:


def game_play(i):
    global value_solar
    global value_wind
    global value_hospital
    global value_factory
    global value_houseA
    global value_houseB
    global flag_crash
    global received_energy
    global spent_energy
    global balance_energy
    global spent_money_generators
    global energy_player
    global money_player
    global all_spent_money
    global all_received_money
    global act_tick
    global balance_money

    # Обнуление переменных
    reset_var()

    # Погода
    value_solar = get_solar()
    value_wind = get_wind()
    value_hospital = get_hospital()
    value_factory = get_factory()
    value_houseA = get_houseA()
    value_houseB = get_houseB()

    # Авария
    flag_crash = get_crash()

    # Данные по энергии
    received_energy = get_received_energy()  # получено
    spent_energy = get_spent_energy()  # потрачено
    balance_energy = received_energy - spent_energy  # баланс

    # Оплата за генераторы
    spent_money_generators = get_money_generators()
    all_spent_money += spent_money_generators

    # Биржа энергии между игроками
    energy_player, money_player = 0, 0
    if trade_players != 0 and False:  # не реализовано!!!!!!!!!!!!!
        energy_player, money_player = get_bidding_players()
        balance_energy += energy_player
        if money_player < 0:
            all_spent_money -= money_player
        else:
            all_received_money += money_player

    # Прибыль
    received_consumer = get_received_consumer()
    all_received_money += received_consumer

    print('\n--------------------------------------------------------------------------')
    print('Тик:', act_tick)

    print('\nВывод игрока:')

    # Действия игрока (на следующий тик)
    player_actions()

    # если энергия != 0, то продаем во внешнюю сеть
    balance_money += all_received_money - all_spent_money
    reset_var()
    if balance_energy < 0:
        spent_to_external_network = get_money_remains()
        all_spent_money += spent_to_external_network
    else:
        received_from_external_network = get_money_remains()
        all_received_money += received_from_external_network

    # Баланс денег
    balance_money += all_received_money - all_spent_money

    # Графики
    if act_tick <= end_tick:
        gen_Total()
    else:
        ani.event_source.stop()

    ax[0].clear()
    ax[1].clear()

    ax[0].set_xlim(0, 101)
    ax[1].set_xlim(1, 100)

    # Настройка 1 графика
    ax[0].title.set_text('Генерация/потребление энергии:')
    ax[0].title.set_fontsize(30)
    ax[0].title.set_fontweight('bold')

    ax[0].spines['right'].set_visible(False)
    ax[0].spines['bottom'].set_visible(False)
    ax[0].spines['top'].set_visible(False)

    ax[0].grid()

    ax[0].spines['left'].set_linewidth(2)
    ax[0].spines['left'].set_color('black')

    main_axis_x = list(range(0, 101))
    main_axis_y = [0 for _ in range(0, 101)]
    ax[0].plot(main_axis_x, main_axis_y, color='black', linewidth=2)

    #     # Рисование 1 графика
    y_solar = normalise_y_data(energy_solar_data, main_axis_y)
    ax[0].fill_between(main_axis_x[:act_tick + 2], y_solar, main_axis_y[:act_tick + 2], facecolor='#FFEC14')
    y_wind = normalise_y_data(energy_wind_data, y_solar)
    ax[0].fill_between(main_axis_x[:act_tick + 2], y_wind, y_solar, facecolor='#A3FFFF')
    y_accamulator_p = normalise_y_data(energy_accamulator_p_data, y_wind)
    ax[0].fill_between(main_axis_x[:act_tick + 2], y_accamulator_p, y_wind, facecolor='#3737FF')
    y_diesel = normalise_y_data(energy_diesel_data, y_accamulator_p)
    ax[0].fill_between(main_axis_x[:act_tick + 2], y_diesel, y_accamulator_p, facecolor='#9C9C9C')
    y_exchange_p = normalise_y_data(energy_exchange_p_data, y_diesel)
    ax[0].fill_between(main_axis_x[:act_tick + 2], y_exchange_p, y_diesel, facecolor='#000000')

    y_hospital = normalise_y_data(energy_hospital_data, main_axis_y, k=-1)
    ax[0].fill_between(main_axis_x[:act_tick + 2], y_hospital, main_axis_y[:act_tick + 2], facecolor='#FF9494')
    y_factory = normalise_y_data(energy_factory_data, y_hospital, k=-1)
    ax[0].fill_between(main_axis_x[:act_tick + 2], y_factory, y_hospital, facecolor='#FFFDBB')
    y_houseA = normalise_y_data(energy_houseA_data, y_factory, k=-1)
    ax[0].fill_between(main_axis_x[:act_tick + 2], y_houseA, y_factory, facecolor='#9DC941')
    y_houseB = normalise_y_data(energy_houseB_data, y_houseA, k=-1)
    ax[0].fill_between(main_axis_x[:act_tick + 2], y_houseB, y_houseA, facecolor='#BFE471')
    y_accamulator_n = normalise_y_data(energy_accamulator_n_data, y_houseB, k=-1)
    ax[0].fill_between(main_axis_x[:act_tick + 2], y_accamulator_n, y_houseB, facecolor='#3737FF')
    y_exchange_n = normalise_y_data(energy_exchange_n_data, y_accamulator_n, k=-1)
    ax[0].fill_between(main_axis_x[:act_tick + 2], y_exchange_n, y_accamulator_n, facecolor='#000000')

    for start, end in crash_tick:
        ax[0].plot(range(start + 1, end + 1), [0 for _ in range(start + 1, end + 1)], color='red', linestyle=' ',
                   marker='o')

    # Донастройка 1 графика
    y_lim_max = max(abs(ax[0].get_ylim()[0]), abs(ax[0].get_ylim()[1]))
    ax[0].set_ylim(-y_lim_max, y_lim_max)

    ax[0].set_xticks([])
    ax[0].set_yticks([-max_value_data_graph(), max_value_data_graph()])
    ax[0].tick_params(labelsize=14)

    # Настройка 2 графика
    ax[1].title.set_text('Данные по игре:')
    ax[1].title.set_fontsize(30)
    ax[1].title.set_fontweight('bold')

    ax[1].set_ylim(-100, 100)

    ax[1].spines['right'].set_visible(False)
    ax[1].spines['bottom'].set_visible(False)
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['left'].set_visible(False)

    ax[1].grid()

    # Рисование 2 графика
    ax[1].fill_between([0], [0], [0], facecolor='#FFEC14', label='Генерация от солнца')
    ax[1].fill_between([0], [0], [0], facecolor='#A3FFFF', label='Генерация от ветра')
    ax[1].fill_between([0], [0], [0], facecolor='#9C9C9C', label='Генерация от дизеля')
    ax[1].fill_between([0], [0], [0], facecolor='#FF9494', label='Потребление больницами')
    ax[1].fill_between([0], [0], [0], facecolor='#FFFDBB', label='Потребление заводами')
    ax[1].fill_between([0], [0], [0], facecolor='#9DC941', label='Потребление домами А')
    ax[1].fill_between([0], [0], [0], facecolor='#BFE471', label='Потребление домами Б')
    ax[1].fill_between([0], [0], [0], facecolor='#3737FF', label='Операции с аккамуляторами')
    ax[1].fill_between([0], [0], [0], facecolor='#000000', label='Операции с внешней сетью')
    ax[1].legend(loc='upper left', prop={'size': 13.5})

    box_x_data = range(23, 57)
    ax[1].fill_between(box_x_data, [90 for _ in box_x_data], [-100 for _ in box_x_data], facecolor='#ffffc3')

    text_about_sys_annotation = 'Аукцион\nПотребители\nГенераторы\nЭнергосистема\nПерегрузка\nБиржа\n\nИтого'

    text_about_sys_data = normalise_num_for_str(Auction) + '\n' + normalise_num_for_str(Consumers) + '\n'
    text_about_sys_data += normalise_num_for_str(Generators) + '\n' + normalise_num_for_str(Power_System) + '\n'
    text_about_sys_data += normalise_num_for_str(Overload) + '\n' + normalise_num_for_str(Exchange)
    text_about_sys_data += '\n\n' + normalise_num_for_str(Total)

    text_about_sys_delta = [normalise_num_for_str(delta_Auction), normalise_num_for_str(delta_Consumers),
                            normalise_num_for_str(delta_Generators), normalise_num_for_str(delta_Power_System),
                            normalise_num_for_str(delta_Overload), normalise_num_for_str(delta_Exchange),
                            normalise_num_for_str(delta_Total)]
    text_about_sys_end = '____________________________\n\n\n'
    if act_tick == end_tick - 1:
        text_about_sys_end += 'Игра окончена'

    ax[1].text(40, -60, text_about_sys_annotation, fontsize=20, ha='right', fontweight='bold')
    ax[1].text(51, -60, text_about_sys_data, fontsize=20, ha='right', fontweight='bold')
    y_delta = -58
    for delta_text in text_about_sys_delta[::-1]:
        ax[1].text(51.5, y_delta, delta_text, fontsize=12, color='grey')
        if delta_text == text_about_sys_delta[-1]: y_delta += 18
        y_delta += 17.8
    ax[1].text(40, -90, text_about_sys_end, fontsize=20, ha='center', fontweight='bold')

    box_x_action = range(60, 100)
    ax[1].fill_between(box_x_action, [90 for _ in box_x_action], [-100 for _ in box_x_action], facecolor='#f0f0f0')

    try:
        data_actions[0] = '- ' + data_actions[0]
        text_action = "\n- ".join(data_actions)  # 10
        ax[1].text(62, -90, text_action, fontsize=18)
    except:
        pass
    else:
        ax[1].text(62, -90, '', fontsize=18)

    # Донастройка 2 графика
    ax[1].set_xticks([])
    ax[1].set_yticks([])

    # Новый тик
    act_tick += 1


# Анимация
ani = animation.FuncAnimation(fig, game_play, interval=100)

# Полноэкранный режим
plt.show()
