import pygame
from pygame.locals import *


class Generel_ship():
    def __init__(self, screen, width, height, pos_left, pos_top, pos_right, pos_bottom):
        self.pos_right = pos_right
        self.pos_left = pos_left
        self.pos_bottom = pos_bottom
        self.pos_top = pos_top
        self.screen = screen
        self.width = width
        self.height = height
        self.shoots = []
        self.velocity = 0.07

    def down(self):
        # перемещение вниз
        if self.pos_top <= self.height - self.pos_bottom:
            self.pos_top += self.velocity

    def up(self):
        # перемещение вверх
        if self.pos_top >= 0:
            self.pos_top -= self.velocity

    def left(self):
        # перемещение налево
        if self.pos_left >= 0:
            self.pos_left -= self.velocity

    def right(self):
        # перемещение направо
        if self.pos_left <= self.width - self.pos_right:
            self.pos_left += self.velocity


class Enemy_ship(Generel_ship, pygame.sprite.Sprite):
    pass


class Player_ship(Generel_ship, pygame.sprite.Sprite):
    def __init__(self, screen, width, height, pos_left, pos_top, pos_right, pos_bottom):
        super().__init__(screen, width, height, pos_left, pos_top, pos_right, pos_bottom)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../sprites/player_ship.png').convert_alpha()
        self.rect = self.image.get_rect(center=(40, 50))
        self.enemy = []

    def make_a_ship(self):
        pygame.draw.rect(self.screen, "blue", [(self.pos_left, self.pos_top), (self.pos_right, self.pos_bottom)])

    def draw_shoot(self):
        # рисование выстрела, его исчезновение и урон по врагам
        for i in range(len(self.shoots)):
            try:
                velocity = 0.1
                x_pos = self.shoots[i][2]
                pygame.draw.rect(self.screen, 'yellow',
                                 [(int(self.shoots[i][1][0]) + velocity * x_pos, self.shoots[i][1][1]), (3, 2)])
                self.shoots[i] = [i, (self.shoots[i][1][0] + velocity * x_pos, self.shoots[i][1][1]), x_pos, 1]
                if self.shoots[i][1][0] > self.width:
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
        pygame.draw.rect(self.screen, "yellow", [(self.pos_left + 51, self.pos_top + 25), (3, 2)])
        self.shoots.append([len(self.shoots) - 1, (self.pos_left + 51, self.pos_top + 25), 1, 1])
