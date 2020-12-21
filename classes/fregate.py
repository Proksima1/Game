import sys
from time import sleep

from ProjectTile import *
from progressbar import ProgressBar


class Generel_ship(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.x = self.rect.x
        self.y = self.rect.y
        self.screen = screen
        self.hp = 100
        self.shoots = []
        self.velocity = 0.05
        self.bar = ProgressBar(self.screen, "red", self.rect.x, self.rect.y + 10, 25, 5)

    def update_bar(self):
        """Обновляет позицию бара и обновление количества Хп"""
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
        """Рисует корабль на переданном экране"""
        self.screen.blit(self.image, self.rect)

    def get_damage(self, amount_number):
        """Отнимает количество переданного урона от хп и обновляет бар"""
        self.hp -= amount_number
        self.update_bar()


class Enemy_ship(Generel_ship):
    filename = '../sprites/fregate/enemy/enemy_ship1.png'

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, Enemy_ship.filename)
        self.velocity = 0
        self.movement = ""

    def update_all_systems(self):
        """Обновляет все заданные 'системы' корабля."""
        self.update_bar()

    def random_move(self, player_ship):
        player_ship = player_ship.rect

        def isValid(value: pygame.Surface):
            try:
                value.get_size()
            except pygame.error:
                return False
            else:
                return True

        while self.hp > 0 and isValid(self.screen):
            if self.hp <= 0:
                self.__del__()
            else:
                try:
                    if player_ship.y + player_ship.h // 2 < self.rect.y:
                        self.rect.y -= self.velocity
                    if player_ship.y > self.rect.y + self.rect.h // 2:
                        self.rect.y += self.velocity
                    if player_ship.y + player_ship.h // 2 == self.rect.y + self.rect.h // 2:
                        pass
                    sleep(0.00001)
                    # print(self.rect.y + self.rect.w // 2)
                except pygame.error:
                    sys.exit()

    def __del__(self):
        """Переназначение метода __del___ на удаление себя."""
        del self


class Player_ship(Generel_ship):
    filename = '../sprites/fregate/player/player_ship.png'

    def __init__(self, screen, x, y):
        """Главный корабль игрока."""
        super().__init__(screen, x, y, Player_ship.filename)
        self.shoot_count = 0
        self.bullet_controller = TileController(screen)
        self.heart_drawer = self.Heart(screen)

    class Heart(pygame.sprite.Sprite):
        def __init__(self, screen: pygame.Surface):
            super().__init__()
            # 0 - полное сердце, 1 - половинка сердца, 2 - пустое сердце
            self.hearts = [pygame.transform.scale(pygame.image.load(f'../sprites/heart/heart{i + 1}.png'),
                                                  (32, 32)) for
                           i in range(3)]
            self.screen = screen

        def draw_hearts(self):
            for i in range(1, 4):
                a = pygame.Rect(25 * i, 30, 19, 32)
                print(a)
                self.screen.blit(self.hearts[0], a)

    def draw_shoot(self, list_of_enemies):
        """Рисование выстрела, его исчезновение и урон по врагам."""
        self.bullet_controller.update_all()
        self.bullet_controller.check_all_collision(list_of_enemies)

    def shoot(self):
        """Добавление выстреда в список и смена выстрела пушки"""
        if self.shoot_count == 0:
            self.bullet_controller.append(Tile(self.screen, (self.rect.x + 38, self.rect.y + 7), 0, 'W'))
            self.shoot_count = 1
        else:
            self.bullet_controller.append(Tile(self.screen, (self.rect.x + 38, self.rect.y + 55), 0, 'W'))
            self.shoot_count = 0

    def draw_heart(self):
        """Рисует хп игрока"""
        self.heart_drawer.draw_hearts()


class Enemy_controller:
    def __init__(self, screen):
        self.list_of_enemies = []
        self.screen = screen

    def append(self, value: Enemy_ship):
        self.list_of_enemies.append(value)
        # print(self.all_sprites.sprites())

    def update_all(self, player_ship):
        for enemy in self.list_of_enemies:
            # self.all_sprites.draw(self.screen)
            thread = threading.Thread(target=enemy.random_move, args=(player_ship,))
            thread.start()
            # self.all_sprites.random_move()
            # enemy.random_move()
            # creen.fill((0, 0, 0))

    # sleep(0.0001)
    # self.screen.fill('black')

    def get_enemies(self):
        for i in self.list_of_enemies:
            if i.hp <= 0:
                del self[i]
        return self.list_of_enemies

    def __delitem__(self, key):
        del self.list_of_enemies[self[key]]

    def __getitem__(self, item):
        return self.list_of_enemies.index(item)
