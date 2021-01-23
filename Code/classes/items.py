import pygame
from SpriteController import *
from typing import Tuple
from random import randint
from settings import *


class Item(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], filename: str):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)  # установка изображения предмета
        self.rect = self.image.get_rect(center=pos)  # установка коллизии предмета
        self.mask = pygame.mask.from_surface(self.image)  # создание маски изображения
        self.x = self.rect.x  # позиция предмета по x
        self.y = self.rect.y  # позиция предмета по y
        self.screen = screen  # экран на котором будет нарисован предмет
        self.picked = False  # подобран ли предмет
        self.pick_sound = None  # звук подбора предмета
        self.count_anim = 1

    def pickup(self, player):
        # проверка на соприкосновение с предметом
        # проверка на то, что предмет соприкоснулся с игроком, и возвращает True, иначе False
        if pygame.sprite.collide_mask(self, player):
            self.picked = True  # установка переменной
            self.__del__()  # удаление предмета
            return True
        return False

    def __del__(self):
        # удаляет предмет
        try:
            del self.image
            del self.rect
            del self.mask
        except AttributeError:
            pass


class Coin(Item):
    basefile = '../sprites/items/coin/1.png'  # главная картинка
    # список, картинок монетки
    f = [pygame.image.load(f'../sprites/items/coin/{i + 1}.png') for i in range(6)]

    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], player):
        super().__init__(screen, pos, Coin.basefile)
        self.player = player  # игрок, который сможет подобрать
        self.coin_amount = randint(coin_amount[0], coin_amount[1])
        # звук подбора монеты
        self.pick_sound = pygame.mixer.Sound('../sounds/pickitem/pickcoin.mp3')

    def update(self):
        try:
            # добавление монеты
            self.screen.blit(Coin.f[int(self.count_anim)], self.rect)
            # если счетчик анимации меньше 6, то добавляем 0.01, иначе устанавливаем 0
            if self.count_anim < 5:
                self.count_anim += 0.01
            else:
                self.count_anim = 0
            # если подобрана монета, то добавляет количество монеток в счет игрока,
            # проигрывает звук, и возвращает True, иначе False
            if self.pickup(self.player) and self.picked:
                self.player.coins_count += self.coin_amount
                channel.play(self.pick_sound)
                return True
            return False
        except AttributeError:
            pass


class Heal(Item):
    basefile = '../sprites/items/heal/healing01.png'  # главная картинка
    # список, картинок хп
    f = [pygame.image.load(f'../sprites/items/heal/healing0{i + 1}.png') for i in range(2)]

    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], player):
        super().__init__(screen, pos, Heal.basefile)
        self.player = player  # игрок, который сможет подобрать
        self.heal_amount = heal_amount  # количество хп, которые будут добавляться от предмета
        # звук подбора монетки
        self.pick_sound = pygame.mixer.Sound('../sounds/pickitem/pickheal.mp3')

    def update(self):
        try:
            # рисует хил на экран
            self.screen.blit(Heal.f[int(self.count_anim)], self.rect)
            # если счетчик анимации меньше 2, то добавляем 0.1, иначе устанавливаем 0
            if self.count_anim < 1:
                self.count_anim += 0.1
            else:
                self.count_anim = 0
            # рисуем хил на экране
            self.screen.blit(self.image, self.rect)
            # если подобран хил, то добавляет количество хп в хп игрока,
            # проигрывает звук, и возвращает True, иначе False
            if self.pickup(self.player) and self.picked:
                # проверка, что хп меньше 100
                if self.player.hp < 100:
                    # добавляем хп
                    self.player.hp += self.heal_amount
                    # если после добавления хп, хп превысило 100, то уменьшаем хп до 100
                    if self.player.hp > 100:
                        self.player.hp = 100
                # проигрываем звук
                channel.play(self.pick_sound)
                return True
            return False
        except AttributeError:
            pass


class ItemController:
    def __init__(self, screen):
        self.screen = screen  # экран на котором будет рисоваться предметы
        self.items = []  # список предметов

    def append(self, value: Item):
        # добавление предмета в список предмета
        self.items.append(value)

    def update_all(self):
        # обновляет все предметы
        for i in self.items:
            i.update()

    def __delitem__(self, key):
        # удаляет элемент из списка
        del self.items[self[key]]

    def __getitem__(self, item):
        # возвращает идекс запрашемого элемента
        return self.items.index(item)
