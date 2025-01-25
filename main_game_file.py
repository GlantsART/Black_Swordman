import pygame, os, sys
from characters import Player, Tile, player_group, tile_group, all_sprites, FallenAngel, antogonisti_sprites
from button import Button, load_image
from decore import Text, word_group, draw_lives

pygame.init()

FPS = 100
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x -= self.dx
        obj.rect.y -= self.dy

    def update(self, target):
        self.dx = (target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = (target.rect.y + target.rect.h // 2 - HEIGHT // 2)


camera = Camera()

def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    return level_map


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


def generate_level(level):
    player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '+':
                Tile('wall1', x, y)
            elif level[y][x] == '-':
                Tile('flour', x, y)
            elif level[y][x] == '=':
                Tile('flour1', x, y)
            elif level[y][x] == '/':
                Tile('flour2', x, y)
            elif level[y][x] == '#':
                Tile('wall2', x, y)
            elif level[y][x] == '@':
                if level[y][x-1] == '-':
                    Tile('flour', x, y)
                    FallenAngel(x, y, 'flour')
                elif level[y][x-1] == '=':
                    Tile('flour1', x, y)
                    FallenAngel(x, y, 'flour1')
                elif level[y][x-1] == '/':
                    Tile('flour2', x, y)
                    FallenAngel(x, y, 'flour2')

            elif level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '$':
                player = Player(x, y)
                Tile('flour', x, y)
    return player


def terminate():
    pygame.display.set_caption('closing')
    pygame.display.set_mode((600, 800))
    ticks = 0
    text = ['please wait', 'please wait.', 'please wait..', 'please wait...']
    font = pygame.font.Font('data/fonts/go3v2.ttf', 50)
    while True:
        ticks += 1
        if ticks == 200:
            break
        screen.blit(load_image('backgrounds/bg6.jpg'), (0, 0))
        txt = font.render(text[ticks // 50], True, (0, 0, 0))
        screen.blit(txt, (20, 20))
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


def options():
    pygame.display.set_caption('options')
    game_mouse_pos = (0, 0)
    back_menu_button = exit_menu_button = Button('backgrounds/button2.png', (30, 30), 'x',
                                                 'data/fonts/go3v2.ttf', 40, 45,
                                                 (0, 0, 0), (255, 176, 176))

    while True:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_menu_button.checkForInput(event.pos):
                    main_menu()
            if event.type == pygame.MOUSEMOTION:
                game_mouse_pos = event.pos

        for button in [back_menu_button]:
            button.changeColor(game_mouse_pos)
            button.update(screen)
        pygame.display.flip()


def load_screen():
    pygame.display.set_caption('launch...')
    ticks = 0
    load_x = 0
    while True:
        screen.fill('black')
        ticks += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if ticks >= 300:
                    main_menu()

        screen.blit(load_image('backgrounds/bg3.jpg'), (-200, 0))

        font = pygame.font.Font('data/fonts/go3v2.ttf', 100)
        text = font.render('Black Swordman', True, (61, 7, 7))
        text2 = font.render('Black Swordman', True, (255, 221, 148))
        screen.blit(text2, (318, 48))
        screen.blit(text, (320, 50))
        pygame.draw.rect(screen, (61, 7, 7), (320, 160, 580, 55), width=3)
        if ticks % 10 == 0 and ticks <= 300:
            load_x += 19
        pygame.draw.rect(screen, (61, 7, 7), (325, 165, load_x, 45))
        font = pygame.font.Font('data/fonts/go3v2.ttf', 40)
        text3 = font.render('loading...', True, (216, 111, 28))
        screen.blit(text3, (335, 166))

        if ticks > 300:
            font = pygame.font.Font('data/fonts/kashimarusbycop.otf', 30)
            text4 = font.render('Нажмите любую кнопку чтобы продолжить.', True, (61, 7, 7))
            screen.blit(text4, (340, 220))

        pygame.display.flip()


def levels_menu():
    pygame.display.set_caption('chouse level')
    lvl_mouse_pos = (0, 0)
    exit_menu_button_lvl = Button('backgrounds/button2.png', (30, 30), 'x',
                                  'data/fonts/go3v2.ttf', 40, 45,
                                  (0, 0, 0), (255, 176, 176))
    level_one_button = Button('backgrounds/level1.png', (200, 400), '',
                              'data/fonts/go3v2.ttf', 40, 45,
                              (0, 0, 0), (255, 176, 176), 'backgrounds/level1-1.png')

    while True:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_menu_button_lvl.checkForInput(event.pos):
                    main_menu()
                if level_one_button.checkForInput(event.pos):
                    game()
            if event.type == pygame.MOUSEMOTION:
                lvl_mouse_pos = event.pos

        for button in [exit_menu_button_lvl, level_one_button]:
            button.changeColor(lvl_mouse_pos)
            if button == level_one_button:
                button.update_photo(lvl_mouse_pos)
            button.update(screen)

        pygame.draw.rect(screen, 'white', (425, 100, 300, 600))
        pygame.draw.rect(screen, 'white', (800, 100, 300, 600))
        pygame.display.flip()


def game():
    pygame.display.set_caption('game')
    game_mouse_pos = (0, 0)
    clock = pygame.time.Clock()
    player = generate_level(load_level('level1.txt'))
    exit_menu_button = Button('backgrounds/button2.png', (30, 30), 'x',
                              'data/fonts/go3v2.ttf', 40, 45,
                              (0, 0, 0), (255, 176, 176))

    attack_flag = False  # когда mousebuttondown                                                 3 +
    attack_ticks = 0
    run_flag = False  # когда не attack и не protection и не dead и не hurt и когда двигается    5 +
    idle_flag = True  # всегда в иных случаях                                                    6
    hurt_flag = False  # когда hp становится меньше                                              2
    dead_flag = False  # когда hp < 0                                                            1 +-
    protection_flag = False  # Когда зажата пкм                                                  4 +
    flag = False

    ticks = 0
    enemis_kick = False
    camera.update(player)
    for tile in all_sprites:
        camera.apply(tile)

    while True:
        screen.fill((4, 5, 25))
        ticks += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                game_mouse_pos = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_menu_button.checkForInput(event.pos):
                    for tile in all_sprites:
                        tile.kill()
                    main_menu()
                else:
                    if not dead_flag and not hurt_flag and not attack_flag:
                        attack_flag = True
                        run_flag, idle_flag, protection_flag = False, False, False
                        if attack_flag:
                            dir, x, y = player.get_attack()
                            for enemis in antogonisti_sprites:
                                enemis.playerShot(dir, x, y)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if not dead_flag and not hurt_flag and not attack_flag:
                    run_flag, idle_flag, protection_flag = False, False, True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                protection_flag, idle_flag = False, True

        player.defend(protection_flag)
        move_x_flag, move_y_flag = False, False
        if not attack_flag and not protection_flag and not hurt_flag and not dead_flag:
            keys = list(pygame.key.get_pressed())
            if keys[4]:
                move_x_flag = player.set_pos((-3, 0))
                idle_flag = False
                run_flag = True
            elif keys[7]:
                move_x_flag = player.set_pos((3, 0))
                idle_flag = False
                run_flag = True
            if keys[22]:
                move_y_flag = player.set_pos((0, 3))
                idle_flag = False
                run_flag = True
            elif keys[26]:
                move_y_flag = player.set_pos((0, -3))
                idle_flag = False
                run_flag = True
        if not move_x_flag and not move_y_flag:
            run_flag = False
        else:
            camera.update(player)
            for tile in all_sprites:
                pass
                camera.apply(tile)

        for enemis in antogonisti_sprites:
            enemis.checkActive(player.get_room())

        if ticks % 200 == 0:
            for enemis in antogonisti_sprites:
                dir, x, y = enemis.attacking()
                flag = player.damage(enemis.aliveORnot(), x, y)
                enemis.kick(x, y, flag)

        dead_flag = player.aliveCheck()

        if not dead_flag and flag == 'yes':
            flag = False
            hurt_flag = True
            attack_ticks, run_flag, idle_flag, protection_flag = False, False, False, False

        attack_flag, run_flag, idle_flag, hurt_flag, dead_flag, protection_flag = player.animation_script(
            attack_flag, run_flag, idle_flag, hurt_flag, dead_flag, protection_flag)

        tile_group.draw(screen)
        player_group.draw(screen)
        antogonisti_sprites.update(screen, player.get_pos(), ticks)

        for button in [exit_menu_button]:
            button.changeColor(game_mouse_pos)
            button.update(screen)

        draw_lives(screen, player.get_hp())

        clock.tick(FPS)
        pygame.display.flip()


def main_menu():
    pygame.display.set_caption('menu')
    menu_mouse_pos = (0, 0)
    play_button = Button('backgrounds/button1.png', (600, 200), 'play',
                         'data/fonts/go3v2.ttf', 70, 80,
                         (0, 0, 0), (255, 176, 176))
    option_button = Button('backgrounds/button1.png', (600, 350), 'options',
                           'data/fonts/go3v2.ttf', 70, 80, (0, 0, 0),
                           (255, 176, 176))
    exit_button = Button('backgrounds/button1.png', (600, 500), 'exit',
                         'data/fonts/go3v2.ttf', 70, 80, (0, 0, 0),
                         (255, 176, 176))
    word = ['B', 55, 'l', 50, 'a', 60, 'c', 60, 'k', 60, ' ', 60, 'S', 55, 'w', 70, 'o', 60, 'r', 60, 'd', 60, 'm', 65,
            'a', 60, 'n', 60]
    if word_group == []:
        for w in range(0, len(word), 2):
            Text(word[w], 190, 80, 'red', (255, 176, 176), word[w + 1])

    while True:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                menu_mouse_pos = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(event.pos):
                    levels_menu()
                if option_button.checkForInput(event.pos):
                    options()
                if exit_button.checkForInput(event.pos):
                    terminate()

        screen.blit(pygame.transform.scale(load_image('backgrounds/bg1.png'), (1200, 800)), (0, 0))
        screen.blit(pygame.transform.scale(load_image('backgrounds/bg1.jpg'), (600, 800)), (300, 0))
        for w in word_group:
            w.CheckForInput(menu_mouse_pos)
            w.draw(screen)

        for button in [play_button, option_button, exit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    load_screen()
