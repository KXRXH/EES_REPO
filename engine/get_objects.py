from engine.engine_const import *
from .parser import parser


class Objects:
    def __init__(self, eng):
        self.eng = eng

        self.real_weather = real_weather

        self.count_type, self.objects = parser()

        self.k = lambda x: min(-0.007 * x**2 + 0.1185 * x + 0.4, 0.9)

        self.objs = dict()
        self.id_to_addr = dict()
        for address in list(self.objects):
            self.objs[address] = dict()

            self.objs[address]['id'] = self.objects[address]['id']
            self.objs[address]['type'] = self.objects[address]['type']
            self.objs[address]['line'] = self.objects[address]['line']
            self.objs[address]['path'] = self.objects[address]['path']
            self.objs[address]['path_all'] = self.objects[address]['path_all']
            self.objs[address]['contract'] = self.objects[address]['contract']

            self.objs[address]['charge'] = 0
            self.objs[address]['delta'] = 0
            self.objs[address]['online'] = True
            self.objs[address]['failed'] = False

            if self.objects[address]['type'] == 'solar':
                self.objs[address]['koaf_gen'] = 0.45 + random.uniform(-0.05, 0.05)
            elif self.objects[address]['type'] == 'wind':
                self.objs[address]['koaf_gen'] = 0.01 + random.uniform(-0.004, 0.004)
            else:
                self.objs[address]['koaf_gen'] = 1

            if self.objects[address]['type'] == 'TPS':
                self.objs[address]['prew_gen'] = 0
                self.objs[address]['fuel'] = 0

            self.objs[address]['score_then'] = []
            self.objs[address]['power_then'] = []
            self.objs[address]['charge_then'] = []


    def get_by_type(self, object_type: str):
        return max(0, self.real_weather[object_type][self.eng.act_tick] + random.uniform(-HALLWAY, HALLWAY))


    def _score_now_income(self, address, contract):
        type = self.objs[address]['type']
        if type in TYPE_CUSTOMERS:
            return contract * self.get_by_type(type)
        return 0

    def _score_now_loss(self, address, contract):
        type = self.objs[address]['type']
        if type == 'TPS':
            return contract + 3.5 * self.objs[address]['fuel']
        if type not in TYPE_CUSTOMERS:
            return contract
        return 0

    def _power_now_generated(self, address, online, failed):
        type = self.objs[address]['type']
        if type == 'solar' and online and not failed:
            return min(self.get_by_type(type) * self.objs[address]['koaf_gen'], MAX_SOLAR)
        if type == 'wind' and online and not failed:
            return min(self.get_by_type(type) ** 3 * self.objs[address]['koaf_gen'], MAX_WIND)
        if type == 'storage' and online and not failed:
            if self.objs[address]['delta'] < 0:
                delta = abs(self.objs[address]['delta'])
                self.objs[address]['delta'] = 0
                return delta
        if type == 'TPS' and online and not failed:
            fuel = self.objs[address]['fuel']
            gen = fuel * self.k(fuel) + 0.6 * (self.objs[address]['prew_gen'] - 0.5)
            self.objs[address]['prew_gen'] = gen
            return gen
        return 0

    def _power_now_consumed(self, address, online, failed):
        type = self.objs[address]['type']
        if type == 'storage' and online and not failed:
            if self.objs[address]['delta'] > 0:
                delta = abs(self.objs[address]['delta'])
                self.objs[address]['delta'] = 0
                return delta
        if type in TYPE_CUSTOMERS and online and not failed:
            return self.get_by_type(type)
        return 0

    def _online(self, address):
        if self.objs[address]['type'] == 'wind':
            if self.get_by_type('wind') ** 3 * self.objs[address]['koaf_gen'] > MAX_POWER_WIND * 100 / MAX_POWER_PERCENT:
                self.objs[address]['online'] = False
            if self.get_by_type('wind') ** 3 * self.objs[address]['koaf_gen'] < MAX_POWER_WIND * MINIMUM_RESUME_PERCENT / MAX_POWER_PERCENT:
                self.objs[address]['online'] = True
        return self.objs[address]['online']  # онлайн

    def _path(self, address):
        line_1 = self.objs[address]['line']
        type_1 = self.objs[address]['path']
        id_1 = self.objs[self.objs[address]['path_all']]['id']

        if self.objs[address]['type'] == 'main':
            return [[]]
        if self.objs[address]['type'] in TYPE_WITH_2_INPUT:
            index = NUM_OBJ.index(address[1])
            address_2 = address[0] + NUM_OBJ[index+1]
            if index % 2 == 0:
                return None
            try:
                _ = self.objs[address_2]
            except:
                return [[{"line": line_1, "id": [type_1, id_1]}]]

            line_2 = self.objs[address_2]['line']
            type_2 = self.objs[address_2]['path']
            id_2 = self.objs[self.objs[address_2]['path_all']]['id']

            return [[{"line": line_1, "id": [type_1, id_1]}, {"line": line_2, "id": [type_2, id_2]}]]
        return [[{"line": line_1, "id": [type_1, id_1]}]]

    def _address(self, address):
        if self.objs[address]['type'] in TYPE_WITH_2_INPUT:
            index = NUM_OBJ.index(address[1])
            if index % 2 == 0:
                return None
            return [address, address[0] + NUM_OBJ[index+1]]
        return [address]

    def get_objects(self):
        self.data_obj = []

        for address in list(self.objs):
            self.add_obj(address)

        return self.data_obj

    def add_obj(self, address: str):
        addr = self._address(address)
        if addr is None:
            return

        contract = self.objs[address]['contract']
        online = self._online(address)
        failed = self.objs[address]['failed']
        path = self._path(address)

        score_now_income = self._score_now_income(address, contract)
        score_now_loss = self._score_now_loss(address, contract)

        power_now_generated = self._power_now_generated(address, online, failed)
        power_now_consumed = self._power_now_consumed(address, online, failed)

        charge = self.objs[address]['charge']

        modules = []

        self.data_obj.append(
            {
                "id": [self.objs[address]['type'], self.objs[address]['id']],
                "address": addr,
                "contract": contract,
                "path": path,
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": self.objs[address]['score_then'].copy()},
                "power": {
                    "now": {"online": online, "consumed": power_now_consumed, "generated": power_now_generated},
                    "then": self.objs[address]['power_then'].copy()},
                "charge": {"now": charge,
                           "then": self.objs[address]['charge_then'].copy()},
                "modules": modules,
                "class": self.objs[address]['type']
            }
        )

        self.objs[address]['score_then'].append({"loss": score_now_loss, "income": score_now_income})
        self.objs[address]['power_then'].append({"online": online, "consumed": power_now_consumed, "generated": power_now_generated})
        self.objs[address]['charge_then'].append(charge)


    def _set_charge(self, address, value):
        self.objs[address]['delta'] = value

    def _set_fuel(self, address, value):
        self.objs[address]['fuel'] = value
