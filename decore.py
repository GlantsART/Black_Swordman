import pygame

word_group = []
s = 190

class Text():
    def __init__(self, text, pos, size, color1, color2, long):
        global s
        self.text = text
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.long = long
        self.pos_x = s
        self.pos = (s, 30)
        s += self.long
        self.font = pygame.font.Font('data/fonts/go3v2.ttf', self.size)
        self.text1 = self.font.render(self.text, True, self.color1)
        word_group.append(self)

    def draw(self, screen):
        screen.blit(self.text1, self.pos)

    def CheckForInput(self, pos):
        global s
        if pos[0] in range(self.pos[0], self.pos[0] + self.long) and pos[1] in range(45, 45 + 65):
            self.pos = (self.pos_x, 15)
            self.font = pygame.font.Font('data/fonts/go3v2.ttf', self.size + 10)
            self.text1 = self.font.render(self.text, True, self.color2)
        else:
            self.pos = (self.pos_x, 30)
            self.font = pygame.font.Font('data/fonts/go3v2.ttf', self.size)
            self.text1 = self.font.render(self.text, True, self.color1)


def draw_lives(screen, hp):
    pygame.draw.rect(screen, (150, 147, 50), (75, 10, 410, 40))
    pygame.draw.rect(screen, (120, 2, 2), (80, 15, hp * 4, 30))
    x = 80
    for _ in range(4):
        pygame.draw.rect(screen, (150, 147, 50), (x, 15, 100, 30), width=2)
        x += 100