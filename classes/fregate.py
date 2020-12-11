import pygame
from pygame.locals import *


class Generel_ship(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.x = 0
        self.y = 0
        self.screen = screen
        self.shoots = []
        self.velocity = 0.01

    def down(self):
        # перемещение вниз
        if int(self.rect.y) + 59 <= self.screen.get_height():
            self.y += self.velocity
            self.rect.y = self.y

    def up(self):
        # перемещение вверх
        if int(self.y) + 5 >= 0:
            self.y -= self.velocity
            self.rect.y = self.y

    def left(self):
        # перемещение налево
        if int(self.x) + 2 >= 0:
            self.x -= self.velocity
            self.rect.x = self.x

    def right(self):
        # перемещение направо
        if int(self.rect.x) + 64 <= self.screen.get_width():
            self.x += self.velocity
            self.rect.x = self.x

    def make_a_ship(self):
        self.screen.blit(self.image, self.rect)


class Enemy_ship(Generel_ship):
    pass


class Player_ship(Generel_ship):
    def __init__(self, screen, x, y, filename):
        super().__init__(screen, x, y, filename)
        self.enemy = []
        self.count = 0

    def draw_shoot(self):
        # рисование выстрела, его исчезновение и урон по врагам
        for i in range(len(self.shoots)):
            try:
                velocity = 0.1
                x_pos = self.shoots[i][2]
                pygame.draw.rect(self.screen, 'yellow',
                                 [(int(self.shoots[i][1][0]) + velocity * x_pos, self.shoots[i][1][1]), (3, 2)])
                self.shoots[i] = [i, (self.shoots[i][1][0] + velocity * x_pos, self.shoots[i][1][1]), x_pos, 1]
                if self.shoots[i][1][0] > self.screen.get_width():
                    del (self.shoots[i])
                if self.enemy[0][0].top <= self.shoots[i][1][1] <= self.enemy[0][0].bottom and \
                        self.enemy[0][0].left <= self.shoots[i][1][0] <= self.enemy[0][0].right:
                    del (self.shoots[i])
                    if self.enemy[0][1] > 0:
                        self.enemy[0][1] -= 20
                    if self.enemy[0][1] <= 0:
                        del (self.enemy[0])
            except IndexError:
                pass

    def shoot(self):
        # выстрел
        if self.count == 0:
            pygame.draw.rect(self.screen, "yellow", [(self.rect.x + 35, self.rect.y + 7), (3, 2)])
            self.shoots.append([len(self.shoots) - 1, (self.rect.x + 35, self.rect.y + 7), 1, 1])
            self.count = 1
        else:
            pygame.draw.rect(self.screen, "yellow", [(self.rect.x + 35, self.rect.y + 55), (3, 2)])
            self.shoots.append([len(self.shoots) - 1, (self.rect.x + 35, self.rect.y + 55), 1, 1])
            self.count = 0
