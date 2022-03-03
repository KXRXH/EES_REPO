# Импортируем собственный модуль расчета энергетического баланса
from powerbalance import *
# Импортируем собственный модуль расчета экономического баланса
from costbalance import *
import operator as o
from get_forecast import read_all


networkBefore = Network(1, 0, 1, 2, 2)
networkAfter = Network(2, 0, 1, 2, 2)


def findCumulativeCost(net1, net2, tick):
    adjust = greedilyFindAdjust(p.network, tick)
    print(f"{adjust=}")
    before = costBalance(networkBefore, adjust)
    print(f"{before=}")
    after = costBalance(networkAfter, adjust)
    powerBefore = powerBalance(networkBefore, *tick)
    powerAfter = powerBalance(networkAfter, *tick)
    if net1.solar + net1.wind != net2.solar + net2.wind:
        return fuzzyop((fuzzyop(after, before, o.sub)), (fuzzyop(powerBefore, powerAfter, o.sub)), o.div)
    return fuzzyop(fuzzyop(after, before, o.sub), [(168, 1)], o.div)


print(findCumulativeCost(networkBefore, networkAfter, read_all()))
