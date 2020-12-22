import pygame
from classes.button import Button
import sys


class MainMenu:
    def __init__(self, screen, height, width):
        self.screen = screen
        self.height = height
        self.width = width

    def show_menu(self, *action):
        # загружаем картинку
        backgroung = pygame.image.load('test_photo.png')
        play = Button(self.screen, 100, 50)
        self.screen.blit(backgroung, (0, 0))  # рисуем задний фон
        # рисуем кнопки
        play.draw((self.width / 2 - 100, self.height / 2 - 150), 'PLAY', 20, action[0])
        settings = Button(self.screen, 100, 50)
        settings.draw((self.width / 2 - 100, self.height / 2 - 50), 'SETTINGS', 13, action[1])
        quit = Button(self.screen, 100, 50)
        quit.draw((self.width / 2 - 100, self.height / 2 + 50), 'QUIT', 20, action[2])

    def show_settings(self, *action):
        a = Button(self.screen, 100, 50)
        a.draw((self.width / 2 - 100, self.height / 2 - 50), 'Hai', 30,  action[0])


# потом можно удалить
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тест')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    main = MainMenu(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        main.show_menu(None, None, quit)
        pygame.display.flip()
    pygame.quit()