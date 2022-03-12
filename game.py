import engine
from engine import Engine
from graph import Graph
from player_code import player_actions


class Game:
    def __init__(self, fig, ax):
        self.eng = Engine()
        self.trade_players = 0
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
        print('Тик:', i)
        print('\nВывод игрока:')

    def one_tick(self, i):
        self.reset_vars()
        self.eng.act_tick = i
        self.eng._update()

        print(f'=============================================== {i} =================================================')
        # Погода

        # Данные по энергии
        received_energy = self.eng.received_energy  # получено
        spent_energy = self.eng.spent_energy  # потрачено
        self.eng.balance_energy = received_energy - spent_energy  # баланс

        # Оплата за генераторы
        self.all_spent_money = self.eng.money_generators

        # Прибыль
        received_consumer = self.eng.received_consumer
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

        self.graph.update_engine(self.fig, self.ax, self.eng)
        self.graph.draw_first_graph(i)
        self.graph.draw_second_graph(i, end_tick=engine.end_tick)
