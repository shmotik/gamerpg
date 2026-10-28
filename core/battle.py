import pygame
import random

from scenes.base_scene import Scene
from systems.combat import calculate_damage
from UI.battle_log import BattleLog
from core import controls
from localization.manager import tr
from UI.text import get_font, fit_text, draw_hint


class Battle(Scene):

    def __init__(self, player, enemy, messages):
        self.player = player
        self.player_stats = player.stats
        self.enemy = enemy
        self.enemy_stats = enemy.stats

        self.messages = messages

        self.state = "player_turn"
        self.finished = False

        self.update_fonts()

        self.actions = ["attack", "skill", "defend", "run"]
        self.selected = 0

        self.skill_index = 0

        self.defending = False

        self.battle_log = BattleLog()
        self.message = "battle.choose"

        self.up_keys = controls.UP
        self.down_keys = controls.DOWN

    def reset(self):
        self.player_stats.reset()
        self.enemy_stats.reset()
        self.state = "player_turn"
        self.finished = False
        self.message = "battle.choose"

    def finish(self, outcome):
        if self.finished:
            return None
        self.finished = True
        self.state = outcome
        return ("battle_end", outcome)

    def surrender(self):
        if self.finished:
            return None
        self.player_stats.hp = 0
        return self.finish("lose")

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height()

        big = int(height * 0.06)
        small = int(height * 0.035)

        self.font = get_font(big)
        self.small = get_font(small)

    def update(self, screen, keys, events, dt):

        for event in events:
            result = self.handle_event(event)
            if result:
                return result

        self.messages.update(dt)

        for skill in self.player.skills:
            skill.tick()

        self.draw(screen)

        return "battle"

    def handle_event(self, event):

        if self.finished or event.type != pygame.KEYDOWN:
            return None

        if event.key in controls.BACK:
            if self.state == "skill_select":
                self.state = "player_turn"
                return None
            return ("battle_pause",)

        if self.state == "player_turn":
            return self.handle_player_input(event)

        elif self.state == "skill_select":
            return self.handle_skill_input(event)

    def handle_player_input(self, event):

        if event.key in self.up_keys:
            self.selected -= 1

        elif event.key in self.down_keys:
            self.selected += 1

        elif event.key in controls.CONFIRM:
            action = self.actions[self.selected]

            if action == "attack":
                return self.player_action("attack")

            elif action == "skill":
                self.state = "skill_select"
                self.skill_index = 0

            elif action == "defend":
                return self.player_action("defend")

            elif action == "run":
                return self.player_action("run")

        self.selected %= len(self.actions)

    def handle_skill_input(self, event):

        skills = self.player.skills

        if event.key in self.up_keys:
            self.skill_index -= 1

        elif event.key in self.down_keys:
            self.skill_index += 1

        elif event.key in controls.BACK:
            self.state = "player_turn"

        elif event.key in controls.CONFIRM:

            if self.skill_index == len(skills):
                self.state = "player_turn"
            else:
                skill = skills[self.skill_index]

                can_use, reason = skill.can_use(self.player_stats)

                if not can_use:
                    self.battle_log.add(reason)
                    return

                return self.player_action("skill", skill)

        self.skill_index %= (len(skills) + 1)

    def get_turns(self, speed_a, speed_b):
        ratio = speed_a / max(1, speed_b)
        return max(1, int(ratio))

    def player_attack(self, turns):
        for _ in range(turns):
            if not self.enemy_stats.is_alive():
                break

            damage, result = calculate_damage(self.player_stats, self.enemy_stats)

            if result == "DODGE":
                self.battle_log.add("Враг уклонился!")
            else:
                self.enemy_stats.hp -= damage

                if result == "CRIT":
                    self.battle_log.add(f"КРИТ! {damage} урона")
                else:
                    self.battle_log.add(f"Вы нанесли {damage} урона")

    def enemy_attack(self, turns):
        for _ in range(turns):
            if not self.player_stats.is_alive():
                break

            damage, result = calculate_damage(self.enemy_stats, self.player_stats)

            if result == "DODGE":
                self.battle_log.add("Вы уклонились!")
                continue

            if self.defending:
                damage = int(damage * 0.5)

            self.player_stats.hp -= damage

            if result == "CRIT":
                self.battle_log.add(f"Враг критует! {damage} урона")
            else:
                self.battle_log.add(f"Враг нанес {damage} урона")

        self.defending = False

    def draw(self, screen):
        screen.fill((40, 0, 40))

        self.draw_ui(screen)

        if self.state == "player_turn":
            self.draw_actions(screen)

        elif self.state == "skill_select":
            self.draw_skills(screen)

        self.battle_log.draw(screen, pygame.Rect(
            screen.get_width() // 2, int(screen.get_height() * 0.53),
            screen.get_width() // 2 - 20, int(screen.get_height() * 0.38)
        ))
        self.draw_statuses(screen)
        draw_hint(screen, "hint.battle")


    def draw_ui(self, screen):
        width, height = screen.get_size()
        title = fit_text(self.font, tr("battle.title"), (255, 255, 255), width - 40)
        screen.blit(title, ((width - title.get_width()) // 2, int(height * 0.07)))

        hp1 = self.small.render(tr("battle.player_hp", hp=self.player_stats.hp), True, (0, 255, 0))
        hp2 = self.small.render(tr("battle.enemy_hp", hp=self.enemy_stats.hp), True, (255, 0, 0))

        mp = self.small.render(
            tr("battle.mana", mana=self.player_stats.mana, maximum=self.player_stats.max_mana),
            True,
            (50, 150, 255)
        )

        screen.blit(hp1, (30, int(height * 0.20)))
        screen.blit(hp2, (30, int(height * 0.27)))
        screen.blit(mp, (30, int(height * 0.34)))


    def draw_actions(self, screen):
        for i, action in enumerate(self.actions):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)

            text = fit_text(self.small, tr(f"battle.{action}"), color, screen.get_width() // 2 - 60)
            screen.blit(text, (30, int(screen.get_height() * (0.53 + i * 0.075))))


    def draw_skills(self, screen):
        skills = self.player.skills

        for i, skill in enumerate(skills):
            color = (255, 255, 0) if i == self.skill_index else (255, 255, 255)

            name = skill.name

            if skill.current_cd > 0:
                name += f" ({skill.current_cd})"

            if skill.mana_cost > self.player_stats.mana:
                name += " " + tr("battle.no_mana")

            text = fit_text(self.small, name, color, screen.get_width() // 2 - 60)
            screen.blit(text, (30, int(screen.get_height() * (0.53 + i * 0.075))))

        # кнопка назад
        back_color = (255, 255, 0) if self.skill_index == len(skills) else (255, 255, 255)
        back = self.small.render(tr("common.back"), True, back_color)
        screen.blit(back, (30, int(screen.get_height() * (0.53 + len(skills) * 0.075))))


    def draw_statuses(self, screen):
        y = int(screen.get_height() * 0.20)

        for status in self.player_stats.statuses:
            text = self.small.render(
                f"{tr('status.' + status['name'])} ({status['turns']})",
                True,
                (200, 200, 50)
            )
            screen.blit(text, (screen.get_width() // 2 + 20, y))
            y += 25

    def player_action(self, action_type, skill=None):

        if self.finished:
            return None

        self.player_stats.process_effects(self.messages)

        if not self.player_stats.is_alive():
            return self.finish("lose")
        self.enemy_stats.process_effects(self.messages)
        if not self.enemy_stats.is_alive():
            return self.finish("win")

        # ХОД ИГРОКА 
        if action_type == "attack":
            self.player_attack(1)

        elif action_type == "skill" and skill:

            if skill.mana_cost > self.player.mana:
                self.battle_log.add("Недостаточно маны!")
                return

            text = skill.use(self.player_stats, self.enemy_stats)
            self.battle_log.add(text)

        elif action_type == "defend":
            self.defending = True
            self.battle_log.add("Вы защищаетесь")

        elif action_type == "run":
            chance = max(15, min(85, 50 + 5 * (
                self.player_stats.get("speed") - self.enemy_stats.get("speed")
            )))
            if random.random() * 100 < chance:
                self.messages.add("Вы успешно сбежали!", color=(100, 255, 100))
                return self.finish("run")
            self.battle_log.add("Побег не удался! Враг ходит.")
            self.messages.add("Побег не удался!", color=(255, 150, 50))

        #  ПРОВЕРКА ПОСЛЕ ХОДА 
        if not self.enemy_stats.is_alive():
            return self.finish("win")

        #  ХОД ВРАГА 
        enemy_turns = self.get_turns(
            self.enemy_stats.get("speed"),
            self.player_stats.get("speed")
        )

        for _ in range(enemy_turns):

            if not self.player_stats.is_alive():
                break

            action = self.enemy.combat_ai.choose_action(self.player, self)

            if action == "attack":
                self.enemy_attack(1)

            elif action == "defend":
                self.battle_log.add("Враг защищается")

            elif isinstance(action, tuple):
                _, skill = action
                text = skill.use(self.enemy_stats, self.player_stats)
                self.battle_log.add(f"Враг использует {skill.name}: {text}")

        #  ПРОВЕРКА ПОСЛЕ ВРАГА 
        if not self.player_stats.is_alive():
            return self.finish("lose")
        else:
            self.state = "player_turn"

        for skill in self.player.skills:
            skill.tick()
