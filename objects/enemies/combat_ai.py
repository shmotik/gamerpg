class CombatAI:
    def __init__(self, enemy):
        self.enemy = enemy
        self.player_history = []

    def choose_action(self, player, battle):

        # 1. собрать действия
        actions = ["attack"]

        if hasattr(self.enemy, "skills"):
            for skill in self.enemy.skills:
                can_use, _ = skill.can_use(self.enemy.stats)
                if can_use:
                    actions.append(("skill", skill))

        actions.append("defend")

        # 2. анализ игрока
        pattern = self.analyze_player()

        # 3. выбрать лучшее
        best = None
        best_score = -9999

        for action in actions:
            score = self.evaluate(action, player, pattern)

            if score > best_score:
                best_score = score
                best = action

        return best

    def evaluate(self, action, player, pattern):

        score = 0

        # атака
        if action == "attack":
            score += 10

        # скиллы
        if isinstance(action, tuple):
            _, skill = action

            score += 20  # базовая ценность

            # если игрок защищается
            if player.stats.has_status("defense"):
                score -= 10

        # защита
        if action == "defend":
            if pattern == "big_attack_soon":
                score += 30

        return score

    def remember(self, action):
        self.player_history.append(action)

        if len(self.player_history) > 5:
            self.player_history.pop(0)

    def analyze_player(self):
        if self.player_history.count("skill") >= 3:
            return "big_attack_soon"

        return None