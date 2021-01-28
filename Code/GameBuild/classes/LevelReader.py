import json

from ProjectGame.Game.GameBuild.classes.fregate import Player_ship
from SpriteController import *


class LevelReader:
    def __init__(self, screen: pygame.Surface, player):
        self.screen = screen
        self.amount_of_enemies, self.amount_of_waves, self.max_level, self.max_speed = None, None, None, None
        self.enemies = []
        self.sp_cont = SpriteController(self.screen)
        self.en_cont = Enemy_controller(self.screen, player)
        self.present_wave = 1
        # self.bd = pygame.image.tostring(pygame.transform.scale(pygame.image.load('../sprites/bg1.png'),
        #                                                       size), 'RGB')
        self.list_of_bd = [pygame.image.tostring(
            pygame.transform.scale(pygame.image.load('../sprites/bg/bg1.png'),
                                   size), 'RGB'),
            pygame.image.tostring(
                pygame.transform.scale(pygame.image.load('../sprites/bg/bg2.png'),
                                       size), 'RGB'),
            pygame.image.tostring(
                pygame.transform.scale(pygame.image.load('../sprites/bg/bg3.png'),
                                       size), 'RGB')]
        self.count = 0

    def read_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as gen:
            text = json.load(gen)
            self.amount_of_enemies = int(text[0]['amount_of_enemies'])
            self.amount_of_waves = int(text[0]['amount_of_waves'])
            self.max_level = int(text[0]['max_level'])
            self.max_speed = int(text[0]['max_speed'])

    def draw_background(self):
        if self.count < len(self.list_of_bd):
            self.screen.blit(pygame.image.frombuffer(self.list_of_bd[int(self.count)], size, 'RGB'), (0, 0))
            self.count += 0.01
        else:
            self.count = 0

    def generate_enemies(self):
        if self.present_wave < self.amount_of_waves + 1:
            self.enemies = [Enemy_level2(self.screen, randint(self.screen.get_width() // 2,
                                                            self.screen.get_width() - 32),
                                       randint(32, self.screen.get_height() - 32)) for _ in
                            range(self.amount_of_waves)]
            for i in self.enemies:
                self.sp_cont.append(i)
                self.en_cont.append(i)
            self.present_wave += 1

    def get_enemies(self):
        for i in self.enemies:
            if i.hp <= 0:
                del self[i]
        return self.enemies

    def check_wave(self):
        if self.en_cont:
            return False
        return True

    def __delitem__(self, key):
        """Удаление врага из списка врагов."""
        del self.enemies[self[key]]

    def __getitem__(self, item):
        """Возвращает индекс элемента из списка."""
        return self.enemies.index(item)


if __name__ == '__main__':
    pygame.init()
    size = width, height = size
    screen = pygame.display.set_mode(size)
    running = True
    pl = Player_ship(screen, 32, 32)
    lreader = LevelReader(screen, pl)
    lreader.read_json('../LevelEditor/1.json')
    lreader.sp_cont.append(pl)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not pl.dead:
                    pl.shoot()
        pl.move()
        lreader.sp_cont.draw_all()
        lreader.en_cont.CoinController.update_all()
        if lreader.check_wave():
            lreader.generate_enemies()
            lreader.en_cont.update_all()
        lreader.en_cont.draw_bullets([pl])
        pl.draw_shoot(lreader.get_enemies())
        pygame.display.flip()
        lreader.draw_background()
    pygame.quit()
