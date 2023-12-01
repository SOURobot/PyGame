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
poses = []
level = 1


run = True
while run:
    timer.tick(fps)

    screen.fill('black')
    screen.blit(BG, (0, 0))

    if level > 0:
        draw_soldier()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()