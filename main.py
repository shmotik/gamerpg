import pygame
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
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
from scenes.settings import Settings

# создаем сцены
menu = Menu()
game = Game()
pause = Pause()
battle = Battle()
settings = Settings()

prev_state = state

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

    elif state == "battle":
        state = battle.update(screen, keys, events, dt)

    elif state == "settings":
        result = settings.update(screen, keys, events)

        if isinstance(result, tuple):
            state, res = result
            screen = pygame.display.set_mode(res)

            menu.update_fonts()
            battle.update_fonts()
            pause.update_fonts()
            settings.update_font()

        else:
            state = result

    elif state == "exit":
        running = False

    if state == "game" and prev_state == "battle":
        battle.reset()

    if prev_state == "battle" and state == "game":

        if battle.state == "win":
            game.location.enemies.remove(game.current_enemy)
            
        game.in_battle = False

    prev_state = state

    # обновление экрана
    pygame.display.update()

pygame.quit()

