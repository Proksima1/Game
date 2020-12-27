# from classes.button import Button
# from classes.progressbar import ProgressBar
import pygame
"""from classes.LevelReader import LevelReader

from classes.fregate import Player_ship"""
from classes.MainMenu import MainMenu
from classes.settings import *
show_menu = True
show_setting = False


def start_game():
    global show_menu
    global show_setting
    pygame.init()
    pygame.display.set_caption('Тест')
    w_size = width, height = size
    screen = pygame.display.set_mode(w_size)
    main = MainMenu(screen, height, width)

    def play():
        global show_menu
        global show_setting
        show_menu = False
        show_setting = False
        running = True
        pl = Player_ship(screen, 32, 32)
        a = LevelReader(screen, pl)
        a.read_json('../LevelEditor/1.json')
        a.sp_cont.append(pl)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not pl.dead:
                        pl.shoot()
            pl.move()
            a.sp_cont.draw_all()
            a.en_cont.CoinController.update_all()
            if a.check_wave():
                a.generate_enemies()
                a.en_cont.update_all()
            a.en_cont.draw_bullets([pl])
            pl.draw_shoot(a.get_enemies())
            pygame.display.flip()
            a.draw_background()

    def return_to_menu():
        global show_menu
        global show_setting
        show_setting = False
        show_menu = True

    def settings():
        global show_menu
        global show_setting
        show_menu = False
        show_setting = True
        screen.fill((0, 0, 0))
        while show_setting:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    show_menu = False
                    show_setting = False
            main.show_settings(events, return_to_menu)
            pygame.display.flip()

    while show_menu:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                show_menu = False
                show_setting = False
        main.show_menu(events, play, settings, quit)
        pygame.display.flip()


start_game()
