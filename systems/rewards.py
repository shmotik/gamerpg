class RewardSkill:
    def __init__(self, skill):
        self.skill = skill

    def give(self, player):
        if self.skill not in player.skills:
            player.skills.append(self.skill)