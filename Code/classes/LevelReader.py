from pygame_widgets import ButtonArray

from SpriteController import *


class LevelReader:
    def __init__(self, screen: pygame.Surface, player):
        self.screen = screen
        self.amount_of_enemies, self.amount_of_waves, self.max_level, self.max_speed = None, None, None, None
        self.enemies = []
        self.sp_cont = SpriteController(self.screen)
        self.en_cont = Enemy_controller(self.screen, player)
        self.present_wave = 0
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
        """Если волны ещё не закончились то создает новую, и возвращает True,
        иначе False."""
        if self.present_wave < self.amount_of_waves:
            self.enemies = [Enemy_level1(self.screen, randint(self.screen.get_width() // 2,
                                                              self.screen.get_width() - 32),
                                         randint(32, self.screen.get_height() - 32)) for _ in
                            range(self.amount_of_enemies)]
            for i in self.enemies:
                self.sp_cont.append(i)
                self.en_cont.append(i)
            self.present_wave += 1
            return True
        else:
            return False

    def get_enemies(self):
        """Очищает список от мертвых врагов и возвращает список."""
        for i in self.enemies:
            if i.hp <= 0:
                del self[i]
        return self.enemies

    def check_wave(self):
        """Возвращает True, если контроллер врагов не пуст, иначе False."""
        if self.en_cont:
            return True
        return False

    def __delitem__(self, key):
        """Удаление врага из списка врагов."""
        del self.enemies[self[key]]

    def __getitem__(self, item):
        """Возвращает индекс элемента из списка."""
        return self.enemies.index(item)


s_size = None
screen = None
clock = None
running = None
pl = None
lreader = None
last_shoot = None
state = None
level_number = None
ended_count = 0
end_time = None
font = None
coins_count = 0


def setup(filename):
    global s_size, screen, clock, running, pl, lreader, last_shoot, state, level_number, font, end_time, ended_count
    s_size = None
    screen = None
    clock = None
    running = None
    pl = None
    lreader = None
    last_shoot = None
    state = None
    level_number = None
    ended_count = 0
    end_time = None
    font = None
    pygame.init()
    s_size = width, height = size
    screen = pygame.display.set_mode(s_size)
    pygame.display.set_caption('Кустик')
    clock = pygame.time.Clock()
    running = True
    pl = Player_ship(screen, 32, 32)
    lreader = LevelReader(screen, pl)
    lreader.sp_cont.append(pl)
    last_shoot = pygame.time.get_ticks()
    state = 'running'
    lreader.read_json(os.path.join('../data/', filename))
    level_number = int(filename[0]) + 1
    font = pygame.font.Font(font_path, 20)


def start(pause_b, end_b, loss, should_continue=None):
    events = pygame.event.get()
    global last_shoot, state, ended_count, end_time, s_size
    if should_continue:
        state = 'running'
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
            if event.key == 27 and state == 'running':  # esc
                state = 'paused'
            elif event.key == 27 and state == 'paused':
                state = 'running'
    else:
        if state == 'running':
            channel.unpause()
            pl.move()
            lreader.sp_cont.draw_all()
            lreader.en_cont.ItemController.update_all()
            lreader.en_cont.draw_bullets([pl])
            pl.draw_shoot(lreader.get_enemies())
            if pl.hp <= 0:
                state = 'dead'
            pygame.display.flip()
            lreader.draw_background()
            coins = font.render(
                f'You collected {pl.get_coins()} riddilions.',
                True, (249, 166, 2))
            coin_rect = coins.get_rect(center=(s_size[0] - 200, 20))
            screen.blit(coins, coin_rect)
            if not lreader.check_wave():
                if lreader.generate_enemies():
                    pass
                else:
                    if not ended_count:
                        end_time = pygame.time.get_ticks()
                        ended_count += 1
                lreader.en_cont.update_all()
            if end_time is not None:
                text = font.render(
                    f'You have another {10 - int(int(pygame.time.get_ticks() - end_time) / 1000)}'
                    f' seconds to collect all the rewards.',
                    True, (249, 166, 2))
                rect = text.get_rect(center=(s_size[0] / 2, 50))
                screen.blit(text, rect)
                if pygame.time.get_ticks() - end_time > 10000:
                    state = 'ended'
        elif state == 'ended':
            draw_end(events, end_b)
            channel.pause()
        elif state == 'paused':
            draw_pause(events, pause_b)
            channel.pause()


def draw_pause(events, pause: ButtonArray):
    global state
    lreader.draw_background()
    pause.draw()
    pause.listen(events)
    pygame.display.flip()


def draw_end(events, end: ButtonArray):
    global level_number, coins_count
    lreader.draw_background()
    end.listen(events)
    end.draw()
    pygame.display.flip()
    with open('../data/save.json', 'r+', encoding='utf-8') as read_coins:
        coins = json.loads(read_coins.read())[0]['coins']
        if coins_count == 0:
            end_count_of_coins = coins + pl.get_coins()
            print(end_count_of_coins)
            coins_count += 1
    with open('../data/save.json', 'w+', encoding='utf-8') as game_saver:
        if coins_count == 0:
            game_saver.write(json.dumps([{
                'level': level_number,
                'coins': end_count_of_coins
            }, {
                'upgrades': {
                    "damage_upg_1": False,
                    "damage_upg_2": False,
                    "damage_upg_3": False,
                    "speed_upg_1": False,
                    "speed_upg_2": False,
                    "speed_upg_3": False,
                    "health_upg_1": False,
                    "health_upg_2": False,
                    "health_upg_3": False}
            }], indent=4, separators=(',', ': ')))


def draw_loss(events, loss: ButtonArray):
    #self.music_text = self.font.render('Music volume', True, (0, 0, 0))
    #self.music_rect = self.music_text.get_rect(center=(self.music_volume.x - 120,
    #                                                  self.music_volume.y + 3))
    #a.draw_background()
    #loss.listen(events)
    pass
    # loss.draw()
    #pygame.display.flip()

