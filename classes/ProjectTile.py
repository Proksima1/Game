import threading
import time
from typing import Tuple
from fregate import Player_ship, Enemy_ship

import pygame


class TileController:
    def __init__(self, screen: pygame.Surface):  # screen: pygame.Surface
        """
        Класс контроллер, обладает данными о всех пулях, имеет возможность передвигать, удалять,
        добавлять новые пули.
        """
        self.screen = screen
        self.bullets = []
        self.velocity = 1

    def __delitem__(self, index):
        # удаляет из списка класса значение по переданному индексу
        del self.bullets[index]

    def append(self, value):
        # добавляет в список класса переданное значение
        self.bullets.append(value)
        #print(self.bullets)

    def __getitem__(self, item):
        try:
            return self.bullets.index(item)  # возвращает индекс переданного значения
        except ValueError:
            return None

    def draw_all(self):
        while True:
            screen.fill((0, 0, 0))
            for bullet in self.bullets:
                # print(bullet)
                if bullet > self.screen.get_size() or bullet < self.screen.get_size():
                    del self[self[bullet]]
                else:
                    bullet.draw_animation()
                if bullet.dir == 'N':
                    bullet.y -= self.velocity
                elif bullet.dir == 'NW':
                    bullet.y -= self.velocity
                    bullet.x += self.velocity
                elif bullet.dir == 'W':
                    bullet.x += self.velocity
                elif bullet.dir == 'SW':
                    bullet.y += self.velocity
                    bullet.x += self.velocity
                elif bullet.dir == 'S':
                    bullet.y += self.velocity
                elif bullet.dir == 'SE':
                    bullet.y += self.velocity
                    bullet.x -= self.velocity
                elif bullet.dir == 'E':
                    bullet.x -= self.velocity
                elif bullet.dir == 'NE':
                    bullet.y -= self.velocity
                    bullet.x -= self.velocity
                bullet.rect.y = bullet.y
                bullet.rect.x = bullet.x
                #print(bullet)
                #print(1)
            time.sleep(0.1)

    def check_all_collision(self):
        for bullet in self.bullets:
            if bullet.check_collision(ship):
                del self[self[bullet]]

    def __str__(self):
        return f'<TileController: {self.bullets}>'


class Tile(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], team: int, dir: str):
        """Аттрибут team означает игрока или врага
        где игрок это 0, а враг это 1.
        Аттрибут dir означает направление пули в сторонах света."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../sprites/bullet/base/base.png').convert_alpha(screen)
        self.screen = screen
        self.rect = self.image.get_rect(center=pos)
        self.x = self.rect.x
        self.y = self.rect.y
        self.dir = dir
        self.team = team
        self.count_anim = 1
        self.list_of_sprites = [pygame.image.load('../sprites/bullet/anim/1.png'),
                                pygame.image.load('../sprites/bullet/anim/2.png'),
                                pygame.image.load('../sprites/bullet/anim/3.png'),
                                pygame.image.load('../sprites/bullet/anim/4.png'),
                                pygame.image.load('../sprites/bullet/anim/5.png')]

    def draw_animation(self):
        """Рисует кадр анимации и считает следующий."""
        if self.dir == 'N':
            self.screen.blit(pygame.transform.rotate(pygame.image.load(f'../sprites/bullet/anim/{self.count_anim}.png'), 90), self.rect)
        elif self.dir == 'W':
            self.screen.blit(pygame.transform.rotate(pygame.image.load(f'../sprites/bullet/anim/{self.count_anim}.png'), 0), self.rect)
        if self.count_anim < 10:
            self.count_anim += 1
        else:
            self.count_anim = 1
        print(self.count_anim)

    def check_collision(self, other_object):
        if self.team == 1:
            if self.rect.colliderect(other_object.rect):
                print('collided')  # исправить на смерть от пули, или нанесение урона
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
        return f'<Tile x={self.x}, y={self.y}, team={self.team}>'

    def __repr__(self):
        """Форматирует вывод."""
        return f'<Tile x={self.x}, y={self.y}, team={self.team}>'


if __name__ == '__main__':
    pygame.init()
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    a = TileController(screen)
    b = Tile(screen, (80, 32), 1, 'W')
    c = Tile(screen, (90, 60), 1, 'N')
    a.append(b)
    a.append(c)
    ship = Player_ship(screen, 32, 32, '../sprites/fregate/player/player_ship.png')
    running = True
    anim = threading.Thread(target=a.draw_all)
    anim.setDaemon(True)
    anim.start()
    while running:
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
        # screen.fill('black')
        # pygame.draw.rect(screen, 'red', c.rect)
        pygame.display.flip()
    pygame.quit()
