import random

from sounds import *
from funcs import *

pygame.init()

size = width, height = 500, 810
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

icon = load_image("game_icon.png")
surv_mode = load_image("classic.png")
time_mode = load_image("timer.png")

pygame.display.set_caption('EGG_FALL')
menu_font = pygame.font.Font("egg_fall/fonts/menu_font.ttf", 85)
second_menu_font = pygame.font.Font("egg_fall/fonts/second_menu_font.otf", 25)
font = pygame.font.Font("egg_fall/fonts/my_font.ttf", 25)

WAIT_FOR_SURVIVE = 1800
WAIT_FOR_TIME = 1200
max_speed = 0
wait = 0

curr_diff = 0
score = 0
pan_score = 0
health = 3
left_fuel = 25
timer = 104


class Egg(pygame.sprite.Sprite):
    image = load_image("white_egg.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Egg.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width-35)
        self.rect.y = 0
        self.speed = random.randint(6, max_speed)

    def update(self, *args):
        self.rect = self.rect.move(0, self.speed)
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
            if args[0].key == pygame.K_a:
                self.rect.x = max(0, self.rect.x - 40)
            if args[0].key == pygame.K_s:
                self.burn()
            if args[0].key == pygame.K_d:
                self.rect.x = min(370, self.rect.x + 40)


def draw_menu():
    screen.blit(icon, (20, 50))
    screen.blit(menu_font.render("EGG FALL", True, (255, 201, 92)), [125, 50])
    draw_text(screen, second_menu_font, "by WanderGames", [140, 150])

    screen.blit(surv_mode, (20, 330))
    draw_text(screen, second_menu_font, "'1' key for CLASSIC game", [100, 350])
    screen.blit(time_mode, (420, 430))
    draw_text(screen, second_menu_font, "'2' key for TIME game", [140, 450])

    draw_text(screen, second_menu_font, "CONTROLS:", [170, 590])
    draw_text(screen, second_menu_font, "'a' to move left", [160, 640])
    draw_text(screen, second_menu_font, "'d' to move right", [160, 680])
    draw_text(screen, second_menu_font, "'s' to clear pan", [160, 720])


def draw_info(conds):
    draw_text(screen, font, score, [53, height - 50])
    flag = False
    if pan_score == 4:
        flag = True
    draw_text(screen, font, str(pan_score) + ' / 4', [330, height - 50], flag)
    flag = False
    if left_fuel <= 5:
        flag = True
    draw_text(screen, font, left_fuel, [330, 710], flag)

    screen.blit(p_s_im, (280, height - 53))
    screen.blit(s_im, (3, height - 57))
    screen.blit(f_l, (280, 707))
    if conds == 1:
        for i in range(health):
            screen.blit(h_p, (5 + i * 42, 707))
    else:
        screen.blit(t_m, (5, 707))
        formatted = str(timer // 60) + ':' + str(timer % 60)
        draw_text(screen, font, formatted, [60, 707])
    pygame.draw.line(screen, pygame.Color("white"), (5, 700), (width - 5, 700), 2)


def egg_fall(passed_time, l_t):
    if passed_time >= wait:
        e = Egg()
        all_sprites.add(e)
        eggs.add(e)
        l_t += passed_time
    return l_t


def update_timer(passed_time):
    if passed_time >= 1000:
        return timer


def reset():
    global curr_diff, score, pan_score, health, left_fuel, timer, all_sprites, eggs, pan
    curr_diff = 0
    score = 0
    pan_score = 0
    health = 3
    left_fuel = 25
    timer = 104

    all_sprites = pygame.sprite.Group()
    eggs = pygame.sprite.Group()
    pan = Pan()
    all_sprites.add(pan)


p_s_im = load_image("pan_score.png")
s_im = load_image("fried_egg.png")
h_p = load_image("health_point.png")
f_l = load_image("fuel.png")
t_m = load_image("time.png")


all_sprites = pygame.sprite.Group()
eggs = pygame.sprite.Group()
pan = Pan()
all_sprites.add(pan)


def survive():
    survive_theme()
    last_tick = 0
    r1 = True
    while r1:
        clock.tick(30)
        all_sprites.update()

        if health <= 0 or pan_score > 4:
            r1 = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r1 = False
            if event.type == pygame.KEYDOWN:
                pan.update(event)

        screen.fill(pygame.Color("black"))
        draw_info(1)
        last_tick = egg_fall(pygame.time.get_ticks() - last_tick, last_tick)
        all_sprites.draw(screen)
        pygame.display.flip()


def time_event():
    global timer
    time_theme()
    last_tick = 0
    seconds = 0
    r2 = True
    while r2:
        clock.tick(30)
        all_sprites.update()
        timer = 104 - seconds

        if timer <= 0 or pan_score > 4:
            r2 = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r2 = False
            if event.type == pygame.KEYDOWN:
                pan.update(event)

        screen.fill(pygame.Color("black"))
        draw_info(2)
        last_tick = egg_fall(pygame.time.get_ticks() - last_tick, last_tick)
        seconds = last_tick // 1000
        all_sprites.draw(screen)
        pygame.display.flip()


running = True
main_theme()
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                wait = WAIT_FOR_SURVIVE
                reset()
                max_speed = 10
                survive()
                main_theme()
            elif event.key == pygame.K_2:
                wait = WAIT_FOR_TIME
                reset()
                max_speed = 14
                time_event()
                main_theme()

    screen.fill(pygame.Color("black"))
    draw_menu()
    pygame.display.flip()


pygame.quit()