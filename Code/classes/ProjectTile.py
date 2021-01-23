from typing import Tuple
import pygame
import threading
from time import sleep
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], dir: str, type_of: int):
        """Аттрибут dir означает направление пули в сторонах света."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../sprites/bullet/base/base.png').convert_alpha(screen)
        self.screen = screen
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = self.rect.x
        self.y = self.rect.y
        self.type_of_bullet = type_of
        self.dir = dir
        self.count_anim = 1
        self.list_of_sprites = [pygame.image.load(f'../sprites/bullet/anim/{i + 1}.png') for i in range(10)]

    def draw_animation(self):
        """Рисует кадр анимации и считает следующий."""
        if self.type_of_bullet == 0:  # проверка на то, что тип пули равен 1
            if self.dir == 'SW':  # если направление пули равно SW, то добавляется пули с соответственным поворотом
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], -45), self.rect)
            elif self.dir == 'W':  # если направление пули равно W, то добавляется пули с соответственным поворотом
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], 0), self.rect)
            elif self.dir == 'NW':  # если направление пули равно NW, то добавляется пули с соответственным поворотом
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], 45), self.rect)
            elif self.dir == 'N':  # если направление пули равно N, то добавляется пули с соответственным поворотом
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], 90), self.rect)
            elif self.dir == 'NE':  # если направление пули равно NE, то добавляется пули с соответственным поворотом
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], 135), self.rect)
            elif self.dir == 'E':  # если направление пули равно E, то добавляется пули с соответственным поворотом
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], 180), self.rect)
            elif self.dir == 'SN':  # если направление пули равно SN, то добавляется пули с соответственным поворотом
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], -135), self.rect)
            elif self.dir == 'S':  # если направление пули равно S, то добавляется пули с соответственным поворотом
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], -90), self.rect)
            # если счетчик анимации не дошел до 10, то прибавляется, иначе устанавливается 0
            if self.count_anim < 9:
                self.count_anim += 1
            else:
                self.count_anim = 0

    def check_collision(self, other_objects: list, damage: int):
        """Проверка пули на коллизию с другими объектами/"""
        for object in other_objects:  # прохождение по списку объектов
            # если пуля соприкоснулась с объектом, наносится урон и возвращается True, иначе False
            if pygame.sprite.collide_mask(self, object):
                object.get_damage(damage)
                return True
        return False

    def __gt__(self, other_pos: Tuple[int, int]):
        """Возвращает True, если одна из координат больше соответсвующие координаты в кортеже, иначе False."""
        if self.x > other_pos[0] + self.image.get_width() or self.y > other_pos[1] + self.image.get_height():
            return True
        return False

    def __lt__(self, other_pos: Tuple[int, int]):
        """Возвращает True, если одна из координат меньше соответсвующие координаты в кортеже, иначе False."""
        if self.x < 0 - self.image.get_width() or self.y < 0 - self.image.get_height():
            return True
        return False

    def __str__(self):
        """Форматирует вывод."""
        return f'<Tile x={self.x}, y={self.y}>'

    def __repr__(self):
        """Форматирует вывод."""
        return f'<Tile x={self.x}, y={self.y}>'


class TileController:
    def __init__(self, screen: pygame.Surface):  # screen: pygame.Surface
        """
        Класс контроллер, обладает данными о всех пулях, имеет возможность передвигать, удалять,
        добавлять новые пули.
        """
        self.screen = screen
        self.bullets = []  # список пуль, обрабатывающиеся данным контроллером
        self.velocity = tile_speed  # скорость пули

    def __delitem__(self, index):
        """удаляет из списка класса значение по переданному индексу"""
        del self.bullets[index]

    def append(self, value: Tile):
        """добавляет в список класса переданное значение"""
        self.bullets.append(value)

    def __getitem__(self, item):
        """возвращает индекс переданного значения"""
        try:
            return self.bullets.index(item)
        except ValueError:
            return None

    def clear(self):
        """Очищает список пуль."""
        self.bullets.clear()

    def update_all(self):
        # скорость пули, при движение пули по диагонали
        speed_in_gradus = speed_when_driving_at_45_degrees
        if self.bullets is not bool:  # если список не пуст
            for bullet in self.bullets:  # прохождение по списку
                if bullet.type_of_bullet == 0:  # если тип пули равен 0
                    # если пуля вышла за экран, удаляется
                    if bullet > self.screen.get_size() or bullet < self.screen.get_size():
                        del self[self[bullet]]
                    else:
                        # иначе обновляет кадр пули
                        bullet.draw_animation()
                    if bullet.dir == 'N':  # проверка направления пули
                        bullet.y -= self.velocity  # движение пули
                    elif bullet.dir == 'NW':  # проверка направления пули
                        # движение пули
                        bullet.y -= self.velocity / speed_in_gradus
                        bullet.x += self.velocity / speed_in_gradus
                    elif bullet.dir == 'W':  # проверка направления пули
                        bullet.x += self.velocity  # движение пули
                    elif bullet.dir == 'SW':  # проверка направления пули
                        # движение пули
                        bullet.y += self.velocity / speed_in_gradus
                        bullet.x += self.velocity / speed_in_gradus
                    elif bullet.dir == 'S':  # проверка направления пули
                        bullet.y += self.velocity  # движение пули
                    elif bullet.dir == 'SE':  # проверка направления пули
                        # движение пули
                        bullet.y += self.velocity / speed_in_gradus
                        bullet.x -= self.velocity / speed_in_gradus
                    elif bullet.dir == 'E':  # проверка направления пули
                        # движение пули
                        bullet.x -= self.velocity
                    elif bullet.dir == 'NE':  # проверка направления пули
                        # движение пули
                        bullet.y -= self.velocity / speed_in_gradus
                        bullet.x -= self.velocity / speed_in_gradus
                    # установка коллизии пули на её местоположение
                    bullet.rect.y = bullet.y
                    bullet.rect.x = bullet.x
                elif bullet.type_of_bullet == 1:
                    bullet.draw_animation()

    def check_all_collision(self, ship: list, damage: int):
        # проверка всех коллизий всех пуль
        for bullet in self.bullets:
            # проверка коллизии пули
            if bullet.check_collision(ship, damage):
                # удалении пули
                del self[self[bullet]]

    def __str__(self):
        """Форматирует вывод."""
        return f'<TileController: {self.bullets}>'
