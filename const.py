import random

COUNT_WEATHER_VALUES = 8
WEATHER_OBJECTS = ['solar', 'wind', 'hospital', 'factory', 'houseA', 'houseB']
WEATHER_WAY = [random.randint(1, COUNT_WEATHER_VALUES) for i in WEATHER_OBJECTS]
FILE = './630.forecasts.csv'
SEED = 1337
random.seed(SEED)
RUBLE = '\u20BD'
