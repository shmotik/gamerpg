import pygame
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# экран
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

# состояние
state = "menu"
running = True

# сцены
from scenes.menu import Menu
from scenes.game import Game
from scenes.pause import Pause
from scenes.settings import Settings
from scenes.battle import Battle

menu = Menu()
game = Game()
pause = Pause()
settings = Settings()

battle = None

scenes = {
    "menu": menu,
    "game": game,
    "pause": pause,
}

settings_from = "menu"


# ================= MAIN LOOP =================
while running:

    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    result = None


    # ================= SETTINGS (OVERLAY) =================
    if state == "settings":

        result = settings.update(screen, keys, events, settings_from)

        if isinstance(result, tuple):
            action, data = result

            # применить разрешение
            if action == "apply":
                w, h = data
                screen = pygame.display.set_mode((w, h))

                menu.update_fonts()
                game.update_fonts()
                pause.update_fonts()
                settings.update_fonts()

                if battle:
                    battle.update_fonts()

                state = settings_from


            # вернуться назад
            elif action == "back":
                state = settings_from


            # остаться в settings
            elif action == "stay":
                state = "settings"


    # ================= BATTLE (ОТДЕЛЬНО) =================
    elif state == "battle":
        if battle:
            result = battle.update(screen, keys, events, dt)

    # ================= ОБЫЧНЫЕ СЦЕНЫ =================
    else:
        scene = scenes.get(state)

        if scene:
            result = scene.update(screen, keys, events, dt)


    # ================= ОБРАБОТКА РЕЗУЛЬТАТОВ =================

    if isinstance(result, tuple):

        # вход в settings
        if result[0] == "settings":
            _, from_state = result
            settings_from = from_state
            state = "settings"


        # вход в battle
        elif result[0] == "battle":
            _, enemy_stats = result

            battle = Battle(game.player, enemy_stats)
            state = "battle"


    elif result == "exit":
        running = False

    elif isinstance(result, str):

        if state =="battle" and result == "game":
            game.in_battle = False

            if hasattr(game, "current_enemy"):
                if game.current_enemy in game.location.enemies:
                    game.location.enemies.remove(game.current_enemy)
                    
        state = result


    pygame.display.update()

pygame.quit()