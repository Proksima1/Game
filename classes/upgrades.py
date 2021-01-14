import pygame
import json
from pygame_widgets import *


class Updates():
    def __init__(self):
        self.damage = 40
        self.speed = 1
        self.health = 200

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


if __name__ == '__main__':
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
    pygame.quit()
