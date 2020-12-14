import pygame
from classes.button import Button
from classes.MainMenu import MainMenu
from classes.progressbar import ProgressBar

show_menu = True
show_setting = False


def start_game():
    global show_menu
    global show_setting
    pygame.init()
    pygame.display.set_caption('Тест')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    main = MainMenu(screen, height, width)
    clock = pygame.time.Clock()

    def play():
        global show_menu
        global show_setting
        show_menu = False
        show_setting = False

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    show_menu = False
                    show_setting = False
            main.show_settings(return_to_menu)
            pygame.display.flip()

    while show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_menu = False
                show_setting = False
        main.show_menu(play, settings, quit)
        pygame.display.set_caption(str(clock.get_fps()))
        pygame.display.flip()
        clock.tick(144)


start_game()
