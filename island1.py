import pygame
import os
import sys
from start_screen import start_screen
from sea_travel import *

FPS = 50
tiles_group = pygame.sprite.Group()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


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
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if not pygame.sprite.spritecollideany(self, tiles_group):
            return True



def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '=':
                Tile('road', x, y)
            elif level[y][x] == '.':
                Tile('house', x, y)
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


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
start_screen()
sea_travel()

tile_images = {
    'road': load_image('road.jpg'),
    'house': load_image('house.jpg'),
    'empty': load_image('sea_tile.png')
}
player_image = load_image('player.jpg')

tile_width = tile_height = 50

player = None

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()

x, y = tile_width * 3, tile_height * 2

player, level_x, level_y = generate_level(load_level('island_map.txt'))

running = True

camera = Camera()

while running:
    for event in pygame.event.get():
        all_sprites.draw(screen)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if player.update():
                if event.key == pygame.K_LEFT:
                    player.rect.x += 50
                if event.key == pygame.K_RIGHT:
                    player.rect.x -= 50
                if event.key == pygame.K_UP:
                    player.rect.y += 50
                if event.key == pygame.K_DOWN:
                    player.rect.y -= 50

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color("yellow"))
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