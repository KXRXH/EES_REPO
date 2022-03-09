from collections import defaultdict
from engine.engine_const import *
from engine.get_objects import Objects


class Engine:
    def __init__(self):
        # Это типо активный тик.
        self.act_tick = 0

        self.balance_energy = 0

        self.graph_history = dict()
        self.graph_history['exchange_p'] = [0]
        self.graph_history['exchange_n'] = [0]
        self.graph_history['exchange_players_p'] = [0]
        self.graph_history['exchange_players_n'] = [0]
        for name in NAME_OBJECTS:
            if name in TYPE_STATION:
                continue
            if name == 'storage':
                self.graph_history[f'{name}_p'] = [0]
                self.graph_history[f'{name}_n'] = [0]
                continue
            self.graph_history[name] = [0]

        self.auction = 0
        self.consumers = 0
        self.generators = 0
        self.power_system = 0
        self.overload = 0
        self.exchange = 0

        self.delta_auction = 0
        self.delta_consumers = 0
        self.delta_generators = 0
        self.delta_power_system = 0
        self.delta_overload = 0
        self.delta_exchange = 0


    def _update(self):
        self.objs = Objects(self).get_objects()

        self.delta_auction = 0
        self.delta_consumers = 0
        self.delta_generators = 0
        self.delta_power_system = 0
        self.delta_overload = 0
        self.delta_exchange = 0

        self.graph_history['exchange_p'].append(0)
        self.graph_history['exchange_n'].append(0)
        self.graph_history['exchange_players_p'].append(0)
        self.graph_history['exchange_players_n'].append(0)
        for name in NAME_OBJECTS:
            if name in TYPE_STATION:
                continue
            if name == 'storage':
                self.graph_history[f'{name}_p'].append(0)
                self.graph_history[f'{name}_n'].append(0)
                continue
            self.graph_history[name].append(0)

        self.calc_money_and_energy()



        self.consumers += self.delta_consumers
        self.generators += self.delta_generators
        self.power_system += self.delta_power_system


    def calc_money_and_energy(self):
        self.received_energy = 0
        self.spent_energy = 0
        self.money_generators = 0
        self.received_consumer = 0

        for obj in self.objs:
            self.received_energy += obj['power']['now']['generated']
            self.spent_energy += obj['power']['now']['consumed']
            self.money_generators += obj['score']['now']['loss']
            self.received_consumer += obj['score']['now']['income']

            type = obj['class']
            if type in TYPE_STATION:
                continue
            if type == 'storage':
                if len(obj['score']['then']) == 0:
                    self.delta_power_system -= obj['score']['now']['loss']
                else:
                    self.delta_power_system -= obj['score']['now']['loss'] - obj['score']['then'][-1]['loss']

                self.graph_history[f'{type}_p'][-1] += obj['power']['now']['generated']
                self.graph_history[f'{type}_n'][-1] += obj['power']['now']['consumed']
                continue
            elif type in TYPE_CUSTOMERS:
                if len(obj['score']['then']) == 0:
                    self.delta_consumers += obj['score']['now']['income']
                else:
                    self.delta_consumers += obj['score']['now']['income'] - obj['score']['then'][-1]['income']

                self.graph_history[type][-1] += obj['power']['now']['consumed']
            else:
                if len(obj['score']['then']) == 0:
                    self.delta_generators -= obj['score']['now']['loss']
                else:
                    self.delta_generators -= obj['score']['now']['loss'] - obj['score']['then'][-1]['loss']

                self.graph_history[type][-1] += obj['power']['now']['generated']

    # Биржа энергии между игроками
    def get_bidding_players(self):
        return None, None

    # если энергии все еще не хватает, то покупаем из внешней сети
    def get_money_remains(self):
        _balance_energy = self.balance_energy

        if _balance_energy < 0:
            cost_power_instant = abs(_balance_energy) * received_power_instant
            self.graph_history['exchange_p'][-1] += abs(_balance_energy)
            self.graph_history['exchange_n'][-1] += 0
            self.delta_exchange -= cost_power_instant
        else:
            cost_power_instant = abs(_balance_energy) * spent_power_instant
            self.graph_history['exchange_p'][-1] += 0
            self.graph_history['exchange_n'][-1] += abs(_balance_energy)
            self.delta_exchange += cost_power_instant

        self.exchange += self.delta_exchange

        return cost_power_instant
