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

        self.quests = []

        # ОБЩАЯ статистика (вся игра)
        self.total_kills = {}
        self.total_items = {}

        # ДЛЯ КВЕСТОВ (с момента взятия)
        self.quest_kills = {}
        self.quest_items = {}

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

    def add_kill(self, enemy_type):
        # общая статистика
        self.total_kills[enemy_type] = self.total_kills.get(enemy_type, 0) + 1

        # квестовая
        self.quest_kills[enemy_type] = self.quest_kills.get(enemy_type, 0) + 1

    def add_item(self, item_name):
        self.total_items[item_name] = self.total_items.get(item_name, 0) + 1
        self.quest_items[item_name] = self.quest_items.get(item_name, 0) + 1

    def add_quest(self, quest):
        if quest not in self.quests:
            self.quests.append(quest)

            #  сбрасываем ТОЛЬКО квестовый прогресс
            self.quest_kills = {}
            self.quest_items = {}
