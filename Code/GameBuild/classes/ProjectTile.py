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
        if self.type_of_bullet == 0:
            if self.dir == 'SW':
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], -45), self.rect)
            elif self.dir == 'W':
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], 0), self.rect)
            elif self.dir == 'NW':
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], 45), self.rect)
            elif self.dir == 'N':
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], 90), self.rect)
            elif self.dir == 'NE':
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], 135), self.rect)
            elif self.dir == 'E':
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], 180), self.rect)
            elif self.dir == 'SN':
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], -135), self.rect)
            elif self.dir == 'S':
                self.screen.blit(pygame.transform.rotate(self.list_of_sprites[self.count_anim], -90), self.rect)
            if self.count_anim < 9:
                self.count_anim += 1
            else:
                self.count_anim = 0
        else:
            pass

    def check_collision(self, other_objects: list, damage: int):
        for object in other_objects:
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
        self.bullets = []
        self.velocity = tile_speed

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
        self.bullets.clear()

    def update_all(self):
        speed_in_gradus = speed_when_driving_at_45_degrees
        if self.bullets is not bool:
            for bullet in self.bullets:
                # print(bullet)
                if bullet.type_of_bullet == 0:
                    if bullet > self.screen.get_size() or bullet < self.screen.get_size():
                        del self[self[bullet]]
                    else:
                        bullet.draw_animation()
                    if bullet.dir == 'N':
                        bullet.y -= self.velocity
                    elif bullet.dir == 'NW':
                        bullet.y -= self.velocity / speed_in_gradus
                        bullet.x += self.velocity / speed_in_gradus
                    elif bullet.dir == 'W':
                        bullet.x += self.velocity
                    elif bullet.dir == 'SW':
                        bullet.y += self.velocity / speed_in_gradus
                        bullet.x += self.velocity / speed_in_gradus
                    elif bullet.dir == 'S':
                        bullet.y += self.velocity
                    elif bullet.dir == 'SE':
                        bullet.y += self.velocity / speed_in_gradus
                        bullet.x -= self.velocity / speed_in_gradus
                    elif bullet.dir == 'E':
                        bullet.x -= self.velocity
                    elif bullet.dir == 'NE':
                        bullet.y -= self.velocity / speed_in_gradus
                        bullet.x -= self.velocity / speed_in_gradus
                    bullet.rect.y = bullet.y
                    bullet.rect.x = bullet.x
                elif bullet.type_of_bullet == 1:
                    bullet.draw_animation()

    def check_all_collision(self, ship: list, damage: int):
        for bullet in self.bullets:
            if bullet.check_collision(ship, damage):
                del self[self[bullet]]

    def __str__(self):
        return f'<TileController: {self.bullets}>'


if __name__ == '__main__':
    pygame.init()
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    lreader = TileController(screen)
    b = Tile(screen, (80, 32), 'W', 0)
    c = Tile(screen, (90, 60), 'SW', 0)
    lreader.append(b)
    lreader.append(c)
    """ship = Player_ship(screen, 32, 32, '../sprites/fregate/player/player_ship.png')
    running = True
    while running:
        screen.fill('black')
        moving = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if moving[pygame.K_LEFT] or moving[pygame.K_a]:
            ship.left()
        if moving[pygame.K_RIGHT] or moving[pygame.K_d]:
            ship.right()
        if moving[pygame.K_UP] or moving[pygame.K_w]:
            ship.up()
        if moving[pygame.K_DOWN] or moving[pygame.K_s]:
            ship.down()
        ship.make_a_ship()
        a.check_all_collision()
        a.update_all()
        # pygame.draw.rect(screen, 'red', c.rect)
        pygame.display.flip()
    pygame.quit()"""
