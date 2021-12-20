import pygame
import os
import sys

FPS = 50

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


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


def start_screen():
    clock = pygame.time.Clock()
    intro_text = ["'тут будет название'", ""]

    fon = pygame.transform.scale(load_image('background.jpg'), (663, 520))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    pygame.draw.rect(screen, pygame.Color(50, 50, 230), (105, 300, 300, 50), 0)
    text = font.render("Start the game!", True, (173, 216, 230))
    text_x = 180
    text_y = 315
    screen.blit(text, (text_x, text_y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 105 <= x <= 405 and 300 <= y <= 350:
                    return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()