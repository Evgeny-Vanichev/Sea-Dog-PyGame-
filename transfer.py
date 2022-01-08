import random

import pygame
import os
import sys

FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def transfer(city_name):
    global size
    global screen
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image(f'icons\\transfer\\{random.randint(1, 5)}.jpg'),
                                 (500, 500))
    screen.blit(fon, (0, 0))
    texts = []

    font = pygame.font.Font("data/icons/GorgeousPixel.ttf", 40)
    text = font.render(city_name, True, (0, 0, 0))
    texts.append((text, (width // 2 - text.get_width() // 2, 20)))
    font = pygame.font.Font(None, 20)

    with open(f'data/cities/{city_name}/info.txt', mode='rt', encoding='utf-8') as file:
        for i, line in enumerate(file.readlines(), start=1):
            text = font.render(line.strip('\n'), True, (0, 0, 0))
            texts.append(
                (text, (width // 2 - text.get_width() // 2, 50 + (text.get_height() + 50) * i)))

    for text, coordinates in texts:
        screen.blit(text, coordinates)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                return
        pygame.display.flip()
        clock.tick(FPS)
