class Item:
    def __init__(self, name, item_type, value=0, description=""):
        self.name = name
        self.type = item_type
        self.value = value
        self.description = description or self.generate_description()

    def use(self, player):
        if self.type == "heal":
            player.stats.hp += self.value
            player.stats.hp = min(player.stats.hp, player.stats.max_hp)
            return f"+{self.value} HP"

        return "Nothing happened"

    def generate_description(self):
        if self.type == "heal":
            return f"Восстанавливает {self.value} HP"
        return "Без описания"