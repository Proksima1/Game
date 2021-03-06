import pygame
# from classes.button import Button
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

from ProjectGame.Game.classes.settings import *


class MainMenu:
    def __init__(self, screen: pygame.Surface, height, width):
        self.font = pygame.font.Font(font_path, 20)
        self.screen = screen
        self.height = height
        self.width = width
        # загружаем картинку
        self.backgroung = pygame.image.load('D:/testrepository/ProjectGame/Game/test_photo.png')
        self.master_volume = Slider(self.screen, self.width // 2, self.height // 3 - 150,
                                    100, 10, min=0, max=100, step=1, colour=(255, 255, 255),
                                    handleRadius=10, initial=master_volume)
        self.effects_volume = Slider(self.screen, self.width // 2, self.height // 3 - 100,
                                     100, 10, min=0, max=100, step=1, colour=(255, 255, 255),
                                     handleRadius=10, initial=effects_volume)
        self.music_volume = Slider(self.screen, self.width // 2, self.height // 3 - 50,
                                   100, 10, min=0, max=100, step=1, colour=(255, 255, 255),
                                   handleRadius=10, initial=music_volume)
        self.master_text = self.font.render('Master volume', True, (0, 0, 0))
        self.master_rect = self.master_text.get_rect(center=(self.master_volume.x - 120,
                                                             self.master_volume.y + 3))
        self.effects_text = self.font.render('Effects volume', True, (0, 0, 0))
        self.effects_rect = self.master_text.get_rect(center=(self.effects_volume.x - 130,
                                                              self.effects_volume.y + 3))
        self.music_text = self.font.render('Music volume', True, (0, 0, 0))
        self.music_rect = self.master_text.get_rect(center=(self.music_volume.x - 120,
                                                            self.music_volume.y + 3))

    def show_menu(self, events, *action):
        play = Button(self.screen, self.width / 2 - 100, self.height / 2 - 150, 100, 50, text='PLAY',
                      margin=20, onClick=lambda: action[0](), font=pygame.font.Font(font_path, 25))
        self.screen.blit(pygame.transform.scale(self.backgroung, self.screen.get_size()), (0, 0))  # рисуем задний фон
        # рисуем кнопки
        play.listen(events)
        play.draw()
        settings = Button(self.screen, self.width / 2 - 100, self.height / 2 - 50, 100, 50,
                          text='SETTINGS', margin=20, onClick=lambda: action[1](), font=pygame.font.Font(font_path, 12))
        settings.listen(events)
        settings.draw()
        quit = Button(self.screen, self.width / 2 - 100, self.height / 2 + 50, 100, 50,
                      text='QUIT', margin=20, onClick=lambda: action[2](), font=pygame.font.Font(font_path, 25))
        quit.listen(events)
        quit.draw()

    def show_settings(self, events, *action):
        self.screen.blit(pygame.transform.scale(self.backgroung, self.screen.get_size()), (0, 0))
        self.master_volume.listen(events)
        self.master_volume.draw()
        self.music_volume.listen(events)
        self.music_volume.draw()
        self.effects_volume.listen(events)
        self.effects_volume.draw()
        self.screen.blit(self.master_text, self.master_rect)
        self.screen.blit(self.music_text, self.music_rect)
        self.screen.blit(self.effects_text, self.effects_rect)
        back = Button(self.screen, 20, self.height - 70, 100, 50,
                      text='BACK', margin=20, onClick=lambda: action[0](), font=pygame.font.Font(font_path, 25))
        back.listen(events)
        back.draw()
        with open('data/config.json', 'w+', encoding='utf-8') as conf:
            conf.write(json.dumps([{'master_volume': str(self.master_volume.getValue()),
                                    'effects_volume': str(self.effects_volume.getValue()),
                                    'music_volume': str(self.music_volume.getValue())}],
                                  indent=4, separators=(',', ': '), sort_keys=True))


# потом можно удалить
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тест')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    main = MainMenu(screen, height, width)
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        main.show_menu(events, quit, None, quit)
        pygame.display.flip()
    pygame.quit()
