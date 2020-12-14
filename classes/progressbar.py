import pygame


class ProgressBar:
    def __init__(self, screen: pygame.Surface, color: str, x: int, y: int, width: int, height: int):
        self.screen = screen
        self.x = x
        self.y = y
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
           #pygame.draw.rect(self.screen, self.color, [(self.x, self.y), (self.width2, self.height)], width=1)
        #pygame.draw.rect(self.screen, self.color,
                        # [(self.x + 0.01, self.y + 0.01), (self.width * (percent / 100) - 0.01, self.height - 0.01)])


# для тестов и показа работы, в последстие удалить
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тест')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    running = True
    per = 100
    a = ProgressBar(screen, "red", 60, 100, 200, 50)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 255, 0))
        a.draw(per)
        #per -= 0.008
        pygame.display.flip()
    pygame.quit()
