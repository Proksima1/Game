from fregate import *


class SpriteController:
    def __init__(self, screen: pygame.Surface):
        """Класс, отвечающий за обработку, и прорисовку всех спрайтов."""
        self.screen = screen
        self.sprites = []

    def append(self, value):
        """Добавляет значение в список."""
        self.sprites.append(value)

    def draw_all(self):
        """Рисует все спрайты с проверками."""
        for sprite in self.sprites:
            if sprite.hp <= 0:  # проверка для врага и игрока
                sprite.dead = True  # меняем значение dead на True
                sou = sprite.exp  # получаем звук взрыва
                channel.play(sou)  # проигрываем звук
                del self[sprite]  # удаляем спрайт
            elif isinstance(sprite, Enemy_ship):
                sprite.update_bar()  # если этот спрайт враг, обновляем бар
            elif isinstance(sprite, Player_ship):
                # если этот спрайт игрок, рисует частицы и обновляем бар с хп
                sprite.draw_heart()
                sprite.make_a_particle()
            elif isinstance(sprite, Item) and sprite.picked:
                # если этот спрайт предмет, и он взят, удаляем из списка
                del self[sprite]
            # блитим этот спрайт на экран
            self.screen.blit(sprite.image, sprite.rect)

    def __delitem__(self, key):
        """Удаление спрайта из списка спрайтов."""
        del self.sprites[self[key]]

    def __getitem__(self, item):
        """Возвращает индекс элемента из списка."""
        return self.sprites.index(item)

    def __len__(self):
        """Возвращает длину списка."""
        return len(self.sprites)

    def __bool__(self):
        """Возвращает True если длина списка не 0, иначе False."""
        return True if self.sprites else False

    def __repr__(self):
        """Форматирует вывод."""
        return f'<Sprite controller: {self.sprites}>'
