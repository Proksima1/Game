from SpriteController import *
from fregate import *

if __name__ == '__main__':
    pygame.init()
    #pygame.mixer.init()
    size = width, height = size
    screen = pygame.display.set_mode(size)
    a = Player_ship(screen, 32, 32)
    b = Enemy_ship(screen, 350, 320)
    c = Enemy_ship(screen, 300, 320)
    cont = SpriteController(screen)
    cont.append(a)
    #cont.append(b)
    cont.append(c)
    controller = Enemy_controller(screen)
    #controller.append(b)
    controller.append(c)
    #shoot = pygame.mixer.Sound('../sounds/shoot/shoot1.wav')
    controller.update_all(a)
    running = True
    clock = pygame.time.Clock()
    while running:
        moving = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not a.dead:
                    a.shoot()
                    #shoot.play()
        if not a.dead:
            if moving[pygame.K_LEFT] or moving[pygame.K_a]:
                a.left()
            if moving[pygame.K_RIGHT] or moving[pygame.K_d]:
                a.right()
            if moving[pygame.K_UP] or moving[pygame.K_w]:
                a.up()
            if moving[pygame.K_DOWN] or moving[pygame.K_s]:
                a.down()
        cont.draw_all()
        a.draw_shoot(controller.get_enemies())
        controller.draw_bullets([a])
        pygame.display.flip()
        #pygame.display.update([i.rect for i in controller.list_of_enemies])
        #pygame.display.update(a.rect)
        screen.fill((0, 0, 0))
    pygame.quit()