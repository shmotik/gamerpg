import pygame
from scenes.base_scene import Scene

class InventoryScene(Scene):
    def __init__(self, player):
        self.tabs = ["inventory", "equipment", "stats"]
        self.tab_index = 0
        self.tab = self.tabs[self.tab_index]

        self.player = player
        self.selected = 0

        self.font = pygame.font.SysFont(None, 50)

    def update(self, screen, keys, events, dt):

        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "game"

                if event.key == pygame.K_LEFT:
                    self.tab_index = (self.tab_index - 1) % len(self.tabs)
                    self.tab = self.tabs[self.tab_index]

                elif event.key == pygame.K_RIGHT:
                    self.tab_index = (self.tab_index + 1) % len(self.tabs)
                    self.tab = self.tabs[self.tab_index]

                elif self.tab == "inventory":
                    if event.key == pygame.K_UP and self.player.inventory.items:
                        self.selected = (self.selected - 1) % len(self.player.inventory.items)

                    elif event.key == pygame.K_DOWN and self.player.inventory.items:
                        self.selected = (self.selected + 1) % len(self.player.inventory.items)

                elif event.key == pygame.K_RETURN:
                    if self.tab == "inventory":
                        items = self.player.inventory.items

                        if not items:
                            return "inventory"

                        item = items[self.selected]

                        if hasattr(item, "slot") and item.slot:
                            result = self.player.equip_item(item)
                            print(result)
                        else:
                            result = item.use(self.player)
                            print(result)
                            self.player.inventory.remove(item)
                            self.selected = max(0, self.selected - 1)


        screen.fill((20, 20, 20))

        # вкладки
        for i, tab in enumerate(self.tabs):
            color = (255, 255, 0) if i == self.tab_index else (150, 150, 150)
            text = self.font.render(tab.upper(), True, color)
            screen.blit(text, (50 + i * 220, 20))

        if self.tab == "inventory":
            self.draw_inventory(screen)

        elif self.tab == "equipment":
            self.draw_equipment(screen)

        elif self.tab == "stats":
            self.draw_stats(screen)

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

    def draw_inventory(self, screen):
        items = self.player.inventory.items

        if not items:
            text = self.font.render("Inventory is empty (← → to switch tabs)", True, (255, 255, 255))
            text = self.font.render("Inventory is empty", True, (255, 255, 255))
            screen.blit(text, (50, 150))
            return

        for i, item in enumerate(items):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(item.name, True, color)
            screen.blit(text, (50, 150 + i * 50))

        selected_item = items[self.selected]

        self.draw_text_multiline(
            screen,
            selected_item.description,
            400,
            200,
            self.font,
            (200, 200, 200)
        )

    def draw_equipment(self, screen):
        y = 150

        for slot, item in self.player.equipment.items():
            text = f"{slot}: "

            if item:
                text += item.name
            else:
                text += "Empty"

            rendered = self.font.render(text, True, (255, 255, 255))
            screen.blit(rendered, (50, y))

            y += 50

    def draw_stats(self, screen):
        y = 150

        min_atk, max_atk = self.player.stats.get_attack_range()

        stats = [
            ("HP", self.player.stats.hp),
            ("Attack", f"{min_atk} - {max_atk}"),
            ("Defense", self.player.stats.defense),
            ("Speed", self.player.stats.speed),
        ]

        for name, value in stats:
            text = f"{name}: {value}"
            rendered = self.font.render(text, True, (255, 255, 255))
            screen.blit(rendered, (50, y))
            y += 50