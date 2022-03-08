import pprint
import random

patterns = []

input_data = \
    {
        "Consumers": {
            "HouseB": 2,
            "HouseA": 1,
            "Hospital": 0,
            "Factory": 0,
        },
        "PowerPlants": {
            "Solar": 1,
            "Wind": 0,
            "Heat": 0
        },
        "Other": {
            "Battery": 0
        }
    }
# M2 e2 m3 m4 (e - A)
prepare = \
    [
        {
            "address": "e2",
            "station": "M2",
            "line": 1
            # Подстанция А1
        },
        {
            "address": "m3",
            "station": "M2",
            "line": 2
            # Подстанция Б1
        },
        {
            "address": "e4",
            "station": "M2",
            "line": 3
            # Подстанция Б2
        }

    ]

out_data = prepare[:]
house_addresses = {}
houses = {"HouseA1": "h1", "HouseB1": "d1", "HouseB2": "d2"}
used_stations = set()
if 2 <= len(list(houses.keys())) <= 3:
    cur_station = random.choice(prepare)
    used_stations.add(cur_station["address"])
    for k in houses:
        data: dict[str, str, int] = \
            {
                "address": houses[k],
                "line": cur_station["line"],
                "station": cur_station["address"]
            }
        out_data.append(data)

# Вывод в нужном виде
q = pprint.pformat(out_data, width=1).replace("'", '"')
print(q)
