import random

class Stats:
    def __init__(self, hp, attack_values, defense, speed=1, extra_stats=None):
        self.max_hp = hp
        self.hp = hp

        self.base_attack = attack_values[:]   # база
        self.base_defense = defense
        self.base_speed = speed

        self.extra = extra_stats or {}

        # ВСЕ бонусы в одном месте
        self.bonus = {}

    def roll_attack(self):
        base = random.choice(self.base_attack)

        # бонусы от предметов
        base += self.bonus.get("attack", 0)

        # бонусы от прокачки
        if hasattr(self, "progress"):
            base += self.get_progress_bonus("attack")

        # крит через luck
        if self.get("luck") > 0:
            if random.random() < self.get("luck") * 0.05:
                return int(base * 1.5)

        return base

    def take_damage(self, damage):
        real_damage = max(1, damage - self.get("defense"))
        self.hp = max(0, self.hp - real_damage)

    def get_attack_range(self):
        bonus = self.bonus.get("attack", 0)
        progress_bonus = self.get_progress_bonus("attack")

        return (
            min(self.base_attack) + bonus + progress_bonus,
            max(self.base_attack) + bonus + progress_bonus
        )

    def get_progress_bonus(self, stat):
        if hasattr(self, "progress"):
            return self.progress.stats.get(stat, 0)
        return 0

    def is_alive(self):
        return self.hp > 0

    def reset(self):
        self.hp = self.max_hp

    def get(self, stat):
        # базовое значение
        if stat == "defense":
            base = self.base_defense
        elif stat == "speed":
            base = self.base_speed
        elif stat == "attack":
            base = 0  # attack считается отдельно (через roll_attack)
        else:
            base = self.extra.get(stat, 0)

        # бонусы от предметов
        bonus = self.bonus.get(stat, 0)

        # бонусы от прокачки 
        progress_bonus = self.get_progress_bonus(stat)

        return base + bonus + progress_bonus

    def add_bonus(self, stat, value):
        self.bonus[stat] = self.bonus.get(stat, 0) + value

    def remove_bonus(self, stat, value):
        if stat in self.bonus:
            self.bonus[stat] -= value