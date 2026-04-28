class Item:
    def __init__(self, name, item_type, value=0, description="", stat_bonus=None, slot=None):
        self.name = name
        self.type = item_type
        self.value = value
        self.slot = slot

        self.stat_bonus = stat_bonus or {}

        self.description = description or self.generate_description()

    def use(self, player):
        if self.type == "heal":
            player.stats.hp += self.value
            player.stats.hp = min(player.stats.hp, player.stats.max_hp)
            return f"+{self.value} HP"

        elif self.type == "buff":
            for stat, val in self.stat_bonus.items():
                player.stats.add_bonus(stat, val)

            return "Бонус применён"

        return "Nothing happened"

    def generate_description(self):
        if self.type == "heal":
            return f"Восстанавливает {self.value} HP"

        elif self.type == "buff":
            parts = []
            for stat, val in self.stat_bonus.items():
                parts.append(f"+{val} {stat}")
            return "Бонус:" + ", ".join(parts)
            
        return "Без описания"