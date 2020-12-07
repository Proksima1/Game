import pygame
from pygame.locals import *


class Ship():
    def __init__(self, screen, width, height):
        self.pos_bottom = 50
        self.pos_top = 50
        self.screen = screen
        self.width = width
        self.height = height
        self.pos_right = 50
        self.pos_left = 50
        self.shoots = []
        self.velocity = 0.07
        self.enemy = []

    def make_a_ship(self):
        pygame.draw.rect(self.screen, "blue", [(self.pos_left, self.pos_top), (self.pos_right, self.pos_bottom)])
        pygame.draw.rect(self.screen, "red", [(200, 200), (50, 50)])

    def make_an_enemy(self):
        self.enemy.append(pygame.draw.rect(self.screen, "red", [(200, 200), (50, 50)]))

    def make_a_ship(self):
        pygame.draw.rect(self.screen, "blue", [(self.pos_left, self.pos_top), (self.pos_right, self.pos_bottom)])

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

    def shoot(self):
        # выстрел
        pygame.draw.rect(self.screen, "yellow", [(self.pos_left + 51, self.pos_top + 25), (3, 2)])
        self.shoots.append([len(self.shoots) - 1, (self.pos_left + 51, self.pos_top + 25), 1, 1])

