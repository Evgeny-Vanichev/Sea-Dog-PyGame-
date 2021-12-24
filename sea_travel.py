import pygame
import os
import sys
from qt_window import *

FPS = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 5, tile_height * pos_y + 5)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('rock', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def sea_travel():
    global all_sprites
    global player_group
    global tile_images
    global tiles_group
    global tile_width
    global tile_height
    global player_image

    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    tile_images = {
        'rock': load_image('sea_tile.png'),
        'empty': load_image('sea_tile.png')
    }
    player_image = load_image('ship.png')

    tile_width = tile_height = 50

    player = None

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()

    x, y = tile_width * 2, tile_height * 2

    player, level_x, level_y = generate_level(load_level('map.txt'))

    running = True
    while running:
        for event in pygame.event.get():
            all_sprites.draw(screen)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x -= 50
                if event.key == pygame.K_RIGHT:
                    x += 50
                if event.key == pygame.K_UP:
                    y -= 50
                if event.key == pygame.K_DOWN:
                    y += 50
                if x >= 500 and y >= 500:
                    return
            if x == -100 and y == 50:
                app = QApplication(sys.argv)
                ex = Main()
                ex.show()
                app.exec()

        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        font = pygame.font.Font(None, 15)
        text = font.render('X: ' + str(x), True, (0, 0, 0))
        text_x = 10
        text_y = 10
        screen.blit(text, (text_x, text_y))
        text = font.render('Y: ' + str(y), True, (0, 0, 0))
        text_x = 10
        text_y = 20
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()

    pygame.quit()