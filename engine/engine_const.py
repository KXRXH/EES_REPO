import random
random.seed(1337)

COUNT_WEATHER_VALUES = 8
WEATHER_OBJECTS = ['solar', 'wind', 'hospital', 'factory', 'houseA', 'houseB']
WEATHER_WAY = [random.randint(1, COUNT_WEATHER_VALUES) for i in WEATHER_OBJECTS]
FILE = './forecast_335.csv'
SEED = 1337
random.seed(SEED)
RUBLE = '\u20BD'
MAX_POWER_WIND = 15
MAX_POWER_PERCENT = 85
MAX_SOLAR = 15
MAX_WIND = 15
MINIMUM_RESUME_PERCENT = 87.5
CONSUMERS = ['houseA', 'houseB', "factory", "hospital"]
CONNECTED_DIESEL = ['M1', 'm1']
COST_DIESEL = 1
COST_MW_DIESEl = 4  # руб/МВт
COUNT_SUBSTATIONS = 1

NAME_OBJECTS = ["main", "miniA", "miniB", "solar", "wind", "houseA", "houseB", "factory", "hospital", "storage", "TPS"]
PREFIX_OBJECTS = {
    "main": 'M',
    "miniA": 'e',
    "miniB": 'm',
    "solar": 's',
    "wind": 'a',
    "houseA": 'h',
    "houseB": 'b', # !!!!!
    "factory": 'f',
    "hospital": 'i', # !!!!!!!
    "storage": 'c',
    "TPS": 't'
}
PREFIX_FOR_OBJECTS = dict()
for name in list(PREFIX_OBJECTS):
    PREFIX_FOR_OBJECTS[PREFIX_OBJECTS[name]] = name
TYPE_CUSTOMERS = ["houseA", "houseB", "factory", "hospital"]
TYPE_WITH_2_INPUT = ["factory", "hospital", "TPS"]
TYPE_STATION = ["main", "miniA", "miniB"]
NUM_OBJ = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
HALLWAY = 0.5

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
