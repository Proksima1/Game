import pygame
from fregate import Enemy_ship


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
            if type(sprite) == Enemy_ship:
                sprite.update_bar()
            self.screen.blit(sprite.image, sprite.rect)

    def __delitem__(self, key):
        del self.sprites[self[key]]

    def __getitem__(self, item):
        return self.sprites.index(item)