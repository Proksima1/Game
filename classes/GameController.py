import pygame
import threading
from fregate import Player_ship, Enemy_ship

if __name__ == '__main__':
    pygame.init()
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    a = Player_ship(screen, 32, 32, '../sprites/fregate/player/player_ship.png')
    b = Player_ship(screen, 350, 320, '../sprites/fregate/enemy/enemy_ship1.png')
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
        a.make_a_ship()
        a.draw_shoot()
        b.make_a_ship()
        b.random_move()
        #pygame.draw.rect(screen, 'red', a.rect)
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
