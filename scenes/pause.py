import pygame


class Pause:

    def __init__(self):
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40)

    def update(self, screen, keys, events):

        # рендер
        screen.fill((10, 10, 40))

        title = self.font.render("PAUSED", True, (255, 255, 255))
        hint1 = self.small_font.render("ESC - back to game", True, (200, 200, 200))
        hint2 = self.small_font.render("M - main menu", True, (200, 200, 200))

        screen.blit(title, (screen.get_width()//2 - 100, 200))
        screen.blit(hint1, (screen.get_width()//2 - 160, 300))
        screen.blit(hint2, (screen.get_width()//2 - 140, 340))

        # переключение сцен
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "game"
                if event.key == pygame.K_m:
                    return "menu"

        return "pause"