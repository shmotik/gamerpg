import pygame


class Menu:

    def __init__(self):
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40)

    def update(self, screen, keys, events):

        # рендер
        screen.fill((20, 20, 20))

        title = self.font.render("MY GAME", True, (255, 255, 255))
        hint = self.small_font.render("PRESS ENTER TO START", True, (200, 200, 200))

        screen.blit(title, (screen.get_width()//2 - 100, 200))
        screen.blit(hint, (screen.get_width()//2 - 180, 300))

        # переключение сцены
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "game"

        return "menu"