import random
import operator as o
from get_forecast import *


# Этот модуль будет использоваться почти во всех остальных решениях
# Операция на «нечетких множествах»
def fuzzyop(fuz1, fuz2, op):
    result = []
    for (val1, prob1) in fuz1:
        for (val2, prob2) in fuz2:
            result.append((op(val1, val2), prob1 * prob2))
    return result


# Оптимизировать представление случайной величины
def squash(d):
    d.sort(key=lambda x: x[0])
    l = len(d)
    newD = []
    acc = 0
    for i in range(len(d) - 1):
        if d[i][0] != d[i + 1][0]:
            x = (d[i][0], acc + d[i][1])
            newD.append(x)
            acc = 0
        else:
            acc += d[i][1]
            x = (d[len(d) - 1][0], acc + d[len(d) - 1][1])
            newD.append(x)
    return newD


# Округление по произвольной базе
def myround(value, step):
    mod = value % step
    div = value // step
    if mod > step / 2:
        return step * (div + 1)
    else:
        return step * div


# Огрубить случайную величину. чтобы ускорить вычисления
# Желательно также убирать вероятности ниже порогового значения
roughstep = 0.2


def rough(fuz):
    result = [(myround(val, roughstep), prob) for (val, prob) in fuz]
    return squash(result)


def tossRandom(f0, f25, f50, f75, f100):
    coin = random.random()
    if coin < 0.25:
        return random.random() * (f25 - f0) + f0
    elif coin < 0.5:
        return random.random() * (f50 - f25) + f25
    elif coin < 0.75:
        return random.random() * (f75 - f50) + f50
    return random.random() * (f100 - f75) + f75


# Получить численную случайную величину из прогноза
def fromForecast(forecast):
    f0, f25, f50, f75, f100 = forecast
    return [(f0, 0.25), (f25, 0.25), (f50, 0.25), (f75, 0.25), (f100, 0)]


# HERE

# Линейные коэффициенты генерации для ветра и солнца
coefSun = [0.12, 0.94, 0.7]
coefWind = [0.09, 0.32, 0.49, 0.41, 0.27, 0.16]


# Вычисление прогноза генерации
def powerForecast(coefficients, values, tick):
    power = [(0, 1)]
    for i in range(0, len(coefficients)):
        if tick - i < 0:
            val = 0
    else:
        val = values[tick - i]
        part = fuzzyop(fromForecast(val), [(coefficients[i], 1)], o.mul)
        power = fuzzyop(power, part, o.add)
    return rough(power)


# Вычисление прогноза генерации
def powerSun(tick, sun):
    return powerForecast(coefSun, sun, tick)


# Вычисление прогноза генерации
linear = 0.44  # коэффициент при x^3


def powerWind(tick, wind):
    tmp = powerForecast(coefWind, wind, tick)
    return [(max(15, linear * (x ** 3)), p) for (x, p) in tmp]


class Network:
    houses = 0
    hospitals = 0
    factories = 0
    wind = 0
    solar = 0

    def __init__(self, h, f, b, w, s):
        self.houses = h
        self.hospitals = b
        self.factories = f
        self.wind = w
        self.solar = s
        # Задаем состав сети


network = Network(2, 2, 1, 1, 2)


def powerBalance(net, sun, wind, factories, hospitals, houses):
    power = [(0, 1)]
    for tick in range(0, 3):
        for i in range(0, net.houses):
            power = fuzzyop(power, fromForecast(houses[tick])[:net.houses], o.sub)
        power = rough(power)
        print(len(power))
        for i in range(0, net.factories):
            power = fuzzyop(power, fromForecast(factories[tick])[:net.factories], o.sub)
        power = rough(power)
        print(len(power))
        for i in range(0, net.hospitals):
            power = fuzzyop(power, fromForecast(hospitals[tick])[:net.hospitals], o.sub)
        power = rough(power)
        print(len(power))
        for i in range(0, net.solar):
            power = fuzzyop(power, powerSun(tick, sun)[:net.solar], o.add)
        power = rough(power)
        print(len(power))
        for i in range(0, net.wind):
            power = fuzzyop(power, powerWind(tick, wind)[:net.solar], o.add)
        print(len(power))
    print("EXIT")
    return rough(power)


def expect(fuz):
    return sum([v * p for v, p in fuz])
