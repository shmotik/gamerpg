import pygame
from PIL import Image

def load_gif(path):
    gif = Image.open(path)
    frames = []

    try:
        while True:
            frame = gif.copy().convert("RGBA")
            pygame_image = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode
            )
            frames.append(pygame_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    return frames