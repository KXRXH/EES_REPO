from game import Game
import matplotlib.pyplot as plt
import matplotlib.animation as animation


SPEED = 50

fig, ax = plt.subplots(2, 1)
fig.set_figwidth(20)
fig.set_figheight(10)

game = Game(fig, ax)
current_tick = 0


def tick(i):
    global current_tick
    game.one_tick(current_tick)
    current_tick += 1


# Анимация
ani = animation.FuncAnimation(fig, tick, interval=SPEED)
plt.show()
