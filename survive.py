import random

from sounds import *
from funcs import *


pygame.init()

size = width, height = 500, 810
screen = pygame.display.set_mode(size)
pygame.display.set_caption('EGG_FALL')
font = pygame.font.Font("egg_fall/fonts/my_font.ttf", 25)
clock = pygame.time.Clock()


level = 1
speed = 6
curr_diff = 0

score = 0
pan_score = 0
health = 3
left_fuel = 20


# def load_image(name, colorkey=None):
#     fullname = os.path.join('egg_fall', name)
#     if not os.path.isfile(fullname):
#         print(f"Файл с изображением '{fullname}' не найден")
#         sys.exit()
#     image = pygame.image.load(fullname)
#     if colorkey is not None:
#         image = image.convert()
#         if colorkey == -1:
#             colorkey = image.get_at((0, 0))
#         image.set_colorkey(colorkey)
#     else:
#         image = image.convert_alpha()
#     return image
#
#
# def draw_text(screen, font, x, coords, red=False):
#     if red:
#         color = (255, 0, 0)
#     else:
#         color = (255, 255, 255)
#     text = font.render(str(x), True, color)
#     screen.blit(text, coords)


class Egg(pygame.sprite.Sprite):
    image = load_image("white_egg.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Egg.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width-35)
        self.rect.y = 0

    def update(self, *args):
        self.rect = self.rect.move(0, speed)
        if pygame.sprite.collide_mask(self, pan):
            global pan_score
            # catch()
            self.kill()
            pan_score += 1
        elif self.rect.top > 655:
            global health
            # miss()
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
        global score, pan_score, left_fuel
        # fire()
        left_fuel = max(0, left_fuel - 1)
        if left_fuel != 0:
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
f_l = load_image("fuel.png")


def draw_info():
    draw_text(screen, font, score, [53, height - 50])
    flag = False
    if pan_score == 4:
        flag = True
    draw_text(screen, font, pan_score, [330, height - 50], flag)
    flag = False
    if left_fuel <= 5:
        flag = True
    draw_text(screen, font, left_fuel, [330, 710], flag)

    screen.blit(p_s_im, (280, height - 53))
    screen.blit(s_im, (3, height - 57))
    screen.blit(f_l, (280, 707))
    for i in range(health):
        screen.blit(h_p, (5 + i * 42, 707))
    pygame.draw.line(screen, pygame.Color("white"), (5, 700), (width - 5, 700), 2)


def egg_fall(passed_time, l_t):
    if passed_time >= 1500:
        e = Egg()
        all_sprites.add(e)
        eggs.add(e)
        l_t += passed_time
    if curr_diff >= 10:
        global speed
        speed *= 1.5
    return l_t


all_sprites = pygame.sprite.Group()
eggs = pygame.sprite.Group()
pan = Pan()
all_sprites.add(pan)


main_theme()
last_tick = 0
running = True
while running:
    clock.tick(30)
    all_sprites.update()

    if health <= 0 or pan_score > 4:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pan.update(event)

    screen.fill(pygame.Color("black"))
    draw_info()
    last_tick = egg_fall(pygame.time.get_ticks() - last_tick, last_tick)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()