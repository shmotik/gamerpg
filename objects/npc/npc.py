import pygame

class NPC:
    def __init__(self, x, y, text, quest=None):
        self.x = x
        self.y = y
        self.size = 50
        self.text = text
        self.quest = quest

    def is_near(self, player):
        dist = ((self.x - player.x)**2 + (self.y - player.y)**2)**0.5
        return dist < 80

    def interact(self, player):
        progress = player.progress

        if not self.quest.given:
            progress.add_quest(self.quest)
            self.quest.given = True
            return "Возьми квест"

        if self.quest.completed:
            return "Ты уже помог мне!"

        if self.quest.check_complete(progress):
            for reward in self.quest.rewards:
                reward.give(player)

            self.quest.completed = True
            return "Ты справился! Я обучу тебя новому навыку."

        return self.quest.get_text(progress)

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(
            screen,
            (0, 0, 255),
            (
                self.x - camera_x,
                self.y - camera_y,
                self.size,
                self.size
            )
        )