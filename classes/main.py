# from classes.button import Button
# from classes.progressbar import ProgressBar
"""from classes.LevelReader import LevelReader

from classes.fregate import Player_ship"""
from LevelReader import *

show_menu = True
show_setting = False
show_game = False
clicked_on_return = None
state = 'running'


def quit_game():
    pygame.quit()
    quit()


def start_game():
    def return_to_menu_from_settings():
        global show_menu
        global show_setting
        show_setting = False
        show_menu = True

    def return_to_menu_from_game():
        global show_menu
        global show_setting
        global show_game
        show_setting = False
        show_menu = True
        show_game = False

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
            main.show_settings(events, return_to_menu_from_settings)
            pygame.display.flip()

    global show_menu
    global show_setting
    global clicked_on_return
    global show_game
    pygame.init()
    pygame.display.set_caption('Тест')
    w_size = width, height = size
    screen = pygame.display.set_mode(w_size)
    main = MainMenu(screen, height, width)

    def continue_game():
        global clicked_on_return
        clicked_on_return = True

    pause_buttons = ButtonArray(screen, width // 3, height // 6, 400, 400, (1, 3),
                                texts=('CONTINUE', 'OPTIONS', 'QUIT'), onClicks=(continue_game, settings, return_to_menu_from_game))
    end_buttons = ButtonArray(screen, width // 3, height // 6, 400, 400, (3, 1),
                              texts=('BACK', 'UPGRADE', 'NEXT'), onClicks=(return_to_menu_from_game, quit_game, quit_game))

    def play():
        global show_menu
        global show_setting
        global show_game
        global clicked_on_return
        global state
        show_game = True
        show_menu = False
        show_setting = False
        setup('../LevelEditor/1.json')
        while show_game:
            if clicked_on_return is None:
                start(pause_buttons, end_buttons, None, state)
            else:
                start(pause_buttons, end_buttons, True, state)
                clicked_on_return = None

    while show_menu:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                show_menu = False
                show_setting = False
        main.show_menu(events, play, settings, quit)
        pygame.display.flip()


start_game()
