import pygame
from typing import Tuple


class ProgressBar:
    def __init__(self, screen, height: int, width: int, color: Tuple[int, int, int]):
        self.screen = screen
        self.height = height
        self.width = width
        self.color = color

    def draw(self, x, y, percent):
        # рисовка рамки бара
        pygame.draw.rect(self.screen, self.color, ((x, y), (x + self.height, y + self.width)), 2)
        # если процентов больше 0, то рисуется квадрат такого размера
        if percent >= 0:
            pygame.draw.rect(screen, self.color, ((x + 5, y + 5),
                                                  (percent / (self.height - 5) * self.height + 5, y + self.width - 10)))


# для тестов и показа работы, в последстие удалить
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тест')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    running = True
    a = ProgressBar(screen, 100, 40, (0, 0, 255))
    clock = pygame.time.Clock()
    per = 100
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        a.draw(20, 20, per)
        per -= 1
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()