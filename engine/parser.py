from engine.engine_const import *

def parser():
    with open('topology.json', 'r', encoding="utf-8") as f:
        DATA = eval(f.read())
        DATA.insert(0,
            {"address": "M2",
             "line": 0,
             "station": "M2",
             "comment": 0}
        )

    objects = dict()
    count_type = dict()
    for name in NAME_OBJECTS:
        count_type[name] = 0

    _id = 0

    for obj in DATA:
        _id += 1
        address = obj['address']
        type = PREFIX_FOR_OBJECTS[address[0]]
        prefix = PREFIX_OBJECTS[type]
        line = obj['line']
        path = PREFIX_FOR_OBJECTS[obj['station'][0]]
        contract = obj['comment']

        count_type[type] += 1
        objects[address] = {
            'id': _id,
            'type': type,
            'prefix': prefix,
            'line': line,
            'path': path,
            'contract': contract
        }

    return count_type, objects
