import pygame
from pygame import mixer
import math


def sound():
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
copters = [pygame.image.load(f'assets/copters/fpvC.png'), pygame.image.load(f'assets/copters/grenadeC.png')]
sd_pos = [(WIDTH/2-75, HEIGHT-240), (WIDTH/2-87, HEIGHT-210), (WIDTH/2-45, HEIGHT-240), (WIDTH/2-100, HEIGHT-210)]
level = 1
curr_move = 1
shoot_time = 0

for i in range(1, 5):
    poses.append(pygame.image.load(f'assets/poses/sd{i}.png'))


run = True
while run:
    timer.tick(fps)

    screen.fill('black')
    screen.blit(BG, (0, 0))

    shoot = False

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
            if passed_time < 500:
                screen.blit(pygame.image.load("assets/icons/reload.png"), (860, 5))
            else:
                shoot = True
                shoot_time = pygame.time.get_ticks()
                sound()
        else:
            shoot = True
            shoot_time = pygame.time.get_ticks()
            sound()

    screen.blit(poses[curr_move - 1], sd_pos[curr_move - 1])

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()