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


def player_actions():
    global flag_Sun
    global flag_Hospital
    global flag_Factory
    global flag_HouseA
    global flag_HouseB

    global waySun
    global wayWind
    global wayHospital
    global wayFactory
    global wayHouseA
    global wayHouseB

    global wind_way
    global sun_k

    from collections import defaultdict
    psm = ips.init()

    '''
    {
        waySun: 1,
        wayWind: [7],
        wayHospital: 2,
        wayFactory: 3,
        wayHouseA: 4,
        wayHouseB: 6
    }

    если у нас отключается верряк, то ставим дизель <--- нужно написать
    генерация ветра <--- написать
    записывать и читать переменные в файл
    продажа на бирже
    выгрузку из накопителей недостающей энергии
    '''

    if psm.tick != 0:
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
        wind_k = input_data['wind_k']
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
        wind_k = []
        sun_k = []

    loss = lambda power: power * 20 / 100 if power > 23 else power * (power * 20 / 23) / 100

    need_energy_next = 0
    need_energy_substation = defaultdict(set)

    gen_energy_next = 0
    gen_energy_substation = defaultdict(set)

    itr_sun = -1
    itr_wind = -1

    if psm.sun.now != 0 and not flag_Sun:
        for i in range(0, 8):
            if psm.forecasts.sun[i][psm.tick] == psm.sun.now:
                waySun = i
                flag_Sun = True
                break
        for obj in psm.objects:
            if obj.type == 'solar':
                sun_k.append(obj.power.now.generated / psm.sun.now)
    # gen_n = weather_s * sun_k[n]

    for i, way in enumerate(wind_way):
        if psm.forecasts.wind[way][psm.tick] != psm.wind.now:
            wind_way.pop(i)
    wayWind = wind_way[0]

    for obj in psm.objects:
        # потребление
        if obj.type == 'hospital':
            if not flag_Hospital:
                for i in range(0, 8):
                    if psm.forecasts.hospital[i][psm.tick] == obj.power.now.consumed:
                        wayHospital = i
                        flag_Hospital = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                need_energy_substation[path].append(psm.forecasts.hospital[wayHospital][psm.tick + 1] / len(obj.path))

        if obj.type == 'factory':
            if not flag_Factory:
                for i in range(0, 8):
                    if psm.forecasts.factory[i][psm.tick] == obj.power.now.consumed:
                        wayFactory = i
                        flag_Factory = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                need_energy_substation[path].append(psm.forecasts.factory[wayFactory][psm.tick + 1] / len(obj.path))

        if obj.type == 'houseA':
            if not flag_HouseA:
                for i in range(0, 8):
                    if psm.forecasts.houseA[i][psm.tick] == obj.power.now.consumed:
                        wayHouseA = i
                        flag_HouseA = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                need_energy_substation[path].append(psm.forecasts.houseA[wayHouseA][psm.tick + 1])

        if obj.type == 'houseB':
            if not flag_HouseB:
                for i in range(0, 8):
                    if psm.forecasts.houseB[i][psm.tick] == obj.power.now.consumed:
                        wayHouseB = i
                        flag_HouseB = True
                        break

            for path in obj.path:
                if not path in list(need_energy_substation):
                    need_energy_substation[path] = []
                need_energy_substation[path].append(psm.forecasts.houseB[wayHouseB][psm.tick + 1])

        # генерация
        if obj.type == 'solar':
            itr_sun += 1
            for path in obj.path:
                if not path in list(gen_energy_substation):
                    gen_energy_substation[path] = []
                if flag_Sun:
                    gen_energy_substation[path].append(sun_k[itr_sun] * psm.forecasts.sun[max(waySun, 0)][psm.tick + 1])

    #         if obj.type == 'wind':
    #             itr_wind += 1
    #             for path in obj.path:
    #                 if not path in list(gen_energy_substation):
    #                     gen_energy_substation[path] = []
    #                 gen_energy_substation[path].append( * psm.forecasts.wind[max(wayWind, 0)][psm.tick + 1])

    for address_powerarea in list(need_energy_substation):
        energy_powerarea = 0
        for power in need_energy_substation[address_powerarea]:
            energy_powerarea += power
        energy_powerarea += loss(energy_powerarea)
        need_energy_next += energy_powerarea + 3  # условно

    print(need_energy_next)

    '''
    написали:
    1) потребление зданий
    2) выработка солнца
    3) потери учитываем
    4) предсказали колонку погоды и потребеления
    5) открыли файлик)))
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
        'wind_k': wind_k,
        'sun_k': sun_k
    }
    with open('./vars', 'w') as f:
        f.write(str(output_data))

    psm.save_and_exit()
