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

scenes = {
    "menu": menu,
    "game": game,
    "pause": pause,
    "battle": battle,
    "settings": settings
}

prev_state = state
settings_from = "menu"

# главный игровой цикл
while running:

    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False


    # переключение сцен
    scene = scenes.get(state)

    if scene:
        result = scene.update(screen, keys, events, dt)

    else:
        result = None
    
    if isinstance(result, tuple):

        # settings
        if result[0] == "settings":
            _, from_state = result
            settings_from = from_state
            state = "settings"
        
        # apply settings
        elif result[0] == "apply":
            _, data = result
            w, h = data

            screen = pygame.display.set_mode((w, h))

            menu.update_fonts()
            battle.update_fonts()
            pause.update_fonts()
            settings.update_fonts()

            state = settings_from

    elif result == "close":
        state = settings_from

    elif result == "exit":
        running = False
        
    elif result is not None:
        state = result


  

    # обновление экрана
    pygame.display.update()

    prev_state = state

pygame.quit()

