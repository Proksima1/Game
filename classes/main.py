import pygame
import threading
from fregate import Ship

if __name__ == '__main__':
    pygame.init()
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    a = Ship(screen, width, height)
    running = True
    while running:
        moving = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                a.shoot()
        if moving[pygame.K_LEFT] or moving[pygame.K_a]:
            a.left()
        if moving[pygame.K_RIGHT] or moving[pygame.K_d]:
            a.right()
        if moving[pygame.K_UP] or moving[pygame.K_w]:
            a.up()
        if moving[pygame.K_DOWN] or moving[pygame.K_s]:
            a.down()
        for i in range(len(a.shoots)):
            try:
                velocity = 0.1
                x_pos = a.shoots[i][2]
                pygame.draw.rect(screen, 'yellow',
                                 [(int(a.shoots[i][1][0]) + velocity * x_pos, a.shoots[i][1][1]), (3, 2)])
                a.shoots[i] = [i, (a.shoots[i][1][0] + velocity * x_pos, a.shoots[i][1][1]), x_pos, 1]
                if a.shoots[i][1][0] > width:
                    del (a.shoots[i])
                if a.shoots[i][1][1] >= a.enemy[0].top and a.shoots[i][1][1] <= a.enemy[0].bottom and \
                        a.shoots[i][1][0] >= a.enemy[0].left and a.shoots[i][1][0] <= a.enemy[0].right:
                    del (a.shoots[i])
            except IndexError:
                pass
        a.make_an_enemy()
        a.make_a_ship()
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
