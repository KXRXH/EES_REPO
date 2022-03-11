def get_networks(eng):
    loss = lambda value: round(((25 * value) / 30) / 100, 3) if value < 30 else 0.25

    power_area = dict()
    for obj in eng.objs:
        for path in obj['path'][0]:
            if str(path) not in list(power_area):
                power_area[str(path)] = dict()

                power_area[str(path)]['upflow'] = 0
                power_area[str(path)]['online'] = 0
                power_area[str(path)]['upflow'] = 0
                power_area[str(path)]['upflow'] = 0
                power_area[str(path)]['upflow'] = 0
                power_area[str(path)]['upflow'] = 0



            # {"upflow": 0.012876051995489336,
            #  "online": true,
            #  "location": [{"line": 2, "id": ["main", 1]}, {"line": 1, "id": ["miniB", 1]}],
            #  "downflow": 0,
            #  "owner": {"place": 1, "player": 1},
            #  "wear": 0.28434246649966055,
            #  "broken": 0,
            #  "losses": 4.269511237383201e-09, "id": 5},