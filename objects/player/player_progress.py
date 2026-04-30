class PlayerProgress:
    def __init__(self):
        self.level = 1
        self.xp = 0
        self.stat_points = 0

        self.stats = {
            "attack": 0,
            "defense": 0,
            "speed": 0,
            "luck": 0,
            "alchemy": 0,
            "smithing": 0
        }

        self.stats_types = {
            "attack": "combat",
            "defense": "combat",
            "speed": "combat",
            "luck": "combat",
            "alchemy": "craft",
            "smithing": "craft"
        }

    def xp_to_next(self):
        return int(100 * (self.level ** 1.5))

    def add_xp(self, amount):
        self.xp += amount

        leveled_up = False

        while self.xp >= self.xp_to_next():
            self.xp -= self.xp_to_next()
            self.level += 1
            self.stat_points += 1
            leveled_up = True

        return leveled_up

    def upgrade_stat(self, stat_name):
        if self.stat_points <= 0:
            return False

        if stat_name not in self.stats:
            return False

        self.stats[stat_name] += 1
        self.stat_points -= 1

        return True