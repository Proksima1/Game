from SpriteController import *

pygame.mixer.init()


class Item(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], filename: str):
        pygame.sprite.Sprite.__init__(self)
        self.image = (pygame.image.load(filename))
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = self.rect.x
        self.y = self.rect.y
        self.screen = screen
        self.picked = False

    def pickup(self, player: Player_ship):
        if pygame.sprite.collide_mask(self, player):
            self.picked = True
            self.__del__()
            return True
        return False

    def __del__(self):
        try:
            del self.image
            del self.rect
            del self.mask
        except AttributeError:
            pass


class Coin(Item):
    filename = '../sprites/items/coin/coin.png'

    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], player: Player_ship):
        super().__init__(screen, pos, Coin.filename)
        self.player = player
        self.coin_amount = coin_amount
        self.pick_sound = pygame.mixer.Sound('../sounds/pickcoin/pick.mp3')

    def update(self):
        try:
            self.screen.blit(self.image, self.rect)
            if self.pickup(self.player) and self.picked:
                self.player.coins_count += self.coin_amount
                self.pick_sound.play()
                self.pick_sound.set_volume(0.1)
                return True
            return False
        except AttributeError:
            pass


class Heal(Item):
    filename = ''

    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], player: Player_ship):
        super().__init__(screen, pos, Heal.filename)
        self.player = player
        self.heal_amount = heal_amount

    def update(self):
        try:
            self.screen.blit(self.image, self.rect)
            if self.pickup(self.player) and self.picked:
                self.player.hp += self.heal_amount
                return True
            return False
        except AttributeError:
            pass


def plus(count):
    font = pygame.font.Font(font_path, 40)
    text = font.render(f'{count}', True, (255, 0, 0))
    screen.blit(text, pygame.Rect((80, 80), (90, 90)))


if __name__ == '__main__':
    pygame.init()
    size = width, height = size
    screen = pygame.display.set_mode(size)
    running = True
    pl = Player_ship(screen, 32, 32)
    clock = pygame.time.Clock()
    cont = SpriteController(screen)
    cont.append(pl)
    coin = Coin(screen, (200, 200), pl)
    coin1 = Coin(screen, (400, 400), pl)
    counting = 0
    while running:
        moving = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pl.shoot()
        if coin.update():
            counting += coin_amount
        if coin1.update():
            counting += coin_amount
        plus(counting)
        if moving[pygame.K_LEFT] or moving[pygame.K_a]:
            pl.left()
        if moving[pygame.K_RIGHT] or moving[pygame.K_d]:
            pl.right()
        if moving[pygame.K_UP] or moving[pygame.K_w]:
            pl.up()
        if moving[pygame.K_DOWN] or moving[pygame.K_s]:
            pl.down()
        cont.draw_all()
        # pl.draw_shoot(a.en_cont.get_enemies())
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
