from engine import ips, Engine
from collections import namedtuple, defaultdict

charges_in_next2 = dict()
Diesel = namedtuple("Diesel", ("power",))
Cell = namedtuple("Cell", ("charge", "delta"))


def player_actions(eng: Engine, delta):
    global charges_in_next2  # !!!!!!!!!!!!!!!!!!! закоментировать на стенде

    # import ips !!!!!!!!!!!!!!!

    psm = ips.init(eng, delta)

    total_generated = 0
    total_spent = 0
    SELL_PRICE = 4
    BUY_PRICE = 2.5
    GENERATORS = ["solar", "wind", "tps"]
    CONSUMERS = ["housea", 'houseb', "factory", "hospital"]
    TPS_POWER = 8
    STOCK_K = 0.8
    HOLIDAY_DELAY1 = 35
    HOLIDAY_DELAY2 = HOLIDAY_DELAY1 + 1

    def enable_all_tps(power):
        for obj in psm.objects:
            if obj.type == 'TPS':
                psm.orders.tps(obj.address[0], power)

    # Включаем линии всегда, когда можем
    for obj in psm.objects:
        if obj.type in ["main", "miniA", "miniB"]:
            address = obj.address[0]
            for i in range(2 if obj.type == "miniB" else 3):
                psm.orders.line_on(address, i + 1)

    selling = not (psm.tick % HOLIDAY_DELAY1 - 2 == 0 or psm.tick % HOLIDAY_DELAY2 - 2 == 0)

    if psm.tick % HOLIDAY_DELAY1 == 0:
        psm.orders.line_off('M2', 2)
        print("ОТключено от М2")
    elif psm.tick % HOLIDAY_DELAY2 == 0:
        psm.orders.line_off('e2', 2)
        print("отключено от e2")

    enable_all_tps(TPS_POWER)

    for obj in psm.objects:
        if obj.type.lower() in GENERATORS:
            total_generated += obj.power.now.generated
        elif obj.type.lower() in CONSUMERS:
            total_spent += obj.power.now.consumed

    print("Генерация:", total_generated)
    print("Потребление:", total_spent)

    balance = total_generated - total_spent

    # Тут Закуп
    if balance > 0 and selling:
        psm.orders.sell(balance * STOCK_K, SELL_PRICE)
        print(f"Продаю {balance * STOCK_K} по {SELL_PRICE}")

    elif balance < 0:
        psm.orders.buy(abs(balance), BUY_PRICE)
        print(f"Покупаю {balance} по {BUY_PRICE}")

    psm.save_and_exit()
