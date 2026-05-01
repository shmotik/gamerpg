class Skill:
    def __init__(self, name, multiplier=1.0, mana_cost=0, cooldown=0, effect=None):
        self.name = name
        self.multiplier = multiplier
        self.mana_cost = mana_cost
        self.cooldown = cooldown
        self.current_cd = 0
        self.effect = effect

    def can_use(self, user):
        if self.current_cd > 0:
            return False, "Перезарядка!"

        if user.mana < self.mana_cost:
            return False, "Не хватает маны!"

        return True, ""

    def use(self, user, target):
        from systems.combat import calculate_damage

        # списываем ману
        user.mana -= self.mana_cost

        # ставим кулдаун
        self.current_cd = self.cooldown

        damage, result = calculate_damage(user, target)
        damage = int(damage * self.multiplier)

        target.hp -= damage

        text = f"{self.name}: {damage} урона"

        if self.effect:
            self.effect(user, target)

        return text

    def tick(self):
        if self.current_cd > 0:
            self.current_cd -= 1