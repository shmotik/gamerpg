import pygame
from scenes.base_scene import Scene

class InventoryScene(Scene):
    def __init__(self, player, messages=None):
        self.tabs = ["inventory", "equipment", "stats"]
        self.tab_index = 0
        self.tab = self.tabs[self.tab_index]

        self.stat_names = ["attack", "defense", "speed", "luck", "alchemy", "smithing"]

        self.player = player
        self.messages = messages
        self.selected = 0

        self.font = pygame.font.SysFont(None, 50)

        self.small = pygame.font.SysFont(None, 30)

        self.selected_equipment = 0

        self.in_upgrade = False
        self.selected_stat = 0

        self.TABS_Y=20
        self.CONTENT_Y=100

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

                elif event.key == pygame.K_UP and self.tab == "inventory" and self.player.inventory.items:
                    self.selected = (self.selected - 1) % len(self.player.inventory.items)

                elif event.key == pygame.K_DOWN and self.tab == "inventory" and self.player.inventory.items:
                    self.selected = (self.selected + 1) % len(self.player.inventory.items)

                elif event.key == pygame.K_RETURN and self.tab == "inventory":
                    items = self.player.inventory.items

                    if not items:
                        return "inventory"

                    item = items[self.selected]

                    if hasattr(item, "slot") and item.slot:
                        result = self.player.equip_item(item)
                        self.messages.add(result)

                        self.player.inventory.remove(item)
                        self.selected = max(0, self.selected - 1)
                    else:
                        result = item.use(self.player)
                        self.messages.add(f"Использовано: {item.name}")
                        self.messages.add(result)

                        self.player.inventory.remove(item)
                        self.selected = max(0, self.selected - 1)
                
                elif self.tab == "equipment":
                    if event.key == pygame.K_UP:
                        if self.player.equipment:
                            self.selected_equipment = (self.selected_equipment - 1) % len(self.player.equipment)

                    elif event.key == pygame.K_DOWN:
                        if self.player.equipment:
                            self.selected_equipment = (self.selected_equipment + 1) % len(self.player.equipment)


                    elif event.key == pygame.K_RETURN:
                        slots = list(self.player.equipment.keys())
                        slot = slots[self.selected_equipment]

                        item = self.player.equipment[slot]

                        if item:
                            result = self.player.unequip_item(slot)
                            self.messages.add(result)

                            self.player.inventory.add(item)

                elif self.tab == "stats":

                    #  если НЕ в режиме прокачки
                    if not self.in_upgrade:

                        if event.key == pygame.K_RETURN:
                            if self.player.progress.stat_points > 0:
                                self.in_upgrade = True

                    #  если В режиме прокачки
                    else:

                        if event.key == pygame.K_ESCAPE:
                            self.in_upgrade = False

                        elif event.key == pygame.K_UP:
                            self.selected_stat = (self.selected_stat - 1) % len(self.stat_names)

                        elif event.key == pygame.K_DOWN:
                            self.selected_stat = (self.selected_stat + 1) % len(self.stat_names)

                        elif event.key == pygame.K_RETURN:
                            stat = self.stat_names[self.selected_stat]

                            if self.player.progress.upgrade_stat(stat):
                                self.messages.add(f"{stat} увеличен!")
                            else:
                                self.messages.add("Нет очков!")

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

        pygame.draw.line(screen, (100, 100, 100), (0, 70), (800, 70), 2)

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
        slots = list(self.player.equipment.items())

        for i, (slot, item) in enumerate(slots):

            color = (255, 255, 0) if i == self.selected_equipment else (255, 255, 255)

            text = f"{slot}: "

            if item:
                text += item.name
            else:
                text += "Empty"

            rendered = self.font.render(text, True, color)
            screen.blit(rendered, (50, y))

            y += 50

    def draw_stats(self, screen):
        progress = self.player.progress

        if progress.stat_points > 0 and not self.in_upgrade:
            hint = "Press ENTER to upgrade"
            screen.blit(self.small.render(hint, True, (200,200,100)), (20, 100))

        level_text = f"Level: {progress.level}"
        xp_text = f"XP: {progress.xp} / {progress.xp_to_next()}"
        points_text = f"Points: {progress.stat_points}"

        y_offset = self.CONTENT_Y

        screen.blit(self.font.render(level_text, True, (255,255,255)), (20, y_offset))
        y_offset += 30

        screen.blit(self.small.render(xp_text, True, (150,200,255)), (20, y_offset))
        y_offset += 25

        screen.blit(self.small.render(points_text, True, (255,255,100)), (20, y_offset))
        y_offset += 30

        y = y_offset + 20

        min_atk, max_atk = self.player.stats.get_attack_range()

        values = {
            "attack": f"{min_atk} - {max_atk}",
            "defense": self.player.stats.get("defense"),
            "speed": self.player.stats.get("speed"),
            "luck": self.player.stats.get("luck"),
            "alchemy": self.player.stats.get("alchemy"),
            "smithing": self.player.stats.get("smithing"),
        }

        for i, stat in enumerate(self.stat_names):

            value = values[stat]

            # 🔹 подсветка
            if self.in_upgrade and i == self.selected_stat:
                color = (255, 255, 0)
                prefix = "> "
            else:
                color = (255, 255, 255)
                prefix = ""

            text = f"{prefix}{stat.capitalize()}: {value}"
            rendered = self.font.render(text, True, color)

            screen.blit(rendered, (50, y_offset))
            y_offset += 50