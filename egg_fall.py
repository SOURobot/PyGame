import os
import random
import sys
import pygame
from sounds import *


size = width, height = 500, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('EGG_FALL')
clock = pygame.time.Clock()

level = 1
speed = 6
score = 0
pan_score = 0
health = 3


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
        if pygame.sprite.collide_mask(self, pan):
            global pan_score
            catch()
            self.kill()
            pan_score += 1
        elif self.rect.top > 655:
            global health
            miss()
            self.kill()
            health -= 1


class Pan(pygame.sprite.Sprite):
    image = load_image("frying_pan.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Pan.image
        self.rect = self.image.get_rect()
        self.rect.x = 185
        self.rect.y = 580

    def burn(self):
        global score, pan_score
        fire()
        score += pan_score
        pan_score = 0

    def update(self, *args):
        if args:
            if event.key == pygame.K_a:
                self.rect.x = max(0, self.rect.x - 40)
            if event.key == pygame.K_s:
                self.burn()
            if event.key == pygame.K_d:
                self.rect.x = min(370, self.rect.x + 40)


p_s_im = load_image("pan_score.png")
s_im = load_image("fried_egg.png")
h_p = load_image("health_point.png")


def draw_info():
    screen.blit(p_s_im, (0, height - 50))
    screen.blit(s_im, (0, 0))
    for i in range(health):
        screen.blit(h_p, (width - 50, i * 50))


all_sprites = pygame.sprite.Group()
eggs = pygame.sprite.Group()
pan = Pan()
all_sprites.add(pan)

for i in range(5):
    e = Egg()
    all_sprites.add(e)
    eggs.add(e)


# main_theme()
running = True
while running:
    clock.tick(30)
    all_sprites.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pan.update(event)

    screen.fill(pygame.Color("black"))
    draw_info()
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()