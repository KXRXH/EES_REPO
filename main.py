import engine
from engine import Engine


def read_file(file_name):
    with open(file_name, 'r', encoding="utf-8") as file:
        data = file.read()
    return eval(data)


consumers = read_file("consumer.json")
generators = read_file("generators.json")


def one_tick(i):
    eng = Engine(
        generators["solar"]["count"],
        generators["wind"]["count"],
        consumers
    )
