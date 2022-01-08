import pygame
import os
import sys
import thorpy

FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def iNeedYou(event):
    global info_text
    try:
        event.el.set_font_color_hover((93, 46, 32))
        lines = ["Заработайте",str(int(event.el.get_value()) ** 3 * 10000),"монет"]
        lines = [x.rjust(len("Заработайте"), ' ') for x in lines]
        info_text.set_text('\n'.join(map(lambda x: x.rjust(len(lines[0]) // 2, ' '), lines)))

        info_text.blit()
        info_text.update()
    except AttributeError:
        pass


def my_reaction():
    global dropdownlist, menu
    if dropdownlist.get_value() != '':
        print(f'sea_travel level {dropdownlist.get_value()} launched')
        # sea_travel(int(dropdownlist.get_value()))
        # menu.play()


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
    global dropdownlist, info_text
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
    ddlist = thorpy.DropDownList(titles=[str(i) for i in range(1, 9)])
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

main_menu()