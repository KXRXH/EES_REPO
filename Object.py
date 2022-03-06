from enum import Enum


class Object(Enum):
    def __init__(self, cost, qty, path, charge, prefix):
        # cost < 0 - Мы платим. для генераторов
        self.prefix = prefix
        self.cost = cost
        self.qty = qty
        self.path = path
        self.charge = charge
        self.score_history = [[]]
        self.power_history = [[]]
        self.online_substation = [True]
