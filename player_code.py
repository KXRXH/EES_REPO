from engine import ips, Engine
from collections import namedtuple, defaultdict

charges_in_next2 = dict()
Diesel = namedtuple("Diesel", ("power",))
Cell = namedtuple("Cell", ("charge", "delta"))


def player_actions(eng: Engine, delta):
    return
    global charges_in_next2  # !!!!!!!!!!!!!!!!!!! закоментировать на стенде

    # import ips !!!!!!!!!!!!!!!

    psm = ips.init(eng, delta)

    '''
    {
        waySun: 1,
        wayWind: [7],
        wayHospital: 2,
        wayFactory: 3,
        wayHouseA: 4,
        wayHouseB: 6
    }

    если у нас отключается ветряк, то что предпринять <--- нужно написать
    ловим момент, когда отключается ветряк и ставим его в 0
    отладка на тестовых играх
    спросить, как заряжаются/разряжаются накопители/аккумуляторы (на следующий или текущий ходы)
    '''

    if psm.eng.act_tick != 0:
        with open('./vars', 'r') as f:
            input_data = eval(f.readline())

        flag_Sun = input_data['flag_Sun']
        flag_Hospital = input_data['flag_Hospital']
        flag_Factory = input_data['flag_Factory']
        flag_HouseA = input_data['flag_HouseA']
        flag_HouseB = input_data['flag_HouseB']

        waySun = input_data['waySun']
        wayWind = input_data['wayWind']
        wayHospital = input_data['wayHospital']
        wayFactory = input_data['wayFactory']
        wayHouseA = input_data['wayHouseA']
        wayHouseB = input_data['wayHouseB']

        wind_way = input_data['wind_way']
        sun_k = input_data['sun_k']

    else:
        flag_Sun = False
        flag_Hospital = False
        flag_Factory = False
        flag_HouseA = False
        flag_HouseB = False

        waySun = -1
        wayWind = -1
        wayHospital = -1
        wayFactory = -1
        wayHouseA = -1
        wayHouseB = -1

        wind_way = list(range(0, 8))
        sun_k = []

    price_in = 3
    price_out = 3

    INDEFINITE_SUN_NEXT = 0.55
    INDEFINITE_WIND_NEXT = -1  # ?

    loss = lambda power: 20 / 100 if power > 23 else (power ** 2 * 20 / (23 ** 2)) / 100

    def wind_solve(x, a, b, c, d, e):
        return a + b * x[0] + c * x[1] + d * x[2] + e * x[3]

    POPT_ALL = [-4.93091421e-01, 4.09513548e-03, -7.48586349e-04, 4.02567947e-03, 7.69533675e-01]
    POPT_LITTLE = [1.38982832e-02, 1.82224517e-03, -1.25583135e-04, -1.18244397e-01, 7.49734816e-01]
    K_ALL = 1.35
    K_LITTLE = 1.6

    need_energy_next = 0
    need_energy_substation = defaultdict(list)

    gen_energy_next = 0
    gen_energy_substation = defaultdict(list)

    need_energy_next2 = 0
    need_energy_substation_next2 = defaultdict(list)

    gen_energy_next2 = 0
    gen_energy_substation_next2 = defaultdict(list)

    itr_sun = -1
    itr_wind = -1

    station_names = {"main", "miniA", "miniB"}

    cells = defaultdict(int)
    charge = 0  # суммарный заряд на аккумуляторах

    storages = set()
    stored = 0  # суммарный заряд на накопителямх

    count_diesels = 0

    can_discharge = 0  # сколько энергии можем разрядить за ход (не сколько энергии у нас всего в накопителях/аккумах)
    charges_in_next2 = dict()

    # Определяем кол-во накопителей/аккумов/дизелей, смотрим сколько можем разрядить за ход, сколько всего в них энергии
    # Определяем их адрес
    for obj in psm.objects:
        if obj.type == "storage":
            addr = obj.address[0]
            storages.add(addr)
            stored += obj.charge.now

            if obj.charge.now >= 15:
                can_discharge += 15
            else:
                can_discharge += obj.charge.now

        if obj.type in station_names:

            # включаем линии
            addr = obj.address[0]
            for i in range(2 if obj.type == "miniB" else 3):
                psm.orders.line_on(addr, i + 1)

            # учёт накопителей
            for m in obj.modules:

                # учёт дизелей
                if isinstance(m, Diesel):  # !!!!!!!!!!!!!! на стенде писать ips.Diesel
                    count_diesels += 1
                    continue

                # учёт аккумуляторов
                if isinstance(m, Cell):  # !!!!!!!!!!!!!! на стенде писать ips.Cell
                    cells[addr] += 1
                    charge += m.charge

                    if m.charge >= 10:
                        can_discharge += 10
                    else:
                        can_discharge += m.charge

    # определяем "путь" солнца
    if psm.sun.now != 0 and not flag_Sun:
        for i in range(0, 8):
            if psm.forecasts.sun[i][psm.eng.act_tick] == psm.sun.now:
                waySun = i
                flag_Sun = True
                break
        for obj in psm.objects:
            if obj.type == 'solar':
                sun_k.append(obj.power.now.generated / psm.sun.now)
    # gen_n = weather_s * sun_k[n]

    # определяем "путь" ветра и удаляем лишние
    for i, way in enumerate(wind_way):
        if psm.forecasts.wind[way][psm.eng.act_tick] != psm.wind.now:
            wind_way.pop(i)
    wayWind = wind_way[0]

    # определяем пути зданий и подключения к энергорайонам
    for obj in psm.objects:
        # потребление
        if obj.type == 'hospital':
            if not flag_Hospital:
                for i in range(0, 8):
                    if psm.forecasts.hospital[i][psm.eng.act_tick] == obj.power.now.consumed:
                        wayHospital = i
                        flag_Hospital = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                    need_energy_substation_next2[path] = []
                need_energy_substation[path].append(
                    psm.forecasts.hospital[wayHospital][psm.eng.act_tick + 1] / len(obj.path))
                need_energy_substation_next2[path].append(
                    psm.forecasts.hospital[wayHospital][psm.eng.act_tick + 2] / len(obj.path))

        if obj.type == 'factory':
            if not flag_Factory:
                for i in range(0, 8):
                    if psm.forecasts.factory[i][psm.eng.act_tick] == obj.power.now.consumed:
                        wayFactory = i
                        flag_Factory = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                    need_energy_substation_next2[path] = []
                need_energy_substation[path].append(
                    psm.forecasts.factory[wayFactory][psm.eng.act_tick + 1] / len(obj.path))
                need_energy_substation_next2[path].append(
                    psm.forecasts.factory[wayFactory][psm.eng.act_tick + 2] / len(obj.path))

        if obj.type == 'houseA':
            if not flag_HouseA:
                for i in range(0, 8):
                    if psm.forecasts.houseA[i][psm.eng.act_tick] == obj.power.now.consumed:
                        wayHouseA = i
                        flag_HouseA = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                    need_energy_substation_next2[path] = []
                need_energy_substation[path].append(psm.forecasts.houseA[wayHouseA][psm.eng.act_tick + 1])
                need_energy_substation_next2[path].append(
                    psm.forecasts.houseA[wayHouseA][psm.eng.act_tick + 2] / len(obj.path))

        if obj.type == 'houseB':
            if not flag_HouseB:
                for i in range(0, 8):
                    if psm.forecasts.houseB[i][psm.eng.act_tick] == obj.power.now.consumed:
                        wayHouseB = i
                        flag_HouseB = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                    need_energy_substation_next2[path] = []
                need_energy_substation[path].append(psm.forecasts.houseB[wayHouseB][psm.eng.act_tick + 1])
                need_energy_substation_next2[path].append(
                    psm.forecasts.houseB[wayHouseB][psm.eng.act_tick + 2] / len(obj.path))

        # Определяем сколько сгенерируем энергии. Для ветра неопределенный коэффициент не обязателен
        if obj.type == 'solar':
            itr_sun += 1
            for path in obj.path:
                if not path in list(gen_energy_substation):
                    gen_energy_substation[path] = []
                    gen_energy_substation_next2[path] = []
                if flag_Sun:
                    gen_energy_substation[path].append(
                        sun_k[itr_sun] * psm.forecasts.sun[max(waySun, 0)][psm.eng.act_tick + 1])
                    gen_energy_substation_next2[path].append(
                        sun_k[itr_sun] * psm.forecasts.sun[max(waySun, 0)][psm.eng.act_tick + 2])
                else:
                    gen_energy_substation[path].append(
                        INDEFINITE_SUN_NEXT * psm.forecasts.sun[max(waySun, 0)][psm.eng.act_tick + 1])
                    gen_energy_substation_next2[path].append(
                        INDEFINITE_SUN_NEXT * psm.forecasts.sun[max(waySun, 0)][psm.eng.act_tick + 2])

        if obj.type == 'wind':
            itr_wind += 1
            for path in obj.path:
                if not path in list(gen_energy_substation):
                    gen_energy_substation[path] = []
                    gen_energy_substation_next2[path] = []

                # предсказание на ход вперед
                w_0 = psm.forecasts.wind[max(wayWind, 0)][psm.eng.act_tick]
                w_p1 = psm.forecasts.wind[max(wayWind, 0)][psm.eng.act_tick + 1]
                w_p2 = psm.forecasts.wind[max(wayWind, 0)][psm.eng.act_tick + 2]
                if psm.eng.act_tick > 0:
                    g_n1 = obj.power.then[-1].generated
                else:
                    g_n1 = 0
                g_0 = obj.power.now.generated

                _solve = wind_solve([w_0, w_p1, g_n1, g_0], *POPT_ALL)
                if _solve < 2 or abs(_solve - g_0) < 2:
                    _solve = wind_solve([w_0, w_p1, g_n1, g_0], *POPT_LITTLE)
                    gen_energy_substation[path].append(min(max(0, K_LITTLE * _solve), 15))
                else:
                    gen_energy_substation[path].append(min(max(0, K_ALL * _solve), 15))

                # предсказание на 2 хода вперед
                _solve2 = wind_solve([w_p1, w_p2, g_0, gen_energy_substation[path][-1]], *POPT_ALL)  # !!!!!!!!!!!!!
                if _solve2 < 2 or abs(_solve2 - gen_energy_substation[path][-1]) < 2:
                    _solve2 = wind_solve([w_p1, w_p2, g_0, gen_energy_substation[path][-1]], *POPT_LITTLE)
                    gen_energy_substation_next2[path].append(min(max(0, K_LITTLE * _solve2), 15))
                else:
                    gen_energy_substation_next2[path].append(min(max(0, K_ALL * _solve2), 15))

    # определение необходимой энергии системе с плохой реализацией потерь (на следующий ход)
    for address_powerarea in list(need_energy_substation):
        energy_powerarea = sum(need_energy_substation[address_powerarea])

        energy_powerarea += loss(energy_powerarea) * energy_powerarea
        need_energy_next += energy_powerarea + 3  # условно +3

    # определение генерируемой энергии в системе с плохой реализацией потерь (на следующий ход)
    for address_powerarea in list(gen_energy_substation):
        energy_powerarea = sum(gen_energy_substation[address_powerarea])

        energy_powerarea -= loss(energy_powerarea) * energy_powerarea
        gen_energy_next += energy_powerarea - 3  # условно -3

    energy_balance = gen_energy_next - need_energy_next

    # определение необходимой энергии системе с плохой реализацией потерь (через ход)
    for address_powerarea in list(need_energy_substation_next2):
        energy_powerarea = sum(need_energy_substation_next2[address_powerarea])

        energy_powerarea += loss(energy_powerarea) * energy_powerarea
        need_energy_next2 += energy_powerarea + 3  # условно +3

    # определение генерируемой энергии в системе с плохой реализацией потерь (через ход)
    for address_powerarea in list(gen_energy_substation_next2):
        energy_powerarea = sum(gen_energy_substation_next2[address_powerarea])

        energy_powerarea -= loss(energy_powerarea) * energy_powerarea
        gen_energy_next2 += energy_powerarea - 3  # условно -3

    energy_balance_next2 = gen_energy_next2 - need_energy_next2

    def dis_or_charge(obj, power):
        global charges_in_next2  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        addr = obj.address[0] + obj.address[1]
        remains_power = abs(power)

        if power >= 0:
            if 'c' in addr:
                power_sent = min(power, 15, 60 - obj.charge.now)
                charges_in_next2[addr] = obj.charge.now + power_sent
            else:
                power_sent = min(power, 10, 35 - obj.modules[0].charge)
                if addr not in list(charges_in_next2):
                    charges_in_next2[addr] = []
                charges_in_next2[addr].append(obj.modules[0].charge + power_sent)

            psm.orders.charge(addr, power_sent)
        else:
            power = abs(power)
            power_sent = 0
            if 'c' in addr:
                power_sent = min(power, 15, obj.charge.now)
                charges_in_next2[addr] = obj.charge.now - power_sent
            '''
            else:
                power_sent = min(power, 10, obj.modules[0].charge)
                if addr not in list(charges_in_next2):
                    charges_in_next2[addr] = []
                charges_in_next2[addr].append(obj.modules[0].charge - power_sent)
            '''
            psm.orders.discharge(addr, power_sent)

        remains_power -= power_sent

        return remains_power, power_sent  # осталось и потратили

    def set_diesel(obj, power):
        addr = obj.address[0] + obj.address[1]
        remains_power = abs(power)

        power_set = min(abs(power), 5)
        psm.orders.diesel(addr, power_set)

        remains_power -= power_set

        return remains_power, power_set  # осталось и потратили

    # на следующий ход
    # разряд накопителей и аккумов (Надо вместо серых комментариев ниже поставить действия разрядки)
    if energy_balance < 0:
        for obj in psm.objects:
            if obj.type == "storage":
                if energy_balance < 0:
                    print(obj)
                    remains_power, power_sent = dis_or_charge(obj, energy_balance)
                    energy_balance += power_sent
                else:
                    break

            if obj.type in station_names:
                for module in obj.modules:
                    if isinstance(module, Cell):  # !!!!!!!!!!!!!! на стенде писать ips.Cell
                        if energy_balance < 0:
                            remains_power, power_sent = dis_or_charge(obj, energy_balance)
                            energy_balance += power_sent
                        else:
                            break

        if energy_balance < 0:
            for obj in psm.objects:
                if obj.type in station_names:
                    for module in obj.modules:
                        if isinstance(module, Diesel):  # !!!!!!!!!!!!!! на стенде писать ips.Diesel
                            if energy_balance < 0:
                                remains_power, power_set = set_diesel(obj, energy_balance)
                                energy_balance += power_set
                            else:
                                break



    # Это зарядка накопителя/аккума
    elif energy_balance > 0:
        for obj in psm.objects:
            if obj.type == "storage":
                if energy_balance > 0:
                    remains_power, power_sent = dis_or_charge(obj, energy_balance)
                    energy_balance -= power_sent

    # через 1 хода
    if energy_balance_next2 < 0:
        for key in list(charges_in_next2):
            if isinstance(charges_in_next2[key], list):
                for value in charges_in_next2[key]:
                    energy_balance_next2 += min(value, abs(energy_balance_next2), 10)
            else:
                energy_balance_next2 += min(charges_in_next2[key], abs(energy_balance_next2), 15)

        if energy_balance_next2 < 0:
            for _ in range(0, count_diesels):
                energy_balance_next2 += min(abs(energy_balance_next2), 5)


    # Это зарядка накопителя/аккума
    elif energy_balance_next2 > 0:
        for key in list(charges_in_next2):
            if isinstance(charges_in_next2[key], list):
                for value in charges_in_next2[key]:
                    energy_balance_next2 -= min(max(0, 35 - value), energy_balance_next2, 10)
            else:
                energy_balance_next2 -= min(max(0, 60 - charges_in_next2[key]), energy_balance_next2, 15)

    else:
        pass

    if energy_balance_next2 < 0:
        psm.orders.buy(energy_balance_next2, price_in)
    else:
        psm.orders.sell(energy_balance_next2, price_out)

    '''
    написали:
    1) потребление зданий
    2) выработка солнца
    3) потери учитываем                               <--- переделать во время тестовых игр
    4) предсказали колонку погоды и потребеления
    5) записываем/читаем переменные из файла/в файл
    6) предсказание генерации
    7) выгрузку из накопителей недостающей энергии    <--- немного доделать
    8) сделать комментарии                            <--- Ваня, допиши некоторые комменты
    9) ставим дизели
    10) определение генерации при неопределенном столбце (для ветра) <--- не обязательно
    11) продажа/покупка на бирже
    '''

    output_data = {
        'flag_Sun': flag_Sun,
        'flag_Hospital': flag_Hospital,
        'flag_Factory': flag_Factory,
        'flag_HouseA': flag_HouseA,
        'flag_HouseB': flag_HouseB,

        'waySun': waySun,
        'wayWind': wayWind,
        'wayHospital': wayHospital,
        'wayFactory': wayFactory,
        'wayHouseA': wayHouseA,
        'wayHouseB': wayHouseB,

        'wind_way': wind_way,
        'sun_k': sun_k
    }
    with open('./vars', 'w') as f:
        f.write(str(output_data))

    psm.save_and_exit()
