import pygame
from fregate import Enemy_ship


class SpriteController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.sprites = []

    def append(self, value):
        self.sprites.append(value)

    def draw_all(self):
        for sprite in self.sprites:
            if type(sprite) == Enemy_ship:
                sprite.update_bar()
            self.screen.blit(sprite.image, sprite.rect)