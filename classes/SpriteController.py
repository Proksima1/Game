import pygame
from fregate import *


class SpriteController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.sprites = []

    def append(self, value):
        self.sprites.append(value)
        #print(self.sprites.index(value))

    def draw_all(self):
        for sprite in self.sprites:
            if sprite.hp <= 0:
                del self[sprite]
            if isinstance(sprite, Enemy_ship):
                sprite.update_bar()
            elif isinstance(sprite, Player_ship):
                sprite.draw_heart()
            self.screen.blit(sprite.image, sprite.rect)

    def __delitem__(self, key):
        del self.sprites[self[key]]

    def __getitem__(self, item):
        return self.sprites.index(item)