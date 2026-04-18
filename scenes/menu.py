import pygame


class Menu:

    def __init__(self):

        self.font = pygame.font.SysFont(None, 60)
        self.small = pygame.font.SysFont(None, 40)

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

        title = self.font.render("MY GAME", True, (255, 255, 255))
        screen.blit(title, (300, 100))

        for i, btn in enumerate(self.buttons):

            color = (255, 255, 0) if i == self.selected else (200, 200, 200)

            text = self.small.render(btn, True, color)
            screen.blit(text, (320, 250 + i * 60))
            
        #hint = self.small.render("PRESS ENTER TO START", True, (200, 200, 200))

        #screen.blit(title, (screen.get_width()//2 - 100, 200))
        #screen.blit(hint, (screen.get_width()//2 - 180, 300))

        # переключение сцены
        #for event in events:
         #   if event.type == pygame.KEYDOWN:
          #      if event.key == pygame.K_RETURN:
           #         return "game"

        return "menu"