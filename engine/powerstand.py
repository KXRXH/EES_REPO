# self.eng.act_tick = 26
import sys
import traceback

from engine.engine import *
from collections import namedtuple
from argparse import Namespace

from engine.engine_const import *


__all__ = [
    "Powerstand", "Object", "Line", "Powerline",
    "Historic", "Receipt", "ExchangeReceipt",
    "Diesel", "Cell",
]

obj_types = [
    "main"  # подстанции
    "miniA",  # мини-подстанции А
    "miniB",  # мини-подстанции Б
    "solar",  # солнечные электростанции
    "wind",  # ветровые электростанции
    "houseA",  # дом А
    "houseB",  # дом Б
    "factory",  # больницы
    "hospital",  # заводы
    "storage",  # накопители
]

station_types = {"miniA", "miniB", "main"}
storage_types = {"miniA", "storage", "main"}

spent_obj = ['miniB', 'miniA', 'storage', 'solar', 'wind', 'main']

Historic = namedtuple("Historic", ("now", "then"))
Historic.__str__ = lambda self: f"{self.now} (было {safe_tail(self.then)})"

Receipt = namedtuple("Receipt", ("income", "loss"))
Receipt.__str__ = lambda self: f"(+{self.income} ₽, -{self.loss} ₽)"
Receipt.__add__ = lambda self, x: __add_receipt(self, x)


def __add_receipt(self, x):
    if isinstance(x, Receipt):
        return Receipt(self.income + x.income, self.loss + x.loss)
    raise TypeError(x)


Data_Weather = namedtuple("Data_Weather", ("sun", "wind", "hospital", "factory", "houseA", "houseB"))

Total_Power = namedtuple("Total_Power", ("generated", "consumed", "external", "losses"))

Object = namedtuple("Object", ("id", "type", "contract", "address", "path",
                               "score", "power", "charge", "modules"))
Object.__str__ = lambda self: f"{self.type} ({self.power.now}, {self.score.now})"

ExchangeReceipt = namedtuple("ExchangeReceipt", ("source", "flux", "price"))
ExchangeReceipt.__str__ = \
    lambda self: f"{pretty_source(self.source)} " \
                 f"({self.flux:.2f} МВт, {self.price:.2f} ₽/МВт)"

Power = namedtuple("Line", ("generated", "consumed", "online"))
Power.__str__ = lambda self: f"{pretty_bool(self.online)} " \
                             f"(+{self.generated} МВт⋅ч -{self.consumed} МВт⋅ч)"
Power.total = lambda self: self.generated - self.consumed

Line = namedtuple("Line", ("id", "line"))
Line.__str__ = lambda self: f"{self.id}-{self.line}"

Powerline = namedtuple("Powerline", ("location", "online", "upflow", "downflow", "losses"))
Powerline.__str__ = lambda self: f"{self.location} ({pretty_bool(self.online)})"

Diesel = namedtuple("Diesel", ("power",))
Diesel.__str__ = lambda self: f"Дизель ({self.power})"

Cell = namedtuple("Cell", ("charge", "delta"))
Cell.__str__ = lambda self: f"Аккумулятор ({self.charge})"


def pretty_bool(v):
    return 'вкл.' if v else 'выкл.'


def pretty_agent(ag):
    return f'{ag["place"]}.{ag["player"]}'


def pretty_source(ag):
    if ag == "exchange":
        return 'контракт c оператором'
    elif ag == 'overload':
        return 'штраф за перегрузку'
    return f'контракт с игроком {ag["place"]}.{ag["player"]}'


def unsource(src):
    tag = src["esType"]
    if tag == "player":
        return src["owner"]
    return tag


def safe_tail(data):
    if len(data):
        return None
    return data[-1]


def safe_head(data):
    if len(data):
        return None
    return data[0]


def make_module(m):
    if m["type"] == "cell":
        return Cell(m["charge"], m["delta"])
    if m["type"] == "diesel":
        return Diesel(m["power"])
    raise NotImplementedError("неизвестный модуль")


def make_historic(d, fn):
    return Historic(fn(**d["now"]), [fn(**x) for x in d["then"][::-1]])


def make_historic_(d, fn):
    return Historic(fn(d["now"]), [fn(x) for x in d["then"][::-1]])


def make_object(d, stations, storages, thermos):
    obj = Object(
        id=d["id"],
        address=tuple(d["address"]),
        contract=d["contract"],
        path=tuple(tuple(Line(tuple(l["id"]), l["line"]) for l in a) for a in d["path"]),
        score=make_historic(d["score"], Receipt),
        power=make_historic(d["power"], Power),
        charge=make_historic_(d["charge"], float),
        modules=tuple(make_module(m) for m in d["modules"]),
        type=d["class"]
    )
    if obj.type in station_types:
        stations[obj.address[0]] = obj.id
    if obj.type in storage_types:
        storages[obj.address[0]] = obj.id
    if obj.type == "TPS":
        thermos[obj.address[0]] = obj.id
    return obj


def make_powerline(d):
    d["location"] = tuple(Line(tuple(l["id"]), l["line"]) for l in d["location"])
    del d["owner"]
    return Powerline(**d)


def from_chipping(d):
    return Historic(d["current"], d["done"][::-1])


def make_forecasts(d):
    arr = [[] for _ in range(0, len(d[0]))]
    for i in range(0, len(d)):
        for j in range(0, len(d[0])):
            arr[j].append(d[i][j])
    return arr


class Powerstand:
    GRAPH_COUNT = 4

    def __init__(self, eng: Engine, score_delta):

        self.eng = eng

        self.__orders = orders = []
        self.__station_index = dict()
        self.__storage_index = dict()
        self.__tps_index = dict()
        self.__user_data = [[] for _ in range(self.GRAPH_COUNT)]

        self.tick = self.eng.act_tick
        self.gameLength = end_tick - start_tick
        self.scoreDelta = score_delta


        self.sun = Historic(real_weather['solar'][self.tick], real_weather['solar'][0:self.tick])
        self.wind = Historic(real_weather['wind'][self.tick], real_weather['wind'][0:self.tick])

        self.forecasts = Data_Weather(make_forecasts(weather_data['solar']),
                                      make_forecasts(weather_data['wind']),
                                      make_forecasts(weather_data['hospital']),
                                      make_forecasts(weather_data['factory']),
                                      make_forecasts(weather_data['houseA']),
                                      make_forecasts(weather_data['houseB']))


        self.objects = [make_object(obj, self.__station_index, self.__storage_index, self.__tps_index)
                        for obj in self.eng.objs]

        self.total_power = Total_Power(eng.received_energy,
                                       eng.spent_energy,
                                       0,
                                       0)  # потери

        self.orders = Namespace(
            tps=lambda address, power: self.__set_tps(address, power),
            charge=lambda address, power: self.__change_cell(address, power, True),
            discharge=lambda address, power: self.__change_cell(address, power, False),
            sell=lambda amount, price: self.__outstanding(amount, price, True),
            buy=lambda amount, price: self.__outstanding(amount, price, False),
            line_on=lambda address, line: self.__set_line(address, line, True),
            line_off=lambda address, line: self.__set_line(address, line, False),
            add_graph=lambda idx, values: self.__add_graph(idx, values),
            # debug functions
            get=lambda: orders.copy(),
            humanize=lambda: self.__humanize_orders(),
        )

    def __check_address(self, address):
        return tuple(address) in self.__station_index

    def __set_tps(self, address, power):
        try:
            power = float(power)
            if power < 0:
                self.__warn_tb("Отрицательное значение энергии на ТЭС. "
                               "Приказ не принят.", cut=3)
                return
        except ValueError:
            self.__warn_tb("Для приказа на ТЭС нужен float-совместимый "
                           "тип. Приказ не принят.", cut=3)
            return
        if address not in self.__tps_index:
            self.__warn_tb("Такой ТЭС не существует. "
                           "Приказ не принят.", cut=3)
            return

        self.eng._objects._set_fuel(address, power)

        self.__orders.append({"orderT": "TPS", "address": address, "power": power})

    def __change_cell(self, address, power, charge=True):
        try:
            power = float(power)
            if power < 0:
                self.__warn_tb("Отрицательное значение энергии в приказе на аккумулятор. "
                               "Приказ не принят.", cut=3)
                return
        except ValueError:
            self.__warn_tb("Для приказа на аккумулятор нужен float-совместимый "
                           "тип. Приказ не принят.", cut=3)
            return
        if address not in self.__storage_index:
            self.__warn_tb("Такого накопителя/подстанции не существует. "
                           "Приказ не принят.", cut=3)
            return

        order = "charge" if charge else "discharge"

        if charge:
            sent_power = min(power, 15, 100 - self.eng._objects.objs[address]['charge'])
        else:
            sent_power = -min(power, 15, self.eng._objects.objs[address]['charge'])

        self.eng._objects._set_charge(address, sent_power)
        self.eng.exchange += (power - sent_power) * spent_power_instant

        self.__orders.append({"orderT": order, "address": ''.join(address), "power": sent_power})

    def __outstanding(self, amount, price, sell=True):
        try:
            amount = float(amount)
            if amount < 0:
                self.__warn_tb("Неположительное значение энергии в заявке на биржу. "
                               "Приказ не принят.", cut=3)
                return
        except ValueError:
            self.__warn_tb("Для заявки на биржу нужно float-совместимое "
                           "значение энергии. Приказ не принят.", cut=3)
            return
        try:
            price = float(price)
            if price < 0:
                self.__warn_tb("Неположительное значение стоимости в заявке на биржу. "
                               "Приказ не принят.", cut=3)
                return
        except ValueError:
            self.__warn_tb("Для заявки на биржу нужно float-совместимое "
                           "значение стоимости. Приказ не принят.", cut=3)
            return
        order = "sell" if sell else "buy"

        if sell:
            sent_power = min(amount, 50)
        else:
            sent_power = min(amount, 50)

        self.eng._set_order(order, sent_power)
        self.eng.exchange += (amount - sent_power) * spent_power_instant

        self.__orders.append({"orderT": order, "amount": amount, "price": price})


    def __set_line(self, address, line, value=True):
        pass

    def __add_graph(self, idx, values):
        pass

    def get_orders(self):
        return self.__humanize_orders()

    def __humanize_orders(self):
        global data_actions
        data_actions = [self.humanize_order(o) for o in self.__orders]

        return data_actions

    @staticmethod
    def __warn_tb(error, warning=False, cut=2):
        level = "Предупреждение" if warning else "Ошибка"
        print("".join(traceback.format_list(traceback.extract_stack()[:-cut])) +
              f"{level}: {error}", file=sys.stderr, flush=True)

    @staticmethod
    def humanize_order(order):
        type = order["orderT"]
        if type == "lineOn":
            return f"включение линии {order['line']['line']} " \
                   f"на подстанции {order['address']}"
        if type == "lineOff":
            return f"выключение линии {order['line']['line']} " \
                   f"на подстанции {order['address']}"
        if type == "sell":
            return f"заявка на продажу {order['amount']:.2f} МВт⋅ч за {order['price']:.2f} ₽"
        if type == "buy":
            return f"заявка на покупку {order['amount']:.2f} МВт⋅ч за {order['price']:.2f} ₽"
        if type == "TPS":
            return f"установка мощности ТЭС {order['address']} в {order['power']:.2f} МВт"
        if type == "diesel":
            return f"установка мощности дизелей {order['address']} в {order['power']:.2f} МВт"
        if type == "charge":
            return f"зарядка аккумуляторов {order['address']} на {order['power']:.2f} МВт⋅ч"
        if type == "discharge":
            return f"разрядка аккумуляторов {order['address']} на {order['power']:.2f} МВт⋅ч"
        if type == "userData":
            return "отправить графики"
        else:
            return "неизвестный приказ"

    def save_and_exit(self):
        self.orders.humanize()
        return 'Конец выполнения'

    def get_user_data(self):
        return 'Конец выполнения'

    class orders:
        def get(self):
            return 'Конец выполнения'

        def humanize(self):
            return 'Конец выполнения'


class ips():
    def init(eng: Engine, delta) -> Powerstand:
        return Powerstand(eng, delta)
