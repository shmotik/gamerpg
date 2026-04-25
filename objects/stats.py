import random

class Stats:
    def __init__(self, hp, attack_values, defense, speed=1, extra_stats=None):
        self.max_hp = hp
        self.hp = hp

        self.attack_values = attack_values

        self.defense = defense
        self.speed = speed

        self.extra = extra_stats or {}

        self.bonus = {}

    def roll_attack(self):
        base = random.choice(self.attack_values)
        base += self.bonus.get("attack", 0)

        if self.get("luck") > 0:
            if random.random() < self.get("luck") * 0.05:
                return int(base * 1.5)
        return base

    def take_damage(self, damage):
        real_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - real_damage)

    def get_attack_range(self):
        bonus = self.bonus.get("attack", 0)
        return min(self.attack_values), max(self.attack_values)

    def is_alive(self):
        return self.hp > 0

    def reset(self):
        self.hp = self.max_hp

    def get(self, stat):
        if stat == "defense":
            base = self.defense
        elif stat == "speed":
            base = self.speed
        else:
            base = self.extra.get(stat, 0) 

        return base + self.bonus.get(stat, 0)

    def add_bonus(self, stat, value):
        self.bonus[stat] = self.bonus.get(stat, 0) + value

    def remove_bonus(self, stat, value):
        if stat in self.bonus:
            self.bonus[stat] -= value