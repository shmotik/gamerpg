import pygame

from scenes.base_scene import Scene


class Battle(Scene):

    def reset(self):
        self.player_stats.reset()
        self.enemy_stats.reset()
        self.state = "player_turn"
        self.message = "Choose action"

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height()

        big = int(height * 0.08)
        small = int(height * 0.05)

        self.font = pygame.font.SysFont(None, big)
        self.small = pygame.font.SysFont(None, small)

    def __init__(self, player, enemy_stats, messages):
        self.messages = messages

        self.player_stats = player.stats
        self.enemy_stats = enemy_stats

        self.state = "player_turn"
        self.message = "Choose action"

        self.update_fonts()

        self.actions = ["Attack", "Defend", "Run"]
        self.selected = 0

        self.defending = False

        self.up_keys = [pygame.K_UP, pygame.K_w]
        self.down_keys = [pygame.K_DOWN, pygame.K_s]

    def update(self, screen, keys, events, dt):

        #переключение сцен
        for event in events:
            if event.type == pygame.KEYDOWN:

                # выход всегда доступен
                if event.key == pygame.K_ESCAPE:
                    return "game"
                    
                # выход после боя
                if self.state in ["win", "lose"]:
                    if event.key == pygame.K_RETURN:
                        return "game"

                #ход игрока
                if self.state == "player_turn":

                    if event.key in self.up_keys:
                        self.selected -= 1

                    if event.key in self.down_keys:
                        self.selected += 1

                    if self.selected < 0:
                        self.selected = len(self.actions) - 1
                    if self.selected >= len(self.actions):
                        self.selected = 0

                    elif event.key == pygame.K_RETURN:
                        action = self.actions[self.selected] 

                        if action == "Attack":
                                self.execute_round()

                        elif action == "Defend":
                            self.defending = True
                            self.messages.add("Вы защищаетесь")

                        elif action == "Run":
                            self.messages.add("Вы сбежали")
                            return "game"

        # рендер
        screen.fill((40, 0, 40))

        title = self.font.render("BATTLE", True, (255, 255, 255))
        screen.blit(title, (screen.get_width()//2 - 100, 50))

        hp1 = self.small.render(f"PLAYER HP: {self.player_stats.hp}", True, (0, 255, 0))
        hp2 = self.small.render(f"ENEMY HP: {self.enemy_stats.hp}", True, (255, 0, 0))

        screen.blit(hp1, (50, 150))
        screen.blit(hp2, (50, 200))

        msg = self.small.render(self.message, True, (255, 255, 255))
        screen.blit(msg, (50, 300))

        # подсказки
        hint_text = None

        if self.state in ["win", "lose"]:
            hint_text = "ENTER - continue"

        # меню действий
        if self.state == "player_turn":
            for i, action in enumerate(self.actions):
                color = (255, 255, 0) if i == self.selected else (255, 255, 255)

                text = self.small.render(action, True, color)
                screen.blit(text, (50, 350 + i * 40))

        if hint_text:
            hint = self.small.render(hint_text, True, (255, 255, 255))
            screen.blit(hint, (50, 450))

        self.messages.update(dt)
        self.messages.draw(screen)

        return "battle"

    def get_turns(self, speed_a, speed_b):
        ratio = speed_a / max(1, speed_b)
        return max(1, int(ratio))

    def execute_round(self):
        player_speed = self.player_stats.get("speed")
        enemy_speed = self.enemy_stats.get("speed")

        player_turns = self.get_turns(player_speed, enemy_speed)
        enemy_turns = self.get_turns(enemy_speed, player_speed)

        if player_speed >= enemy_speed:
            self.player_attack(player_turns)
            if self.enemy_stats.is_alive():
                self.enemy_attack(enemy_turns)
        else:
            self.enemy_attack(enemy_turns)
            if self.player_stats.is_alive():
                self.player_attack(player_turns)

        # проверка конца боя
        if not self.enemy_stats.is_alive():
            self.state = "win"
            self.messages.add("Враг повержен")
        elif not self.player_stats.is_alive():
            self.state = "lose"
            self.messages.add("Вы проиграли")
        else:
            self.state = "player_turn"

    def player_attack(self, turns):
        for _ in range(turns):
            if not self.enemy_stats.is_alive():
                break

            dmg = self.player_stats.roll_attack()
            self.enemy_stats.take_damage(dmg)
            self.messages.add(f"Вы нанесли {dmg} урона")

    def enemy_attack(self, turns):
        for _ in range(turns):
            if not self.player_stats.is_alive():
                break

            dmg = self.enemy_stats.roll_attack()

            if self.defending:
                dmg //= 2

            self.player_stats.take_damage(dmg)
            self.messages.add(f"Враг нанес {dmg} урона")

        self.defending = False