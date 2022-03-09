from engine.engine_const import *
from .parser import parser


class Objects:
    def __init__(self, eng):
        self.eng = eng

        self.real_weather = real_weather

        self.count_type, self.objects = parser()

        self.objs = dict()
        for address in list(self.objects):
            self.objs[address] = dict()

            self.objs[address]['id'] = self.objects[address]['id']
            self.objs[address]['type'] = self.objects[address]['type']
            self.objs[address]['line'] = self.objects[address]['line']
            self.objs[address]['path'] = self.objects[address]['path']
            self.objs[address]['contract'] = self.objects[address]['contract']

            self.objs[address]['charge'] = 0
            self.objs[address]['delta'] = 0
            self.objs[address]['online'] = True
            self.objs[address]['failed'] = False

            if self.objects[address]['type'] == 'solar':
                self.objs[address]['koaf_gen'] = 0.7 + random.uniform(-0.1, 0.1)
            elif self.objects[address]['type'] == 'wind':
                self.objs[address]['koaf_gen'] = 0.011 + random.uniform(-0.004, 0.004)
            else:
                self.objs[address]['koaf_gen'] = 1

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
                return abs(self.objs[address]['delta'])
        return 0

    def _power_now_consumed(self, address, online, failed):
        type = self.objs[address]['type']
        if type == 'storage' and online and not failed:
            if self.objs[address]['delta'] > 0:
                return abs(self.objs[address]['delta'])
        if type in TYPE_CUSTOMERS and online and not failed:
            if type in TYPE_WITH_2_INPUT:
                index = NUM_OBJ.index(address)
                if index % 2 == 0 and address[0] + NUM_OBJ[index-1] in list(self.objs):
                    return self.get_by_type(type) / 2
                elif index % 2 != 0 and address[0] + NUM_OBJ[index+1] in list(self.objs):
                    return self.get_by_type(type) / 2
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
        if self.objs[address]['type'] == 'main':
            return [[]]
        return [{"line": self.objs[address]['line'], "id": [self.objs[address]['path'], self.objs[address]['id']]}]

    def get_objects(self):
        self.data_obj = []

        for address in list(self.objs):
            self.add_obj(address)

        return self.data_obj

    def add_obj(self, address: str):
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
                "address": address,
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
