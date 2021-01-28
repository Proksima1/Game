import json
import pygame
from pygame_widgets import *
import os


class ButtonUpgrade(Button):
    def __init__(self, win, x, y, width, height, **kwargs):
        super().__init__(win, x, y, width, height, **kwargs)
        self.click_count = 0
        self.click_time = None

    def listen(self, events):
        """ Wait for inputs
                :param events: Use pygame.event.get()
                :type events: list of pygame.event.Event
                """
        now = pygame.time.get_ticks()
        if self.click_time is not None:
            if now - self.click_time > 8000 and self.click_count == 1:
                self.click_count = 0
                self.click_time = None
        if not self.hidden:
            pressed = pygame.mouse.get_pressed()[0]
            x, y = pygame.mouse.get_pos()
            if self.contains(x, y):
                if pressed:
                    self.colour = self.pressedColour
                    if not self.clicked:
                        self.clicked = True
                        self.onClick(*self.onClickParams)
                        if self.click_count < 2:
                            self.click_count += 1
                        self.click_time = pygame.time.get_ticks()
                elif self.clicked:
                    self.clicked = False
                    self.onRelease(*self.onReleaseParams)

                else:
                    self.colour = self.hoverColour

            elif not pressed:
                self.clicked = False
                self.colour = self.inactiveColour

    def blit_text(self, surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def change_color(self, desc):
        font = pygame.font.Font(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fonts/SuperLegendBoy-4w8Y.ttf'), 15)
        if self.click_count == 0:
            self.inactiveColour = (150, 150, 150)
        elif self.click_count == 1:
            self.inactiveColour = (120, 120, 120)
            a = pygame.Surface((100, 200))
            #text = font.render(desc, True, (255, 0, 0))
            #rect = text.get_rect(center=(a.get_rect().width // 2, a.get_rect().height))
            a.fill((220, 220, 220))
            #print(a.get_rect().width)
            self.blit_text(a, desc, (0, 0), font)
            self.win.blit(a, pygame.Rect(self.x - 10, self.y + self.height + 5, a.get_rect().width, a.get_rect().height))
            #self.win.blit(text, rect)
        elif self.click_count == 2:
            self.inactiveColour = (100, 100, 100)
        self.hoverColour = self.inactiveColour


class UpgrateItem:
    def __init__(self, screen, name, pos, description, filename=None):
        """Предмет улучшения корабля
        :param screen: На чем будет нарисован предмет
        :type screen: pygame.Surface
        :param name: Имя улучшения, будет выведенно, если filename не указан
        :type name: str
        :param pos: принимает 4 значения: позиция по x,
        позиция по y, ширина и высота соответственно.
        :type pos: Tuple[int, int, int, int]
        :param description: Описание улучшения.
        :type description: str
        :param filename: Принимает путь к файлу иконки
        :type filename: str"""
        self.screen = screen
        self.name = name
        self.filename = filename
        self.pos = pos
        self.desc = description
        self.inactive_color = (150, 150, 150)
        if self.filename is None:
            self.button = ButtonUpgrade(self.screen, self.pos[0], self.pos[1], self.pos[2], self.pos[3], text=self.name)
        else:
            try:
                self.button = ButtonUpgrade(self.screen, self.pos[0], self.pos[1], self.pos[2], self.pos[3],
                                            image=pygame.transform.scale(pygame.image.load(self.filename),
                                                                         (self.pos[2], self.pos[3])),
                                            imageHAlign='centre', imageVAlign='centre',
                                            inactiveColour=self.inactive_color)
            except FileNotFoundError:
                self.button = ButtonUpgrade(self.screen, self.pos[0], self.pos[1], self.pos[2], self.pos[3], text=self.name)

    def draw(self, events):
        self.button.listen(events)
        self.button.draw()
        self.button.change_color(self.desc)


class UpgrateController:
    def __init__(self, screen):
        self.screen = screen
        self.damage = 40
        self.speed = 1
        self.health = 200
        self.updatesItems = []

    def append(self, value: UpgrateItem):
        self.updatesItems.append(value)

    def damage_upg(self):
        with open('../data/save.json', 'w+', encoding='utf-8') as game_saver:
            upgrades = json.load(game_saver)
        for upds in upgrades:
            if not upds["damage_upg_1"]:
                self.damage += 10
                upds["damage_upg_1"] = True
            elif upds["damage_upg_1"] and not upds["damage_upg_2"]:
                upds["damage_upg_2"] = True
                self.damage += 10
            elif upds["damage_upg_1"] and upds["damage_upg_2"] and not upds["damage_upg_3"]:
                self.damage += 10
                upds["damage_upg_3"] = True

    def speed_upg(self):
        with open('../data/save.json', 'w+', encoding='utf-8') as game_saver:
            upgrades = json.load(game_saver)
        for upds in upgrades:
            if not upds["speed_upg_1"]:
                self.speed += 1
                upds["speed_upg_1"] = True
            elif upds["speed_upg_1"] and not upds["speed_upg_2"]:
                upds["speed_upg_2"] = True
                self.speed += 1
            elif upds["speed_upg_1"] and upds["speed_upg_2"] and not upds["speed_upg_3"]:
                self.speed += 1
                upds["speed_upg_3"] = True

    def health_upg(self):
        with open('../data/save.json', 'w+', encoding='utf-8') as game_saver:
            upgrades = json.load(game_saver)
        for upds in upgrades:
            if not upds["health_upg_1"]:
                self.health += 25
                upds["health_upg_1"] = True
            elif upds["health_upg_1"] and not upds["health_upg_2"]:
                upds["health_upg_2"] = True
                self.health += 1
            elif upds["health_upg_1"] and upds["health_upg_2"] and not upds["health_upg_3"]:
                self.health += 1
                upds["health_upg_3"] = True

    def show_updates(self):
        button_damage_upd = Button(screen, 50, 50, 50, 50, inactiveColour=damage_upgd_color,
                                   hoverColour=damage_upgd_color, pressedColour=damage_upgd_color)
        button_speed_upd = Button(screen, 150, 50, 50, 50, inactiveColour=speed_upgd_color,
                                  hoverColour=speed_upgd_color, pressedColour=speed_upgd_color)
        button_health_upd = Button(screen, 250, 50, 50, 50, inactiveColour=health_upgd_color,
                                   hoverColour=health_upgd_color, pressedColour=health_upgd_color)

        button_damage_upd.listen(events)
        button_damage_upd.draw()

        button_speed_upd.listen(events)
        button_speed_upd.draw()

        button_health_upd.listen(events)
        button_health_upd.draw()


"""if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    money = 5000
    running = True
    click_damage_upd = 0
    click_speed_upd = 0
    click_health_upd = 0
    position = (0, 0)
    damage_upgd_color = "red"
    speed_upgd_color = "red"
    health_upgd_color = "red"
    upgs = Updates()
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    position = event.pos
                    if 50 <= position[0] <= 100 and 50 <= position[1] <= 100:
                        click_damage_upd += 1
                        click_speed_upd = 0
                        click_health_upd = 0
                    elif 150 <= position[0] <= 200 and 50 <= position[1] <= 100:
                        click_speed_upd += 1
                        click_damage_upd = 0
                        click_health_upd = 0
                    elif 250 <= position[0] <= 300 and 50 <= position[1] <= 100:
                        click_health_upd += 1
                        click_speed_upd = 0
                        click_damage_upd = 0
                    else:
                        click_damage_upd = 0
                        click_speed_upd = 0
                        click_health_upd = 0
        with open('../data/save.json', 'w+', encoding='utf-8') as game_saver:
            upgrades = json.load(game_saver)
        for upds in upgrades:
            if click_damage_upd == 2:
                upgs.damage_upg()
                if upds["damage_upg_3"]:
                    if money >= 1700:
                        damage_upgd_color = "gold"
                        money -= 1700
                    else:
                        print("No money - no funny")
                elif upds["damage_upg_2"]:
                    if money >= 1200:
                        damage_upgd_color = "green"
                        money -= 1200
                    else:
                        print("No money - no funny")
                elif upds["damage_upg_1"]:
                    if money >= 1000:
                        damage_upgd_color = "blue"
                        money -= 1000
                    else:
                        print("No money - no funny")
                click_damage_upd = 0

            if click_speed_upd == 2:
                upgs.speed_upg()
                if upds["speed_upg_3"]:
                    if money >= 1000:
                        speed_upgd_color = "gold"
                        money -= 1000
                    else:
                        print("No money - no funny")
                elif upds["speed_upg_2"]:
                    if money >= 1200:
                        speed_upgd_color = "green"
                        money -= 1000
                    else:
                        print("No money - no funny")
                elif upds["speed_upg_1"]:
                    if money >= 1700:
                        speed_upgd_color = "blue"
                        money -= 1700
                    else:
                        print("No money - no funny")
                click_speed_upd = 0

            if click_health_upd == 2:
                upgs.health_upg()
                if upds["health_upg_3"]:
                    if money >= 1700:
                        health_upgd_color = "gold"
                        money -= 1700
                    else:
                        print("No money - no funny")
                elif upds["health_upg_2"]:
                    if money >= 1200:
                        health_upgd_color = "green"
                        money -= 1200
                    else:
                        print("No money - no funny")
                elif upds["health_upg_1"]:
                    if money >= 1000:
                        health_upgd_color = "blue"
                        money -= 1000
                    else:
                        print("No money - no funny")
                click_health_upd = 0
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()"""
if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    lreader = UpgrateItem(screen, 'fasfas', (20, 20, 80, 80), "Improves player's cannon damage.", filename='../sprites/upgrades/damage_upgrade.png')
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        lreader.draw(events)
        pygame.display.flip()
        screen.fill((0, 0, 0))
