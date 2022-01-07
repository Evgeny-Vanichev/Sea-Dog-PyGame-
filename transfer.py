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


def terminate():
    pygame.quit()
    sys.exit()


def transfer():
    global size
    global screen
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image(f'icons\\transfer\\{random.randint(1, 5)}.jpg'), (500, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 20)
    text = font.render("здесь расположены ведущие в этом мире поля и сады.", True, (0, 0, 0))
    text_x = 65
    text_y = 15
    screen.blit(text, (text_x, text_y))
    font = pygame.font.Font(None, 20)
    text = font.render("Быть может цены на растительные товары тут ниже?", True, (0, 0, 0))
    text_x = 70
    text_y = 45
    screen.blit(text, (text_x, text_y))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)
transfer()