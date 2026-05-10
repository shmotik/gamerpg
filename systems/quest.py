class Quest:
    def __init__(self, name, objectives, rewards=None):
        self.name = name
        self.objectives = objectives  # список целей
        self.completed = False
        self.rewards = rewards or []
        self.given = False  # выдан ли квест

    def check_complete(self, progress):
        for obj in self.objectives:
            if not obj.is_done(progress):
                return False

        self.completed = True
        return True

    def get_text(self, progress):
        lines = [self.name]
        for obj in self.objectives:
            lines.append(obj.get_text(progress))
        return " | ".join(lines)

class KillObjective:
    def __init__(self, enemy_type, amount):
        self.enemy_type = enemy_type
        self.amount = amount

    def is_done(self, progress):
        return progress.quest_kills.get(self.enemy_type, 0) >= self.amount

    def get_text(self, progress):
        current = progress.quest_kills.get(self.enemy_type, 0)
        return f"Убить {self.enemy_type}: {current}/{self.amount}"

class CollectObjective:
    def __init__(self, item_name, amount):
        self.item_name = item_name
        self.amount = amount

    def is_done(self, progress):
        return progress.quest_items.get(self.item_name, 0) >= self.amount

    def get_text(self, progress):
        current = progress.quest_items.get(self.item_name, 0)
        return f"Собрать {self.item_name}: {current}/{self.amount}"