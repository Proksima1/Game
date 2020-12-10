import pygame
import threading
import time
from typing import Tuple


class TileController:
    def __init__(self, screen: pygame.Surface):  # screen: pygame.Surface
        """
        Класс контроллер, обладает данными о всех пулях, имеет возможность передвигать, удалять,
        добавлять новые пули.
        """
        self.screen = screen
        self.bullets = []
        self.velocity = 5

    def __delitem__(self, index):
        # удаляет из списка класса значение по переданному индексу
        del self.bullets[index]

    def append(self, value):
        # добавляет в список класса переданное значение
        self.bullets.append(value)
        print(self.bullets)

    def __getitem__(self, item):
        try:
            return self.bullets.index(item)  # возвращает индекс переданного значения
        except ValueError:
            return None

    def draw_all(self):
        #while True:
            for bullet in self.bullets:
                if bullet > self.screen.get_size() or bullet < self.screen.get_size():
                    del self[self[bullet]]
                else:
                    bullet.draw_animation()
                bullet.x += self.velocity
                bullet.rect.x = bullet.x

    def __str__(self):
        return f'TileController: {self.bullets}'


class Tile(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], team: int):
        """Аттрибут team означает игрока или врага
        где игрок это 0, а враг это 1."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../sprites/bullet/base/base.png').convert_alpha(screen)
        self.screen = screen
        self.rect = self.image.get_rect(center=pos)
        print(self.rect)
        self.x = self.rect.x
        self.y = self.rect.y
        self.team = team
        self.count_anim = 0
        self.list_of_sprites = [pygame.image.load('../sprites/bullet/anim/1.png'),
                                pygame.image.load('../sprites/bullet/anim/2.png'),
                                pygame.image.load('../sprites/bullet/anim/3.png'),
                                pygame.image.load('../sprites/bullet/anim/4.png'),
                                pygame.image.load('../sprites/bullet/anim/5.png')]

    def draw_animation(self):
        #while True:
            screen.fill((0, 0, 0))
            self.screen.blit(self.list_of_sprites[self.count_anim], self.rect)
            #print(self.count_anim)
            #self.now_image = self.list_of_sprites[self.count_anim]
            if self.count_anim < len(self.list_of_sprites) - 1:
                self.count_anim += 1
            else:
                self.count_anim = 0
            time.sleep(0.1)

    # возвращает True, если одна из координат больше соответсвующие координаты в кортеже, иначе False
    def __gt__(self, other_pos: Tuple[int, int]):
        if self.x > other_pos[0] + self.image.get_width() or self.y > other_pos[1] + self.image.get_height():
            return True
        return False

    # возвращает True, если одна из координат меньше соответсвующие координаты в кортеже, иначе False
    def __lt__(self, other_pos: Tuple[int, int]):
        if self.x < 0 or self.y < 0:
            return True
        return False

    # форматирует вывод
    def __str__(self):
        return f'Tile x={self.x}, y={self.y}, team={self.team}'

    # форматирует вывод
    def __repr__(self):
        return f'<Tile x={self.x}, y={self.y}, team={self.team}>'


if __name__ == '__main__':
    pygame.init()
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    print(screen.get_size())
    a = TileController(screen)
    b = Tile(screen, (32, 32), 1)
    c = Tile(screen, (64, 64), 1)
    a.append(b)
    a.append(c)
    running = True
    #anim = threading.Thread(target=b.draw_animation)
    #anim.setDaemon(True)
    #anim.start()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #screen.fill('black')
        a.draw_all()
        print(a.bullets)
        pygame.draw.rect(screen, 'red', c.rect)
        pygame.display.flip()
    pygame.quit()