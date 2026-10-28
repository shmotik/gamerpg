import pygame
from scenes.base_scene import Scene
from core import controls
from localization.manager import tr
from UI.text import get_font, fit_text, draw_hint

class InventoryScene(Scene):
    def __init__(self, player, messages=None):
        self.tabs = ["inventory", "equipment", "stats"]
        self.tab_index = 0
        self.tab = self.tabs[self.tab_index]

        self.stat_names = ["attack", "defense", "speed", "luck", "alchemy", "smithing"]

        self.player = player
        self.messages = messages
        self.selected = 0

        self.update_fonts()

        self.selected_equipment = 0

        self.in_upgrade = False
        self.selected_stat = 0

        self.TABS_Y = 20

    def update_fonts(self):
        height = pygame.display.get_surface().get_height()
        self.font = get_font(height * 0.045)
        self.small = get_font(height * 0.033)
        self.CONTENT_Y = int(height * 0.22)

    def update(self, screen, keys, events, dt):

        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key in controls.BACK:
                    if self.in_upgrade:
                        self.in_upgrade = False
                        break
                    return "game"

                if event.key in controls.LEFT:
                    self.in_upgrade = False
                    self.tab_index = (self.tab_index - 1) % len(self.tabs)
                    self.tab = self.tabs[self.tab_index]

                elif event.key in controls.RIGHT:
                    self.in_upgrade = False
                    self.tab_index = (self.tab_index + 1) % len(self.tabs)
                    self.tab = self.tabs[self.tab_index]

                elif event.key in controls.UP and self.tab == "inventory" and self.player.inventory.items:
                    self.selected = (self.selected - 1) % len(self.player.inventory.items)

                elif event.key in controls.DOWN and self.tab == "inventory" and self.player.inventory.items:
                    self.selected = (self.selected + 1) % len(self.player.inventory.items)

                elif event.key in controls.CONFIRM and self.tab == "inventory":
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
                    if event.key in controls.UP:
                        if self.player.equipment:
                            self.selected_equipment = (self.selected_equipment - 1) % len(self.player.equipment)

                    elif event.key in controls.DOWN:
                        if self.player.equipment:
                            self.selected_equipment = (self.selected_equipment + 1) % len(self.player.equipment)


                    elif event.key in controls.CONFIRM:
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

                        if event.key in controls.CONFIRM:
                            if self.player.progress.stat_points > 0:
                                self.in_upgrade = True

                    #  если В режиме прокачки
                    else:

                        if event.key in controls.BACK:
                            self.in_upgrade = False

                        elif event.key in controls.UP:
                            self.selected_stat = (self.selected_stat - 1) % len(self.stat_names)

                        elif event.key in controls.DOWN:
                            self.selected_stat = (self.selected_stat + 1) % len(self.stat_names)

                        elif event.key in controls.CONFIRM:
                            stat = self.stat_names[self.selected_stat]

                            if self.player.progress.upgrade_stat(stat):
                                self.messages.add(f"{stat} увеличен!")
                            else:
                                self.messages.add("Нет очков!")

        screen.fill((20, 20, 20))

        # вкладки
        for i, tab in enumerate(self.tabs):
            color = (255, 255, 0) if i == self.tab_index else (150, 150, 150)
            column_width = screen.get_width() // len(self.tabs)
            text = fit_text(self.font, tr(f"inventory.{tab}"), color, column_width - 24)
            screen.blit(text, (i * column_width + (column_width - text.get_width()) // 2, self.TABS_Y))

        if self.tab == "inventory":
            self.draw_inventory(screen)

        elif self.tab == "equipment":
            self.draw_equipment(screen)

        elif self.tab == "stats":
            self.draw_stats(screen)

        pygame.draw.line(screen, (100, 100, 100), (0, self.CONTENT_Y - 60),
                         (screen.get_width(), self.CONTENT_Y - 60), 2)
        draw_hint(screen, "hint.upgrade" if self.in_upgrade else "hint.inventory")

        return "inventory"

    def draw_text_multiline(self, screen, text, x, y, font, color):
        words = text.split(" ")
        line = ""
        lines = []


        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] > screen.get_width() - x - 30:
                lines.append(line)
                line = word + " "
            else:
                line = test_line

        lines.append(line)

        for i, l in enumerate(lines):
            line_y = y + i * font.get_linesize()
            if line_y + font.get_linesize() > screen.get_height() - 50:
                break
            rendered = fit_text(font, l, color, screen.get_width() - x - 30)
            screen.blit(rendered, (x, line_y))

    def draw_inventory(self, screen):
        items = self.player.inventory.items

        if not items:
            text = fit_text(self.font, tr("inventory.empty"), (255, 255, 255), screen.get_width() - 60)
            screen.blit(text, (30, self.CONTENT_Y))
            return

        row_height = self.font.get_linesize() + 10
        visible_count = max(1, (screen.get_height() - self.CONTENT_Y - 60) // row_height)
        start = max(0, self.selected - visible_count + 1)
        for i in range(start, min(len(items), start + visible_count)):
            item = items[i]
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = fit_text(self.font, item.name, color, screen.get_width() // 2 - 60)
            screen.blit(text, (30, self.CONTENT_Y + (i - start) * row_height))

        selected_item = items[self.selected]

        self.draw_text_multiline(
            screen,
            selected_item.description,
            screen.get_width() // 2 + 20,
            self.CONTENT_Y,
            self.small,
            (200, 200, 200)
        )

    def draw_equipment(self, screen):
        y = self.CONTENT_Y
        slots = list(self.player.equipment.items())

        for i, (slot, item) in enumerate(slots):

            color = (255, 255, 0) if i == self.selected_equipment else (255, 255, 255)

            text = tr(f"slot.{slot}") + ": "

            if item:
                text += item.name
            else:
                text += tr("common.empty")

            rendered = fit_text(self.font, text, color, screen.get_width() - 80)
            screen.blit(rendered, (50, y))

            y += self.font.get_linesize() + 12

    def draw_stats(self, screen):
        progress = self.player.progress

        if progress.stat_points > 0 and not self.in_upgrade:
            hint = fit_text(self.small, tr("inventory.upgrade"), (200,200,100), screen.get_width() - 40)
            screen.blit(hint, (20, self.CONTENT_Y - 40))

        level_text = tr("inventory.level", level=progress.level)
        xp_text = tr("inventory.xp", xp=progress.xp, maximum=progress.xp_to_next())
        points_text = tr("inventory.points", points=progress.stat_points)

        y_offset = self.CONTENT_Y

        screen.blit(self.font.render(level_text, True, (255,255,255)), (20, y_offset))
        y_offset += self.font.get_linesize()

        screen.blit(self.small.render(xp_text, True, (150,200,255)), (20, y_offset))
        y_offset += self.small.get_linesize()

        screen.blit(self.small.render(points_text, True, (255,255,100)), (20, y_offset))
        y_offset += self.small.get_linesize() + 10

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

            text = f"{prefix}{tr('stat.' + stat)}: {value}"
            rendered = fit_text(self.font, text, color, screen.get_width() - 80)

            screen.blit(rendered, (50, y_offset))
            y_offset += self.font.get_linesize() + 4
