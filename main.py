import pygame

pygame.init()

# экран
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

# состояние игры
state = "menu"
running = True

# подключаем сцены
from scenes.menu import Menu
from scenes.game import Game
from scenes.pause import Pause
from scenes.battle import Battle

# создаем сцены
menu = Menu()
game = Game()
pause = Pause()
battle = Battle()

# главный игровой цикл
while running:

    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # переключение сцен
    if state == "menu":
        state = menu.update(screen, keys, events)

    elif state == "game":
        state = game.update(screen, keys, events, dt)
        if prev_state == "battle":
            game.in_battle = False

    elif state == "pause":
        state = pause.update(screen, keys, events)

    elif state == "battle":
        state = battle.update(screen, keys, events, dt)

    # обновление экрана
    pygame.display.update()

pygame.quit()

