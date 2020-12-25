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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not a.dead:
                    a.shoot()
                    #shoot.play()
        a.move()
        cont.draw_all()
        a.draw_shoot(controller.get_enemies())
        controller.draw_bullets([a])
        pygame.display.flip()
        #pygame.display.update([i.rect for i in controller.list_of_enemies])
        #pygame.display.update(a.rect)
        screen.fill((0, 0, 0))
    pygame.quit()