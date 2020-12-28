import os
import json

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
enemy_speed = 0.3
player_speed = 1
tile_speed = 2
hp = 100
enemy_level1_hp = 80
size = (1280, 720)
player_damage = 25
enemy_damage = 20
speed_when_driving_at_45_degrees = 1.5
font_path = os.path.join(path, 'fonts/SuperLegendBoy-4w8Y.ttf')
heal_amount = 20
coin_amount = (2, 10)
font_size = 30
with open(os.path.join(path, 'data/config.json'), 'r+', encoding='utf-8') as conf:
    text = json.load(conf)
try:
    effects_volume = int(text[0]['effects_volume'])
    music_volume = int(text[0]['music_volume'])
except KeyError:
    effects_volume = 100
    music_volume = 100
