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

    def __init__(self, player, enemy_stats):
        self.player_stats = player.stats
        self.enemy_stats = enemy_stats

        self.state = "player_turn"
        self.message = "Choose action"

        self.update_fonts()

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

                    if event.key == pygame.K_a:  # ATTACK

                        damage = self.player_stats.roll_attack()
                        self.enemy_stats.take_damage(damage)

                        self.message = f"You hit enemy: -{damage}"

                        if  not self.enemy_stats.is_alive() :
                            self.state = "win"
                            self.message = "YOU WIN!"
                        else:
                            self.state = "enemy_turn"
                
        # ход врага
        if self.state == "enemy_turn":

            damage = self.enemy_stats.roll_attack()
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

        if self.state == "player_turn":
            hint_text = "A - ATTACK"

        elif self.state == "enemy_turn":
            hint_text = "Enemy turn..."

        elif self.state in ["win", "lose"]:
            hint_text = "ENTER - continue"

        if hint_text:
            hint = self.small.render(hint_text, True, (255, 255, 255))
            screen.blit(hint, (50, 450))

        return "battle"