import os
import random
import sys

import pygame

size = width, height = 600, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('EGG_FALL')
clock = pygame.time.Clock()

level = 1
speed = 6


def load_image(name, colorkey=None):
    fullname = os.path.join('egg_fall', name)
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


class Egg(pygame.sprite.Sprite):
    image = load_image("white_egg.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Egg.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width)
        self.rect.y = 0

    def update(self, *args):
        self.rect = self.rect.move(0, speed)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos) or self.rect.top > height - 45:
            self.kill()


class Pan(pygame.sprite.Sprite):
    image = load_image("frying_pan.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Pan.image
        self.rect = self.image.get_rect()
        self.rect.x = 235
        self.rect.y = 700

    def update(self, *args):
        pass


all_sprites = pygame.sprite.Group()
eggs = pygame.sprite.Group()
pan = Pan()
all_sprites.add(pan)

for i in range(5):
    e = Egg()
    all_sprites.add(e)
    eggs.add(e)

running = True
while running:
    clock.tick(30)
    all_sprites.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            all_sprites.update(event)

    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()