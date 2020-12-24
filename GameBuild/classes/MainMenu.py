import pygame
from classes.button import Button


class MainMenu:
    def __init__(self, screen, height, width):
        self.screen = screen
        self.height = height
        self.width = width

    def show_menu(self, *action):
        # загружаем картинку
        backgroung = pygame.image.load('test_photo.png')
        play = Button((self.width / 2 - 100, self.height / 2 - 150), 'PLAY', self.screen, action[0], size=(100, 50))
        self.screen.blit(backgroung, (0, 0))  # рисуем задний фон
        # рисуем кнопки
        play.draw()
        settings = Button((self.width / 2 - 100, self.height / 2 - 50), 'SETTINGS', self.screen, action[1],
                          size=(100, 50), font_size=12)
        settings.draw()
        quit = Button((self.width / 2 - 100, self.height / 2 + 50), 'QUIT', self.screen, action[2], size=(100, 50))
        quit.draw()

    def show_settings(self, *action):
        a = Button((self.width / 2 - 100, self.height / 2 - 50), 'Hai', self.screen, action[0], size=(100, 50),
                   font_size=25)
        a.draw()


# потом можно удалить
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тест')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    main = MainMenu(screen, height, width)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        main.show_menu(None, None, quit)
        pygame.display.flip()
    pygame.quit()
