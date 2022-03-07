import random

COUNT_WEATHER_VALUES = 8
WEATHER_OBJECTS = ['solar', 'wind', 'hospital', 'factory', 'houseA', 'houseB']
WEATHER_WAY = [random.randint(1, COUNT_WEATHER_VALUES) for i in WEATHER_OBJECTS]
FILE = './forecast.csv'
SEED = 1337
random.seed(SEED)
RUBLE = '\u20BD'
MAX_POWER_WIND = 15
MAX_POWER_PERCENT = 75
MAX_SOLAR = 15
MAX_WIND = 15
MINIMUM_RESUME_PERCENT = 62.5
CONSUMERS = ['houseA', 'houseB', "factory", "hospital"]
CONNECTED_DIESEL = ['M1', 'm1']
COST_DIESEL = 1
COST_MW_DIESEl = 4  # руб/МВт
COUNT_SUBSTATIONS = 1

# Рынок мгновенной мощности
spent_power_instant = 1  # руб/МВт
received_power_instant = 10  # руб/МВт


score_then_substation = [[]]
power_then_substation = [[]]
score_then_mini_substationB = [[]]
power_then_mini_substationB = [[]]
score_then_mini_substationA = [[]]
power_then_mini_substationA = [[]]
score_then_storage = [[]]
power_then_storage = [[]]
charge_then_storage = [[]]


# Работа с энергией
# Главная подстанция +
qty_substation = 1
prefix_address_substation = 'M'
contract_substation = [0]
line_substation = [[]]
path_substation = [[]]
online_substation = [True]


# Мини подстанция Б +
qty_mini_substationB = 1
prefix_address_mini_substationB = 'm'
contract_mini_substationB = [2]
line_mini_substationB = [[1]]
path_mini_substationB = [[["main", 1]]]
online_mini_substationB = [True]

# Мини подстанция А +
qty_mini_substationA = 1
prefix_address_mini_substationA = 'e'
contract_mini_substationA = [5]
line_mini_substationA = [[1]]
path_mini_substationA = [[["main", 1]]]
online_mini_substationA = [True]

# Дизель +
qty_diesel = 2
power_diesel = [0, 0]
connected_diesel = ['M1', 'm1']
max_power_diesel = 5
cost_diesel = 1
cost_MW_diesel = 4 # руб/МВт

# Аккамулятор +
delta_accamulator = [0, 0] # -x - разрядка, 0 - хранение, x - зарядка
charge_accamulator = [0, 0] # Заряд аккамуляторов
connected_accamulator  = ['M1', 'M1']
max_power_accamulator = 50
max_exchange_power_accamulator = 10 # МВт/тик
cost_accamulator = 5

# Накопитель +
qty_storage = 1
charge_storage = [0]
delta_storage = [0]
prefix_address_storage = 't'
contract_storage = [5]
line_storage = [[1]]
path_storage = [[["main", 1]]]
online_storage = [True]
max_power_storage = 100
max_exchange_power_storage = 15 # МВт/тик

# Солнечка +
qty_solar = 1
prefix_address_solar = 's'
contract_solar = [5]
line_solar = [[1]]
path_solar = [[["main", 1]]]

score_then_solar = [[] for _ in range(0, qty_solar)]
power_then_solar = [[] for _ in range(0, qty_solar)]
online_solar = [True for _ in range(0, qty_solar)]
max_power_solar = 15
koaf_solar_gen = [0.7+random.uniform(-0.1, 0.1) for _ in range(0, qty_solar)]

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
max_power_percent = 75 # процент от ветра, с которого на ветряке 15МВт
min_percent_for_resume = 62.5 # процент от ветра, с которого ветряк выходит из режима защиты
koaf_wind_gen = [0.011+random.uniform(-0.004, 0.004) for _ in range(0, qty_wind)]

# Потребители
# Больницы +
qty_hospital = 1
prefix_address_hospital = 'b'
contract_hospital = [5]
line_hospital = [[1]]
path_hospital = [[["main", 1]]]
score_then_hospital = [[]]
power_then_hospital = [[]]
online_hospital = [True]

# Заводы +
qty_factory = 1
prefix_address_factory = 'f'
contract_factory = [5]
line_factory = [[1]]
path_factory = [[["main", 1]]]
score_then_factory = [[]]
power_then_factory = [[]]
online_factory = [True]

# Дом А +
qty_houseA = 1
prefix_address_houseA = 'h'
contract_houseA = [5]
line_houseA = [[1]]
path_houseA = [[["main", 1]]]
score_then_houseA = [[]]
power_then_houseA = [[]]
online_houseA = [True]

# Дом Б +
qty_houseB = 1
prefix_address_houseB = 'd'
contract_houseB = [5]
line_houseB = [[1]]
path_houseB = [[["main", 1]]]
score_then_houseB = [[]]
power_then_houseB = [[]]
online_houseB = [True]

start_tick = 0
end_tick = 100
act_tick = start_tick

weather_objects = ['solar', 'wind', 'hospital', 'factory', 'houseA', 'houseB']
weather_way = [random.randint(1, COUNT_WEATHER_VALUES) for _ in weather_objects]

from engine.io import get_weather_data

weather_data, real_weather = get_weather_data(
    FILE, COUNT_WEATHER_VALUES, weather_objects, weather_way
)
