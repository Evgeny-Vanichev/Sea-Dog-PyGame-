import csv

import pygame.event

from pirate_test import *
import thorpy
from start_screen import *
from transfer import *
from level_completed import *

FPS = 50
# Предварительная инициализация pygame
pygame.init()
SIZE = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


def terminate():
    # save_items()
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    player_x, player_y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile('empty', x, y)
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                player_x, player_y = x, y
            elif level[y][x] in '123456789':
                create_npc(level[y][x], x, y)
    new_player = Player(1, 7, player_x, player_y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def generate_sea_map(level):
    new_player = None
    for obj in level:
        obj_type, x, y = level[obj]
        if obj_type == 'player':
            new_player = Player(1, 1, x // 50, y // 50)
        else:
            Tile(obj_type, x // 50, y // 50)
    return new_player


def create_npc(number, x, y):
    """NPC(level[y][x], x, y)"""
    con = sqlite3.connect("data/npc/npc.db")
    npc_type = con.cursor().execute(
        f"""SELECT function FROM functions
            WHERE id == {number}""").fetchone()[0]
    if npc_type == 'merchant':
        Merchant(number, x, y)
    elif npc_type == 'buyer':
        Buyer(number, x, y)
    else:
        NPC(number, npc_type, x, y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(walls_group, tiles_group, all_sprites)
        elif tile_type == 'island':
            super().__init__(island_group, tiles_group, all_sprites)
        elif tile_type == 'pirate':
            super().__init__(pirate_group, tiles_group, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, columns, rows, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.delta = 5
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dx = 0
        self.left = True
        self.moving = False
        self.change_image(columns, rows)
        self.rect = self.image.get_rect().move(tile_width * self.pos_x, tile_height * self.pos_y)
        self.rect = self.rect.move((tile_width - self.rect.width) // 2, 0)

    def change_image(self, columns, rows):
        self.frames = []
        self.cut_sheet(player_image, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * self.pos_x, tile_height * self.pos_y)
        self.rect = self.rect.move((tile_width - self.rect.width) // 2, 0)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.moving:
            self.delta = (self.delta + 1) % 5
            if self.delta == 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.left = True
                self.turn_over(self.dx)

    def turn_over(self, dx):
        if dx == 0:
            return
        if dx < 0:
            if not self.left:
                self.image = pygame.transform.flip(self.image, True, False)
                self.left = True
                return
        else:
            if self.left:
                self.image = pygame.transform.flip(self.image, True, False)
                self.left = False

    def move(self, dx, dy):
        self.dx = dx
        self.pos_x += dx
        self.pos_y += dy
        self.rect = self.rect.move(dx * tile_width, dy * tile_height)
        self.moving = (dx, dy) != (0, 0)
        try:
            if not (level_0 <= self.pos_x <= level_x and level_0 <= self.pos_y <= level_y):
                raise IndexError
            if pygame.sprite.spritecollideany(self, walls_group):
                raise IndexError
        except IndexError:
            self.rect = self.rect.move(-dx * tile_width, -dy * tile_height)
            self.pos_x -= dx
            self.pos_y -= dy


def draw_text(text, x, y, foreground=(255, 255, 255), background=(0, 0, 0), surface=screen):
    font = pygame.font.Font(None, 20)
    text = font.render(text, True, foreground)

    text_w = text.get_width()
    text_h = text.get_height()
    if background is not None:
        pygame.draw.rect(surface, background,
                         (x, y,
                          text_w + 10,
                          text_h + 10), 0)
    surface.blit(text, (x + 5, y + 5))


def create_button(text, func, surface, h_w=(80, 30), align=('right', 0.1)):
    button = thorpy.Clickable(text)
    painter = thorpy.painters.optionnal.human.Human(size=h_w,
                                                    radius_ext=0.5,
                                                    radius_int=0.4,
                                                    border_color=(95, 45, 30),
                                                    color=(255, 220, 130))
    button.set_painter(painter)
    button.finish()
    button.set_font_color_hover((95, 45, 30))
    button.user_func = func
    button.surface = surface
    if align[0] == 'right':
        x = WIDTH * 0.75
    else:
        x = WIDTH * 0.25
    button.set_center((x, HEIGHT * align[1] + h_w[1] // 2))
    button.blit()
    button.update()

    return button


def create_box(elements):
    box = thorpy.Box(elements)
    box.set_size((WIDTH * 0.75, 40))
    box.set_main_color((255, 220, 130, 120))
    return box


def get_good_info(good):
    con = sqlite3.connect(f"data/cities/{current_city}/price_list.db")
    result = con.cursor().execute(
        f"""SELECT * FROM goods
            WHERE name == '{good}'""").fetchall()
    if not result:
        return ["Ничего", "1шт", "0"]
    return [str(x) for x in list(*result)]


class NPC(pygame.sprite.Sprite):
    def __init__(self, npc_number, npc_type, pos_x, pos_y):
        super().__init__(all_sprites, Npc_group)
        self.flag = True
        self.number = npc_number
        self.npc_type = npc_type
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = load_image(f'npc/npc{npc_number}.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + (50 - self.image.get_width()) // 2,
            tile_height * pos_y + (50 - self.image.get_height()) // 2)
        self.text_ok = "ОК"
        self.text_bye = "Пока"

    def get_line(self):
        filename = f"data/npc/{self.npc_type}.txt"
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r', encoding='utf-8') as mapFile:
            lines = [line.strip() for line in mapFile]
        return random.choice(lines)

    def intro_dialog(self):
        self.flag = True
        line = self.get_line()
        screen2 = pygame.Surface((WIDTH, HEIGHT * 0.5))
        screen2.fill((250, 230, 180))
        font = pygame.font.Font(None, 25)
        text = font.render(line, True, (0, 0, 0))
        text_x = (WIDTH - text.get_width()) // 2
        text_y = HEIGHT * 0.1
        screen2.blit(text, (text_x, text_y))

        btn_open = create_button(self.text_ok, self.special_function, screen2, align=('left', 0.4))
        btn_quit = create_button(self.text_bye, self.finish_dialog, screen2, align=('right', 0.4))

        screen.blit(screen2, (0, 0))
        while self.flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                btn_open.react(event)
                btn_quit.react(event)
                screen.blit(screen2, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)

    def finish_dialog(self):
        self.flag = False

    def special_function(self):
        self.finish_dialog()


class Merchant(NPC):
    def __init__(self, npc_number, pos_x, pos_y):
        super().__init__(npc_number, "merchant", pos_x, pos_y)
        self.money_left = None
        self.con_taisia_db = sqlite3.connect(
            'data/login_db.db')  # !!! ТУТ НУЖНО УКАЗАТЬ СВОЙ ПУТЬ ДО login_db.db
        self.cur_taisia_db = self.con_taisia_db.cursor()
        self.text_ok = "Магазин"
        self.inserters = []
        f = open(f'data/cities/{current_city}/{self.number}_shop.txt', encoding='utf-8')
        self.shop = f.read().split('\n')
        f.close()

    def open_shop(self):
        screen2 = pygame.Surface((WIDTH, HEIGHT))
        screen2.fill((250, 230, 180))
        elements = []
        self.inserters = []
        line = ["Название:", "количество:", "стоимость:", "  купить:"]
        text = thorpy.OneLineText(''.join(map(lambda x: x.ljust(12, ' '), line)))
        text.set_font('consolas')
        elements.append(create_box([text]))
        for i, good in enumerate(self.shop, start=1):
            line = get_good_info(good)
            text1 = thorpy.OneLineText(''.join(map(lambda x: x.ljust(12, ' '), line)))
            text1.set_font('consolas')
            inserter = thorpy.Inserter(value="0")
            box = create_box([text1, inserter])
            elements.append(box)
            thorpy.store(box, mode="h")
            self.inserters.append(inserter)

        coin_image = thorpy.Image(path="data/icons/coin.png")
        coin_image.set_topleft((5, 5))
        coin_image.blit()
        coin_image.update()

        self.money_left = \
            self.cur_taisia_db.execute(
                f"SELECT money FROM users WHERE name='{current_player}'").fetchone()[0]
        self.money_text = thorpy.make_text(str(self.money_left), font_size=10, font_color=(0, 0, 0))
        self.money_text.set_topleft((25, 5))
        self.money_text.blit()
        self.money_text.update()

        central_box = thorpy.Box(elements=elements)
        central_box.set_size((WIDTH * 0.8, HEIGHT * 0.7))
        central_box.set_main_color((255, 220, 130, 120))
        central_box.set_topleft((50, 50))
        central_box.add_lift()

        text_inventory = f"Места в инвентаре: {10 - sum(inventory.values())}" # by Taisia
        text_inventory = thorpy.make_text(text_inventory, font_size=10, font_color=(0, 0, 0)) # by Taisia
        text_inventory.set_topleft((25, 5)) # by Taisia
        text_inventory.blit() # by Taisia
        text_inventory.update() # by Taisia

        menu = thorpy.Menu(central_box)
        for element in menu.get_population():
            element.surface = screen2
        central_box.blit()
        central_box.update()
        btn_buy = create_button("Совершить покупку", self.purchase_items,
                                screen2, (150, 30), ('left', 0.9))
        btn_quit = create_button("Отменить покупку", self.finish_dialog,
                                 screen2, (150, 30), ('right', 0.9))
        screen.blit(screen2, (0, 0))
        while self.flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                btn_quit.react(event)
                btn_buy.react(event)
                menu.react(event)
            pygame.display.flip()
            screen.blit(screen2, (0, 0))
            coin_image.blit()
            self.money_text.blit()
            text_inventory.blit()
            clock.tick(FPS)

    def purchase_items(self):
        global inventory
        temp = inventory.copy()
        total = 0
        try:
            for txt_box, good in zip(self.inserters, self.shop):
                amount = int(txt_box.get_value())
                if amount < 0:
                    raise ValueError
                if amount > 0:
                    total += int(get_good_info(good)[-1]) * amount
                    temp[good] = temp.get(good, 0) + amount

            if total > self.money_left:
                raise AttributeError
            if sum(temp.values()) > 10:
                raise IndexError
            self.money_left -= total
            self.cur_taisia_db.execute(f'UPDATE users SET money=? WHERE name="{current_player}"',
                                       (self.money_left,))
            self.con_taisia_db.commit()
            inventory = temp.copy()
            # save_items()
        except ValueError:
            thorpy.launch_blocking_alert(title="Ошибка!",
                                         text="Некорректные данные! Попробуйте снова",
                                         parent=None,
                                         ok_text="Я больше так не буду!")
            return
        except AttributeError:
            thorpy.launch_blocking_alert(title="Ошибка!",
                                         text="У вас недостаточно денег!",
                                         parent=None,
                                         ok_text="Я больше так не буду!")
            return
        except IndexError:
            thorpy.launch_blocking_alert(title="Ошибка!",
                                         text="Ваш корабль столько не увезёт!",
                                         parent=None,
                                         ok_text="Я больше так не буду!")
            return
        thorpy.launch_blocking_alert(title="Успех!",
                                     text=f"Покупка успешна.",
                                     parent=None,
                                     ok_text="Доставить покупки на корабль")
        self.flag = False

    def special_function(self):
        self.open_shop()


class Buyer(NPC):
    def __init__(self, npc_number, pos_x, pos_y):
        super().__init__(npc_number, "buyer", pos_x, pos_y)
        self.text_ok = "Магазин"
        self.inserters = []
        self.shop = list(inventory.keys())

    def open_shop(self):
        global inventory
        self.shop = list(inventory.keys())
        screen2 = pygame.Surface((WIDTH, HEIGHT))
        screen2.fill((250, 230, 180))
        elements = []
        self.inserters = []
        line = ["Название:", "количество:", "стоимость:", "  купить:"]
        text = thorpy.OneLineText(''.join(map(lambda x: x.ljust(12, ' '), line)))
        text.set_font('consolas')
        elements.append(create_box([text]))
        for i, good in enumerate(self.shop, start=1):
            line = get_good_info(good)
            text1 = thorpy.OneLineText(''.join(map(lambda x: x.ljust(12, ' '), line)))
            text1.set_font('consolas')
            slider = thorpy.SliderX(40, (0, inventory[good]),
                                    type_=int, initial_value=0)

            box = create_box([text1, slider])
            elements.append(box)
            thorpy.store(box, mode="h")
            self.inserters.append(slider)

        coin_image = thorpy.Image(path="data/icons/coin.png")
        coin_image.set_topleft((5, 5))
        coin_image.blit()
        coin_image.update()

        self.con_taisia_db = sqlite3.connect(
            'data/login_db.db')  # !!! ТУТ НУЖНО УКАЗАТЬ СВОЙ ПУТЬ ДО login_db.db
        self.cur_taisia_db = self.con_taisia_db.cursor()
        self.money_left = \
            self.cur_taisia_db.execute(
                f"SELECT money FROM users WHERE name='{current_player}'").fetchone()[0]
        self.money_text = thorpy.make_text(str(self.money_left), font_size=10, font_color=(0, 0, 0))
        self.money_text.set_topleft((25, 5))
        self.money_text.blit()
        self.money_text.update()

        central_box = thorpy.Box(elements=elements)
        central_box.set_size((WIDTH * 0.8, HEIGHT * 0.7))
        central_box.set_main_color((255, 220, 130, 120))
        central_box.set_topleft((50, 50))
        central_box.add_lift()

        menu = thorpy.Menu(central_box)
        for element in menu.get_population():
            element.surface = screen2
        central_box.blit()
        central_box.update()
        btn_buy = create_button("Совершить продажу", self.sell_items,
                                screen2, (150, 30), ('left', 0.9))
        btn_quit = create_button("Отменить продажу", self.finish_dialog,
                                 screen2, (150, 30), ('right', 0.9))
        screen.blit(screen2, (0, 0))
        while self.flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                btn_quit.react(event)
                btn_buy.react(event)
                menu.react(event)
            pygame.display.flip()
            screen.blit(screen2, (0, 0))
            coin_image.blit()  # by Taisia
            self.money_text.blit()  # by Taisia
            clock.tick(FPS)

    def sell_items(self):
        global inventory

        temp = inventory.copy()
        total = 0

        try:
            for txt_box, good in zip(self.inserters, self.shop):
                amount = int(txt_box.get_value())
                if amount < 0:
                    raise ValueError
                if amount > 0:
                    total += int(get_good_info(good)[-1]) * amount
                    temp[good] = temp.get(good, 0) - amount
                    if temp[good] == 0:
                        del temp[good]

            self.money_left += total
            self.cur_taisia_db.execute(f'UPDATE users SET money=? WHERE name="{current_player}"',
                                       (self.money_left,))
            self.con_taisia_db.commit()
            inventory = temp.copy()
            # save_items()
        except ValueError:
            thorpy.launch_blocking_alert(title="Ошибка!",
                                         text="Некорректные данные! Попробуйте снова",
                                         parent=None,
                                         ok_text="Я больше так не буду!")
            return
        thorpy.launch_blocking_alert(title="Успех!",
                                     text=f"Продажа успешна!",
                                     parent=None,
                                     ok_text="Отослать товары с корабля")
        self.flag = False

    def special_function(self):
        self.open_shop()


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target, ignore_borders=False):
        if ignore_borders or 4 < target.pos_x < level_x - 4:
            self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        if ignore_borders or 4 < target.pos_y < level_y - 4:
            self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def enter_city(time):
    set_configuration("city")

    global player, level_0, level_x, level_y

    level_0 = 0
    level = load_level('cities/' + current_city + '/city.txt')
    player, level_x, level_y = generate_level(level)
    PLAYER_MOVE_EVENT = pygame.USEREVENT + 1
    move_x, move_y = 0, 0

    image = load_image("icons/inv_button.png")
    screen.blit(image, (440, 5))

    pygame.time.set_timer(PLAYER_MOVE_EVENT, 150)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and move_x != -1:
                    move_x = -1
                    player.move(move_x, move_y)
                    pygame.time.set_timer(PLAYER_MOVE_EVENT, 150)
                elif event.key == pygame.K_RIGHT and move_x != 1:
                    move_x = 1
                    player.move(move_x, move_y)
                    pygame.time.set_timer(PLAYER_MOVE_EVENT, 150)
                elif event.key == pygame.K_UP and move_y != -1:
                    move_y = -1
                    player.move(move_x, move_y)
                    pygame.time.set_timer(PLAYER_MOVE_EVENT, 150)
                elif event.key == pygame.K_DOWN and move_y != 1:
                    move_y = 1
                    player.move(move_x, move_y)
                    pygame.time.set_timer(PLAYER_MOVE_EVENT, 150)
                elif event.key == pygame.K_SPACE:
                    for sprite in Npc_group:
                        if not isinstance(sprite, NPC):
                            continue
                        if abs(sprite.pos_x - player.pos_x) <= 1 and abs(
                                sprite.pos_y - player.pos_y) <= 1:
                            sprite.intro_dialog()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    move_x = 0
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    move_y = 0
            elif event.type == PLAYER_MOVE_EVENT:
                player.move(move_x, move_y)
        player.update()
        if player.pos_y == level_y:
            return time

        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        for sprite in Npc_group:
            if not isinstance(sprite, NPC):
                continue
            if abs(sprite.pos_x - player.pos_x) <= 1 and abs(sprite.pos_y - player.pos_y) <= 1:
                draw_text('нажмите space для диалога',
                          sprite.rect.x - tile_width // 2,
                          sprite.rect.y - tile_height // 2)

        font = pygame.font.Font(None, 15)
        text = font.render('%02d:%02d' % ((time // 1000) // 60, (time // 1000) % 60),
                           True, (0, 0, 0))
        text_x = 20
        text_y = 30
        screen.blit(text, (text_x, text_y))
        time += clock.tick(FPS)
        pygame.display.flip()


def set_configuration(param):
    global player_group
    global Npc_group
    global tiles_group
    global island_group
    global all_sprites
    global walls_group
    global pirate_group

    global tile_images
    global player_image

    if param == "sea":
        screen.fill((153, 217, 234))
        tile_images = {
            'pirate': load_image('icons/pirate_water.png'),
            'empty': load_image('icons/sea_tile.png'),
            'island': load_image('icons/road.png')
        }
        player_image = load_image('icons/ship.png')
        all_sprites = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        island_group = pygame.sprite.Group()
        Npc_group = pygame.sprite.Group()
        walls_group = pygame.sprite.Group()
        pirate_group = pygame.sprite.Group()

    elif param == "city":
        Npc_group = pygame.sprite.Group()
        tile_images['wall'] = load_image('icons/house.png')
        tile_images['empty'] = load_image('icons/road.png')
        player_image = load_image('icons/player_sheet.png')


def sea_travel(level_number):
    global current_city
    global level_0, level_x, level_y
    level_0 = -float("inf")
    level_x = float("inf")
    level_y = float("inf")

    set_configuration('sea')
    level = dict()
    time = -7900
    with open(f'data/basic_profile/sea_map_{level_number}.csv', mode='rt',
              encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for line in reader:
            obj_name, obj_type, x, y = line
            level[obj_name] = (obj_type, int(x), int(y))

    player = generate_sea_map(level)
    camera = Camera()
    running = True

    image = load_image("icons/inv_button.png") # Taisia вставила иконку инвентаря
    screen.blit(image, (400, 5)) # Taisia вставила иконку инвентаря

    PLAYER_MOVE_EVENT = pygame.USEREVENT + 1
    move_x, move_y = 0, 0
    pygame.time.set_timer(PLAYER_MOVE_EVENT, 150)
    global player_image
    player_image = load_image("icons/ship.png")
    player.change_image(1, 1)
    while running:
        for event in pygame.event.get():
            all_sprites.draw(screen)
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN: # Taisia вставила иконку инвентаря
                if 400 <= event.pos[0] <= 500 and 5 <= event.pos[1] <= 60: # Taisia вставила иконку инвентаря
                    return # Taisia вставила иконку инвентаря, тут надо запустить функцию из кода inventory.py
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and move_x != -1:
                    move_x = -1
                    player.move(move_x, move_y)
                    pygame.time.set_timer(PLAYER_MOVE_EVENT, 150)
                elif event.key == pygame.K_RIGHT and move_x != 1:
                    move_x = 1
                    player.move(move_x, move_y)
                    pygame.time.set_timer(PLAYER_MOVE_EVENT, 150)
                elif event.key == pygame.K_UP and move_y != -1:
                    move_y = -1
                    player.move(move_x, move_y)
                    pygame.time.set_timer(PLAYER_MOVE_EVENT, 150)
                elif event.key == pygame.K_DOWN and move_y != 1:
                    move_y = 1
                    player.move(move_x, move_y)
                    pygame.time.set_timer(PLAYER_MOVE_EVENT, 150)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    move_x = 0
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    move_y = 0
            elif event.type == PLAYER_MOVE_EVENT:
                player.move(move_x, move_y)
            if pygame.sprite.spritecollideany(player, island_group):
                current_city = ''
                for key in level:
                    if level[key] == ('island', player.pos_x * 50, player.pos_y * 50):
                        current_city = key
                        break
                level['player'] = ('player', (player.pos_x - 1) * 50, player.pos_y * 50)
                move_x = move_y = 0
            elif pygame.sprite.spritecollideany(player, pirate_group):
                test = PirateTest(0)
                if not test.launch_game():
                    con = sqlite3.connect("data/login_db.db")
                    con.cursor().execute(
                        f"""UPDATE users
                            SET money = money * 0.9
                            WHERE name = '{current_player}'""")
                    con.commit()
                    inventory.clear()
                player.move(0, -1)
                level['player'] = ('player', player.pos_x * 50, player.pos_y * 50)
                move_x = move_y = 0
            else:
                level['player'] = ('player', player.pos_x * 50, player.pos_y * 50)

        if current_city:
            transfer(current_city)
            time = enter_city(time)
            current_city = ''
            set_configuration("sea")
            player = generate_sea_map(level)
            level_0 = -float("inf")
            level_x = float("inf")
            level_y = float("inf")
            con = sqlite3.connect("data/login_db.db")
            total_money = con.cursor().execute(
                    f"SELECT money FROM users WHERE name='{current_player}'").fetchone()[
                    0]
            if total_money >= level_number ** 3 * 10000:
                level_completed(total_money, time, current_player, level_number)
                return True

        camera.update(player, ignore_borders=True)
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill((155, 215, 235))
        player.update()
        screen.blit(image, (400, 5)) # Taisia вставила иконку инвентаря
        tiles_group.draw(screen)
        player_group.draw(screen)
        font = pygame.font.Font(None, 15)
        text = font.render('X: ' + str(player.pos_x * tile_width), True, (0, 0, 0))
        text_x = 20
        text_y = 10
        screen.blit(text, (text_x, text_y))
        text = font.render('Y: ' + str(player.pos_y * tile_height), True, (0, 0, 0))
        text_x = 20
        text_y = 20
        screen.blit(text, (text_x, text_y))
        text = font.render('%02d:%02d' % ((time // 1000) // 60, (time // 1000) % 60),
                           True, (0, 0, 0))
        text_x = 20
        text_y = 30
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()
        time += clock.tick(FPS)
    pygame.quit()


def iNeedYou(event):
    global info_text
    try:
        event.el.set_font_color_hover((93, 46, 32))

        level = int(dropdownlist.get_value())
        con = sqlite3.connect("data/login_db.db")
        max_level = con.cursor().execute(
            f"""SELECT level FROM users
                WHERE name = '{current_player}'""").fetchone()[0]
        if level > max_level:
            lines = "Завершите предыдущие уровни".split()
        else:
            lines = ["Заработайте", str(int(event.el.get_value()) ** 3 * 10000), "монет"]
        lines = [x.rjust(len(lines[0]), ' ') for x in lines]
        info_text.set_text('\n'.join(map(lambda x: x.rjust(len(lines[0]) // 2, ' '), lines)))
        info_text.blit()
        info_text.update()
    except AttributeError:
        pass


def my_reaction():
    global dropdownlist, menu
    if dropdownlist.get_value() != '':
        level = int(dropdownlist.get_value())
        con = sqlite3.connect("data/login_db.db")
        max_level = con.cursor().execute(
            f"""SELECT level FROM users
                WHERE name = '{current_player}'""").fetchone()[0]
        if level > max_level:
            return
        con.cursor().execute(f"UPDATE users SET money={2000} "
                             f"WHERE name='{current_player}'")
        con.commit()
        if sea_travel(level) and level == max_level:
            con.cursor().execute(f"UPDATE users SET level={max_level + 1} "
                                 f"WHERE name='{current_player}'")
            con.commit()
        menu.play()


def basic_styling(obj):
    obj.set_font("data/icons/GorgeousPixel.ttf")
    obj.set_main_color((252, 247, 165))
    obj.set_font_size(50)
    obj.scale_to_title()
    try:
        obj.set_font_color_hover((93, 46, 32))
    except AttributeError:
        obj.set_font_color((93, 46, 32))
        obj.set_font("data/icons/GorgeousPixel.ttf")


def main_menu():
    global dropdownlist, info_text, menu
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    text = thorpy.make_text("Выбери уровень")
    basic_styling(text)

    info_text = thorpy.Element()
    info_text.set_main_color((252, 247, 165))
    info_text.set_font_size(25)
    info_text.set_font("data/icons/GorgeousPixel.ttf")
    info_text.set_size((175, 70))
    ddlist = thorpy.DropDownList(titles=[str(i) for i in range(5)])
    ddlist.set_font("data/icons/GorgeousPixel.ttf")
    ddlist.set_main_color((252, 247, 165))
    ddlist.set_font_size(40)

    dropdownlist = thorpy.DropDownListLauncher(const_text="level ",
                                               var_text="",
                                               titles=ddlist)
    dropdownlist.add_reaction(thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                              reac_func=iNeedYou,
                                              event_args={"id": thorpy.constants.EVENT_DDL}))
    basic_styling(dropdownlist)

    btn_start = thorpy.make_button("start", my_reaction)
    basic_styling(btn_start)

    background = thorpy.Background(image='data\icons\menu.png',
                                   elements=[text, dropdownlist, info_text, btn_start])
    thorpy.store(background, align="center")
    menu = thorpy.Menu(background)
    menu.play()


current_player = start_screen()
money = 0
current_city = ''
inventory = dict()
camera = Camera()
tile_width = tile_height = 50
tile_images = {
    'wall': load_image('icons/house.png'),
    'empty': load_image('icons/road.png')
}
main_menu()