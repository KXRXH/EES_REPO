from collections import defaultdict
import csv


def get_weather_data(weather_data_file, weather_objects, weather_way):
    if '.csv' in weather_data_file:
        weather_data, real_weather = get_file_weather_data(weather_data_file)
    else:
        weather_data, real_weather = get_generated_weather_data()

    return weather_data, real_weather


def get_file_weather_data(weather_data_file, count_weather):
    first_line = True
    weather_data_array = defaultdict(list)
    real_weather_array = defaultdict(list)

    with open(weather_data_file, newline='', encoding="utf-8") as File:
        reader = csv.reader(File)
        for values_tick in reader:
            if first_line:
                first_line = False
                for _object in WEATHER_OBJECTS:
                    weather_data_array[_object] = []
                    real_weather_array[_object] = []
                continue

            values_tick_valid = list(map(float, values_tick))
            for itr, _object in enumerate(WEATHER_OBJECTS):
                data_tick_array = values_tick_valid[itr * count_weather:(itr + 1) * count_weather]
                real_value = data_tick_array[WEATHER_WAY[itr] - 1]

                weather_data_array[_object].append(data_tick_array)
                real_weather_array[_object].append(real_value)

    return weather_data_array, real_weather_array


def get_generated_weather_data():
    return None, None
