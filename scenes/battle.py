import pygame
import random


class Battle:

    def __init__(self):
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40)

        # HP
        self.player_hp = 100
        self.enemy_hp = 50

        # состояния боя
        self.state = "player_turn"  # player_turn / enemy_turn / win / lose

        self.message = "Choose action"

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
                        damage = random.randint(5, 15)
                        self.enemy_hp -= damage
                        self.message = f"You hit enemy: -{damage} HP"

                        if self.enemy_hp <= 0:
                            self.state = "win"
                            self.message = "YOU WIN!"
                        else:
                            self.state = "enemy_turn"

        if self.state not in ["win", "lose"]:
            # ход врага (автоматический)
            if self.state == "enemy_turn":
                damage = random.randint(3, 10)
                self.player_hp -= damage
                self.message = f"Enemy hits you: -{damage} HP"

                if self.player_hp <= 0:
                    self.state = "lose"
                    self.message = "YOU LOSE!"
                else:
                    self.state = "player_turn"

        # рендер
        screen.fill((40, 0, 40))

        title = self.font.render("BATTLE", True, (255, 255, 255))
        screen.blit(title, (screen.get_width()//2 - 100, 50))

        hp1 = self.small_font.render(f"PLAYER HP: {self.player_hp}", True, (0, 255, 0))
        hp2 = self.small_font.render(f"ENEMY HP: {self.enemy_hp}", True, (255, 0, 0))

        screen.blit(hp1, (50, 150))
        screen.blit(hp2, (50, 200))

        msg = self.small_font.render(self.message, True, (255, 255, 255))
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
            hint = self.small_font.render(hint_text, True, (255, 255, 255))
            screen.blit(hint, (50, 450))

        return "battle"