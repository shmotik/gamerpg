import pygame

class MessageLog:
    def __init__(self):
        self.messages = []
        self.font = None

    def set_font(self, font):
        self.font = font

    def add(self, text, duration=3, color = (255,255,255)):
        self.messages.append({
            "text": text,
            "time": duration,
            "color": color
        })

    def update(self, dt):
        for msg in self.messages:
            msg["time"] -= dt

        self.messages = [m for m in self.messages if m["time"] > 0]

    def draw(self, screen):   
        if not self.font:
            return
        y = 500  # позиция (можешь менять)

        for msg in self.messages:
            text = self.font.render(msg["text"], True, msg["color"])
            screen.blit(text, (50, y))
            y += 30

        