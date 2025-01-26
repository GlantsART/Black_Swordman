import pygame, os, sys
import random

player_img = 'samurai/randered/baze.png'
tiles_image = {'wall1': 'backgrounds/wall1.png',
               'wall2': 'backgrounds/wall2.png',
               'flour': 'backgrounds/flour1.png',
               'flour1': 'backgrounds/flour2.png',
               'flour2': 'backgrounds/flour1.png',
               'flour3': 'backgrounds/flour1.png',
               'flour4': 'backgrounds/flour1.png',
               'flour5': 'backgrounds/flour1.png',
               'flour6': 'backgrounds/flour1.png',
               'empty': 'backgrounds/Empty.png'}
player_group = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
wall1_sprites = pygame.sprite.Group()
wall2_sprites = pygame.sprite.Group()
end_group = pygame.sprite.Group()
room1 = pygame.sprite.Group()
room2 = pygame.sprite.Group()
room3 = pygame.sprite.Group()
room4 = pygame.sprite.Group()
room5 = pygame.sprite.Group()
room6 = pygame.sprite.Group()
room7 = pygame.sprite.Group()
room8 = pygame.sprite.Group()
room9 = pygame.sprite.Group()
room10 = pygame.sprite.Group()
room11 = pygame.sprite.Group()


antogonisti_sprites = pygame.sprite.Group()
health_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.dir = False
        self.protection_flag = False
        self.attack = 0
        self.run = 0
        self.dead = 0
        self.hurt = 0
        self.idle = 0
        self.image = load_image('samurai/randered/baze.png')
        self.hp = 100
        self.ticks = 0
        self.attack_anim = [load_image('samurai/randered/Attack1.png'), load_image('samurai/randered/Attack2.png'),
                            load_image('samurai/randered/Attack3.png'), load_image('samurai/randered/Attack4.png'),
                            load_image('samurai/randered/Attack5.png')]
        self.rect = self.image.get_rect().move((x * 50, y * 50))

    def set_pos(self, pos):
        self.rect = self.rect.move(pos[0], pos[1])
        if pos[0] < 0:
            self.dir = True
        elif pos[0] > 0:
            self.dir = False
        if pygame.sprite.spritecollideany(self, wall1_sprites) or pygame.sprite.spritecollideany(self, wall2_sprites):
            self.rect.move_ip((-pos[0], -pos[1]))
            return False
        return True

    def get_attack(self):
        return self.dir, self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2

    def get_pos(self):
        return self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2

    def get_hp(self):
        return self.hp

    def animation_script(self, attack_flag, run_flag, idle_flag, hurt_flag, dead_flag, protection_flag):
        self.ticks += 1
        if dead_flag:
            attack_flag, run_flag, idle_flag, hurt_flag, protection_flag = False, False, False, False, False
            if self.ticks % 6 == 0:
                self.dead += 1
                if self.dead <= 6:
                    self.image = pygame.transform.flip(load_image(f'samurai/randered/Dead{self.dead}.png'), self.dir,
                                                       False)
                elif self.dead > 10:
                    self.kill()
        elif hurt_flag:
            if self.ticks % 8 == 0:
                self.hurt += 1
                self.image = pygame.transform.flip(load_image(f'samurai/randered/Hurt{self.hurt}.png'), self.dir, False)
                if self.hurt == 3:
                    hurt_flag = False
                    idle_flag = True
                    self.hurt = 0
                    self.image = pygame.transform.flip(load_image('samurai/randered/baze.png'), self.dir, False)
        elif attack_flag:
            if self.ticks % 6 == 0:
                if self.attack == 7:
                    attack_flag = False
                    idle_flag = True
                    self.attack = 0
                    self.image = pygame.transform.flip(load_image('samurai/randered/baze.png'), self.dir, False)
                elif self.attack <= 4:
                    self.image = pygame.transform.flip(self.attack_anim[self.attack], self.dir, False)
                self.attack += 1
        elif protection_flag:
            self.image = pygame.transform.flip(load_image('samurai/randered/Protection.png'), self.dir, False)
        elif run_flag:
            if self.ticks % 6 == 0:
                self.run = (self.run) % 8 + 1
                self.image = pygame.transform.flip(load_image(f'samurai/randered/Run{self.run}.png'), self.dir, False)
                self.rect = pygame.Rect(self.rect.x, self.rect.y, 55, 104)
        else:
            if self.ticks % 10 == 0:
                self.idle = self.idle % 6 + 1
                self.image = pygame.transform.flip(load_image(f'samurai/randered/Idle{self.idle}.png'), self.dir, False)
            self.run = 0

        return attack_flag, run_flag, idle_flag, hurt_flag, dead_flag, protection_flag

    def get_room(self):
        if pygame.sprite.spritecollideany(self, room1):
            return 'flour'
        elif pygame.sprite.spritecollideany(self, room2):
            return 'flour1'
        elif pygame.sprite.spritecollideany(self, room3):
            return 'flour2'
        elif pygame.sprite.spritecollideany(self, room4):
            return 'flour3'
        elif pygame.sprite.spritecollideany(self, room5):
            return 'flour4'
        elif pygame.sprite.spritecollideany(self, room6):
            return 'flour5'

    def aliveCheck(self):
        if self.hp <= 0:
            return True
        return False

    def damage(self, flag, x, y, damage):
        if abs(self.rect.x + self.rect.w // 2 - x) < 100 and abs(
                self.rect.y + self.rect.h // 2 - y) < 100 and flag:
            if not self.protection_flag:
                self.hp -= damage
                return 'yes'
            return True
        return False

    def defend(self, flag):
        self.protection_flag = flag

    def health_upp(self, hlth):
        if pygame.sprite.spritecollideany(self, hlth):
            if self.hp <= 80:
                self.hp += 20
            else:
                self.hp = 100
            return True
        return False


class FallenAngel(pygame.sprite.Sprite):
    def __init__(self, image, type, x, y, place):
        super().__init__(antogonisti_sprites, all_sprites)
        self.image_start = image
        self.type = type
        self.image = load_image(f'{self.image_start}/base.png')
        self.rect = self.image.get_rect(center=(x * 50, y * 50))
        if self.type == 'Fallen Angel':
            self.hp = random.choice([100, 150, 200])
            self.damage = random.randint(10, 50)
            self.attack_max, self.dead_max = 6, 6
        elif self.type == 'Sceleton':
            self.hp = random.randint(10, 100)
            self.attack_max, self.dead_max = 4, 4
            self.damage = random.randint(10, 20)
        self.dir = False
        self.place = place
        self.active = False
        self.ticks = 0
        self.animation = 0
        self.attack_animation = 0
        self.attack_animation_flag = False
        self.dead_ticks = 0
        self.dead_flag = False

    def aliveORnot(self):
        if self.hp <= 0:
            return False
        return True

    def get_damage(self):
        return self.damage

    def kick(self, x, y, flag):
        if flag:
            self.attack_animation_flag = True

    def update(self, screen, pos, ticks):
        self.ticks += 1
        if self.active and self.hp > 0:
            x, y = 0, 0
            if not self.attack_animation_flag:
                if abs(self.rect.x + self.rect.w // 2 - pos[0]) > 70 or abs(
                        self.rect.y + self.rect.h // 2 - pos[1]) > 60:
                    if self.rect.x - pos[0] < 0:
                        self.rect = self.rect.move((2, 0))
                        x = 2
                        self.dir = False
                    else:
                        self.rect = self.rect.move((-2, 0))
                        x = -2
                        self.dir = True
                    if self.rect.y - pos[1] < 0:
                        self.rect = self.rect.move((0, 2))
                        y = 2
                    else:
                        self.rect = self.rect.move((0, -2))
                        y = -2
                    if self.ticks % 5 == 0:
                        self.animation = self.animation % 8 + 1
                        self.image = pygame.transform.flip(
                            load_image(f'{self.image_start}/Run{self.animation}.png'),
                            self.dir, False)

                    if pygame.sprite.spritecollideany(self, wall1_sprites):
                        self.rect = self.rect.move((-x, 0))

                    if pygame.sprite.spritecollideany(self, wall2_sprites):
                        self.rect = self.rect.move((0, -y))
            else:
                if self.ticks % 6 == 0:
                    if self.attack_animation != self.attack_max:
                        self.attack_animation += 1
                        self.image = pygame.transform.flip(
                            load_image(f'{self.image_start}/Attack{self.attack_animation}.png'), self.dir, False)
                    else:
                        self.attack_animation_flag = False
                        self.attack_animation = 0
                        self.image = pygame.transform.flip(
                            load_image(f'{self.image_start}/base.png'), self.dir, False)


        elif self.hp <= 0 and self.dead_ticks == 0:
            self.animation = 1
            self.dead_ticks += 1
        elif ((self.dead_ticks == 42 and self.type == 'Fallen Angel') or (self.dead_ticks in [31, 32, 34, 33, 36, 35, 37, 38, 39, 40, 41] and self.type == 'Sceleton')) and self.ticks % 150 == 0:
            self.kill()
        elif self.hp <= 0 and self.dead_ticks > 0 and self.animation <= self.dead_max:
            self.dead_ticks += 1
            if (self.dead_ticks % 7 == 0 and self.type == 'Fallen Angel') or (self.ticks % 10 == 0 and self.type == 'Sceleton'):
                self.image = pygame.transform.flip(load_image(f'{self.image_start}/Dead{self.animation}.png'),
                                                   self.dir, False)
                self.animation += 1
        screen.blit(self.image, self.rect)

    def playerShot(self, dir, x, y):
        if not dir:
            if self.rect.x + self.rect.w // 2 in range(x, x + 100) and self.rect.y + self.rect.h // 2 in range(y - 50,
                                                                                                               y + 70):
                self.hp -= 50
        else:
            if self.rect.x + 38 in range(x - 80, x) and self.rect.y + 44 in range(y - 50, y + 70):
                self.hp -= 50

    def checkActive(self, place):
        if self.place == place:
            self.active = True

    def attacking(self):
        return self.dir, self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, flag=False):
        super().__init__(tile_group, all_sprites)
        self.image = load_image(tiles_image[tile_type])
        self.type = tile_type
        if flag:
            self.rect = pygame.Rect(pos_x, pos_y, 20, 5)
        else:
            self.rect = pygame.Rect(50 * pos_x, 50 * pos_y, 20, 5)

        if self.type == 'wall1':
            wall1_sprites.add(self)
        elif self.type == 'wall2':
            wall2_sprites.add(self)
        elif self.type == 'flour':
            room1.add(self)
        elif self.type == 'flour1':
            room2.add(self)
        elif self.type == 'flour2':
            room3.add(self)
        elif self.type == 'flour3':
            room4.add(self)
        elif self.type == 'flour4':
            room5.add(self)
        elif self.type == 'flour5':
            room6.add(self)
        self.hp = 100

    def get_type(self):
        return self.type

class Health(pygame.sprite.Sprite):
    def __init__(self, image1, image2, x, y):
        super().__init__(health_group, all_sprites, tile_group)
        self.image = load_image(image1)
        self.image2 = image2
        self.rect = pygame.Rect(50 * x, 50 * y, 20, 5)
        self.pos_x, self.pos_y = x, y
        self.used = False

    def destroy(self, flag):
        if flag:
            self.image = load_image(self.image2)
            self.used = True

    def get_full(self):
        return self.used

class EndTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(tile_group, all_sprites, end_group)
        self.image = load_image('backgrounds/portal.png')
        self.rect = pygame.Rect(50 * x, 50 * y, 20, 5)

    def checkCollision(self, player):
        if pygame.sprite.spritecollideany(self, player):
            return True
        return False
