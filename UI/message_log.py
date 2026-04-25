import pygame

class MessageLog:
    def __init__(self):
        self.messages = []

    def add(self, text, duration=3):
        self.messages.append({
            "text": text,
            "time": duration
        })

    def update(self, dt):
        for msg in self.messages:
            msg["time"] -= dt

        self.messages = [m for m in self.messages if m["time"] > 0]

    def draw(self, screen):
        font = pygame.font.SysFont(None, 30)
        y = 500  # позиция (можешь менять)

        for msg in self.messages:
            text = font.render(msg["text"], True, (255, 255, 255))
            screen.blit(text, (50, y))
            y -= 30