import random

class Stats:
    def __init__(self, hp, attack_values, defense, speed=1):
        self.max_hp = hp
        self.hp = hp

        self.attack_values = attack_values

        self.defense = defense
        self.speed = speed

    def roll_attack(self):
        return random.randint(min(self.attack_values), max(self.attack_values))

    def take_damage(self, damage):
        real_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - real_damage)

    def is_alive(self):
        return self.hp > 0

    def reset(self):
        self.hp = self.max_hp