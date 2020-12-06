import pygame
from classes.fregate import Ship

if __name__ == '__main__':
    pygame.init()
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    a = Ship(screen, width, height)
    running = True
    move_delay = 3
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                a.shoot()
        moving = pygame.key.get_pressed()
        if moving[pygame.K_LEFT] or moving[pygame.K_a]:
            pygame.time.delay(move_delay)
            a.left()
        if moving[pygame.K_RIGHT] or moving[pygame.K_d]:
            pygame.time.delay(move_delay)
            a.right()
        if moving[pygame.K_UP] or moving[pygame.K_w]:
            pygame.time.delay(move_delay)
            a.up()
        if moving[pygame.K_DOWN] or moving[pygame.K_s]:
            pygame.time.delay(move_delay)
            a.down()
        for i in range(len(a.shoots)):
            velocity = 0.1
            x_pos = a.shoots[i][2]
            pygame.draw.rect(screen, 'yellow', [(int(a.shoots[i][1][0]) + velocity * x_pos, a.shoots[i][1][1]), (3, 2)])
            a.shoots[i] = [i, (a.shoots[i][1][0] + velocity * x_pos, a.shoots[i][1][1]), x_pos, 1]
            if a.shoots[i][1][0] > width:
                del(a.shoots[i])
        a.make_a_ship()
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
