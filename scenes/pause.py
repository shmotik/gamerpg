import pygame


class Pause:

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height()

        font_size_big = int(height * 0.08)
        font_size_small = int(height * 0.05)

        self.font = pygame.font.SysFont(None, font_size_big)
        self.small = pygame.font.SysFont(None, font_size_small)    

    def __init__(self):

        self.update_fonts()

    def update(self, screen, keys, events):

        # рендер
        screen.fill((10, 10, 40))

        title = self.font.render("PAUSED", True, (255, 255, 255))
        hint1 = self.small.render("ESC - back to game", True, (200, 200, 200))
        hint2 = self.small.render("M - main menu", True, (200, 200, 200))

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