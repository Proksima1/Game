import pygame
from fregate import *
from random import choice


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
                sprite.dead = True
                sou = sprite.exp
                sou.set_volume(effects_volume / 100)
                sou.play()
                del self[sprite]
            elif isinstance(sprite, Enemy_ship):
                sprite.update_bar()
            elif isinstance(sprite, Player_ship):
                sprite.draw_heart()
                sprite.make_a_particle()
            elif isinstance(sprite, Coin) and sprite.picked:
                del self[sprite]
            self.screen.blit(sprite.image, sprite.rect)

    def __delitem__(self, key):
        del self.sprites[self[key]]

    def __getitem__(self, item):
        return self.sprites.index(item)

    def __len__(self):
        return len(self.sprites)

    def __bool__(self):
        print(self.sprites)
        return True if self.sprites else False

    def __repr__(self):
        return f'<Sprite controller: {self.sprites}>'