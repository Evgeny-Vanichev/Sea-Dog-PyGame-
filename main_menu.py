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


def main_menu():
    global size
    global screen

    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    fon = pygame.transform.scale(load_image('icons\menu.png'), (500, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("data/icons/GorgeousPixel.ttf", 50)
    name = font.render("Main menu", True, (0, 0, 0))
    name_x = 125
    name_y = 120
    screen.blit(name, (name_x, name_y))
    font = pygame.font.Font("data/icons/GorgeousPixel.ttf", 30)
    text = font.render("Level 1", True, (0, 0, 0))
    text_x = 200
    text_y = 315
    screen.blit(text, (text_x, text_y))
    font = pygame.font.Font(None, 40)
    text = font.render("Соберите 1000 монет", True, (0, 0, 0))
    text_x = 120
    text_y = 250
    screen.blit(text, (text_x, text_y))
    rect = pygame.draw.rect(screen, (0, 0, 0), (193, 310, 110, 45), 5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 105 <= event.pos[0] <= 405 and 300 <= event.pos[1] <= 350:
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


main_menu()