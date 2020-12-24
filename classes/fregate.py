import sys
from random import randint, choice
from time import sleep

from ProjectTile import *
from progressbar import ProgressBar


# pygame.mixer.init()


class Generel_ship(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = (pygame.image.load(filename))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.x = self.rect.x
        self.y = self.rect.y
        self.screen = screen
        self.hp = hp
        self.piy = [pygame.mixer.Sound('../sounds/shoot/shoot1.wav'),
                    pygame.mixer.Sound('../sounds/shoot/shoot3.mp3')]
        self.exp = [pygame.mixer.Sound('../sounds/explosion/expl1.wav')]
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

    def get_pos(self):
        return self.x, self.y


class Enemy_ship(Generel_ship):
    filename = '../sprites/fregate/enemy/enemy_ship1.png'

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, Enemy_ship.filename)
        self.enemy_bullet_controller = TileController(screen)
        self.velocity = enemy_speed
        self.enemy_shoot_count = 0
        self.movement = ""

    def update_all_systems(self):
        """Обновляет все заданные 'системы' корабля."""
        self.update_bar()

    def random_move(self, player):
        player_ship = player.rect
        a = randint(1, 2)
        flag = False

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
                    if self.rect.top == player_ship.bottom or self.rect.y == player_ship.y or self.rect.bottom == player_ship.top:
                        if not player.dead:
                            self.enemy_shoot()
                        sleep(0.6)
                    if a == 1:
                        if player_ship.x + player_ship.w + 200 <= self.rect.x:
                            self.x -= self.velocity
                            self.rect.x = self.x
                        if player_ship.x + player_ship.w + 200 >= self.rect.x:
                            self.x += self.velocity
                            self.rect.x = self.x
                        if player_ship.y + player_ship.h - 50 < self.rect.y:
                            self.y -= self.velocity
                            self.rect.y = self.y
                        if player_ship.y + 50 > self.rect.y + self.rect.h:
                            self.y += self.velocity
                            self.rect.y = self.y
                    elif a == 2:
                        if player_ship.y + player_ship.h // 2 < self.rect.y:
                            self.y -= self.velocity
                            self.rect.y = self.y
                        if player_ship.y > self.rect.y + self.rect.h // 2:
                            self.y += self.velocity
                            self.rect.y = self.y
                        if player_ship.y + player_ship.h // 2 == self.rect.y + self.rect.h // 2:
                            pass
                    elif a == 3:
                        if not flag:
                            self.y -= self.velocity
                            self.rect.y = self.y
                            if self.rect.y <= 0:
                                flag = True
                        else:
                            self.y += self.velocity
                            self.rect.y = self.y
                            if self.rect.y + self.rect.h >= self.screen.get_height():
                                flag = False
                    # print(self.rect)
                    sleep(0.00001)
                except pygame.error:
                    sys.exit()
        try:
            sou = choice(self.exp)
            sou.set_volume(0.1)
            sou.play()
        except pygame.error:
            sys.exit()

    def player_damage(self, player_ship):
        self.enemy_bullet_controller.update_all()
        self.enemy_bullet_controller.check_all_collision(player_ship)

    def enemy_shoot(self):
        """Добавление выстреда в список и смена выстрела пушки"""
        if self.enemy_shoot_count == 0:
            self.enemy_bullet_controller.append(Tile(self.screen, (self.rect.x + 7, self.rect.y + 9), 'E'))
            self.enemy_shoot_count = 1
        elif self.enemy_shoot_count == 1:
            self.enemy_bullet_controller.append(Tile(self.screen, (self.rect.x + 7, self.rect.y + 13), 'E'))
            self.enemy_shoot_count = 2
        elif self.enemy_shoot_count == 2:
            self.enemy_bullet_controller.append(Tile(self.screen, (self.rect.x + 7, self.rect.y + 51), 'E'))
            self.enemy_shoot_count = 3
        else:
            self.enemy_bullet_controller.append(Tile(self.screen, (self.rect.x + 7, self.rect.y + 55), 'E'))
            self.enemy_shoot_count = 0
        sou = choice(self.piy)
        sou.set_volume(0.1)
        sou.play()

    def __del__(self):
        """Переназначение метода __del___ на удаление себя."""
        del self

    def __repr__(self):
        return f'<Enemy ship: hp-{self.hp}>'


class Player_ship(Generel_ship):
    filename = '../sprites/fregate/player/player_ship.png'

    def __init__(self, screen, x, y):
        """Главный корабль игрока."""
        super().__init__(screen, x, y, Player_ship.filename)
        self.shoot_count = 0
        self.velocity = player_speed
        self.bullet_controller = TileController(screen)
        self.heart_drawer = self.Heart(screen)
        self.dead = False
        self.particles = []
        self.coins_count = 0

    class Heart(pygame.sprite.Sprite):
        def __init__(self, screen: pygame.Surface):
            super().__init__()
            # 0 - полное сердце, 1 - половинка сердца, 2 - пустое сердце
            s = screen.get_size()
            self.hearts = [pygame.transform.scale(pygame.image.load(f'../sprites/heart/heart{i + 1}.png'),
                                                  (16, 16)) for
                           i in range(3)]
            self.screen = screen

        def draw_hearts(self, hp):
            x = 5
            # рисовка полных сердечек
            for i in range(hp // 10 // 2):
                self.screen.blit(self.hearts[0], pygame.Rect(x, 5, 19, 32))
                x += 20
            # если нужно рисовка неполного сердечка
            if not hp // 10 % 2 == 0:
                self.screen.blit(self.hearts[1], pygame.Rect(x, 5, 19, 32))
                x += 20
            # рисовка пустых сердечек
            for i in range(int(5 - hp / 20)):
                self.screen.blit(self.hearts[2], pygame.Rect(x, 5, 19, 32))
                x += 20

    def draw_shoot(self, list_of_enemies):
        """Рисование выстрела, его исчезновение и урон по врагам."""
        self.bullet_controller.update_all()
        self.bullet_controller.check_all_collision(list_of_enemies)

    def shoot(self):
        """Добавление выстреда в список и смена выстрела пушки."""
        if self.shoot_count == 0:
            self.bullet_controller.append(Tile(self.screen, (self.rect.x + 38, self.rect.y + 7), 'W'))
            self.shoot_count = 1
        else:
            self.bullet_controller.append(Tile(self.screen, (self.rect.x + 38, self.rect.y + 55), 'W'))
            self.shoot_count = 0

        sou = choice(self.piy)
        sou.set_volume(0.1)
        sou.play()

    def draw_heart(self):
        """Рисует хп игрока"""
        self.heart_drawer.draw_hearts(self.hp)

    def __repr__(self):
        return f'<Player ship: hp-{self.hp}>'

    def make_a_particle(self):
        self.particles.append([[self.rect.x + 3, self.rect.centery], [-2, randint(0, 20) / 10 - 1], randint(4, 8)])
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.2
            #particle[1][0] -= 0.1
            a = randint(50, 255), randint(0, 80), randint(0, 40)
            pygame.draw.circle(self.screen, a, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles.remove(particle)


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

    def draw_bullets(self, player: list):
        for i in self.list_of_enemies:
            i.player_damage(player)

    def __delitem__(self, key):
        del self.list_of_enemies[self[key]]

    def __getitem__(self, item):
        return self.list_of_enemies.index(item)

    def __repr__(self):
        return f'<Enemy controller: {self.list_of_enemies}>'

    def __bool__(self):
        return True if len(self.list_of_enemies) else False
