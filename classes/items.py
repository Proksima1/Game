import pygame
from SpriteController import *
from typing import Tuple
from random import randint
from settings import *


class Item(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], filename: str):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = self.rect.x
        self.y = self.rect.y
        self.screen = screen
        self.picked = False
        self.pick_sound = None
        self.count_anim = 1


    def pickup(self, player):
        if pygame.sprite.collide_mask(self, player):
            self.picked = True
            self.__del__()
            return True
        return False

    def __del__(self):
        try:
            del self.image
            del self.rect
            del self.mask
        except AttributeError:
            pass


class Coin(Item):
    basefile = '../sprites/items/coin/1.png'
    f = [pygame.image.load(f'../sprites/items/coin/{i + 1}.png') for i in range(6)]

    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], player):
        super().__init__(screen, pos, Coin.basefile)
        self.player = player
        self.coin_amount = randint(coin_amount[0], coin_amount[1])
        self.pick_sound = pygame.mixer.Sound('../sounds/pickitem/pickcoin.mp3')

    def update(self):
        try:
            self.screen.blit(Coin.f[int(self.count_anim)], self.rect)
            if self.count_anim < 5:
                self.count_anim += 0.01
            else:
                self.count_anim = 0
            if self.pickup(self.player) and self.picked:
                self.player.coins_count += self.coin_amount
                self.pick_sound.play()
                channel.play(self.pick_sound)
                return True
            return False
        except AttributeError:
            pass


class Heal(Item):
    filename = ''

    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], player):
        super().__init__(screen, pos, Heal.filename)
        self.player = player
        self.heal_amount = heal_amount
        self.pick_sound = pygame.mixer.Sound('../sounds/pickitem/pickheal.mp3')

    def update(self):
        try:
            self.screen.blit(Heal.f[self.count_anim], self.rect)
            if self.count_anim < 5:
                self.count_anim += 1
            else:
                self.count_anim = 0
            self.screen.blit(self.image, self.rect)
            if self.pickup(self.player) and self.picked:
                self.player.hp += self.heal_amount
                self.pick_sound.play()
                channel.play(self.pick_sound)
                return True
            return False
        except AttributeError:
            pass


class ItemController:
    def __init__(self, screen):
        self.screen = screen
        self.items = []

    def append(self, value: Item):
        self.items.append(value)

    def update_all(self):
        for i in self.items:
            i.update()

    def __delitem__(self, key):
        del self.items[self[key]]

    def __getitem__(self, item):
        return self.items.index(item)
