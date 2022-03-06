import random

COUNT_WEATHER_VALUES = 8
WEATHER_OBJECTS = ['solar', 'wind', 'hospital', 'factory', 'houseA', 'houseB']
WEATHER_WAY = [random.randint(1, COUNT_WEATHER_VALUES) for i in WEATHER_OBJECTS]
FILE = './630.forecasts.csv'
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

# Рынок мгновенной мощности
spent_power_instant = 1  # руб/МВт
received_power_instant = 10  # руб/МВт


score_then_substation = [[]]
power_then_substation = [[]]
score_then_mini_substationB = [[]]
power_then_mini_substationB = [[]]
score_then_mini_substationA = [[]]
power_then_mini_substationA = [[]]
score_then_substation = [[]]
power_then_substation = [[]]
score_then_storage = [[]]
power_then_storage = [[]]
charge_then_storage = [[]]
