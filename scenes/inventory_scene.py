import pygame
from scenes.base_scene import Scene

class InventoryScene(Scene):
    def __init__(self, player):
        self.player = player
        self.selected = 0

        self.font = pygame.font.SysFont(None, 50)

    def update(self, screen, keys, events, dt):

        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "game"

                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.player.inventory.items)

                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.player.inventory.items)

                elif event.key == pygame.K_RETURN:
                    items = self.player.inventory.items

                    if not items:
                        return "inventory"

                    item = items[self.selected]
                    result = item.use(self.player)
                    print(result)

                    self.player.inventory.remove(item)

                    self.selected = max(0, self.selected - 1)

        if len(self.player.inventory.items) == 0:
            screen.fill((20, 20, 20))

            text = self.font.render("Inventory is empty", True, (255, 255, 255))
            screen.blit(text, (50, 150))

            return "inventory"

        # рендер
        screen.fill((20, 20, 20))

        title = self.font.render("INVENTORY", True, (255, 255, 255))
        screen.blit(title, (50, 50))

        for i, item in enumerate(self.player.inventory.items):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)

            text = self.font.render(item.name, True, color)
            screen.blit(text, (50, 150 + i * 50))

        selected_item = self.player.inventory.items[self.selected]

        self.draw_text_multiline(screen, selected_item.description, 400, 200, self.font, (200, 200, 200))
        return "inventory"

    def draw_text_multiline(self, screen, text, x, y, font, color):
        words = text.split(" ")
        line = ""
        lines = []


        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] > 300:
                lines.append(line)
                line = word + " "
            else:
                line = test_line

        lines.append(line)

        for i, l in enumerate(lines):
            rendered = font.render(l, True, color)
            screen.blit(rendered, (x, y + i * 30))