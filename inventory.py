import pygame
import os
import sys
import csv

FPS = 50
current_player = None


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


def inventory():
    global size
    global screen
    global current_player

    current_player = None

    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    csv_file = open('data/basic_profile/inventory.csv', encoding='utf-8')
    reader = csv.reader(csv_file, delimiter=";")
    screen.fill((250, 230, 180))

    image = load_image("icons/krest.png")
    screen.blit(image, (440, 5))

    font = pygame.font.Font("data/icons/GorgeousPixel.ttf", 30)
    name = font.render("Inventory", True, (0, 0, 0))
    screen.blit(name, (190, 30))

    font = pygame.font.Font(None, 30)
    x, y = 80, 100

    for row in reader:
        text = row[0] + ": " + row[1]
        name = font.render(text, True, (0, 0, 0))
        screen.blit(name, (x, y))
        y += 100
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 440 <= event.pos[0] <= 500 and 5 <= event.pos[1] <= 60:
                    return
        pygame.display.flip()
        clock.tick(FPS)


inventory()