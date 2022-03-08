from collections import defaultdict
from engine.engine_const import *

random.seed(1337)

crash_tick = [[15, 25], [40, 60], [65, 85]]  # Заглушка


class Engine:
    def __init__(self, count_solar, count_wind, consumer_data):
        self.real_weather = real_weather
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
            'solar': [0],
            'wind': [0],
            'storage': [0],
            'diesel': [0],
            'storage_n': [0]
        }
        for k in consumer_data:
            self.history[k] = [0]

        self.exchange = 0
        self.consumers = 0
        self.generators = 0
        self.delta_exchange = 0
        self.delta_consumers = 0
        self.delta_generators = 0

    def get_by_type(self, object_type: str):
        """
        Заменяет get_houseB и прочие гэтеры
        """
        return self.real_weather[object_type][self.act_tick]

    # Авария
    def get_crash(self):  # Краш, краш. Понавыдумывали зумеры словечек!
        value_crash = False
        for start_crash, end_crash in crash_tick:
            if start_crash <= self.act_tick < end_crash:
                value_crash = True

        return value_crash

    def calculate_solar_energy(self):
        energy = 0
        for i in range(self.count_solar):
            energy += min(self.get_by_type('solar') * self.koaf_solar_gen[i], MAX_SOLAR)
        return energy

    def calculate_wind_energy(self):
        energy = 0
        for itr in range(0, self.count_wind):
            value_wind = self.get_by_type('wind')
            if value_wind ** 3 * self.koaf_wind_gen[itr] > MAX_POWER_WIND * 100 / MAX_POWER_PERCENT:
                self.online_wind[itr] = False
            if value_wind ** 3 * self.koaf_wind_gen[itr] < MAX_POWER_WIND * MINIMUM_RESUME_PERCENT / MAX_POWER_PERCENT:
                self.online_wind[itr] = True
            if self.online_wind[itr]:
                energy += min(value_wind ** 3 * self.koaf_wind_gen[itr], MAX_POWER_WIND)
        return energy

    # Данные по энергии
    def get_received_energy(self):  # получено
        total_energy = 0
        solarE = self.calculate_solar_energy()
        windE = self.calculate_wind_energy()

        # Проверить работоспособность
        storageE, accumE = 0, 0
        for itr, mode in enumerate(self.delta_storage):
            if mode < 0:
                storageE += mode
                self.delta_storage[itr] = 0
        for itr, delta in enumerate(self.delta_accumulator):
            if delta < 0:
                accumE += delta
                self.delta_accumulator[itr] = 0

        dieselE = 0
        for mode in self.power_diesel:
            dieselE += mode

        self.history['solar'].append(solarE)
        self.history['wind'].append(windE)
        self.history['storage'].append(storageE + accumE)
        self.history['diesel'].append(dieselE)

        total_energy = solarE + windE + storageE + accumE + dieselE

        return total_energy

    def get_spent_energy(self):  # потрачено
        energy = defaultdict(int)
        for consumer in CONSUMERS:
            self.history[consumer].append(0)
            for i in range(self.consumer_data[consumer]["count"]):
                _energy = self.get_by_type(consumer)
                energy[consumer] += _energy
                self.history[consumer][-1] += _energy

        for itr, mode in enumerate(self.delta_storage):
            if mode > 0:
                energy['storage'] += mode
                self.delta_storage[itr] = 0

        for itr, delta in enumerate(self.delta_accumulator):
            if delta > 0:
                energy['accumulator'] += delta
                self.delta_accumulator[itr] = 0

        self.history['storage_n'].append(
            energy['accumulator'] + energy['storage']
        )
        return sum(list(energy.values()))

    # Оплата за генераторы
    def get_money_generators(self, generators):
        '''
        generators = {
            "substationB": [1],
            "wind": [4, 4, 1],
        }
        '''
        spent_diesel = 0
        gens = defaultdict(int)
        for generator, c in generators.items():
            contracts = c["contracts"]
            for cost in contracts:
                gens[generator] += cost

        for itr, connect in enumerate(CONNECTED_DIESEL):
            if not connect is None:
                spent_diesel += COST_DIESEL
                spent_diesel += self.power_diesel[itr] * COST_MW_DIESEl

        all_spent_money = sum(list(gens.values())) + spent_diesel

        self.delta_generators = -all_spent_money
        self.generators -= all_spent_money

        self.delta_power_system = - all_spent_money - self.delta_generators
        self.power_system += self.delta_power_system

        return all_spent_money

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

    # Прибыль
    def get_received_consumer(self, consumers):
        profit = defaultdict(int)
        for consumer, data in consumers.items():
            consumer_profit = 0
            for cost in data['contracts']:
                consumer_profit += cost * self.get_by_type(consumer)

            profit[consumer] += consumer_profit

        total_profit = sum(list(profit.values()))
        self.delta_consumers = total_profit
        self.consumers += total_profit
        return total_profit
