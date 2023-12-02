import random

import pygame
from pygame import mixer
import math


def shot():
    mixer.init()
    mixer.music.load("assets/sounds/shoot.mp3")
    mixer.music.play()


pygame.init()
fps = 60
timer = pygame.time.Clock()

WIDTH = 1000
HEIGHT = 574
screen = pygame.display.set_mode([WIDTH, HEIGHT])

BG = pygame.image.load("assets/bg.jpg")
banners = []
poses = []
# copters = [pygame.image.load(f'assets/copters/fpvC.png'), pygame.image.load(f'assets/copters/grenadeC.png')]
copters = []
sd_pos = [(WIDTH/2-75, HEIGHT-240), (WIDTH/2-87, HEIGHT-210), (WIDTH/2-45, HEIGHT-240), (WIDTH/2-100, HEIGHT-210)]
level = 1
curr_move = 1
shoot_time = 0

copters_in_sky = [[], [], [], []]
coords = [[(75, 320), (125, 320), (175, 320), (225, 320)], [(100, 104), (150, 134), (200, 164), (250, 194)],
          [(925, 320), (875, 320), (825, 320), (775, 320)], [(900, 104), (850, 134), (800, 164), (750, 194)]]
last_launch = 2000
limit = 1
delay = 1500

for i in range(1, 5):
    poses.append(pygame.image.load(f'assets/poses/sd{i}.png'))
    copters.append(pygame.image.load(f'assets/copters/fpvC{i}.png'))

def sky_conds(f_c):
    c = 0
    free = [1, 2, 3, 4]
    for i in range(len(f_c)):
        if len(f_c[i]) != 0:
            c += 1
            free.remove(i + 1)
    vect = random.choice(free)
    return c, vect


run = True
while run:
    timer.tick(fps)

    screen.fill('black')
    screen.blit(BG, (0, 0))

    shoot = False

    passed_delay = pygame.time.get_ticks()
    if passed_delay - last_launch == 1000:
        number, free_vect = sky_conds(copters_in_sky)
        if number < limit:
            copters_in_sky[free_vect-1].append(0)
            copters_in_sky[free_vect-1].append(0)
            copters_in_sky[free_vect-1].append(pygame.time.get_ticks())

    new_list = []
    for copter in copters_in_sky:
        if copter:
            timer = pygame.time.get_ticks()
            if timer - copter[2] >= delay:
                screen.blit(copters[copter[1]], coords[copter[0]])
                new_list.append([copter[0] + 1, copter[1] + 1, timer])

    copters_in_sky = new_list.copy()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w] and str(curr_move) in '13':
        curr_move += 1
    if pressed[pygame.K_s] and str(curr_move) in '24':
        curr_move -= 1
    if pressed[pygame.K_d] and str(curr_move) in '12':
        curr_move += 2
    if pressed[pygame.K_a] and str(curr_move) in '34':
        curr_move -= 2
    if pressed[pygame.K_SPACE]:
        if shoot_time != 0:
            passed_time = pygame.time.get_ticks() - shoot_time
            if passed_time < 750:
                screen.blit(pygame.image.load("assets/icons/reload.png"), (860, 5))
            else:
                shoot = True
                shoot_time = pygame.time.get_ticks()
                shot()
        else:
            shoot = True
            shoot_time = pygame.time.get_ticks()
            shot()

    screen.blit(poses[curr_move - 1], sd_pos[curr_move - 1])

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()