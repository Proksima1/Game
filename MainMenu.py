import pygame
from classes.button import Button
import sys


class MainMenu:
    def __init__(self):
        self.buttons = [Button(screen, 100, 50)]

    def show_menu(self, *action):
        play = Button(screen, 100, 50)
        play.draw(width / 2 - 100, height / 2 - 150, 'PLAY', action[0])
        settings = Button(screen, 100, 50)
        settings.draw(width / 2 - 100, height / 2 - 50, 'SETTINGS', action[1])
        quit = Button(screen, 100, 50)
        quit.draw(width / 2 - 100, height / 2 + 50, 'QUIT', action[2])


def quit():
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тест')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    main = MainMenu()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        main.show_menu(None, None, quit)
        pygame.display.flip()
    pygame.quit()