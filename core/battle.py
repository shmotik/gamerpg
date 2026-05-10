import pygame

from scenes.base_scene import Scene
from systems.combat import calculate_damage
from UI.battle_log import BattleLog


class Battle(Scene):

    def __init__(self, player, enemy, messages):
        self.player = player
        self.player_stats = player.stats
        self.enemy = enemy
        self.enemy_stats = enemy.stats

        self.messages = messages

        self.state = "player_turn"

        self.update_fonts()

        self.actions = ["Attack", "Skill", "Defend", "Run"]
        self.selected = 0

        self.skill_index = 0

        self.defending = False

        self.battle_log = BattleLog()
        self.message = "Choose action"

        self.up_keys = [pygame.K_UP, pygame.K_w]
        self.down_keys = [pygame.K_DOWN, pygame.K_s]

    def reset(self):
        self.player_stats.reset()
        self.enemy_stats.reset()
        self.state = "player_turn"
        self.message = "Choose action"

    def update_fonts(self):
        screen = pygame.display.get_surface()
        height = screen.get_height()

        big = int(height * 0.08)
        small = int(height * 0.05)

        self.font = pygame.font.SysFont(None, big)
        self.small = pygame.font.SysFont(None, small)

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

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_ESCAPE:
            return "game"

        if self.state in ["win", "lose"]:
            if event.key == pygame.K_RETURN:
                return "game"

        if self.state == "player_turn":
            return self.handle_player_input(event)

        elif self.state == "skill_select":
            return self.handle_skill_input(event)

    def handle_player_input(self, event):

        if event.key in self.up_keys:
            self.selected -= 1

        elif event.key in self.down_keys:
            self.selected += 1

        elif event.key == pygame.K_RETURN:
            action = self.actions[self.selected]

            if action == "Attack":
                self.player_action("attack")

            elif action == "Skill":
                self.state = "skill_select"
                self.skill_index = 0

            elif action == "Defend":
                self.player_action("defend")

            elif action == "Run":
                self.battle_log.add("Вы сбежали")
                return "game"

        self.selected %= len(self.actions)

    def handle_skill_input(self, event):

        skills = self.player.skills

        if event.key in self.up_keys:
            self.skill_index -= 1

        elif event.key in self.down_keys:
            self.skill_index += 1

        elif event.key == pygame.K_ESCAPE:
            self.state = "player_turn"

        elif event.key == pygame.K_RETURN:

            if self.skill_index == len(skills):
                self.state = "player_turn"
            else:
                skill = skills[self.skill_index]

                can_use, reason = skill.can_use(self.player_stats)

                if not can_use:
                    self.battle_log.add(reason)
                    return

                self.player_action("skill", skill)

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

        if self.state in ["win", "lose"]:
            hint = self.small.render("ENTER - continue", True, (255, 255, 255))
            screen.blit(hint, (50, 450))

        self.battle_log.draw(screen)
        self.draw_statuses(screen)


    def draw_ui(self, screen):
        title = self.font.render("BATTLE", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - 100, 50))

        hp1 = self.small.render(f"PLAYER HP: {self.player_stats.hp}", True, (0, 255, 0))
        hp2 = self.small.render(f"ENEMY HP: {self.enemy_stats.hp}", True, (255, 0, 0))

        mp = self.small.render(
            f"MP: {self.player_stats.mana}/{self.player_stats.max_mana}",
            True,
            (50, 150, 255)
        )

        screen.blit(hp1, (50, 150))
        screen.blit(hp2, (50, 200))
        screen.blit(mp, (50, 250))


    def draw_actions(self, screen):
        for i, action in enumerate(self.actions):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)

            text = self.small.render(action, True, color)
            screen.blit(text, (50, 350 + i * 40))


    def draw_skills(self, screen):
        skills = self.player.skills

        for i, skill in enumerate(skills):
            color = (255, 255, 0) if i == self.skill_index else (255, 255, 255)

            name = skill.name

            if skill.current_cd > 0:
                name += f" ({skill.current_cd})"

            if skill.mana_cost > self.player_stats.mana:
                name += " [NO MANA]"

            text = self.small.render(name, True, color)
            screen.blit(text, (50, 350 + i * 40))

        # кнопка назад
        back_color = (255, 255, 0) if self.skill_index == len(skills) else (255, 255, 255)
        back = self.small.render("Back", True, back_color)
        screen.blit(back, (50, 350 + len(skills) * 40))


    def draw_statuses(self, screen):
        y = 280

        for status in self.player_stats.statuses:
            text = self.small.render(
                f"{status['name']} ({status['turns']})",
                True,
                (200, 200, 50)
            )
            screen.blit(text, (50, y))
            y += 25

    def player_action(self, action_type, skill=None):

        self.player_stats.process_effects(self.messages)
        self.enemy_stats.process_effects(self.messages)

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

        #  ПРОВЕРКА ПОСЛЕ ХОДА 
        if not self.enemy_stats.is_alive():
            self.state = "win"
            self.battle_log.add("Враг повержен")
            return

        #  ХОД ВРАГА 
        enemy_turns = self.get_turns(
            self.enemy_stats.get("speed"),
            self.player_stats.get("speed")
        )

        for _ in range(enemy_turns):

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
            self.state = "lose"
            self.battle_log.add("Вы проиграли")
        else:
            self.state = "player_turn"

        for skill in self.player.skills:
            skill.tick()