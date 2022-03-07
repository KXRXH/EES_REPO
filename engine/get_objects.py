from engine_const import *
from engine.engine import Engine


def get_objects(eng: Engine, modules: dict):
    score_then_solar = [[] for _ in range(0, eng.count_wind)]
    power_then_solar = [[] for _ in range(0, eng.count_solar)]

    data_obj = []
    id_itr = 1

    # Главная подстанция
    address_itr = 1
    for itr in range(eng.count_substation):
        address = "M" + hex(address_itr)[2:]
        contract = contract_substation[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        modules = []

        for itr_accamulator, connect in enumerate(connected_accamulator):
            if address == connect:
                score_now_loss += cost_accamulator
                modules.append(
                    {"delta": delta_accamulator[itr_accamulator], "charge": charge_accamulator[itr_accamulator],
                     "type": "cell"})

        for itr_diesel, connect in enumerate(connected_diesel):
            if address == connect:
                score_now_loss += COST_DIESEL
                score_now_loss += power_diesel[itr_diesel] * cost_MW_diesel
                power_now_generated += power_diesel[itr_diesel]
                modules.append({"power": power_diesel[itr_diesel], "type": "diesel"})

        data_obj.append(
            {
                "id": ["main", id_itr],
                "address": address,
                "contract": contract,
                "line": line_substation[itr],
                "path": path_substation[itr],
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_substation[itr].copy()},
                "power": {"now": {"online": online_substation[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_substation[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "main"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_substation[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_substation[itr].append(
            {"online": online_substation[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Мини подстанция Б
    address_itr = 1
    for itr in range(0, qty_mini_substationB):
        address = prefix_address_mini_substationB + hex(address_itr)[2:]
        contract = contract_mini_substationB[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_mini_substationB[itr])):
            path.append([{"line": line_mini_substationB[itr][itr_line], "id": path_mini_substationB[itr][itr_line]}])

        score_now_loss += contract

        for itr_accamulator, connect in enumerate(connected_accamulator):
            if address == connect:
                score_now_loss += cost_accamulator
                modules.append(
                    {"delta": delta_accamulator[itr_accamulator], "charge": charge_accamulator[itr_accamulator],
                     "type": "cell"})

        for itr_diesel, connect in enumerate(connected_diesel):
            if address == connect:
                score_now_loss += COST_DIESEL
                score_now_loss += power_diesel[itr_diesel] * cost_MW_diesel
                power_now_generated += power_diesel[itr_diesel]
                modules.append({"power": power_diesel[itr_diesel], "type": "diesel"})

        data_obj.append(
            {
                "id": ["miniB", id_itr],
                "address": address,
                "contract": contract,
                "line": line_mini_substationB[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_mini_substationB[itr].copy()},
                "power": {"now": {"online": online_mini_substationB[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_mini_substationB[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "miniB"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_mini_substationB[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_mini_substationB[itr].append(
            {"online": online_mini_substationB[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Мини подстанция А
    address_itr = 1
    for itr in range(0, qty_mini_substationA):
        address = prefix_address_mini_substationA + hex(address_itr)[2:]
        contract = contract_mini_substationA[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_mini_substationA[itr])):
            path.append([{"line": line_mini_substationA[itr][itr_line], "id": path_mini_substationA[itr][itr_line]}])

        score_now_loss += contract

        for itr_accamulator, connect in enumerate(connected_accamulator):
            if address == connect:
                score_now_loss += cost_accamulator
                modules.append(
                    {"delta": delta_accamulator[itr_accamulator], "charge": charge_accamulator[itr_accamulator],
                     "type": "cell"})

        for itr_diesel, connect in enumerate(connected_diesel):
            if address == connect:
                score_now_loss += COST_DIESEL
                score_now_loss += power_diesel[itr_diesel] * cost_MW_diesel
                power_now_generated += power_diesel[itr_diesel]
                modules.append({"power": power_diesel[itr_diesel], "type": "diesel"})

        data_obj.append(
            {
                "id": ["miniA", id_itr],
                "address": address,
                "contract": contract,
                "line": line_mini_substationA[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_mini_substationA[itr].copy()},
                "power": {"now": {"online": online_mini_substationA[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_mini_substationA[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "miniA"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_mini_substationA[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_mini_substationA[itr].append(
            {"online": online_mini_substationA[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Накопитель
    address_itr = 1
    for itr in range(0, qty_storage):
        address = prefix_address_storage + hex(address_itr)[2:]
        contract = contract_storage[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_storage[itr])):
            path.append([{"line": line_storage[itr][itr_line], "id": path_storage[itr][itr_line]}])

        score_now_loss += contract

        if delta_storage[itr] < 0:
            power_now_generated += delta_storage[itr]

        if delta_storage[itr] > 0:
            power_now_consumed += delta_storage[itr]

        data_obj.append(
            {
                "id": ["storage", id_itr],
                "address": address,
                "contract": contract,
                "line": line_storage[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_storage[itr].copy()},
                "power": {"now": {"online": online_storage[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_storage[itr].copy()},
                "charge": {"now": charge_storage[itr],
                           "then": charge_then_storage[itr].copy()},
                "modules": modules,
                "class": "storage"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_storage[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_storage[itr].append(
            {"online": online_storage[itr], "consumed": power_now_consumed, "generated": power_now_generated})
        charge_then_storage[itr].append(charge_storage[itr])

    # Солнечка
    address_itr = 1
    for itr in range(0, qty_solar):
        address = prefix_address_solar + hex(address_itr)[2:]
        contract = contract_solar[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_solar[itr])):
            path.append([{"line": line_solar[itr][itr_line], "id": path_solar[itr][itr_line]}])

        score_now_loss += contract

        power_now_generated += min(eng.get_by_type('solar') * koaf_solar_gen[itr], max_power_solar)

        data_obj.append(
            {
                "id": ["solar", id_itr],
                "address": address,
                "contract": contract,
                "line": line_solar[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_solar[itr].copy()},
                "power": {"now": {"online": eng.online_solar[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_solar[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "solar"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_solar[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_solar[itr].append(
            {"online": eng.online_solar[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Ветряк
    address_itr = 1
    for itr in range(0, qty_wind):
        address = prefix_address_wind + hex(address_itr)[2:]
        contract = contract_wind[itr]
        score_now_income = 0
        score_now_loss = 0 # отличия
        power_now_generated = 0 # отличия
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_wind[itr])):
            path.append([{"line": line_wind[itr][itr_line], "id": path_wind[itr][itr_line]}])

        score_now_loss += contract

        if online_wind[itr]:
            power_now_generated += min(eng.get_by_type('wind') ** 3 * koaf_wind_gen[itr], max_power_wind)

        data_obj.append(
            {
                "id": ["wind", id_itr],
                "address": address,
                "contract": contract,
                "line": line_wind[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_wind[itr].copy()},
                "power": {"now": {"online": online_wind[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_wind[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "wind"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_wind[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_wind[itr].append(
            {"online": online_wind[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Больницы
    address_itr = 1
    for itr in range(0, qty_hospital):
        address = prefix_address_hospital + hex(address_itr)[2:]
        contract = contract_hospital[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_hospital[itr])):
            path.append([{"line": line_hospital[itr][itr_line], "id": path_hospital[itr][itr_line]}])

        power_now_consumed += eng.get_by_type('hospital')

        score_now_income += contract_hospital[itr] * eng.get_by_type('hospital')

        data_obj.append(
            {
                "id": ["hospital", id_itr],
                "address": address,
                "contract": contract,
                "line": line_hospital[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_hospital[itr].copy()},
                "power": {"now": {"online": online_hospital[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_hospital[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "hospital"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_hospital[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_hospital[itr].append(
            {"online": online_hospital[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Заводы
    address_itr = 1
    for itr in range(0, qty_factory):
        address = prefix_address_factory + hex(address_itr)[2:]
        contract = contract_factory[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_factory[itr])):
            path.append([{"line": line_factory[itr][itr_line], "id": path_factory[itr][itr_line]}])

        power_now_consumed += eng.get_by_type("factory")

        score_now_income += contract_factory[itr] * eng.get_by_type('factory')

        data_obj.append(
            {
                "id": ["factory", id_itr],
                "address": address,
                "contract": contract,
                "line": line_factory[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_factory[itr].copy()},
                "power": {"now": {"online": online_factory[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_factory[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "factory"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_factory[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_factory[itr].append(
            {"online": online_factory[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Дом А
    address_itr = 1
    for itr in range(0, qty_houseA):
        address = prefix_address_houseA + hex(address_itr)[2:]
        contract = contract_houseA[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_houseA[itr])):
            path.append([{"line": line_houseA[itr][itr_line], "id": path_houseA[itr][itr_line]}])

        power_now_consumed += eng.get_by_type('houseA')

        score_now_income += contract_houseA[itr] * eng.get_by_type('houseA')

        data_obj.append(
            {
                "id": ["houseA", id_itr],
                "address": address,
                "contract": contract,
                "line": line_houseA[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_houseA[itr].copy()},
                "power": {"now": {"online": online_houseA[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_houseA[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "houseA"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_houseA[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_houseA[itr].append(
            {"online": online_houseA[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    # Дом Б
    address_itr = 1
    for itr in range(0, qty_houseB):
        address = prefix_address_houseB + hex(address_itr)[2:]
        contract = contract_houseB[itr]
        score_now_income = 0
        score_now_loss = 0
        power_now_generated = 0
        power_now_consumed = 0
        path = []
        modules = []

        for itr_line in range(0, len(line_houseB[itr])):
            path.append([{"line": line_houseB[itr][itr_line], "id": path_houseB[itr][itr_line]}])

        power_now_consumed += eng.get_by_type('houseB')

        score_now_income += contract_houseB[itr] * eng.get_by_type('houseB')

        data_obj.append(
            {
                "id": ["houseB", id_itr],
                "address": address,
                "contract": contract,
                "line": line_houseB[itr],
                "path": path.copy(),
                "score": {"now": {"loss": score_now_loss, "income": score_now_income},
                          "then": score_then_houseB[itr].copy()},
                "power": {"now": {"online": online_houseB[itr], "consumed": power_now_consumed,
                                  "generated": power_now_generated},
                          "then": power_then_houseB[itr].copy()},
                "charge": {"now": 0,
                           "then": []},
                "modules": modules,
                "class": "houseB"
            }
        )

        id_itr += 1
        address_itr += 1
        score_then_houseB[itr].append({"loss": score_now_loss, "income": score_now_income})
        power_then_houseB[itr].append(
            {"online": online_houseB[itr], "consumed": power_now_consumed, "generated": power_now_generated})

    return data_obj
