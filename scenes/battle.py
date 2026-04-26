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
                            damage = self.player_stats.roll_attack()
                            self.enemy_stats.take_damage(damage)

                            self.message = f"You hit enemy: -{damage}"

                            if not self.enemy_stats.is_alive():
                                self.state = "win"
                                self.message = "YOU WIN!"
                                self.messages.add("Враг повержен")
                            else:
                                self.state = "enemy_turn"

                        elif action == "Defend":
                            self.defending = True
                            self.message = "You defend!"
                            self.state = "enemy_turn"

                        elif action == "Run":
                            self.message = "You ran away!"
                            return "game"
                
        # ход врага
        if self.state == "enemy_turn":

            damage = self.enemy_stats.roll_attack()

            if self.defending:
                damage //= 2
                self.defending = False

            self.player_stats.take_damage(damage)

            self.message = f"Enemy hits you: -{damage}"

            if not self.player_stats.is_alive():
                self.state = "lose"
                self.message = "YOU LOSE!"
            else:
                self.state = "player_turn"


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

        if self.state == "enemy_turn":
            hint_text = "Enemy turn..."

        elif self.state in ["win", "lose"]:
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

        return "battle"