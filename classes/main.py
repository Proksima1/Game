# from classes.button import Button
# from classes.progressbar import ProgressBar
import pygame
"""from classes.LevelReader import LevelReader

from classes.fregate import Player_ship"""
from MainMenu import MainMenu
from settings import *
from LevelReader import *
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
        setup('../LevelEditor/1.json')
        st = start()
        while st:
            if st == 'paused':
                while True:
                    pa = draw_pause()
                    if type(pa) == tuple:
                        st = start()
                        continue
                #st = start()
            elif st == 'ended':
                draw_end()
            else:
                st = start()

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
