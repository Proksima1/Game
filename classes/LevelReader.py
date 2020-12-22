import json

from SpriteController import *


class LevelReader:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.amount_of_enemies, self.amount_of_waves, self.max_level, self.max_speed = None, None, None, None
        self.enemies = []
        self.sp_cont = SpriteController(self.screen)
        self.en_cont = Enemy_controller(self.screen)
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
            self.enemies = [[Enemy_ship(self.screen, randint(self.screen.get_width() // 2,
                                                             self.screen.get_width() - 32),
                                        randint(32, self.screen.get_height() - 32)), 1] for _ in
                            range(self.amount_of_waves)]
            for i in self.enemies:
                self.sp_cont.append(i[0])
                self.en_cont.append(i[0])
            self.present_wave += 1

    def check_wave(self):
        if self.en_cont:
            return False
        return True


if __name__ == '__main__':
    pygame.init()
    size = width, height = size
    screen = pygame.display.set_mode(size)
    running = True
    pl = Player_ship(screen, 32, 32)
    a = LevelReader(screen)
    a.read_json('../LevelEditor/1.json')
    a.sp_cont.append(pl)
    a.en_cont.update_all(pl)
    # print(a.check_wave())
    clock = pygame.time.Clock()
    while running:
        moving = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pl.shoot()
        if moving[pygame.K_LEFT] or moving[pygame.K_a]:
            pl.left()
        if moving[pygame.K_RIGHT] or moving[pygame.K_d]:
            pl.right()
        if moving[pygame.K_UP] or moving[pygame.K_w]:
            pl.up()
        if moving[pygame.K_DOWN] or moving[pygame.K_s]:
            pl.down()
        # print(a.check_wave())
        a.sp_cont.draw_all()
        # print(a.check_wave())
        if a.check_wave():
            a.generate_enemies()
        # print(a.en_cont)
        # a.en_cont.update_all(pl)
        a.en_cont.draw_bullets([pl])
        pl.draw_shoot(a.en_cont.get_enemies())
        pygame.display.flip()
        a.draw_background()
        # pygame.display.set_caption("fps: " + str(clock.get_fps()))
        # clock.tick(120)
        # screen.fill((0, 0, 0))
    pygame.quit()
