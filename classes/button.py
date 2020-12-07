import pygame


class Button:
    def __init__(self, screen, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (23, 204, 58)
        self.active_color = (13, 162, 58)
        self.screen = screen

    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # проверяется находится ли мышка на кнопке
        if x <= mouse[0] <= x + self.width:
            if y <= mouse[1] <= y + self.height:
                # рисование квадрата цветом наводки
                pygame.draw.rect(self.screen, self.inactive_color, (x, y, self.width, self.height))
                # если нажато по кнопке вызывается функция
                if click[0] == 1:
                    pygame.time.delay(150)
                    if action is not None:
                        pygame.time.delay(150)
                        action()
            # иначе рисуется квадрат обычного цвета
            else:
                pygame.draw.rect(self.screen, self.active_color, (x, y, self.width, self.height))
        else:
            pygame.draw.rect(self.screen, self.active_color, (x, y, self.width, self.height))
        # расчет размера текста и центрирование относительно кнопки
        font = pygame.font.Font(None, self.width // len(message) + 5)
        text = font.render(message, True, (255, 0, 0))
        self.screen.blit(text, ((x + self.width / 2) - text.get_width() / 2,
                                (y + self.height / 2) - font.get_height() / 2))
