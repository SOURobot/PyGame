import os
import pygame
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('egg_fall/images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_text(screen, font, x, coords, red=False):
    if red:
        color = (255, 0, 0)
    else:
        color = (255, 255, 255)
    text = font.render(str(x), True, color)
    screen.blit(text, coords)