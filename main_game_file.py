import pygame, os, sys
from scripts.characters import Player, Tile, player_group, tile_group, all_sprites, FallenAngel, antogonisti_sprites, \
    Health, health_group, EndTile
from scripts.button import Button, load_image
from scripts.decore import Text, word_group, draw_lives

pygame.init()

FPS = 100
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
level_now = 1
load_screen_music = pygame.mixer.Sound('data/sounds/load_screen.mp3')
sound1 = pygame.mixer.Sound('data/sounds/click.ogg')
sound2 = pygame.mixer.Sound('data/sounds/sword.mp3')
sound3 = pygame.mixer.Sound('data/sounds/sword_shot.mp3')
sound4 = pygame.mixer.Sound('data/sounds/win.ogg')
sound5 = pygame.mixer.Sound('data/sounds/hill.mp3')
sound6 = pygame.mixer.Sound('data/sounds/game over.mp3')

with open('settings_files/player_settings', 'r') as file:
    for i, row in enumerate(file):
        if i == 0:
            game_volume = float(row)
        elif i == 1:
            menu_volume = float(row)
        else:
            another_volume = float(row)
    file.close()


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
    if 1 <= level_now <= 3:
        a = 0
    elif 4 <= level_now <= 6:
        a = 1
    player, portal = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '+':
                Tile('wall1', x, y, a)
            elif level[y][x] == '-':
                Tile('flour', x, y, a)
            elif level[y][x] == '=':
                Tile('flour1', x, y, a)
            elif level[y][x] == '|':
                Tile('flour5', x, y, a)
            elif level[y][x] == '%':
                Tile('flour4', x, y, a)
            elif level[y][x] == '^':
                Tile('flour3', x, y, a)
            elif level[y][x] == '/':
                Tile('flour2', x, y, a)
            elif level[y][x] == ':':
                Tile('flour6', x, y, a)
            elif level[y][x] == '(':
                Tile('flour7', x, y, a)
            elif level[y][x] == '#':
                Tile('wall2', x, y, a)
            elif level[y][x] == ';':
                Tile('flour8', x, y, a)
            elif level[y][x] == '*':
                Tile('flour9', x, y, a)

            elif level[y][x] == '@':
                if level[y][x - 1] == '-':
                    Tile('flour', x, y, a)
                    FallenAngel('fallen_angels/rendered', 'Fallen Angel', x, y, 'flour')
                elif level[y][x - 1] == '=':
                    Tile('flour1', x, y, a)
                    FallenAngel('fallen_angels/rendered', 'Fallen Angel', x, y, 'flour1')
                elif level[y][x - 1] == '/':
                    Tile('flour2', x, y, a)
                    FallenAngel('fallen_angels/rendered', 'Fallen Angel', x, y, 'flour2')
                elif level[y][x - 1] == '^':
                    Tile('flour3', x, y, a)
                    FallenAngel('fallen_angels/rendered', 'Fallen Angel', x, y, 'flour3')
                elif level[y][x - 1] == '%':
                    Tile('flour4', x, y, a)
                    FallenAngel('fallen_angels/rendered', 'Fallen Angel', x, y, 'flour4')
                elif level[y][x - 1] == '|':
                    Tile('flour5', x, y, a)
                    FallenAngel('fallen_angels/rendered', 'Fallen Angel', x, y, 'flour5')
                elif level[y][x - 1] == ':':
                    Tile('flour6', x, y, a)
                    FallenAngel('fallen_angels/rendered', 'Fallen Angel', x, y, 'flour6')
                elif level[y][x - 1] == '(':
                    Tile('flour7', x, y, a)
                    FallenAngel('fallen_angels/rendered', 'Fallen Angel', x, y, 'flour7')
                elif level[y][x - 1] == ';':
                    Tile('flour8', x, y, a)
                    FallenAngel('fallen_angels/rendered', 'Fallen Angel', x, y, 'flour8')
                elif level[y][x - 1] == '*':
                    Tile('flour9', x, y, a)
                    FallenAngel('fallen_angels/rendered', 'Fallen Angel', x, y, 'flour9')


            elif level[y][x] == '&':
                if level[y][x - 1] == '-':
                    Tile('flour', x, y, a)
                    FallenAngel('skeleton/rendered1', 'Sceleton', x, y, 'flour')
                elif level[y][x - 1] == '=':
                    Tile('flour1', x, y, a)
                    FallenAngel('skeleton/rendered1', 'Sceleton', x, y, 'flour1')
                elif level[y][x - 1] == '/':
                    Tile('flour2', x, y, a)
                    FallenAngel('skeleton/rendered1', 'Sceleton', x, y, 'flour2')
                elif level[y][x - 1] == '^':
                    Tile('flour3', x, y, a)
                    FallenAngel('skeleton/rendered1', 'Sceleton', x, y, 'flour3')
                elif level[y][x - 1] == '%':
                    Tile('flour4', x, y, a)
                    FallenAngel('skeleton/rendered1', 'Sceleton', x, y, 'flour4')
                elif level[y][x - 1] == '|':
                    Tile('flour5', x, y, a)
                    FallenAngel('skeleton/rendered1', 'Sceleton', x, y, 'flour5')
                elif level[y][x - 1] == ':':
                    Tile('flour6', x, y, a)
                    FallenAngel('skeleton/rendered1', 'Sceleton', x, y, 'flour6')
                elif level[y][x - 1] == '(':
                    Tile('flour7', x, y, a)
                    FallenAngel('skeleton/rendered1', 'Sceleton', x, y, 'flour7')
                elif level[y][x - 1] == ';':
                    Tile('flour8', x, y, a)
                    FallenAngel('skeleton/rendered1', 'Sceleton', x, y, 'flour8')
                elif level[y][x - 1] == '*':
                    Tile('flour9', x, y, a)
                    FallenAngel('skeleton/rendered1', 'Sceleton', x, y, 'flour9')

            elif level[y][x] == '.':
                Tile('empty', x, y, 0)
            elif level[y][x] == '$':
                player = Player(x, y)
                Tile('flour', x, y, a)
            elif level[y][x] == '!':
                Health('health1', 'health2', x, y, a)
            elif level[y][x] == '}':
                portal = EndTile(x, y)
    return player, portal


def terminate():
    '''pygame.display.set_caption('closing')
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
        pygame.display.flip()'''
    pygame.quit()
    sys.exit()


def options():
    global menu_volume, game_volume, another_volume
    pygame.display.set_caption('options')
    game_mouse_pos = (0, 0)
    back_menu_button = Button('backgrounds/button2.png', (30, 30), 'x',
                              'data/fonts/go3v2.ttf', 40, 45,
                              (0, 0, 0), (255, 176, 176))
    height_menu_music = Button('backgrounds/button5.png', (500, 385), '+',
                               'data/fonts/kashimarusbycop.otf', 50, 70,
                               (255, 255, 255), (217, 217, 217))
    less_menu_music = Button('backgrounds/button5.png', (375, 385), '-',
                             'data/fonts/kashimarusbycop.otf', 50, 70,
                             (255, 255, 255), (217, 217, 217))
    height_game_music = Button('backgrounds/button5.png', (500, 320), '+',
                               'data/fonts/kashimarusbycop.otf', 50, 70,
                               (255, 255, 255), (217, 217, 217))
    less_game_music = Button('backgrounds/button5.png', (375, 320), '-',
                             'data/fonts/kashimarusbycop.otf', 50, 70,
                             (255, 255, 255), (217, 217, 217))
    height_another_music = Button('backgrounds/button5.png', (575, 445), '+',
                                  'data/fonts/kashimarusbycop.otf', 50, 70,
                                  (255, 255, 255), (217, 217, 217))
    less_another_music = Button('backgrounds/button5.png', (450, 445), '-',
                                'data/fonts/kashimarusbycop.otf', 50, 70,
                                (255, 255, 255), (217, 217, 217))

    while True:
        words = ['run: a, w, s, d', 'hit: left mouse button', 'block: right mouse button']
        screen.blit(pygame.transform.scale(load_image('backgrounds/bg8.jpg'), (1200, 800)), (0, 0))

        font = pygame.font.Font('data/fonts/go3v2.ttf', 75)
        text1 = font.render('Options', True, (204, 3, 0))
        font = pygame.font.Font('data/fonts/go3v2.ttf', 40)
        text3 = font.render('game music:', True, (204, 3, 0))
        text4 = font.render('menu music:', True, (204, 3, 0))
        text5 = font.render('another color:', True, (204, 3, 0))
        text2 = font.render('control:', True, (204, 3, 0))
        font = pygame.font.Font('data/fonts/go3v2.ttf', 35)
        y = 100
        for word in words:
            text = font.render(word, True, (204, 3, 0))
            screen.blit(text, (100, y))
            y += 40
        screen.blit(text1, (450, 0))
        screen.blit(text2, (100, 40))
        screen.blit(text3, (100, 300))
        screen.blit(text4, (100, 360))
        screen.blit(text5, (100, 420))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_menu_button.checkForInput(event.pos):
                    sound1.play()
                    with open('settings_files/player_settings', 'w') as file:
                        file.write(str(game_volume) + '\n')
                        file.write(str(menu_volume) + '\n')
                        file.write(str(another_volume) + '\n')
                    file.close()
                    main_menu()
                elif height_menu_music.checkForInput(event.pos) and menu_volume < 0.95:
                    sound1.play()
                    menu_volume += 0.1
                    pygame.mixer.music.set_volume(menu_volume)
                elif less_menu_music.checkForInput(event.pos) and menu_volume >= 0.1:
                    sound1.play()
                    menu_volume -= 0.1
                    pygame.mixer.music.set_volume(menu_volume)
                elif height_game_music.checkForInput(event.pos) and game_volume < 0.95:
                    sound1.play()
                    game_volume += 0.1
                elif less_game_music.checkForInput(event.pos) and game_volume >= 0.1:
                    sound1.play()
                    game_volume -= 0.1
                elif height_another_music.checkForInput(event.pos) and another_volume < 0.95:
                    sound1.play()
                    another_volume += 0.1
                elif less_another_music.checkForInput(event.pos) and another_volume >= 0.1:
                    sound1.play()
                    another_volume -= 0.1
            if event.type == pygame.MOUSEMOTION:
                game_mouse_pos = event.pos

        if menu_volume > 0.95:
            text_menu_music = font.render('max', True, (0, 0, 0))
            x = -10
        elif menu_volume >= 0.1:
            text_menu_music = font.render(str(round(menu_volume, 1)), True, (0, 0, 0))
            x = 0
        else:
            text_menu_music = font.render('off', True, (0, 0, 0))
            x = -5

        if game_volume > 0.95:
            text_game_music = font.render('max', True, (0, 0, 0))
            xx = -10
        elif game_volume >= 0.1:
            text_game_music = font.render(str(round(game_volume, 1)), True, (0, 0, 0))
            xx = 0
        else:
            text_game_music = font.render('off', True, (0, 0, 0))
            xx = -5

        if another_volume > 0.95:
            text_another_volume = font.render('max', True, (0, 0, 0))
            xxx = -10
        elif another_volume >= 0.1:
            text_another_volume = font.render(str(round(another_volume, 1)), True, (0, 0, 0))
            xxx = 0
        else:
            text_another_volume = font.render('off', True, (0, 0, 0))
            xxx = -5
        screen.blit(text_menu_music, (415 + x, 365))
        screen.blit(text_game_music, (415 + xx, 305))
        screen.blit(text_another_volume, (490 + xxx, 425))
        update_sounds()

        for button in [back_menu_button, height_menu_music, less_menu_music, less_game_music, height_game_music,
                       height_another_music, less_another_music]:
            button.changeColor(game_mouse_pos)
            button.update(screen)
        pygame.display.flip()


def update_sounds():
    pygame.mixer.music.set_volume(menu_volume)
    sound1.set_volume(another_volume)
    sound2.set_volume(another_volume)
    sound3.set_volume(another_volume)
    sound4.set_volume(another_volume)
    sound5.set_volume(another_volume)
    sound6.set_volume(another_volume)




def dead_menu():
    global level_now
    dead_menu_mouse_pos = (0, 0)
    sound6.play()
    restart = Button('backgrounds/button1.png', (400, 450), 'restart', 'data/fonts/go3v2.ttf', 60, 65,
                     (0, 0, 0), (255, 176, 176))
    back_menu_button = Button('backgrounds/button1.png', (800, 450), 'menu', 'data/fonts/go3v2.ttf', 60, 65,
                              (0, 0, 0), (255, 176, 176))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                dead_menu_mouse_pos = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_menu_button.checkForInput(event.pos):
                    sound1.play()
                    sound6.stop()
                    main_menu()
                elif restart.checkForInput(event.pos):
                    sound1.play()
                    sound6.stop()
                    game(level_now)

        pygame.draw.rect(screen, 'black', (0, 200, 1800, 400))
        font = pygame.font.Font('data/fonts/go3v2.ttf', 100)
        text = font.render('You died', True, (128, 5, 5))
        screen.blit(text, (400, 220))

        for button in [back_menu_button, restart]:
            button.changeColor(dead_menu_mouse_pos)
            button.update(screen)

        pygame.display.flip()


def load_screen():
    pygame.display.set_caption('launch...')
    ticks = 0
    load_x = 0
    load_screen_music.play()
    while True:
        screen.fill('black')
        ticks += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if ticks >= 300:
                    load_screen_music.stop()
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
    global level_now
    pygame.display.set_caption('chouse level')
    lvl_mouse_pos = (0, 0)
    complited_levels = ''
    with open('settings_files/complited_levels.txt', 'r') as file:
        for i, s in enumerate(file):
            complited_levels += s
        file.close()

    exit_menu_button_lvl = Button('backgrounds/button2.png', (30, 30), 'x',
                                  'data/fonts/go3v2.ttf', 40, 45,
                                  (0, 0, 0), (255, 176, 176))
    level_one_button = Button('backgrounds/level1.png', (130, 237), '',
                              'data/fonts/go3v2.ttf', 40, 45,
                              (0, 0, 0), (255, 176, 176), 'backgrounds/level1-1.png')
    level_two_button = Button('backgrounds/level2.png', (300, 237), '',
                              'data/fonts/go3v2.ttf', 40, 45,
                              (0, 0, 0), (255, 176, 176), 'backgrounds/level2-1.png')
    level_three_button = Button('backgrounds/level3.png', (470, 237), '',
                                'data/fonts/go3v2.ttf', 40, 45,
                                (0, 0, 0), (255, 176, 176), 'backgrounds/level3-1.png')
    level_four_button = Button('backgrounds/level4.png', (130, 512), '',
                               'data/fonts/go3v2.ttf', 40, 45,
                               (0, 0, 0), (255, 176, 176), 'backgrounds/level4-1.png')
    level_five_button = Button('backgrounds/level5.png', (300, 512), '',
                               'data/fonts/go3v2.ttf', 40, 45,
                               (0, 0, 0), (255, 176, 176), 'backgrounds/level5-1.png')
    level_six_button = Button('backgrounds/level6.png', (470, 512), '',
                              'data/fonts/go3v2.ttf', 40, 45,
                              (0, 0, 0), (255, 176, 176), 'backgrounds/level6-1.png')

    while True:
        screen.blit(load_image('backgrounds/bg7.jpg'), (0, 0))
        font = pygame.font.Font('data/fonts/go3v2.ttf', 75)
        text = font.render('Levels', True, (219, 0, 0))
        font = pygame.font.Font('data/fonts/go3v2.ttf', 25)
        text1 = font.render('location 1: underground', True, (219, 0, 0))
        text2 = font.render('location 2: streets of town', True, (219, 0, 0))

        screen.blit(text, (450, 0))
        screen.blit(text1, (150, 100))
        screen.blit(text2, (150, 375))

        pygame.draw.rect(screen, (237, 214, 5), (50, 100, 500, 245), width=2)
        pygame.draw.rect(screen, (237, 214, 5), (50, 375, 500, 245), width=2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_menu_button_lvl.checkForInput(event.pos):
                    sound1.play()
                    main_menu()
                elif level_one_button.checkForInput(event.pos):
                    sound1.play()
                    level_now = 1
                    pygame.mixer.music.pause()
                    game(1)
                elif level_two_button.checkForInput(event.pos) and '2' in complited_levels:
                    level_now = 2
                    pygame.mixer.music.pause()
                    sound1.play()
                    game(2)
                elif level_three_button.checkForInput(event.pos) and '3' in complited_levels:
                    level_now = 3
                    sound1.play()
                    pygame.mixer.music.pause()
                    game(3)
                elif level_four_button.checkForInput(event.pos) and '4' in complited_levels:
                    level_now = 4
                    sound1.play()
                    pygame.mixer.music.pause()
                    game(4)
                elif level_five_button.checkForInput(event.pos) and '5' in complited_levels:
                    level_now = 5
                    sound1.play()
                    pygame.mixer.music.pause()
                    game(5)
                elif level_six_button.checkForInput(event.pos) and '6' in complited_levels:
                    level_now = 6
                    sound1.play()
                    pygame.mixer.music.pause()
                    game(6)
            if event.type == pygame.MOUSEMOTION:
                lvl_mouse_pos = event.pos

        for button in [exit_menu_button_lvl, level_one_button, level_two_button, level_three_button, level_four_button,
                       level_five_button, level_six_button]:
            button.changeColor(lvl_mouse_pos)
            if button in [level_one_button, level_two_button, level_three_button, level_four_button, level_five_button,
                          level_six_button]:
                button.update_photo(lvl_mouse_pos)
            button.update(screen)

        pygame.display.flip()


def victory_menu():
    global level_now
    mouse_pos = (0, 0)
    sound4.play()
    next_level_button = Button('backgrounds/button4.png', (400, 450), 'next level', 'data/fonts/go3v2.ttf', 47, 52,
                               (0, 0, 0), (255, 246, 163))
    back_menu_button = Button('backgrounds/button4.png', (800, 450), 'menu', 'data/fonts/go3v2.ttf', 50, 57,
                              (0, 0, 0), (255, 246, 163))
    with open('settings_files/complited_levels.txt', 'a') as file:
        file.write(str(level_now + 1))
        file.close()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_level_button.checkForInput(event.pos):
                    level_now += 1
                    sound1.play()
                    game(level_now)
                elif back_menu_button.checkForInput(event.pos):
                    sound1.play()
                    main_menu()

        pygame.draw.rect(screen, 'black', (0, 200, 1800, 400))
        font = pygame.font.Font('data/fonts/go3v2.ttf', 120)
        text = font.render('Victory', True, (224, 202, 0))
        screen.blit(text, (390, 220))

        for button in [back_menu_button, next_level_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        pygame.display.flip()


def game(level_number):
    pygame.display.set_caption('game')
    pygame.mixer.music.load('data/sounds/game.mp3')
    pygame.mixer.music.set_volume(game_volume)
    pygame.mixer.music.play(-1)
    game_mouse_pos = (0, 0)
    player, portal = generate_level(load_level(f'data/levels/level{level_number}.txt'))
    exit_menu_button = Button('backgrounds/button2.png', (30, 30), 'x',
                              'data/fonts/go3v2.ttf', 40, 45,
                              (0, 0, 0), (255, 176, 176))

    attack_flag = False  # когда mousebuttondown                                                 3 +
    run_flag = False  # когда не attack и не protection и не dead и не hurt и когда двигается    5 +
    idle_flag = True  # всегда в иных случаях                                                    6
    hurt_flag = False  # когда hp становится меньше                                              2
    dead_flag = False  # когда hp < 0                                                            1 +-
    protection_flag = False  # Когда зажата пкм                                                  4 +
    flag = False

    ticks = 0
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
                    sound1.play()
                    for tile in all_sprites:
                        tile.kill()
                    main_menu()
                else:
                    if not dead_flag and not hurt_flag and not attack_flag:
                        sound2.play()
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
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                move_x_flag = player.set_pos((-3, 0))
                idle_flag = False
                run_flag = True
            elif keys[pygame.K_d]:
                move_x_flag = player.set_pos((3, 0))
                idle_flag = False
                run_flag = True
            if keys[pygame.K_s]:
                move_y_flag = player.set_pos((0, 3))
                idle_flag = False
                run_flag = True
            elif keys[pygame.K_w]:
                move_y_flag = player.set_pos((0, -3))
                idle_flag = False
                run_flag = True
        if not move_x_flag and not move_y_flag:
            run_flag = False
        else:
            camera.update(player)
            for tile in all_sprites:
                camera.apply(tile)

        for enemis in antogonisti_sprites:
            enemis.checkActive(player.get_room())

        if ticks % 200 == 0:
            for enemis in antogonisti_sprites:
                dir, x, y = enemis.attacking()
                flag = player.damage(enemis.aliveORnot(), x, y, enemis.get_damage())
                if flag:
                    sound3.play()
                enemis.kick(x, y, flag)

        dead_flag = player.aliveCheck()

        if not dead_flag and flag == 'yes':
            flag = False
            hurt_flag = True
            attack_ticks, run_flag, idle_flag, protection_flag = False, False, False, False

        attack_flag, run_flag, idle_flag, hurt_flag, dead_flag, protection_flag, stop = player.animation_script(
            attack_flag, run_flag, idle_flag, hurt_flag, dead_flag, protection_flag)

        for hlth in health_group:
            group = pygame.sprite.Group()
            group.add(hlth)
            if not hlth.get_full():
                flag2 = player.health_upp(group)
                if flag2:
                    sound5.play()
                hlth.destroy(flag2)

        tile_group.draw(screen)
        antogonisti_sprites.update(screen, player.get_pos(), ticks)
        player_group.draw(screen)

        if portal.checkCollision(player_group):
            for elem in all_sprites:
                elem.kill()
            victory_menu()

        if stop:
            for elem in all_sprites:
                elem.kill()
            dead_menu()

        for button in [exit_menu_button]:
            button.changeColor(game_mouse_pos)
            button.update(screen)

        draw_lives(screen, player.get_hp())

        clock.tick(FPS)
        pygame.display.flip()


def main_menu():
    pygame.display.set_caption('menu')
    pygame.mixer.music.load('data/sounds/menu.mp3')
    pygame.mixer.music.set_volume(menu_volume)
    pygame.mixer.music.play(-1)
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
                    sound1.play()
                    levels_menu()
                if option_button.checkForInput(event.pos):
                    sound1.play()
                    options()
                if exit_button.checkForInput(event.pos):
                    sound1.play()
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
    main_menu()
