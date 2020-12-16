import pygame


class Button:
    def __init__(self, screen, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (23, 204, 58)
        self.active_color = (13, 162, 58)
        self.screen = screen

    def draw(self, x: int, y: int, message: str, action=None):
        button = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(self.screen, self.active_color, button)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if button.collidepoint(mouse):
            pygame.draw.rect(self.screen, self.inactive_color, (x, y, self.width, self.height))
            if click[0] == 1:
                pygame.time.delay(150)
                if action is not None:
                    pygame.time.delay(150)
                    action()
        font = pygame.font.Font(None, self.width // len(message) + 5)
        text = font.render(message, True, (255, 0, 0))
        self.screen.blit(text, ((x + self.width / 2) - text.get_width() / 2,
                                (y + self.height / 2) - font.get_height() / 2))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тест')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    running = True
    a = Button(screen, 200, 50)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        a.draw(40, 40, 'HELLO')
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()