from enum import Enum


class Consumer(Enum):
    Hospital = (5, -10)
    Factory = (5, -5)
    HouseA = (5, -5.5)
    HouseB = (4, -5)

    def __init__(self, price, charge):
        self.price = price
        self.charge = charge


class PowerPlant(Enum):
    Solar = 8
    Wind = 10
    Battery = 0

    def __init__(self, charge):
        self.charge = charge
