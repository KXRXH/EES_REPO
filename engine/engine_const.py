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

start_tick = 0
end_tick = 100

weather_objects = ['solar', 'wind', 'hospital', 'factory', 'houseA', 'houseB']
weather_way = [random.randint(1, COUNT_WEATHER_VALUES) for _ in weather_objects]

from engine.io import get_weather_data

weather_data, real_weather = get_weather_data(
    FILE, COUNT_WEATHER_VALUES, weather_objects, weather_way
)
