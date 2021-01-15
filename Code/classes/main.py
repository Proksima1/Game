from pygame_widgets import ButtonArray

from LevelReader import *
from MainMenu import MainMenu
from upgrades import *

show_menu = True
show_setting = False
show_game = False
clicked_on_return = None
update_menu = False
navigation_menu = False
_state = ''
level = 1
with open('../data/save.json', 'a+', encoding='utf-8') as _:
    pass


def quit_game():
    pygame.quit()
    quit()


def start_game():
    def return_to_menu_from_settings():
        global show_menu
        global show_setting
        global navigation_menu
        show_setting = False
        navigation_menu = False
        show_menu = True

    def show_updates():
        global update_menu
        global show_game
        show_game = False
        update_menu = True

    def return_to_menu_from_game():
        global show_menu
        global show_setting
        global show_game
        global _state
        show_setting = False
        show_menu = True
        show_game = False
        _state = '1'

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

    def navigation():
        global navigation_menu
        global show_menu
        navigation_menu = True
        while navigation_menu:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    show_menu = False
                    navigation_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pygame.draw.rect(screen, "invisible", )

    def updates():
        global update_menu
        global show_game
        while update_menu:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    update_menu = False
                    show_game = False
            main.update(events, show_updates)
            pygame.display.flip()

    def next_level():
        global level, _state
        _state = 'new_level'
        play()

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
    end_buttons = ButtonArray(screen, width // 3, height // 6, 200, 200, (3, 1),
                              texts=('BACK', 'UPGRADE', 'NEXT'), onClicks=(return_to_menu_from_game, quit_game, next_level))

    def play():
        global show_menu, show_setting, show_game
        global clicked_on_return, _state, level
        show_game = True
        show_menu = False
        show_setting = False
        with open('../data/save.json', 'r', encoding='utf-8') as level_picker:
            level = json.loads(level_picker.read())[0]['level']
        setup(f'{level}.json')
        while show_game:
            if clicked_on_return is None:
                start(pause_buttons, end_buttons)
            else:
                start(pause_buttons, end_buttons, True)
                clicked_on_return = None
            if _state != '':
                _state = ''
                break

    while show_menu:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                show_menu = False
                show_setting = False
        main.show_menu(events, play, settings, quit, navigation)
        pygame.display.flip()


start_game()
