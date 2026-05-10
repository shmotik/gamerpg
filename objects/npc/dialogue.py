import pygame

class DialogueBox:
    def __init__(self):
        self.active = False
        self.text = ""
        self.font = pygame.font.SysFont(None, 32)

    def open(self, text):
        self.text = text
        self.active = True

    def close(self):
        self.active = False

    def draw(self, screen):
        if not self.active:
            return

        w, h = screen.get_size()

        # фон
        pygame.draw.rect(screen, (10, 10, 10), (0, h-180, w, 180))
        pygame.draw.rect(screen, (255,255,255), (0, h-180, w, 180), 2)

        # текст
        y = h - 160
        for line in self.wrap_text(self.text, w - 40):
            surf = self.font.render(line, True, (255,255,255))
            screen.blit(surf, (20, y))
            y += 30

    def wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current = ""

        for word in words:
            test = current + " " + word if current else word
            if self.font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = word

        if current:
            lines.append(current)

        return lines