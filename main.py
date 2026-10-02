import pygame
import os
import random
from scenes.save_load import SaveLoadScene
from core.save_system import save_game, load_game
#-
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

from objects.items.item_drop import ItemDrop
from objects.enemies.enemy_types import ENEMY_TYPES

# сцены
from scenes.menu import Menu
from core.game import Game
from scenes.pause import Pause
from scenes.settings import Settings
from core.battle import Battle
from scenes.inventory_scene import InventoryScene

menu = Menu()
game = Game()
game.update_fonts()
pause = Pause()
settings = Settings()
save_load_scene = SaveLoadScene()

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

            # ==========================================
            # ПРИМЕНИТЬ РАЗРЕШЕНИЕ
            # ==========================================

            if action == "apply_resolution":

                w, h = data

                screen = pygame.display.set_mode(
                    (w, h)
                )

                menu.update_fonts()
                game.update_fonts()
                pause.update_fonts()
                settings.update_fonts()
                save_load_scene.update_fonts()

                if battle:
                    battle.update_fonts()

                state = settings_from

            # ==========================================
            # ПРИМЕНИТЬ ZOOM
            # ==========================================

            elif action == "apply_zoom":

                game.zoom = data

                state = settings_from

            # ==========================================
            # НАЗАД
            # ==========================================

            elif action == "back":

                state = settings_from

    # ================= SAVE / LOAD =================
    elif state == "save_load":

        result = save_load_scene.update(
            screen, keys, events, dt
        )


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

                # Открытие меню сохранения / загрузки
        if result[0] == "save_load":

            _, mode, return_state = result

            save_load_scene.open(mode, return_state)
            state = "save_load"

        # Сохранение в выбранный слот
        elif result[0] == "save":

            _, slot, return_state = result

            if save_game(game, slot):
                game.messages.add(
                    f"Игра сохранена в слот {slot}",
                    color=(0, 255, 0)
                )

            state = return_state

        # Загрузка выбранного слота
        elif result[0] == "load":
            _, slot, return_state = result

            if load_game(game, slot):
                game.messages.add(
                    f"Загружен слот {slot}",
                    color=(0, 255, 0)
                )
                state = "game"
            else:
                state = "save_load"

        # Возврат из меню слотов
        elif result[0] == "back":

            state = result[1]

        # вход в settings
        if result[0] == "settings":
            _, from_state = result
            settings_from = from_state
            state = "settings"


        # вход в battle
        elif result[0] == "battle":
            _, enemy, messages = result

            battle = Battle(game.player, enemy, messages)
            state = "battle"

        elif result[0] == "inventory":
            _, player, messages = result
            inventory = InventoryScene(player, messages)
            scenes["inventory"] = inventory
            state = "inventory"


    elif result == "exit":
        running = False

    elif isinstance(result, str):

        if state =="battle" and result == "game":
            game.in_battle = False

            if hasattr(game, "current_enemy"):
                enemy = game.current_enemy
                enemy_type = enemy.data

                game.on_enemy_killed(enemy)

                for drop_func, chance in enemy_type.drops:
                    if random.random() < chance:
                        item = drop_func()
                        game.player.inventory.add(item)

                        game.messages.add(f"Вы победили {enemy.type}!", color=(255,250,0))
                        game.messages.add(f"Вы получили {item.name}", color=(0,255,0))

                game.current_enemy.die()
                    
        state = result


    pygame.display.update()

pygame.quit()