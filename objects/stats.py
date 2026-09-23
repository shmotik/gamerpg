import random

class Stats:
    def __init__(self, hp, attack_values, defense, speed=1, extra_stats=None):
        self.max_hp = hp
        self.hp = hp

        self.base_attack = attack_values[:]   # база
        self.base_defense = defense
        self.base_speed = speed

        self.extra = extra_stats or {}

        self.max_mana = 50
        self.mana = self.max_mana

        self.statuses = []
        self.temp_stats = {}

        self.stats = {
            "attack": 0,
            "defense": defense,
            "speed": speed,
            **self.extra
        }

        # ВСЕ бонусы в одном месте
        self.bonus = {}

    def roll_attack(self):

        # заморозка — нельзя атаковать
        for status in self.statuses:
            if status["name"] == "freeze":
                return 0

        base = random.choice(self.base_attack)

        base += self.bonus.get("attack", 0)

        if hasattr(self, "progress"):
            base += self.get_progress_bonus("attack")

        #  горение снижает урон
        for status in self.statuses:
            if status["name"] == "burn":
                base = int(base * 0.8)

        #  крит
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
        base = self.stats.get(stat, 0)

        bonus = 0
        if stat in self.temp_stats:
            for buff in self.temp_stats[stat]:
                bonus += buff["value"]

        return base + bonus

    def add_bonus(self, stat, value):
        self.bonus[stat] = self.bonus.get(stat, 0) + value

    def remove_bonus(self, stat, value):
        if stat in self.bonus:
            self.bonus[stat] -= value

    def restore_mana(self, amount):
        self.mana = min(self.max_mana, self.mana + amount)

    def add_status(self, name, turns):
        self.statuses.append({"name": name, "turns": turns})

    def add_temp(self, stat, value, turns):
        if stat not in self.temp_stats:
            self.temp_stats[stat] = []

        self.temp_stats[stat].append({
            "value": value,
            "turns": turns
        })

    def process_effects(self, messages=None):

        # СТАТУСЫ
        for status in self.statuses[:]:

            name = status["name"]

            if name == "poison":
                dmg = max(1, int(self.max_hp * 0.05))
                self.hp -= dmg

                if messages:
                    messages.add(f" Яд наносит {dmg} урона")

            elif name == "burn":
                dmg = max(1, int(self.max_hp * 0.03))
                self.hp -= dmg

                if messages:
                    messages.add(f" Горение наносит {dmg} урона")

            elif name == "regen":
                heal = max(1, int(self.max_hp * 0.04))
                self.hp = min(self.max_hp, self.hp + heal)

                if messages:
                    messages.add(f" Регенерация лечит {heal}")

            elif name == "freeze":
                # просто эффект, логика будет в бою
                if messages:
                    messages.add(" Персонаж заморожен")

            status["turns"] -= 1

            if status["turns"] <= 0:
                self.statuses.remove(status)

    def to_dict(self):
        return {
            "hp": self.hp,
            "max_hp": self.max_hp,
            "mana": self.mana,
            "max_mana": self.max_mana,
            "stats": self.stats,
            "bonus": self.bonus,
            "statuses": self.statuses,
            "temp_stats": self.temp_stats
        }

    def from_dict(self, data):
        self.hp = data.get("hp", self.hp)
        self.max_hp = data.get("max_hp", self.max_hp)

        self.mana = data.get("mana", self.mana)
        self.max_mana = data.get("max_mana", self.max_mana)

        self.stats = data.get("stats", self.stats)
        self.bonus = data.get("bonus", self.bonus)
        self.statuses = data.get("statuses", self.statuses)
        self.temp_stats = data.get("temp_stats", self.temp_stats)