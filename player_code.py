from engine import ips, Engine
from collections import namedtuple, defaultdict

charges_in_next2 = dict()
Diesel = namedtuple("Diesel", ("power",))
Cell = namedtuple("Cell", ("charge", "delta"))


def player_actions(eng: Engine, delta):
    global charges_in_next2  # !!!!!!!!!!!!!!!!!!! закоментировать на стенде

    # import ips !!!!!!!!!!!!!!!

    psm = ips.init(eng, delta)

    station_names = {"main", "miniA", "miniB"}

    for obj in psm.objects:
        if obj.type == 'TPS':
            psm.orders.tps(obj.address[0], 10)
        if obj.type in station_names:
            # включаем линии
            addr = obj.address[0]
            for i in range(2 if obj.type == "miniB" else 3):
                psm.orders.line_on(addr, i + 1)

    d = {"prev": 0}
    if psm.tick != 0:
        with open('./vars', 'r') as f:
            d = eval(f.readline())
    else:
        with open("./vars", "w", encoding="utf-8") as f:
            f.write("{'prev': 0}")

    try:
        prev = d["prev"]
    except KeyError:
        prev = 0
    gen = 0
    spend = 0
    # for index, net in psm.networks.items():
    #     gen += net.upflow
    #     spend += net.downflow


    not_used = gen - spend
    if not_used > 0:
        psm.orders.sell(not_used // 2, 4)

    with open("./vars", "w", encoding="utf-8") as f:
        f.write(str(d))

    psm.save_and_exit()
