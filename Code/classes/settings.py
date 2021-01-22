import os
import json
import pygame
from upgrades import *
pygame.mixer.init()  # инициализация миксера
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # путь к папке проекта
enemy_speed_level1 = 0.3  # скорость врага 1 уровня
enemy_speed_level2 = 0.8  # скорость врага 2 уровня
player_speed = 1  # скорость игрока
tile_speed = 2  # скорость пули
hp = 100  # хп игрока
enemy_level1_hp = 1000  # хп 1 уровня врага
size = (1280, 720)  # размер экрана
player_damage = 1000  # урон игрока
enemy_damage = 20  # урон врага
speed_when_driving_at_45_degrees = 1.5  # скорость движения при движении на 45 градусов
font_path = os.path.join(path, 'fonts/SuperLegendBoy-4w8Y.ttf')  # путь к шрифту
heal_amount = 20  # количество хп, которое прибавляет хил
coin_amount = (2, 10)  # количество монет, которые могут выпасть
font_size = 30  # размер шрифта
channel = pygame.mixer.Channel(1)  # канал для всех эффектов
mus_channel = pygame.mixer.Channel(1)  # канал для музыки
with open(os.path.join(path, 'data/config.json'), 'r+', encoding='utf-8') as conf:
    # открытие файла конфига
    text = json.load(conf)  # чтение файла
try:
    effects_volume = int(text[0]['effects_volume'])  # получение уровня эффектов
    music_volume = int(text[0]['music_volume'])  # получение уровня музыки
except KeyError:
    effects_volume = 100  # если нету такой переменной, устанавливается уровень эффектов
    music_volume = 100  # если нету такой переменной, устанавливается уровень эффектов
pygame.mixer.music.load("../sounds/music/mus.mp3")  # установка музыки
pygame.mixer.music.set_volume(music_volume / 100)  # установка уровня мызыки
channel.set_volume(effects_volume / 100)  # установка уровня эффектов
