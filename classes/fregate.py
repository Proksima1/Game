from random import randint
from threading import Thread
from time import sleep

import pygame

from progressbar import ProgressBar


class Generel_ship(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.x = self.rect.x
        self.y = self.rect.y
        self.screen = screen
        self.hp = 100
        self.shoots = []
        self.velocity = 0.05
        self.movement = ""
        self.bar = ProgressBar(self.screen, "red", self.rect.x, self.rect.y + 10, 25, 5)

    def update_bar(self):
        self.bar.x = self.rect.x
        self.bar.y = self.rect.y
        self.bar.draw(self.hp)

    def down(self):
        # перемещение вниз
        if int(self.rect.y) + 59 <= self.screen.get_height():
            self.y += self.velocity
            self.rect.y = self.y
        self.make_a_ship()

    def up(self):
        # перемещение вверх
        if int(self.y) + 5 >= 0:
            self.y -= self.velocity
            self.rect.y = self.y
        self.make_a_ship()

    def left(self):
        # перемещение налево
        if int(self.x) + 2 >= 0:
            self.x -= self.velocity
            self.rect.x = self.x
        self.make_a_ship()

    def right(self):
        # перемещение направо
        if int(self.rect.x) + 64 <= self.screen.get_width():
            self.x += self.velocity
            self.rect.x = self.x
        self.make_a_ship()

    def make_a_ship(self):
        self.screen.blit(self.image, self.rect)

    def get_damage(self, amount_number):
        self.hp -= amount_number
        self.update_bar()


class Enemy_ship(Generel_ship):
    def __init__(self, screen, x, y, filename):
        super().__init__(screen, x, y, filename)
        self.shoot_count = 0
        self.velocity = 0.3
        self.stop = 1

    def update_all_systems(self):
        self.update_bar()
        self.make_a_ship()

    def random_move(self, screen):
        screen.fill((0, 0, 0))
        while True:
            a = randint(1, 6)
            if a == 1:
                if self.movement != "right":
                    for _ in range(randint(50, 70)):
                        if self.screen.get_width() // 2 <= self.rect.x:
                            sleep(0.001)
                            self.left()
                            self.update_all_systems()
                self.movement = "left"

            if a == 2:
                if self.movement != "left":
                    for _ in range(randint(50, 70)):
                        if self.screen.get_width() - 100 >= self.rect.x:
                            sleep(0.001)
                            self.right()
                            self.update_all_systems()
                self.movement = "right"

            if a == 3:
                for _ in range(randint(80, 100)):
                    if 150 <= self.rect.y:
                        sleep(0.001)
                        self.up()
                        self.update_all_systems()
            if a == 4:
                for _ in range(randint(80, 100)):
                    if self.screen.get_width() - 150 >= self.rect.y:
                        sleep(0.001)
                        self.down()
                        self.update_all_systems()

            if a == 5 or a == 6:
                sleep(0.025)
                self.update_all_systems()


class Player_ship(Generel_ship):
    def __init__(self, screen, x, y, filename):
        super().__init__(screen, x, y, filename)
        self.shoot_count = 0

    def draw_shoot(self):
        # рисование выстрела, его исчезновение и урон по врагам
        for i in range(len(self.shoots)):
            try:
                velocity = 0.1
                x_pos = self.shoots[i][2]
                pygame.draw.rect(self.screen, 'yellow',
                                 [(int(self.shoots[i][1][0]) + velocity * x_pos, self.shoots[i][1][1]), (3, 2)])
                self.shoots[i] = [i, (self.shoots[i][1][0] + velocity * x_pos, self.shoots[i][1][1]), x_pos, 1]
                if self.shoots[i][1][0] > self.screen.get_width():
                    del (self.shoots[i])
            except IndexError:
                pass

    def shoot(self):
        # выстрел
        if self.shoot_count == 0:
            pygame.draw.rect(self.screen, "yellow", [(self.rect.x + 35, self.rect.y + 7), (3, 2)])
            self.shoots.append([len(self.shoots) - 1, (self.rect.x + 35, self.rect.y + 7), 1, 1])
            self.shoot_count = 1
        else:
            pygame.draw.rect(self.screen, "yellow", [(self.rect.x + 35, self.rect.y + 55), (3, 2)])
            self.shoots.append([len(self.shoots) - 1, (self.rect.x + 35, self.rect.y + 55), 1, 1])
            self.shoot_count = 0


class Enemy_controller:
    def __init__(self):
        self.list_of_enemies = []

    def append(self, value: Enemy_ship):
        self.list_of_enemies.append(value)

    def update_all(self, screen):
        for enemy in self.list_of_enemies:
            thread = Thread(target=enemy.random_move, args=(screen,))
            thread.start()
            # enemy.random_move()
            sleep(0.001)
            # creen.fill((0, 0, 0))
