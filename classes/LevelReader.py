from random import randint

from pygame_widgets import ButtonArray

from MainMenu import *
from SpriteController import *

class LevelReader:
    def __init__(self, screen: pygame.Surface, player):
        self.screen = screen
        self.amount_of_enemies, self.amount_of_waves, self.max_level, self.max_speed = None, None, None, None
        self.enemies = []
        self.sp_cont = SpriteController(self.screen)
        self.en_cont = Enemy_controller(self.screen, player)
        self.present_wave = 1
        self.pause = False
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

    def world_pause(self):
        if self.pause:
            return True
        return False

    def draw_background(self):
        if self.count < len(self.list_of_bd):
            self.screen.blit(pygame.image.frombuffer(self.list_of_bd[int(self.count)], size, 'RGB'), (0, 0))
            self.count += 0.01
        else:
            self.count = 0

    def generate_enemies(self):
        if self.present_wave < self.amount_of_waves + 1:
            self.enemies = [Enemy_level1(self.screen, randint(self.screen.get_width() // 2,
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


pygame.init()
s_size = width, height = size
screen = pygame.display.set_mode(s_size)
pygame.display.set_caption('Кустик')
clock = pygame.time.Clock()
running = True
pl = Player_ship(screen, 32, 32)
a = LevelReader(screen, pl)
a.sp_cont.append(pl)
pause_menu = ButtonArray(screen, width // 3, height // 6, 400, 400, (1, 3),
                         border=100, texts=('CONTINUE', 'OPTIONS', 'QUIT'), onClicks=(1, 2, quit))
end_buttons = ButtonArray(screen, width // 2, height // 2, 400, 400, (3, 1),
                          texts=('BACK', 'UPGRADE', 'NEXT'))
last_shoot = pygame.time.get_ticks()


def setup(filename):
    a.read_json(filename)


def start():
    """global running
    while running:"""
    events = pygame.event.get()
    global last_shoot
    current_time = pygame.time.get_ticks()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not pl.dead:
                if current_time - last_shoot > 500:
                    pl.shoot()
                    last_shoot = pygame.time.get_ticks()
        if event.type == pygame.KEYDOWN:
            if event.key == 27 and not a.pause:  # esc
                a.pause = True
                pause_menu.listen(events)
                pause_menu.draw()
                continue

    # if not a.pause:
    pl.move()
    a.sp_cont.draw_all()
    a.en_cont.CoinController.update_all()
    a.en_cont.draw_bullets([pl])
    pl.draw_shoot(a.get_enemies())
    pygame.display.flip()
    a.draw_background()
    if a.check_wave():
        a.generate_enemies()
        a.en_cont.update_all()
    if a.present_wave > a.amount_of_waves:
        return 'ended'
    elif not a.pause and not a.present_wave > a.amount_of_waves:
        return True
    else:
        return 'paused'


def draw_pause():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == 27 and a.pause:  # esc
                a.pause = False
                return tuple,
                #continue
    a.draw_background()
    pause_menu.listen(events)
    pause_menu.draw()
    return True


def draw_end():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    a.draw_background()
    end_buttons.listen(events)
    end_buttons.draw()
    return True
