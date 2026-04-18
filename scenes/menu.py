import pygame


class Menu:

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height()

        font_size_big = int(height * 0.08)
        font_size_small = int(height * 0.05)

        self.font = pygame.font.SysFont(None, font_size_big)
        self.small = pygame.font.SysFont(None, font_size_small)

    def __init__(self):

        self.update_fonts()

        self.up_keys = [pygame.K_UP, pygame.K_w]
        self.down_keys = [pygame.K_DOWN, pygame.K_s]

        self.buttons = ["START", "SETTINGS", "EXIT"]
        self.selected = 0

    def update(self, screen, keys, events):

        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key in self.up_keys:
                    self.selected -= 1

                if event.key in self.down_keys:
                    self.selected += 1

                if self.selected < 0:
                    self.selected = len(self.buttons) - 1
                if self.selected >= len(self.buttons):
                    self.selected = 0

                if event.key == pygame.K_RETURN:

                    if self.buttons[self.selected] == "START":
                        return "game"

                    if self.buttons[self.selected] == "SETTINGS":
                        return "settings"

                    if self.buttons[self.selected] == "EXIT":
                        return "exit"

        # рендер
        screen.fill((20, 20, 20))

        width, height = screen.get_size()

        title = self.font.render("MY GAME", True, (255, 255, 255))
        screen.blit(title, (300, 100))

        for i, btn in enumerate(self.buttons):

            color = (255, 255, 0) if i == self.selected else (200, 200, 200)

            text = self.small.render(btn, True, color)

            x = width // 2 - text.get_width() // 2
            y = height // 2 + i * 60
            screen.blit(text, (x, y))
            
        #hint = self.small.render("PRESS ENTER TO START", True, (200, 200, 200))

        #screen.blit(title, (screen.get_width()//2 - 100, 200))
        #screen.blit(hint, (screen.get_width()//2 - 180, 300))

        # переключение сцены
        #for event in events:
         #   if event.type == pygame.KEYDOWN:
          #      if event.key == pygame.K_RETURN:
           #         return "game"

        return "menu"