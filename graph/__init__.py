import engine


class Graph:
    def __init__(self, ax, fig, eng):
        self.data_actions = []

        self.total = 0
        self.delta_total = 0

        self.energy_exchange_p_data = [0]
        self.energy_exchange_n_data = [0]

        self.max_energy_data = 0.01

        self.update_engine(fig, ax, eng)

    def update_engine(self, fig, ax, new_engine):
        self.eng = new_engine
        self.fig = fig
        self.ax = ax
        self.fig.set_figwidth(20), self.fig.set_figheight(10)

        self.ax[0].clear(), self.ax[1].clear()

        self.ax[0].set_xlim(0, 101), self.ax[1].set_xlim(1, 100)
        self.generated_Total()

    @staticmethod
    def normalise_y_data(y1, y2, k=1) -> list:
        return [k * (y1[i] + k * (y2[i])) for i in range(0, len(y1))]

    @staticmethod
    def normalise_num_for_str(data) -> str:
        data = round(data, 2)
        if data >= 0:
            return "".join(('+', str(data), engine.RUBLE))
        return "".join((str(data), engine.RUBLE))

    def generated_Total(self):
        self.delta_total = self.eng.delta_consumers + \
                           self.eng.delta_generators + self.eng.delta_power_system + \
                           self.eng.delta_exchange
        self.total = self.eng.consumers + self.eng.generators + self.eng.power_system + self.eng.exchange

    def max_value_data_graph(self) -> int:

        positive_value = self.eng.history['solar'][-1] + self.eng.history['wind'][-1] + \
                         self.eng.history['storage'][-1] \
                         + self.eng.history['diesel'][-1] + self.energy_exchange_p_data[-1]

        negative_value = self.eng.history["hospital"][-1] + self.eng.history["factory"][-1] + \
                         self.eng.history["houseA"][-1] \
                         + self.eng.history["houseB"][-1] + self.eng.history['storage_n'][-1] \
                         + self.energy_exchange_n_data[-1]

        if positive_value > self.max_energy_data:
            self.max_energy_data = positive_value
        if negative_value > self.max_energy_data:
            self.max_energy_data = negative_value

        return self.max_energy_data

    def draw_first_graph(self, act_tick: int, crash_tick: list):
        # Настройка 1 графика
        self.ax[0].title.set_text('Генерация/потребление энергии:')
        self.ax[0].title.set_fontsize(30)
        self.ax[0].title.set_fontweight('bold')

        self.ax[0].grid()

        self.ax[0].spines['left'].set_linewidth(2)
        self.ax[0].spines['left'].set_color('black')

        main_axis_x = list(range(0, 101))
        main_axis_y = [0 for _ in range(0, 101)]
        self.ax[0].plot(main_axis_x, main_axis_y, color='black', linewidth=2)

        # Рисование 1 графика
        y_solar = self.normalise_y_data(self.eng.history['solar'], main_axis_y)

        y_wind = self.normalise_y_data(self.eng.history['wind'], y_solar)

        y_accamulator_p = self.normalise_y_data(self.eng.history['storage'], y_wind)
        self.ax[0].fill_between(main_axis_x[:act_tick + 2], y_accamulator_p, y_wind, facecolor='#3737FF')

        y_diesel = self.normalise_y_data(self.eng.history['diesel'], y_accamulator_p)
        self.ax[0].fill_between(main_axis_x[:act_tick + 2], y_diesel, y_accamulator_p, facecolor='#9C9C9C')

        y_exchange_p = self.normalise_y_data(self.energy_exchange_p_data, y_diesel)
        self.ax[0].fill_between(main_axis_x[:act_tick + 2], y_exchange_p, y_diesel, facecolor='#000000')

        y_hospital = self.normalise_y_data(self.eng.history["hospital"], main_axis_y, k=-1)
        self.ax[0].fill_between(main_axis_x[:act_tick + 2], y_hospital, main_axis_y[:act_tick + 2], facecolor='#FF9494')

        y_factory = self.normalise_y_data(self.eng.history["factory"], y_hospital, k=-1)
        self.ax[0].fill_between(main_axis_x[:act_tick + 2], y_factory, y_hospital, facecolor='#FFFDBB')

        y_house_a = self.normalise_y_data(self.eng.history["houseA"], y_factory, k=-1)
        self.ax[0].fill_between(main_axis_x[:act_tick + 2], y_house_a, y_factory, facecolor='#9DC941')
        self.ax[0].fill_between(main_axis_x[:act_tick + 2], y_wind, y_solar, facecolor='#A3FFFF')
        self.ax[0].fill_between(main_axis_x[:act_tick + 2], y_solar, main_axis_y[:act_tick + 2], facecolor='#FFEC14')
        y_house_b = self.normalise_y_data(self.eng.history["houseB"], y_house_a, k=-1)
        self.ax[0].fill_between(main_axis_x[:act_tick + 2], y_house_b, y_house_a, facecolor='#BFE471')
        '''
        y_accamulator_n = self.normalise_y_data(self.eng.history['storage_n'], y_house_b, k=-1)
        self.ax[0].fill_between(main_axis_x[:act_tick + 2], y_accamulator_n, y_house_b, facecolor='#3737FF')
        y_exchange_n = self.normalise_y_data(self.energy_exchange_n_data, y_accamulator_n, k=-1)
        self.ax[0].fill_between(main_axis_x[:act_tick + 2], y_exchange_n, y_accamulator_n, facecolor='#000000')

        '''
        for start, end in crash_tick:
            self.ax[0].plot(range(start + 1, end + 1), [0 for _ in range(start + 1, end + 1)], color='red',
                            linestyle=' ', marker='o')

        # Донастройка 1 графика
        y_lim_max = max(abs(self.ax[0].get_ylim()[0]), abs(self.ax[0].get_ylim()[1]))
        self.ax[0].set_ylim(-y_lim_max, y_lim_max)

        self.ax[0].set_xticks([])
        self.ax[0].set_yticks([-self.max_value_data_graph(), self.max_value_data_graph()])
        self.ax[0].tick_params(labelsize=14)

    def draw_second_graph(self, act_tick: int, end_tick: int):
        # Настройка 2 графика
        self.ax[1].title.set_text('Данные по игре:')
        self.ax[1].title.set_fontsize(30)
        self.ax[1].title.set_fontweight('bold')

        self.ax[1].set_ylim(-100, 100)

        self.ax[1].spines['right'].set_visible(False)
        self.ax[1].spines['bottom'].set_visible(False)
        self.ax[1].spines['top'].set_visible(False)
        self.ax[1].spines['left'].set_visible(False)

        self.ax[1].grid()

        # Рисование 2 графика
        self.ax[1].fill_between([0], [0], [0], facecolor='#FFEC14', label='Генерация от солнца')
        self.ax[1].fill_between([0], [0], [0], facecolor='#A3FFFF', label='Генерация от ветра')
        self.ax[1].fill_between([0], [0], [0], facecolor='#9C9C9C', label='Генерация от дизеля')
        self.ax[1].fill_between([0], [0], [0], facecolor='#FF9494', label='Потребление больницами')
        self.ax[1].fill_between([0], [0], [0], facecolor='#FFFDBB', label='Потребление заводами')
        self.ax[1].fill_between([0], [0], [0], facecolor='#9DC941', label='Потребление домами А')
        self.ax[1].fill_between([0], [0], [0], facecolor='#BFE471', label='Потребление домами Б')
        self.ax[1].fill_between([0], [0], [0], facecolor='#3737FF', label='Операции с аккамуляторами')
        self.ax[1].fill_between([0], [0], [0], facecolor='#000000', label='Операции с внешней сетью')
        self.ax[1].legend(loc='upper left', prop={'size': 13.5})

        box_x_data = range(23, 57)
        self.ax[1].fill_between(box_x_data, [90 for _ in box_x_data], [-100 for _ in box_x_data], facecolor='#ffffc3')

        text_about_sys_data = self.normalise_num_for_str(0) + '\n' + self.normalise_num_for_str(
            self.eng.consumers) + '\n'
        text_about_sys_data += self.normalise_num_for_str(self.eng.generators) + '\n' + self.normalise_num_for_str(
            self.eng.power_system) + '\n'
        text_about_sys_data += self.normalise_num_for_str(0) + '\n' + self.normalise_num_for_str(
            self.eng.exchange)
        text_about_sys_data += '\n\n' + self.normalise_num_for_str(self.total)
        text_about_sys_delta = [
            self.normalise_num_for_str(0),
            self.normalise_num_for_str(self.eng.delta_consumers),
            self.normalise_num_for_str(self.eng.delta_generators),
            self.normalise_num_for_str(self.eng.delta_power_system),
            self.normalise_num_for_str(0),
            self.normalise_num_for_str(self.eng.delta_exchange),
            self.normalise_num_for_str(self.delta_total)
        ]
        text_about_sys_end = '____________________________\n\n\n'
        text_about_sys_end += "Игра окончена" if act_tick == end_tick - 1 else ""

        self.ax[1].text(40, -60, 'Аукцион\nПотребители\nГенераторы\nЭнергосистема\nПерегрузка\nБиржа\n\nИтого',
                        fontsize=20, ha='right', fontweight='bold')
        self.ax[1].text(51, -60, text_about_sys_data, fontsize=20, ha='right', fontweight='bold')
        y_delta = -58
        for delta_text in text_about_sys_delta[::-1]:
            self.ax[1].text(51.5, y_delta, delta_text, fontsize=12, color='grey')
            if delta_text == text_about_sys_delta[-1]:
                y_delta += 18
            y_delta += 17.8
        self.ax[1].text(40, -90, text_about_sys_end, fontsize=20, ha='center', fontweight='bold')

        box_x_action = range(60, 100)
        self.ax[1].fill_between(box_x_action, [90 for _ in box_x_action], [-100 for _ in box_x_action],
                                facecolor='#f0f0f0')

        try:
            self.data_actions[0] = '- ' + self.data_actions[0]
            text_action = "\n- ".join(self.data_actions)  # 10
            self.ax[1].text(62, -90, text_action, fontsize=18)
        except Exception:
            pass
        else:
            self.ax[1].text(62, -90, '', fontsize=18)

        # Донастройка 2 графика
        self.ax[1].set_xticks([])
        self.ax[1].set_yticks([])
