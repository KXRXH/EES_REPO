# act_tick = 26

from collections import namedtuple

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


def get_fails():
    fails = []
    for start_crash, end_crash in crash_tick + [[end_tick, end_tick]]:
        fails += [False] * (start_crash - len(fails))
        fails += [True] * (end_crash - start_crash)
    return fails


def make_object(d, stations, storages):
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
        stations[obj.address] = obj.id
    if obj.type in storage_types:
        storages[obj.address] = obj.id
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

    def __init__(self, data):

        self.__orders = orders = []
        self.__station_index = dict()
        self.__storage_index = dict()
        self.__user_data = [[] for _ in range(self.GRAPH_COUNT)]

        self.tick = act_tick
        self.gameLength = end_tick - start_tick
        self.scoreDelta = all_received_money - all_spent_money

        self.fails = get_fails()

        self.sun = Historic(real_weather['solar'][act_tick], real_weather['solar'][0:act_tick])
        self.wind = Historic(real_weather['wind'][act_tick], real_weather['wind'][0:act_tick])
        self.hospital = Historic(real_weather['hospital'][act_tick], real_weather['hospital'][0:act_tick])
        self.factory = Historic(real_weather['factory'][act_tick], real_weather['factory'][0:act_tick])
        self.houseA = Historic(real_weather['houseA'][act_tick], real_weather['houseA'][0:act_tick])
        self.houseB = Historic(real_weather['houseB'][act_tick], real_weather['houseB'][0:act_tick])

        self.forecasts = Data_Weather(make_forecasts(weather_data['solar']),
                                      make_forecasts(weather_data['wind']),
                                      make_forecasts(weather_data['hospital']),
                                      make_forecasts(weather_data['factory']),
                                      make_forecasts(weather_data['houseA']),
                                      make_forecasts(weather_data['houseB']))

        self.objs = get_objects()
        self.objects = [make_object(obj, self.__station_index, self.__storage_index)
                        for obj in self.objs]

        self.total_power = Total_Power(received_energy,
                                       spent_energy,
                                       energy_player,  # полученно с биржи
                                       0)  # потери

        self.orders = Namespace(
            diesel=lambda address, power: self.__set_diesel(address, power),
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
        return address in self.__station_index

    def __set_diesel(self, address, power):
        try:
            power = float(power)
            if power < 0:
                raise ("Отрицательное значение энергии на дизеле. Приказ не принят.")
        except ValueError:
            raise ("Для приказа на дизель нужен float-совместимый тип. Приказ не принят.")
        if not self.__check_address(address):
            raise ("Такой подстанции не существует. Приказ не принят.")

        global power_diesel
        local_power = power
        for itr, connect in enumerate(connected_diesel):
            if address == tuple(connect):
                power_diesel[itr] = min(local_power, max_power_diesel)
                local_power -= power_diesel[itr]
        self.__orders.append({"orderT": "diesel", "address": ''.join(address), "power": power - local_power})

    def __change_cell(self, address, power, charge=True):
        try:
            power = float(power)
            if power < 0:
                raise ("Отрицательное значение энергии в приказе на аккумулятор. Приказ не принят.")
        except ValueError:
            raise ("Для приказа на аккумулятор нужен float-совместимый тип. Приказ не принят.")
        if address not in list(self.__storage_index):
            raise ("Такого накопителя/подстанции не существует. Приказ не принят.")

        order = "charge" if charge else "discharge"
        global delta_accamulator
        global charge_accamulator
        global delta_storage
        global charge_storage
        local_power = power
        if prefix_address_storage in address:
            itr = 0
            for obj in self.objects:
                if prefix_address_storage in obj.address: itr += 1
                if obj.address != address: continue
                itr -= 1
                if charge:
                    delta_storage[itr] = min(local_power, max_power_storage - charge_storage[itr],
                                             max_exchange_power_storage)
                    charge_storage[itr] += delta_storage[itr]
                    local_power -= delta_storage[itr]
                else:
                    delta_storage[itr] = -1 * min(local_power, charge_storage[itr], max_exchange_power_storage)
                    charge_storage[itr] += delta_storage[itr]
                    local_power -= -delta_storage[itr]
            if itr == len(self.objects): raise ("Такого накопителя/подстанции не существует. Приказ не принят.")
        else:
            for itr, connect in enumerate(connected_accamulator):
                if address == tuple(connect):
                    if charge:
                        delta_accamulator[itr] = min(local_power, max_power_accamulator - charge_accamulator[itr],
                                                     max_exchange_power_accamulator)
                        charge_accamulator[itr] += delta_accamulator[itr]
                        local_power -= delta_accamulator[itr]
                    else:
                        delta_accamulator[itr] = -1 * min(local_power, charge_accamulator[itr],
                                                          max_exchange_power_accamulator)
                        charge_accamulator[itr] += delta_accamulator[itr]
                        local_power -= -delta_accamulator[itr]
        self.__orders.append({"orderT": order, "address": ''.join(address), "power": power - local_power})

    def __outstanding(self, amount, price, sell=True):
        pass

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
        self.orders.humanize
        return 'Конец выполнения'

    def get_user_data(self):
        return 'Конец выполнения'

    class orders:
        def get(self):
            return 'Конец выполнения'

        def humanize(self):
            return 'Конец выполнения'


class ips():
    def init() -> Powerstand:
        return Powerstand(None)

    def init_test() -> Powerstand:
        return from_json(stub_input)

    def from_json(string) -> Powerstand:
        return Powerstand(None)

    def from_file(filename) -> Powerstand:
        return Powerstand(None)

    def from_log(filename, step) -> Powerstand:
        return Powerstand(None)
