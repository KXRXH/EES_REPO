import engine
from engine import Engine
from graph import Graph
from player_code import player_actions


class Game:
    def __init__(self, fig, ax):
        self.consumers = self.read_file("consumer.json")
        self.generators = self.read_file("generators.json")
        self.eng = Engine(
            self.generators["solar"]["count"],
            self.generators["wind"]["count"],
            self.consumers
        )
        self.all_spent_money = 0
        self.all_received_money = 0
        self.balance_money = 0

        self.fig = fig
        self.ax = ax
        self.graph = Graph(self.ax, self.fig, self.eng)

    @staticmethod
    def read_file(file_name):
        with open(file_name, 'r', encoding="utf-8") as file:
            data = file.read()
        return eval(data)

    def reset_vars(self):
        self.all_received_money = 0
        self.all_spent_money = 0

    def print_tick(self, i):
        print('\n--------------------------------------------------------------------------')
        print(f'Тик: {i}')
        print('\nВывод игрока:')

    def one_tick(self, i):
        self.reset_vars()
        self.eng.act_tick = i
        # Оплата за генераторы
        spent_money_generators = self.eng.get_money_generators(self.generators)
        self.all_spent_money += spent_money_generators
        '''
        # Биржа энергии между игроками
        energy_player, money_player = 0, 0
        if trade_players != 0 and False:  # не реализовано!!!!!!!!!!!!!
            energy_player, money_player = get_bidding_players()
            balance_energy += energy_player
            if money_player < 0:
                all_spent_money -= money_player
            else:
                all_received_money += money_player
        '''
        # Прибыль
        received_consumer = self.eng.get_received_consumer(self.generators)
        self.all_received_money += received_consumer

        # Действия игрока (на следующий тик)
        player_actions(self.eng, self.all_received_money - self.all_spent_money)

        # если энергия != 0, то продаем во внешнюю сеть
        self.balance_money += self.all_received_money - self.all_spent_money
        self.reset_vars()
        if self.eng.balance_energy < 0:
            spent_to_external_network = self.eng.get_money_remains()
            self.all_spent_money += spent_to_external_network
        else:
            received_from_external_network = self.eng.get_money_remains()
            self.all_received_money += received_from_external_network

        # Баланс денег
        self.balance_money += self.all_received_money - self.all_spent_money

        self.graph.update_engine(self.eng)
        self.graph.draw_first_graph(i, crash_tick=engine.crash_tick)
        self.graph.draw_second_graph(i, end_tick=engine.end_tick)

