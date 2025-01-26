import pygame, os, sys

pygame.init()

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


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, text, font, font_size, font_size_two, text_color, text_color_two, image2=None):
        super().__init__()
        self.rect_x, self.rect_y = pos[0], pos[1]
        self.image = load_image(image)
        self.image1 = image
        self.image2 = image2
        self.pos = pos
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.font_font = font
        self.font_size = font_size
        self.font_size_two = font_size_two
        self.font = pygame.font.Font(self.font_font, self.font_size)
        self.text_input = text
        self.text_color = text_color
        self.text = self.font.render(self.text_input, True, self.text_color)
        self.text_rect = self.text.get_rect(center=(pos[0], pos[1]))
        self.text_color_two = text_color_two

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.font = pygame.font.Font(self.font_font, self.font_size_two)
            self.text = self.font.render(self.text_input, True, self.text_color_two)
            self.text_rect = self.text.get_rect(center=(self.rect_x, self.rect_y))
        else:
            self.font = pygame.font.Font(self.font_font, self.font_size)
            self.text = self.font.render(self.text_input, True, self.text_color)
            self.text_rect = self.text.get_rect(center=(self.rect_x, self.rect_y))

    def update_photo(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.image = pygame.transform.scale(load_image(self.image2), (325, 625))
            self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        else:
            self.image = load_image(self.image1)
            self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))