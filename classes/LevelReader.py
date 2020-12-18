import json
from fregate import Enemy_ship
from random import randint


class LevelReader:
    def __init__(self, screen):
        self.screen = screen
        self.amount_of_enemies, self.amount_of_waves, self.max_level, self.max_speed = None, None, None, None
        self.enemies = []

    def read_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as gen:
            text = json.load(gen)
            self.amount_of_enemies = int(text[0]['amount_of_enemies'])
            self.amount_of_waves = int(text[0]['amount_of_waves'])
            self.max_level = int(text[0]['max_level'])
            self.max_speed = int(text[0]['max_speed'])
        self.enemies = [{Enemy_ship(self.screen, randint(Enemy_ship.filename.)): 1} for _ in range(self.amount_of_waves)]
        print(self.enemies)

    def draw_background(self):
        pass


if __name__ == '__main__':
    a = LevelReader()
    a.read_json('../LevelEditor/1.json')
