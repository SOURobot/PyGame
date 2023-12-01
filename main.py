import pygame
import math


pygame.init()
fps = 60
timer = pygame.time.Clock()

WIDTH = 1000
HEIGHT = 574
screen = pygame.display.set_mode([WIDTH, HEIGHT])

BG = pygame.image.load("assets/bg.jpg")
banners = []
level = 1


def draw_soldier(move):
    sd_pos = (WIDTH/2-75, HEIGHT-240)
    pose = pygame.image.load(f'assets/poses/sd{move}.png')
    screen.blit(pose, sd_pos)


run = True
while run:
    timer.tick(fps)

    screen.fill('black')
    screen.blit(BG, (0, 0))

    if level > 0:
        draw_soldier(1)

    curr_move = 1
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        if curr_move == 1:
            draw_soldier(2)
            curr_move = 2
        elif curr_move == 3:
            draw_soldier(4)
            curr_move = 4
    if pressed[pygame.K_DOWN]:
        if curr_move == 2:
            draw_soldier(1)
            curr_move = 1
        elif curr_move == 4:
            draw_soldier(3)
            curr_move = 3
    if pressed[pygame.K_LEFT]:
        if curr_move > 2:
            draw_soldier(curr_move - 2)
            curr_move -= 2
    if pressed[pygame.K_RIGHT]:
        if curr_move < 3:
            draw_soldier(curr_move + 2)
            curr_move += 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()