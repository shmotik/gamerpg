import pygame


class Battle:

    def __init__(self):
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40)

    def update(self, screen, keys, events, dt):

        #переключение сцен
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "game"   # выход из боя

        #рендер
        screen.fill((40, 0, 40))

        title = self.font.render("BATTLE!", True, (255, 255, 255))
        hint = self.small_font.render("ESC - exit battle", True, (200, 200, 200))

        screen.blit(title, (screen.get_width()//2 - 100, 200))
        screen.blit(hint, (screen.get_width()//2 - 160, 300))

        return "battle"