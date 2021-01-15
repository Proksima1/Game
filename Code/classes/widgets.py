from typing import Tuple

import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


class TextBoxUpdated(Slider):
    def __init__(self, win, x, y, width, height):
        super().__init__(win, x, y, width, height)


class ProgressBar:
    def __init__(self, screen: pygame.Surface, color: str, x: int, y: int, width: int, height: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.height = height
        self.width = width
        self.width2 = width
        self.color = color

    def draw(self, percent):
        if percent >= 0:
            try:
                sc = pygame.Surface((self.width2, self.height))
                sc.fill((255, 0, 0))
                self.screen.blit(sc, (self.x, self.y))
                self.width2 = self.width / 100 * percent
            except pygame.error:
                pass


class Button:
    def __init__(self, pos: Tuple[int, int], message: str, screen: pygame.Surface, action=None, size=(80, 50),
                 font_size=20, font_color=(0, 0, 0)):
        self.bg = (23, 204, 58)
        self.active_color = (13, 162, 58)
        self.inactive_color = (23, 204, 58)
        self.pos = pos
        self.size = size
        self.font = pygame.font.Font(font_path, font_size)
        self.message = message
        self.screen = screen
        self.txt_surf = self.font.render(self.message, True, font_color)
        self.txt_rect = self.txt_surf.get_rect(center=[s // 2 for s in self.size])
        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=pos)
        self.action = action

    def draw(self):
        self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        self.screen.blit(self.surface, self.rect)

    def mouseover(self):
        # self.bg = self.bg
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect.collidepoint(pos):
            self.bg = self.active_color
            if click[0] == 1:
                pygame.time.delay(100)
                if self.action is not None:
                    self.action()
        else:
            self.bg = self.inactive_color


if __name__ == '__main__':
    import pygame
    from pygame_widgets import Button

    pygame.init()
    win = pygame.display.set_mode((600, 600))

    button = Button(
        win, 100, 100, 300, 150, text='Hello',
        fontSize=50, margin=20,
        inactiveColour=(255, 0, 0),
        pressedColour=(0, 255, 0),
        onClick=lambda: print('Click'),
        image=pygame.transform.scale(pygame.image.load('../test_photo.png'), (300, 150))
    )

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        button.listen(events)
        button.draw()

        pygame.display.update()