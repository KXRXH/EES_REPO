# from engine.engine_const import *


class Objects:
    def __init__(self):
        self.real_weather = real_weather
        # self.DATA = topology.json
        # Это типо активный тик.
        self.act_tick = 0

        self.NAME_OBJECTS = ["main", "miniA", "miniB", "solar", "wind", "houseA", "houseB", "factory", "hospital",
                             "storage"]
        self.NAME2_OBJECTS = {
            "main": 'substation',
            "miniA": 'mini_substationA',
            "miniB": 'mini_substationB',
            "solar": 'solar',
            "wind": 'wind',
            "houseA": 'houseA',
            "houseB": 'houseB',
            "factory": 'factory',
            "hospital": 'hospital',
            "storage": 'storage'
        }

        self.TYPE_CUSTOMERS = ["houseA", "houseB", "factory", "hospital"]
        self.TYPE_STATION = ["main", "miniA", "miniB"]

        self.HALLWAY = 0.5

        '''
        для определения нужно count, prefix, contract, path
        '''


        # self.count = dict()
        # self.prefix = dict()
        # self.contract = dict()
        # self.path = dict()
        # for name in self.NAME_OBJECTS:
        #     self.count[self.NAME2_OBJECTS[name]] = count
        #     self.prefix[self.NAME2_OBJECTS[name]] = prefix
        #     self.contract[self.NAME2_OBJECTS[name]] = contract
        #     self.path[self.NAME2_OBJECTS[name]] = contract

        # self.koaf_solar_gen = [0.7 + random.uniform(-0.1, 0.1) for _ in range(0, count_solar)]
        # self.koaf_wind_gen = [0.011 + random.uniform(-0.004, 0.004) for _ in range(0, count_wind)]
        # self.online_wind = [True for _ in range(0, count_solar)]
        # self.online_solar = [True for _ in range(0, count_wind)]
        # self.delta_storage = [0 for _ in range(0, count_storage)]


        self.history = dict()

        for name in self.NAME_OBJECTS:
            self.history[name] = dict()
            self.history[name][self.make_name(name, 'score_then')] = []
            self.history[name][self.make_name(name, 'power_then')] = []
            self.history[name][self.make_name(name, 'charge_then')] = []
            for itr in range(0, self._qty(name)):
                self.history[name][self.make_name(name, 'score_then')].append([])
                self.history[name][self.make_name(name, 'power_then')].append([])
                self.history[name][self.make_name(name, 'charge_then')].append([])

    def make_name(self, obj, name):
        return f'{name}_{obj}'

    def get_by_type(self, object_type: str):
        """
        Заменяет get_houseB и прочие гэтеры
        """
        return max(0, self.real_weather[object_type][self.act_tick] + random.uniform(-self.HALLWAY, self.HALLWAY))


    def _qty(self, obj):
        return eval(f'qty_{self.NAME2_OBJECTS[obj]}') # count

    def _address(self, obj):
        return eval(f'prefix_address_{self.NAME2_OBJECTS[obj]}') + hex(self.address_itr)[2:] # prefix

    def _contract(self, obj, itr):
        return eval(f'contract_{self.NAME2_OBJECTS[obj]}[{itr}]') # contract

    def _score_now_income(self, obj, contract):
        if obj in self.TYPE_CUSTOMERS:
            return contract * self.get_by_type('obj')
        return 0

    def _score_now_loss(self, obj, contract):
        if obj not in self.TYPE_CUSTOMERS:
            return contract
        return 0

    def _power_now_generated(self, obj, itr, online):
        if obj == 'solar' and online:
            return min(self.get_by_type('solar') * koaf_solar_gen[itr], max_power_solar)
        if obj == 'wind' and online:
            return min(self.get_by_type('wind') ** 3 * koaf_wind_gen[itr], max_power_wind)
        if obj == 'storage' and online:
            if delta_storage[itr] < 0:
                return abs(delta_storage[itr])
        return 0

    def _power_now_consumed(self, obj, itr, online):
        if obj == 'storage' and online:
            if delta_storage[itr] > 0:
                return abs(delta_storage[itr])
        if obj in self.TYPE_CUSTOMERS and online:
            return self.get_by_type('obj')
        return 0

    def _charge(self, obj, itr):
        if obj == 'storage':
            return charge_storage[itr]
        return 0

    def _online(self, obj, itr):
        if obj == 'wind':
            if self.get_by_type('wind') ** 3 * koaf_wind_gen[itr] > MAX_POWER_WIND * 100 / MAX_POWER_PERCENT:
                online_wind[itr] = False
            if self.get_by_type('wind') ** 3 * koaf_wind_gen[itr] < MAX_POWER_WIND * MINIMUM_RESUME_PERCENT / MAX_POWER_PERCENT:
                online_wind[itr] = True
        return eval(f'online_{self.NAME2_OBJECTS[obj]}[{itr}]') # онлайн

    def _path(self, obj, itr):
        path = []
        line_connected = eval(self.make_name(self.NAME2_OBJECTS[obj], 'line') + f'[{itr}]') # линия подключения
        path_connected = eval(self.make_name(self.NAME2_OBJECTS[obj], 'path') + f'[{itr}]') # путь подключения

        for itr_line in range(0, len(line_connected)):
            path.append([{"line": line_connected[itr_line], "id": path_connected[itr_line]}])

        return path

    def get_objects(self):
        self.data_obj = []
        self.id_itr = 0

        for name in self.NAME_OBJECTS:
            self.add_obj(name)

        return self.data_obj

    def add_obj(self, obj: str):
        self.address_itr = 0

        for itr in range(0, self._qty(obj)):
            self.id_itr += 1
            self.address_itr += 1

            address = self._address(obj)
            contract = self._contract(obj, itr)
            online = self._online(obj, itr)
            path = self._path(obj, itr)

            score_now_income = self._score_now_income(obj, contract)
            score_now_loss = self._score_now_loss(obj, contract)

            power_now_generated = self._power_now_generated(obj, itr, online)
            power_now_consumed = self._power_now_consumed(obj, itr, online)

            charge = self._charge(obj, itr)

            modules = []

            self.data_obj.append(
                {
                    "id": [obj, self.id_itr],
                    "address": address,
                    "contract": contract,
                    "path": path,
                    "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                              "then": self.history[obj][self.make_name(obj, 'score_then')][itr].copy()},
                    "power": {
                        "now": {"online": online, "consumed": power_now_consumed, "generated": power_now_generated},
                        "then": self.history[obj][self.make_name(obj, 'power_then')][itr].copy()},
                    "charge": {"now": charge,
                               "then": self.history[obj][self.make_name(obj, 'charge_then')][itr].copy()},
                    "modules": modules,
                    "class": obj
                }
            )

            self.history[obj][self.make_name(obj, 'score_then')][itr].append(
                {"loss": score_now_loss, "income": score_now_income}
            )
            self.history[obj][self.make_name(obj, 'power_then')][itr].append(
                {"online": online, "consumed": power_now_consumed, "generated": power_now_generated}
            )
            self.history[obj][self.make_name(obj, 'charge_then')][itr].append(charge)
