from random import randint
from threading import Thread
from time import sleep
import pygame
from progressbar import ProgressBar
from ProjectTile import *
import sys


class Generel_ship(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.x = self.rect.x
        self.y = self.rect.y
        self.screen = screen
        self.hp = 100
        self.shoots = []
        self.velocity = 0.05
        self.bar = ProgressBar(self.screen, "red", self.rect.x, self.rect.y + 10, 25, 5)

    def update_bar(self):
        self.bar.x = self.rect.x
        self.bar.y = self.rect.y
        self.bar.draw(self.hp)

    def down(self):
        """Перемещение вниз."""
        if int(self.rect.y) + 59 <= self.screen.get_height():
            self.y += self.velocity
            self.rect.y = self.y

    def up(self):
        """Перемещение вверх."""
        if int(self.y) + 5 >= 0:
            self.y -= self.velocity
            self.rect.y = self.y

    def left(self):
        """Перемещение налево."""
        if int(self.x) + 2 >= 0:
            self.x -= self.velocity
            self.rect.x = self.x

    def right(self):
        """Перемещение направо."""
        if int(self.rect.x) + 64 <= self.screen.get_width():
            self.x += self.velocity
            self.rect.x = self.x

    def make_a_ship(self):
        self.screen.blit(self.image, self.rect)

    def get_damage(self, amount_number):
        self.hp -= amount_number
        self.update_bar()


class Enemy_ship(Generel_ship):
    filename = '../sprites/fregate/enemy/enemy_ship1.png'

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, Enemy_ship.filename)
        self.shoot_count = 0
        self.velocity = 0.3
        self.stop = 1
        self.movement = ""

    def update_all_systems(self):
        self.update_bar()
        #self.make_a_ship()
        #self.screen.fill('black')

    def random_move(self):
        while self.hp > 0:
            if self.hp <= 0:
                self.__del__()
            else:
                try:
                    a = randint(1, 6)
                    if a == 1:
                        if self.movement != "right":
                            for _ in range(randint(50, 70)):
                                if self.screen.get_width() // 2 <= self.rect.x:
                                    sleep(0.00001)
                                    self.left()
                                    self.update_all_systems()
                        self.movement = "left"
                    if a == 2:
                        if self.movement != "left":
                            for _ in range(randint(50, 70)):
                                if self.screen.get_width() - 100 >= self.rect.x:
                                    sleep(0.00001)
                                    self.right()
                                    self.update_all_systems()
                        self.movement = "right"
                    if a == 3:
                        for _ in range(randint(80, 100)):
                            if 150 <= self.rect.y:
                                sleep(0.00001)
                                self.up()
                                self.update_all_systems()
                    if a == 4:
                        for _ in range(randint(80, 100)):
                            if self.screen.get_width() - 150 >= self.rect.y:
                                sleep(0.00001)
                                self.down()
                                self.update_all_systems()
                    if a == 5 or a == 6:
                        sleep(0.00001)
                        self.update_all_systems()
                except pygame.error:
                    sys.exit()

    def __del__(self):
        del self


class Player_ship(Generel_ship):
    filename = '../sprites/fregate/player/player_ship.png'

    def __init__(self, screen, x, y):
        """Главный корабль игрока."""
        super().__init__(screen, x, y, Player_ship.filename)
        self.shoot_count = 0
        self.bullet_controller = TileController(screen)

    def draw_shoot(self, list_of_enemies):
        """Рисование выстрела, его исчезновение и урон по врагам."""
        self.bullet_controller.update_all()
        self.bullet_controller.check_all_collision(list_of_enemies)

    def shoot(self):
        # выстрел
        if self.shoot_count == 0:
            self.bullet_controller.append(Tile(self.screen, (self.rect.x + 38, self.rect.y + 7), 0, 'W'))
            self.shoot_count = 1
        else:
            self.bullet_controller.append(Tile(self.screen, (self.rect.x + 38, self.rect.y + 55), 0, 'W'))
            self.shoot_count = 0


class Enemy_controller:
    def __init__(self, screen):
        self.list_of_enemies = []
        self.screen = screen

    def append(self, value: Enemy_ship):
        self.list_of_enemies.append(value)
        #print(self.all_sprites.sprites())

    def update_all(self):
        for enemy in self.list_of_enemies:
            #self.all_sprites.draw(self.screen)
            thread = threading.Thread(target=enemy.random_move)
            thread.start()
            #self.all_sprites.random_move()
            # enemy.random_move()
            # creen.fill((0, 0, 0))
       # sleep(0.0001)
        #self.screen.fill('black')

    def get_enemies(self):
        for i in self.list_of_enemies:
            if i.hp <= 0:
                del self[i]
        return self.list_of_enemies

    def __delitem__(self, key):
        del self.list_of_enemies[self[key]]

    def __getitem__(self, item):
        return self.list_of_enemies.index(item)