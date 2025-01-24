from time import process_time_ns

import pygame, os, sys
import random

player_img = 'samurai/randered/baze.png'
tiles_image = {'wall1': 'backgrounds/wall1.png',
               'wall2': 'backgrounds/wall2.png',
               'flour': 'backgrounds/flour1.png',
               'flour1': 'backgrounds/flour2.png',
               'flour2': 'backgrounds/flour1.png',
               'empty': 'backgrounds/Empty.png'}
player_group = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
wall1_sprites = pygame.sprite.Group()
wall2_sprites = pygame.sprite.Group()
room1 = pygame.sprite.Group()
room2 = pygame.sprite.Group()
room3 = pygame.sprite.Group()
antogonisti_sprites = pygame.sprite.Group()


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
            self.image = pygame.transform.flip(load_image('samurai/randered/baze.png'), self.dir, False)
            self.run = 0

        return attack_flag, run_flag, idle_flag, hurt_flag, dead_flag, protection_flag

    def get_room(self):
        if pygame.sprite.spritecollideany(self, room1):
            return 'flour'
        elif pygame.sprite.spritecollideany(self, room2):
            return 'flour1'
        elif pygame.sprite.spritecollideany(self, room3):
            return 'flour2'

    def aliveCheck(self):
        if self.hp <= 0:
            return True
        return False

    def damage(self, flag, x, y):
        if abs(self.rect.x + self.rect.w // 2 - x) < 100 and abs(
                self.rect.y + self.rect.h // 2 - y) < 100 and flag:
            if not self.protection_flag:
                self.hp -= 50
                return 'yes'
            return True
        return False

    def defend(self, flag):
        self.protection_flag = flag


class FallenAngel(pygame.sprite.Sprite):
    def __init__(self, x, y, place):
        super().__init__(antogonisti_sprites, all_sprites)
        self.image = load_image('fallen_angels/rendered/angel.png')
        self.rect = self.image.get_rect(center=(x * 50, y * 50))
        self.hp = 100
        self.dir = False
        self.place = place
        self.active = False
        self.ticks = 0
        self.dir = False
        self.animation = 0
        self.attack_animation = 0
        self.attack_animation_flag = False
        self.dead_ticks = 0
        self.dead_flag = False

    def aliveORnot(self):
        if self.hp <= 0:
            return False
        return True

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
                        self.rect = self.rect.move((1, 0))
                        x = 2
                        self.dir = False
                    else:
                        self.rect = self.rect.move((-1, 0))
                        x = -2
                        self.dir = True
                    if self.rect.y - pos[1] < 0:
                        self.rect = self.rect.move((0, 1))
                        y = 2
                    else:
                        self.rect = self.rect.move((0, -1))
                        y = -2
                    if self.ticks % 5 == 0:
                        self.animation = self.animation % 8 + 1
                        self.image = pygame.transform.flip(
                            load_image(f'fallen_angels/rendered/Run{self.animation}.png'),
                            self.dir, False)

                    if pygame.sprite.spritecollideany(self, wall1_sprites):
                        self.rect = self.rect.move((-x, 0))

                    if pygame.sprite.spritecollideany(self, wall2_sprites):
                        self.rect = self.rect.move((0, -y))
            else:
                if self.ticks % 6 == 0:
                    if self.attack_animation != 6:
                        self.attack_animation += 1
                        self.image = pygame.transform.flip(
                            load_image(f'fallen_angels/rendered/Attack{self.attack_animation}.png'), self.dir, False)
                    else:
                        self.attack_animation_flag = False
                        self.attack_animation = 0
                        self.image = pygame.transform.flip(
                            load_image(f'fallen_angels/rendered/angel.png'), self.dir, False)


        elif self.hp <= 0 and self.dead_ticks == 0:
            self.animation = 1
            self.dead_ticks += 1
        elif self.dead_ticks == 42 and self.ticks % 150 == 0:
            self.kill()
        elif self.hp <= 0 and self.dead_ticks > 0 and self.animation <= 6:
            self.dead_ticks += 1
            if self.dead_ticks % 7 == 0:
                self.image = pygame.transform.flip(load_image(f'fallen_angels/rendered/Dead{self.animation}.png'),
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
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_group, all_sprites)
        self.image = load_image(tiles_image[tile_type])
        self.type = tile_type
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
        self.hp = 100

    def get_type(self):
        return self.type
