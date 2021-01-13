import os
import json
import pygame
pygame.mixer.init()
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
enemy_speed_level1 = 0.3
enemy_speed_level2 = 0.8
player_speed = 1
tile_speed = 2
hp = 100
enemy_level1_hp = 80
size = (1280, 720)
player_damage = 1000
enemy_damage = 20
speed_when_driving_at_45_degrees = 1.5
font_path = os.path.join(path, 'fonts/SuperLegendBoy-4w8Y.ttf')
heal_amount = 20
coin_amount = (2, 10)
font_size = 30
channel = pygame.mixer.Channel(1)
with open(os.path.join(path, 'data/config.json'), 'r+', encoding='utf-8') as conf:
    text = json.load(conf)
try:
    effects_volume = int(text[0]['effects_volume'])
    music_volume = int(text[0]['music_volume'])
except KeyError:
    effects_volume = 100
    music_volume = 100
channel.set_volume(effects_volume / 100)
#print(json.loads(open('../data/save.json', 'r+', encoding='utf-8').read()))
#print(json.load(open('../data/save.json', 'r+', encoding='utf-8').read()))
