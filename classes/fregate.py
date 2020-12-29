import sys
from ProjectTile import *
from items import *
from widgets import ProgressBar
from time import sleep
from random import choice
from LevelReader import *


class Generel_ship(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, x, y, filename):
        """Главный класс корабля."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.x = self.rect.x
        self.y = self.rect.y
        self.screen = screen
        self.hp = hp
        self.piy = [pygame.mixer.Sound('../sounds/shoot/shoot1.wav'),
                    pygame.mixer.Sound('../sounds/shoot/shoot3.mp3')]
        self.exp = pygame.mixer.Sound('../sounds/explosion/expl1.wav')
        self.shoots = []
        self.velocity = 0.05
        self.bar = ProgressBar(self.screen, "red", self.rect.x, self.rect.y + 10, 25, 5)
        self.last_shoot = pygame.time.get_ticks()

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
        """Возвращает позицию игрока."""
        return self.x, self.y


class Enemy_ship(Generel_ship):
    def __init__(self, screen, x, y, filename):
        """Класс врага."""
        super().__init__(screen, x, y, filename)
        self.enemy_bullet_controller = TileController(screen)
        self.velocity = enemy_speed
        self.enemy_shoot_count = 0
        self.movement = ""

    def update_all_systems(self):
        """Обновляет все заданные 'системы' корабля."""
        self.update_bar()

    def random_move(self, player):
        """"Движение врага."""
        pass

    def player_damage(self, player_ship):
        """Проверка коллизии с кораблём и движение пули."""
        if not player_ship[0].dead:
            self.enemy_bullet_controller.update_all()
            self.enemy_bullet_controller.check_all_collision(player_ship, enemy_damage)
        else:
            self.enemy_bullet_controller.clear()

    def enemy_shoot(self):
        """Добавление выстреда в список и смена выстрела пушки"""
        pass

    def __del__(self):
        """Переназначение метода __del___ на удаление себя."""
        del self

    def __repr__(self):
        """Форматирует вывод."""
        return f'<Enemy ship: hp-{self.hp}>'


class Enemy_level1(Enemy_ship):
    filename = '../sprites/fregate/enemy/enemy_level1.png'

    def __init__(self, screen, x, y):
        """Враг, стреляющий пулями."""
        super().__init__(screen, x, y, Enemy_level1.filename)
        self.current_time = pygame.time.get_ticks()

    def random_move(self, player):
        player_ship = player.rect
        a = randint(1, 2)
        flag = False

        def isValid(value: pygame.Surface):
            """Проверка валидности экрана."""
            try:
                value.get_size()
            except pygame.error:
                return False
            else:
                return True

        # запуск движения врага
        while self.hp > 0 and isValid(self.screen):
            if self.hp <= 0:
                self.__del__()
            else:
                try:
                    if not player.dead:
                        if pygame.sprite.collide_mask(self, player):
                            player.hp = 0
                            self.hp = 0
                        if a != 2:
                            if self.enemy_shoot_count == 0:
                                if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 30 < player_ship.y + player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                    if not player.dead:
                                        self.enemy_shoot()
                                    sleep(0.3)
                                else:
                                    if player_ship.y + 30 < self.rect.y:
                                        self.up()
                                    if player_ship.y + 30 > self.rect.y:
                                        self.down()
                            if self.enemy_shoot_count == 1:
                                if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 34 < player_ship.bottom - player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                    if not player.dead:
                                        self.enemy_shoot()
                                    sleep(0.3)
                                else:
                                    if player_ship.y + 20 < self.rect.y:
                                        self.up()
                                    if player_ship.y + 20 > self.rect.y:
                                        self.down()
                            if self.enemy_shoot_count == 2:
                                if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 68 < player_ship.bottom - player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                    if not player.dead:
                                        self.enemy_shoot()
                                    sleep(0.3)
                                else:
                                    if player_ship.y - 20 < self.rect.y:
                                        self.up()
                                    if player_ship.y - 20 > self.rect.y:
                                        self.down()
                            if self.enemy_shoot_count == 3:
                                if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 72 < player_ship.bottom - player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                    if not player.dead:
                                        self.enemy_shoot()
                                    sleep(0.3)
                                else:
                                    if player_ship.y - 30 < self.rect.y:
                                        self.up()
                                    if player_ship.y - 30 > self.rect.y:
                                        self.down()
                        if a == 1:
                            if player_ship.x + player_ship.w + 200 <= self.rect.x:
                                self.x -= self.velocity
                                self.rect.x = self.x
                            if player_ship.x + player_ship.w + 200 >= self.rect.x:
                                self.x += self.velocity
                                self.rect.x = self.x
                        elif a == 2:
                            if self.enemy_shoot_count == 0:
                                if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 30 < player_ship.y + player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                    if not player.dead:
                                        self.enemy_shoot()
                                        sleep(0.3)
                            if self.enemy_shoot_count == 1:
                                if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 34 < player_ship.bottom - player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                    if not player.dead:
                                        self.enemy_shoot()
                                        sleep(0.3)
                            if self.enemy_shoot_count == 2:
                                if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 68 < player_ship.bottom - player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                    if not player.dead:
                                        self.enemy_shoot()
                                        sleep(0.3)
                            if self.enemy_shoot_count == 3:
                                if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 72 < player_ship.bottom - player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                    if not player.dead:
                                        self.enemy_shoot()
                                        sleep(0.3)
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
                            if self.rect.x < player_ship.left:
                                a = 1
                        # print(self.rect)
                        sleep(0.00001)
                except pygame.error:
                    sys.exit()

    def enemy_shoot(self):
        if self.current_time - self.last_shoot > 500:
            if self.enemy_shoot_count == 0:
                self.enemy_bullet_controller.append(Tile(self.screen, (self.rect.x + 7, self.rect.y + 13), 'E', 0))
                self.enemy_shoot_count = 1
            elif self.enemy_shoot_count == 1:
                self.enemy_bullet_controller.append(Tile(self.screen, (self.rect.x + 7, self.rect.y + 51), 'E', 0))
                self.enemy_shoot_count = 0
            self.last_shoot = pygame.time.get_ticks()
            # воспроизведение звука выстрела
            sou = choice(self.piy)
            sou.set_volume(effects_volume / 100)
            sou.play()
        self.current_time = pygame.time.get_ticks()


class Enemy_level2(Enemy_ship):
    filename = '../sprites/fregate/enemy/enemy_level2.png'

    def __init__(self, screen, x, y):
        """Враг, стреляющий лазером."""
        super().__init__(screen, x, y, Enemy_level2.filename)

    def random_move(self, player):
        player_ship = player.rect

        def isValid(value: pygame.Surface):
            """Проверка валидности экрана."""
            try:
                value.get_size()
            except pygame.error:
                return False
            else:
                return True

        # запуск движения врага
        while self.hp > 0 and isValid(self.screen):
            if self.hp <= 0:
                self.__del__()
            else:
                try:
                    if not player.dead:
                        if pygame.sprite.collide_mask(self, player):
                            player.hp = 0
                            self.hp = 0
                        if self.enemy_shoot_count == 0:
                            if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 30 < player_ship.y + player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                if not player.dead:
                                    self.enemy_shoot()
                                sleep(0.3)
                            else:
                                if player_ship.y + 30 < self.rect.y:
                                    self.up()
                                if player_ship.y + 30 > self.rect.y:
                                    self.down()
                        if self.enemy_shoot_count == 1:
                            if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 34 < player_ship.bottom - player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                if not player.dead:
                                    self.enemy_shoot()
                                sleep(0.3)
                            else:
                                if player_ship.y + 20 < self.rect.y:
                                    self.up()
                                if player_ship.y + 20 > self.rect.y:
                                    self.down()
                        if self.enemy_shoot_count == 2:
                            if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 68 < player_ship.bottom - player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                if not player.dead:
                                    self.enemy_shoot()
                                sleep(0.3)
                            else:
                                if player_ship.y - 20 < self.rect.y:
                                    self.up()
                                if player_ship.y - 20 > self.rect.y:
                                    self.down()
                        if self.enemy_shoot_count == 3:
                            if player_ship.y + player_ship.h // 2 + 10 < self.rect.y + 72 < player_ship.bottom - player_ship.h // 2 + 35 and self.rect.x > player_ship.right:
                                if not player.dead:
                                    self.enemy_shoot()
                                sleep(0.3)
                            else:
                                if player_ship.y - 30 < self.rect.y:
                                    self.up()
                                if player_ship.y - 30 > self.rect.y:
                                    self.down()
                        if player_ship.x + player_ship.w + 200 <= self.rect.x:
                            self.x -= self.velocity
                            self.rect.x = self.x
                        if player_ship.x + player_ship.w + 200 >= self.rect.x:
                            self.x += self.velocity
                            self.rect.x = self.x
                    sleep(0.00001)
                except pygame.error:
                    sys.exit()

    def enemy_shoot(self):
        if self.enemy_shoot_count == 0:
            self.enemy_bullet_controller.append(Tile(self.screen, (self.rect.x + 7, self.rect.y + 9), 'E', 0))
            self.enemy_shoot_count = 1
        elif self.enemy_shoot_count == 1:
            self.enemy_bullet_controller.append(Tile(self.screen, (self.rect.x + 7, self.rect.y + 13), 'E', 0))
            self.enemy_shoot_count = 2
        elif self.enemy_shoot_count == 2:
            self.enemy_bullet_controller.append(Tile(self.screen, (self.rect.x + 7, self.rect.y + 51), 'E', 0))
            self.enemy_shoot_count = 3
        else:
            self.enemy_bullet_controller.append(Tile(self.screen, (self.rect.x + 7, self.rect.y + 55), 'E', 0))
            self.enemy_shoot_count = 0
        sou = choice(self.piy)
        sou.set_volume((effects_volume / 100))
        print(effects_volume)
        sou.play()


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
            """Иницирует класс сердечек."""
            super().__init__()
            # 0 - полное сердце, 1 - половинка сердца, 2 - пустое сердце
            self.hearts = [pygame.transform.scale(pygame.image.load(f'../sprites/heart/heart{i + 1}.png'),
                                                  (16, 16)) for
                           i in range(3)]
            self.screen = screen

        def draw_hearts(self, hp):
            """Рисует сердца с заданным количеством хп."""
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
        if not self.dead:
            self.bullet_controller.update_all()
            self.bullet_controller.check_all_collision(list_of_enemies, player_damage)
        else:
            self.bullet_controller.clear()

    def shoot(self):
        """Добавление выстреда в список и смена выстрела пушки."""
        if self.shoot_count == 0:
            self.bullet_controller.append(Tile(self.screen, (self.rect.x + 38, self.rect.y + 7), 'W', 0))
            self.shoot_count = 1
        else:
            self.bullet_controller.append(Tile(self.screen, (self.rect.x + 38, self.rect.y + 55), 'W', 0))
            self.shoot_count = 0
        # поигрыш звука выстрела
        sou = choice(self.piy)
        sou.set_volume((effects_volume / 100))
        sou.play()

    def draw_heart(self):
        """Рисует хп игрока"""
        self.heart_drawer.draw_hearts(self.hp)

    def __repr__(self):
        """Форматирует """
        return f'<Player ship: hp-{self.hp}>'

    def make_a_particle(self):
        """Рисует след за ракетой по направлению движения."""
        moving = pygame.key.get_pressed()
        if moving[pygame.K_LEFT] or moving[pygame.K_a]:
            self.particles.append([[self.rect.x + 3, self.rect.centery], [-2, 0], randint(4, 8)])
        elif moving[pygame.K_RIGHT] or moving[pygame.K_d]:
            self.particles.append(
                [[self.rect.x + 3, self.rect.centery], [-4, 0], randint(5, 10)])
        elif moving[pygame.K_UP] or moving[pygame.K_w]:
            self.particles.append([[self.rect.x + 3, self.rect.centery], [-2, randint(0, 10) / 7 - 1], randint(4, 8)])
        elif moving[pygame.K_DOWN] or moving[pygame.K_s]:
            self.particles.append([[self.rect.x + 3, self.rect.centery], [-2, randint(0, 10) / 7 - 1], randint(4, 8)])
        elif moving:
            self.particles.append([[self.rect.x + 3, self.rect.centery], [-0.5, 0], randint(2, 6)])
        # обновляет каждую частицу
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.2
            a = randint(50, 255), randint(0, 80), randint(0, 40)
            pygame.draw.circle(self.screen, a, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles.remove(particle)
        #print(self.coins_count)

    def move(self):
        if not self.dead:
            moving = pygame.key.get_pressed()
            if moving[pygame.K_LEFT] or moving[pygame.K_a]:
                self.left()
            if moving[pygame.K_RIGHT] or moving[pygame.K_d]:
                self.right()
            if moving[pygame.K_UP] or moving[pygame.K_w]:
                self.up()
            if moving[pygame.K_DOWN] or moving[pygame.K_s]:
                self.down()


class Enemy_controller:
    def __init__(self, screen, player: Player_ship):
        """Контроллирует всех врагов."""
        self.list_of_enemies = []
        self.player = player
        self.screen = screen
        self.CoinController = ItemController(self.screen)

    def append(self, value: Enemy_ship):
        """Добавляет врага в список врагов."""
        self.list_of_enemies.append(value)

    def append_list(self, value: list):
        for i in value:
            # print(value)
            self.list_of_enemies.append(i)

    def update_all(self):
        """Запускает движение всех врагов."""
        for enemy in self.list_of_enemies:
            thread = threading.Thread(target=enemy.random_move, args=(self.player,))
            thread.start()

    def get_enemies(self):
        """Возвращает всех врагов, у которых хп больше 0."""
        for i in self.list_of_enemies:
            if i.hp <= 0:
                i.__del__()
                self.list_of_enemies.pop(self.list_of_enemies.index(i))
        return self.list_of_enemies

    def draw_bullets(self, player: list):
        """"Нанесение урона игроку"""
        for i in self.list_of_enemies:
            if i.hp <= 0:
                del self[i]
                self.CoinController.append(Coin(self.screen, i.get_pos(), self.player))
            else:
                i.player_damage(player)

    def __delitem__(self, key):
        """Удаление врага из списка врагов."""
        del self.list_of_enemies[self[key]]

    def __getitem__(self, item):
        """Возвращает индекс элемента из списка."""
        return self.list_of_enemies.index(item)

    def __repr__(self):
        """Форматирует вывод."""
        return f'<Enemy controller: {self.list_of_enemies}>'

    def __bool__(self):
        """Возвращает True если длина списка не 0, иначе False."""
        return True if len(self.list_of_enemies) else False
