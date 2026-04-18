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

# создаем сцены
menu = Menu()
game = Game()
pause = Pause()

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

    elif state == "pause":
        state = pause.update(screen, keys, events)

    # обновление экрана
    pygame.display.update()

pygame.quit()

