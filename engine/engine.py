from collections import defaultdict
from engine.engine_const import *
from get_objects import Objects

crash_tick = [[15, 25], [40, 60], [65, 85]]  # Заглушка


class Engine:
    def __init__(self, count_solar, count_wind, consumer_data):
        obj = Objects()
        obj.__init__()
        self.objs = obj.get_objects()

        # Это типо активный тик.
        self.act_tick = 0

        self.koaf_solar_gen = [0.7 + random.uniform(-0.1, 0.1) for _ in range(count_solar)]
        self.koaf_wind_gen = [0.011 + random.uniform(-0.004, 0.004) for _ in range(0, count_wind)]
        self.count_solar = count_solar
        self.count_wind = count_wind
        self.online_wind = [True] * self.count_wind
        self.online_solar = [True] * self.count_solar
        self.delta_storage = [0]
        self.delta_accumulator = [0]
        self.power_diesel = [0, 0]
        self.consumer_data = consumer_data
        self.power_system = 0
        self.delta_power_system = 0
        self.power_diesel = [0, 0]
        self.balance_energy = 0
        self.energy_exchange_p_data = [0]
        self.energy_exchange_n_data = [0]

        self.history = {
            'solar': [],
            'wind': [],
            'storage': [],
            'diesel': [],
            'storage_n': []
        }
        for k in consumer_data:
            self.history[k] = [0]

        self.exchange = 0
        self.consumers = 0
        self.generators = 0
        self.delta_exchange = 0
        self.delta_consumers = 0
        self.delta_generators = 0

    # Авария
    def get_crash(self):  # Краш, краш. Понавыдумывали зумеры словечек!
        value_crash = False
        for start_crash, end_crash in crash_tick:
            if start_crash <= self.act_tick < end_crash:
                value_crash = True

        return value_crash

    # received_energy = получено
    # spent_energy = потрачено
    # money_generators = оплата
    # received_consumer = прибыль

    '''
    дописать историю
    '''

    def calc(self):
        received_energy = 0
        spent_energy = 0
        money_generators = 0
        received_consumer = 0

        for obj in self.objs:
            received_energy += obj['power']['now']['generated']
            spent_energy += obj['power']['now']['consumed']
            money_generators += obj['score']['now']['loss']
            received_consumer += obj['score']['now']['income']

        return received_energy, spent_energy, money_generators, received_consumer



    # # Данные по энергии
    # def get_received_energy(self):  # получено
    # def get_spent_energy(self):  # потрачено
    # # Оплата за генераторы
    # def get_money_generators(self, generators):
    # # Прибыль
    # def get_received_consumer(self, consumers):


    # Биржа энергии между игроками
    def get_bidding_players(self):
        return None, None

    # если энергии все еще не хватает, то покупаем из внешней сети
    def get_money_remains(self):
        cost_power_instant = 0
        _balance_energy = self.balance_energy

        if _balance_energy < 0:
            if self.get_crash():
                cost_power_instant += max(0, abs(_balance_energy) - 10) * received_power_instant
            cost_power_instant += abs(_balance_energy) * received_power_instant
            self.energy_exchange_p_data.append(abs(_balance_energy))
            self.energy_exchange_n_data.append(0)
            k = -1
        else:
            if self.get_crash():
                cost_power_instant += max(0, abs(_balance_energy) - 10) * received_power_instant
            cost_power_instant += abs(_balance_energy) * spent_power_instant
            self.energy_exchange_n_data.append(abs(_balance_energy))
            self.energy_exchange_p_data.append(0)
            k = 1

        self.delta_exchange = cost_power_instant * k
        self.exchange += cost_power_instant * k

        return cost_power_instant
