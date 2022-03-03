import csv
import random

COUNT_DATA = 5

to_nums = lambda row: [eval(i) for i in row]
data = []
with open('forecasts.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(list(row.values()))


def delete_error(row):
    '''
    Удалить самы выбивающийся параметр как ошибку
    '''
    row = sorted(row)
    if row[1] - row[0] < row[-1] - row[-2]:
        return row[:-1]
    return row[1:]


def medium(row):
    return sum(row) / len(row)


def get_row_by_type(row: list, obj_type: str):
    if obj_type == "sun":
        r = row[8:16]
        r = [(1 - i // 8) * i for i in r]
        return r


def get_five(data_row: list) -> list:
    data_row.sort()
    start = random.choice((1, 2))
    return data_row[start:start + 5]


def read_all():
    global data
    sun, wind, factories, hospitals, houses = [], [], [], [], []
    for row in data[:COUNT_DATA]:
        row = to_nums(row)
        sun.append(get_five(row[:8]))
        wind.append(get_five(row[8:16]))
        hospitals.append(get_five(row[16:24]))
        factories.append(get_five(row[24:32]))
        houses.append(get_five(row[32:40]))
    return sun, wind, factories, hospitals, houses
