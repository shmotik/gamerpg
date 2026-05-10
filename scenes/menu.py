import pygame

from scenes.base_scene import Scene


class Menu(Scene):

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height()

        font_size_big = int(height * 0.08)
        font_size_small = int(height * 0.05)

        self.font = pygame.font.SysFont(None, font_size_big)
        self.small = pygame.font.SysFont(None, font_size_small)

    def __init__(self):

        self.update_fonts()

        self.button_rects = []

        self.up_keys = [pygame.K_UP, pygame.K_w]
        self.down_keys = [pygame.K_DOWN, pygame.K_s]

        self.buttons = ["START", "SETTINGS", "EXIT"]
        self.selected = 0

    def update(self, screen, keys, events, dt=None):

        for event in events:
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    mouse_pos = pygame.mouse.get_pos()

                    for i, rect in enumerate(self.button_rects):

                        if rect.collidepoint(mouse_pos):

                            self.selected = i

                            if self.buttons[i] == "START":
                                return "game"

                            if self.buttons[i] == "SETTINGS":
                                return ("settings", "menu")

                            if self.buttons[i] == "EXIT":
                                return "exit"

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
                        self.switch_to("game")
                        return "game"

                    if self.buttons[self.selected] == "SETTINGS":
                        return ("settings", "menu")

                    if self.buttons[self.selected] == "EXIT":
                        self.switch_to("exit")
                        return "exit"

        # рендер
        screen.fill((20, 20, 20))

        width, height = screen.get_size()

        title = self.font.render("MY GAME", True, (255, 255, 255))
        screen.blit(title, (300, 100))

        self.button_rects.clear()
        mouse_pos = pygame.mouse.get_pos()

        for i, btn in enumerate(self.buttons):

            text = self.small.render(btn, True, (255,255,255))

            x = width // 2 - text.get_width() // 2
            y = height // 2 + i * 60

            rect = pygame.Rect(
                x - 20,
                y - 10,
                text.get_width() + 40,
                text.get_height() + 20
            )

            self.button_rects.append(rect)

            hovered = rect.collidepoint(mouse_pos)

            # hover мышкой
            if hovered:
                self.selected = i

            # цвет
            color = (255,255,0) if i == self.selected else (200,200,200)

            # фон кнопки
            pygame.draw.rect(screen, (40,40,40), rect)

            # рамка
            pygame.draw.rect(screen, color, rect, 2)

            text = self.small.render(btn, True, color)

            screen.blit(text, (x, y))
            

        return "menu"