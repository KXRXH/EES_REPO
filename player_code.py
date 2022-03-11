from engine import ips, Engine
from collections import namedtuple, defaultdict

charges_in_next2 = dict()
need_energy_substation_next1 = dict()
need_energy_substation_next2 = dict()

def player_actions(eng: Engine, delta):
    global charges_in_next2
    global need_energy_substation_next1
    global need_energy_substation_next2

    # import ips !!!!!!!!!!!!!!!

    psm = ips.init(eng, delta)

    total_generated = 0
    total_spent = 0
    SELL_PRICE = 4.5
    BUY_PRICE = 2.5
    GENERATORS = ["solar", "wind", "tps"]
    CONSUMERS = ["housea", 'houseb', "factory", "hospital"]
    TPS_POWER = 8
    STOCK_K = 0.9
    HOLIDAY_DELAY1 = 40
    HOLIDAY_DELAY2 = HOLIDAY_DELAY1 + 2

    def enable_all_tps(power):
        for obj in psm.objects:
            if obj.type == 'TPS':
                psm.orders.tps(obj.address[0], power)

    black_list = []

    if psm.tick > HOLIDAY_DELAY1 // 2:
        try:
            if psm.tick % HOLIDAY_DELAY1 < 2:
                black_list.append(("e2", 2))
                print("ОТключено 1")
            elif psm.tick % HOLIDAY_DELAY2 < 2:
                black_list.append(('eC', 2))
                print("отключено 2")
        except Exception:
            print("ОШИБКА")

    enable_all_tps(TPS_POWER)

    # Включаем линии всегда, когда можем
    for obj in psm.objects:
        if obj.type in ["main", "miniA", "miniB"]:
            address = obj.address[0]
            for i in range(2 if obj.type == "miniB" else 3):
                if not ((address, i + 1) in black_list):
                    psm.orders.line_on(address, i + 1)
                else:
                    psm.orders.line_off(address, i + 1)

    for obj in psm.objects:
        if obj.type.lower() in GENERATORS:
            total_generated += obj.power.now.generated
        elif obj.type.lower() in CONSUMERS:
            total_spent += obj.power.now.consumed

    print("Генерация:", total_generated)
    print("Потребление:", total_spent)

    balance = total_generated - total_spent

    # Тут Закуп
    if balance > 0:
        psm.orders.sell(balance * STOCK_K, SELL_PRICE)
        print(f"Продаю {balance * STOCK_K} по {SELL_PRICE}")

    elif balance < 0:
        psm.orders.buy(abs(balance), BUY_PRICE)
        print(f"Покупаю {balance} по {BUY_PRICE}")

    psm.save_and_exit()
