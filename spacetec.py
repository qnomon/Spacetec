import pygame
import random
import math

WIDTH = 600
HEIGHT = 800
FPS = 60
POWERUP_TIME = 5000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 16)

# initialize pygame and create window
ind = 0
icon = pygame.image.load('Sprites/Spaceship.png')
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Fatecs")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
time = pygame.time.get_ticks()
font_name = pygame.font.match_font('arial')
highscore = ''


def newmet():
    m = Meteoro()
    all_sprites.add(m)
    meteors.add(m)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def newpow():
    if random.random() > 0.95:
        pow = Pow(hit.rect.center)
        all_sprites.add(pow)
        powerups.add(pow)

def hs_screen():
    hsscreen = True
    while hsscreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(event.pos):
                    hsscreen = False

        screen.blit(bg,(0,0))
        screen.blit(trophy, (202, 100))
        back  = pygame.draw.rect(screen, (210,60,60), ((105, 649), (388,80)))
        draw_text(screen, 'Back to Menu', 40, 300, 665)
        draw_text(screen, str(highscore), 40, WIDTH/2, HEIGHT/2)
        screen.blit(mouse_cursor, pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(FPS)


def opt_screen():
    optscreen = True
    global music_volume, volume
    msc_volume = 500
    sndvolume = 220
    while optscreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if music.collidepoint(event.pos):
                    msc_volume = event.pos[0]
                if snd.collidepoint(event.pos):
                    sndvolume = event.pos[0]
                if back.collidepoint(event.pos):
                    optscreen = False



        music = pygame.draw.rect(screen, BLACK, ((98,150), (400,5)))
        snd = pygame.draw.rect(screen, BLACK, ((98,290), (400,5)))
        screen.blit(bg,(0,0))
        pygame.draw.line(screen, WHITE, (100, 150) , (500,150), 5)
        pygame.draw.line(screen, WHITE, (100, 290), (500, 290), 5)
        pygame.draw.rect(screen, (210,60,60),((msc_volume,140) , (10,20)))
        pygame.draw.rect(screen, (210,60,60), ((sndvolume, 280), (10, 20)))
        sndt = 'Sound Effect Volume'
        back = pygame.draw.rect(screen, (210, 60, 60), ((105, 649), (388, 80)))
        draw_text(screen, 'Back to Menu', 40, 300, 665)
        draw_text(screen, 'Music Volume', 40, 300, 50)
        draw_text(screen, sndt, 40, 300, 190)

        screen.blit(mouse_cursor, pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(FPS)
    music_volume = (msc_volume - 100) / 400
    volume = (sndvolume - 100) / 400




def menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if ng.collidepoint(event.pos):
                    menu = False
                if hs.collidepoint(event.pos):
                    hs_screen()
                if op.collidepoint(event.pos):
                    opt_screen()

        ng = pygame.draw.rect(screen, (52, 152, 235), ((105, 202), (388, 133)))
        hs = pygame.draw.rect(screen, (52, 152, 235), ((105, 408), (388, 133)))
        op = pygame.draw.rect(screen, (52,152,235), ((105, 615), (388,133)))

        screen.blit(menu_sprite, (0, 0))
        screen.blit(mouse_cursor, pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(FPS)


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

        draw_text(screen, 'Pause: Press C to continue', 40, WIDTH / 2, HEIGHT / 2)
        pygame.display.update()
        clock.tick(20)


def explode():
    player_die_sound.play()
    death_explosion = Explosion(player.rect.center, 'player')
    all_sprites.add(death_explosion)
    player.hide()
    player.lives -= 1
    player.shield = 100


def set_highscore():
    global highscore
    with open('highscore.txt', 'r') as file:
        try:
            read = int(file.read())
            highscore = read
        except:
            highscore = 0


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 37 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 150
    BAR_HEIGHT = 15
    fill = (pct / 100) * BAR_LENGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (77, 231, 255), fill_rect)
    screen.blit(shield_bar, (10, 10))


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/Spaceship.png').convert()
        self.image.set_colorkey(BLACK)
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius,5)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 200
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        # timeout powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power -= 1
            self.power_timer = pygame.time.get_ticks()
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = (WIDTH / 2, HEIGHT - 10)
            self.rect.bottom = HEIGHT - 10
        if self.power >= 4:
            self.shoot_delay = 100
        else:
            self.shoot_delay = 200
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy = -7
        if keystate[pygame.K_DOWN]:
            self.speedy = 7
        self.rect.y += self.speedy
        if keystate[pygame.K_LEFT]:
            self.speedx = -7
        if keystate[pygame.K_RIGHT]:
            self.speedx = 7
        if keystate[pygame.K_z]:
            self.shoot()
        if keystate[pygame.K_p]:
            pause()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > 825:
            self.rect.bottom = 825

    def powerup(self):
        self.power += 1
        self.power_timer = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if (now - self.last_shoot) > self.shoot_delay:
            self.last_shoot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                random.choice (player_shootlist).play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                random.choice (player_shootlist).play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                random.choice (player_shootlist).play()

    def hide(self):
        # Hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 25)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load('Sprites/Enemy.png')
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.8 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -60)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.shoot_delay = 750
        self.last_shoot = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -64 or self.rect.right > WIDTH + 64:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -60)
            self.speedy = random.randrange(1, 8)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            bullet = Enemy_bullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
            enemy_shootsnd.play()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        # self.image.fill = RED
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.8 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 1)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -60)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -64 or self.rect.right > WIDTH + 64:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -60)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/shoot.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if its move to top of screen
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(('shield', 'gun', 'drone'))
        self.image = powerup_images[self.type]
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        # kill if its move to top of screen
        if self.rect.top > HEIGHT:
            self.kill()


class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/enemy_bullet.png').convert()
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speed = 10
        self.angle = 0
        self.tiro = self.rect.centerx

    def update(self):
        self.rect.y += self.speed
        self.angle += 0.2
        self.rect.centerx = self.tiro + (math.sin(self.angle) * 7)
        if self.rect.top > HEIGHT:
            self.kill()


class Drone(Player):
    def __init__(self):
        Player.__init__(self)
        self.image = pygame.image.load("Sprites/drone.png").convert()
        self.image.set_colorkey((255, 0, 255))
        self.rect.centerx = player.rect.centerx + 90
        self.rect.bottom = player.rect.bottom + 10
        self.power = 1
        self.power_timer = pygame.time.get_ticks()
        self.angle = 0

    def update(self):
        self.rect.centerx = math.cos(self.angle) * 15 + player.rect.centerx + 90
        self.rect.bottom = math.sin(self.angle) * 15 + player.rect.bottom
        self.angle += 0.1
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_z]:
            self.shoot()
        if self.power >= 1 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power_timer = pygame.time.get_ticks()
            self.power -= 1
        if self.power == 0:
            self.kill()


def show_go_screen():
    global time
    global ind
    waiting = True
    while waiting:
        time_now = pygame.time.get_ticks()
        if time_now - time > 50:
            time = time_now
            ind += 1
        if ind > 15:
            ind = 0
        screen.blit(img_go_screen[ind], (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# load all game graphics
background = pygame.image.load("Sprites/bg_stars.png").convert()
bg = pygame.transform.scale(background, (600, 800))
background_rect = bg.get_rect()
portrait = pygame.image.load('Sprites/Portrait.png').convert()
mouse_cursorload = pygame.image.load('Sprites/cursor.png').convert()
mouse_cursorload.set_colorkey((255,0,255))
mouse_cursor = pygame.transform.scale(mouse_cursorload, (17,24))
menu_sprite = pygame.image.load("Sprites/menu.png").convert()
player_img = pygame.image.load('Sprites/Spaceship.png').convert()
player_mini_image = pygame.transform.scale(player_img, (32, 32))
player_mini_image.set_colorkey(BLACK)
meteor_images = []
meteor_list = ['Sprites/Meteoro.png', 'Sprites/meteoro_grande.png', 'Sprites/meteoro_pequeno.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'Sprites/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append((img_sm))
    filename = 'Sprites/sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
img_go_screen = []
for i in range(16):
    filename = 'GO/Go_Screen0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img_go_screen.append(img)

pygame.mouse.set_visible(False)

powerup_images = {}
powerup_images['shield'] = pygame.image.load('Sprites/shield.png').convert()
powerup_images['gun'] = pygame.image.load('Sprites/bolt.png').convert()
powerup_images['drone'] = pygame.image.load('Sprites/dronepwr.png').convert()
shield_bar = pygame.image.load("Sprites/Shield_bar.png").convert()
shield_bar.set_colorkey((255, 0, 255))
shield_img = pygame.image.load("Sprites/shield.png").convert()
shield_img.set_colorkey((255, 0, 255))
shield = pygame.transform.scale(shield_img, (30, 30))
stars = pygame.image.load('Sprites/stars.png').convert()
trophyload = pygame.image.load('Sprites/trophy.png').convert()
trophyload.set_colorkey((255,0,255))
trophy = pygame.transform.scale(trophyload, (192, 240))

stars.set_colorkey((231, 231, 231))
stars.set_alpha(110)
y = 0

# load all the game sounds
volume = 0.3
player_shootsnd = pygame.mixer.Sound('Sounds/player_shoot.wav')
player_shootsnd.set_volume(volume)
player_shootsnd2 = pygame.mixer.Sound('Sounds/player_shoot2.wav')
player_shootsnd2.set_volume(volume)
player_shootsnd3 = pygame.mixer.Sound('Sounds/player_shoot3.wav')
player_shootsnd3.set_volume(volume)
player_shootlist = [player_shootsnd, player_shootsnd2, player_shootsnd3]
enemy_shootsnd = pygame.mixer.Sound('Sounds/enemy_shoot.wav')
enemy_shootsnd.set_volume(volume)
shieldsnd = pygame.mixer.Sound('Sounds/powerup3.wav')
shieldsnd.set_volume(volume)
powerupsnd = pygame.mixer.Sound('Sounds/powerup2.wav')
powerupsnd.set_volume(volume)
player_die_sound = pygame.mixer.Sound('Sounds/rumble1.ogg')
expl_sounds = []
soundlist = [player_shootsnd, enemy_shootsnd, shieldsnd, powerupsnd, player_die_sound]
for snd in ['Sounds/Explosion.wav', 'Sounds/Explosion2.wav', 'Sounds/Explosion3.wav']:
    expl_sounds.append(pygame.mixer.Sound(snd))
for snd in expl_sounds:
    snd.set_volume(volume)
    soundlist.append(snd)

music_volume = 1
pygame.mixer.music.load('Sounds/music.mp3')


drone = 0

# Game loop
set_highscore()
game_over = True
running = True
ismenu = True

while running:
    if ismenu:
        menu()
        ismenu = False
    if game_over:
        set_highscore()
        show_go_screen()
        game_over = False
        score = 0
        all_sprites = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        player = Player()
        # drone = Drone()
        # all_sprites.add(drone)
        all_sprites.add(player)
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        for i in range(4):
            newmob()
        for i in range(4):
            newmet()
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(loops=-1)
        for snd in soundlist:
            snd.set_volume(volume)
        moremobs = False
        controll = True
        levels = [10000, 20000, 40000, 60000, 80000,100000, 1000000000]
        levelsind = 0

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    for mob in mobs:
        if (mob.rect.x - 16 <= player.rect.x - 32 and mob.rect.x > player.rect.x - 32) or (
                mob.rect.x + 16 >= player.rect.x + 32 and mob.rect.x < player.rect.x + 32):
            mob.shoot()

    # Update
    all_sprites.update()

    #Test boss
    if score > levels[levelsind] and controll:
        moremobs = True
        controll = False


    if score >= levels[levelsind] and moremobs == True:
        moremobs = False
        newmob()
        newmob()
        levelsind += 1
        controll = True


    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()
        newpow()

    # check to see if a bullet hit a meteor
    hits2 = pygame.sprite.groupcollide(meteors, bullets, True, True)
    for hit in hits2:
        score += 50 - hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        random.choice(expl_sounds).play()
        newmet()
        newpow()

    # check to see if a enemy bullet hit the player
    hits3 = pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_rect)
    for hit in hits3:
        player.shield -= 45
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.shield <= 0:
            explode()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 45
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            explode()

    hits2 = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
    for hit in hits2:
        player.shield -= hit.radius * 1.2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmet()
        if player.shield <= 0:
            explode()

    # check if the player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 35)
            shieldsnd.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            powerupsnd.play()
        if hit.type == 'drone':
            if all_sprites.has(drone):
                drone.power += 1
            else:
                drone = Drone()
                all_sprites.add(drone)

    # if the player died and the explosion has finished playing
    if player.lives == 0:
        if score > highscore:
            with open('highscore.txt', 'w') as file:
                file.write(str(score))
        game_over = True
        ismenu = True
        set_highscore()

    # Draw / render
    screen.fill(BLUE)
    screen.blit(bg, background_rect)
    rel_y = y % stars.get_rect().height
    screen.blit(stars, (0, rel_y - stars.get_rect().height))
    if rel_y < HEIGHT:
        screen.blit(stars, (0, rel_y))
    y += 5
    all_sprites.draw(screen)
    draw_text(screen, str(score), 28, WIDTH / 2, 10)
    # draw_text(screen, str('Shield'), 22, 75, 25)
    draw_shield_bar(screen, 15, 15, player.shield)
    draw_lives(screen, WIDTH - 120, 10, player.lives, player_mini_image)
    screen.blit(shield, (175, 10))

    # *after* drawing everything, flip the display
    pygame.display.flip()
pygame.quit()