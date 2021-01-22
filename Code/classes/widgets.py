import pygame


class ProgressBar:
    def __init__(self, screen: pygame.Surface, color: str, x: int, y: int, width: int, height: int):
        """Класс прогресс бара"""
        self.screen = screen  # экран, на котором будет нарисован прогресс бар
        self.x = x  # позиция верхнего левого угла по x
        self.y = y  # позиция верхнего левого угла по y
        self.rect = pygame.Rect(x, y, width, height)  #
        self.height = height  # высота прогресс бара
        self.width = width  # полная ширина прогресс бара
        self.width2 = width  # нынешняя длина прогресс бара
        self.color = color  # цвет прогресс бара

    def draw(self, percent):
        if percent >= 0:  # проверка на то, что процентов больше 0
            try:
                sc = pygame.Surface((self.width2, self.height))  # создание прогресс бара
                sc.fill((255, 0, 0))  # заполнение прогресс бара красным цветом
                self.screen.blit(sc, (self.x, self.y))  # добавление прогресс бара на экран
                self.width2 = self.width / 100 * percent  # изменение длина прогресс бара
            except pygame.error:
                pass
