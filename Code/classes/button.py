from typing import Tuple

import pygame
from classes.settings import *


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
    pygame.init()
    pygame.display.set_caption('Тест')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    running = True
    a = Button((60, 30), 'hello', screen)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        a.draw()
        pygame.display.flip()
    pygame.quit()
