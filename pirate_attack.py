import thorpy, pygame


def click_to_leave(event):
    thorpy.functions.quit_menu_func()


my_reaction = thorpy.Reaction(reacts_to=pygame.MOUSEBUTTONDOWN,
                              reac_func=click_to_leave)


def attack():
    text1 = thorpy.make_text("На вас напали пираты!", font_size=30,
                             font_color=(240, 105, 80))
    text2 = thorpy.make_text("Пройдите тест, чтобы спастись!", font_size=30,
                             font_color=(240, 105, 80))
    # my_gif = thorpy.AnimatedGif.make("data/pirates.gif", colorkey=None, low=2)
    background = thorpy.Background.make(image=None, elements=[text1, text2])
    background.set_main_color((145, 205, 255))
    background.add_reaction(my_reaction)
    thorpy.store(background)
    menu = thorpy.Menu(background)
    menu.play()


def test_passed():
    text1 = thorpy.make_text("Ладно, плыви дальше!", font_size=30,
                             font_color=(240, 105, 80))
    text2 = thorpy.make_text("На этот раз...", font_size=30,
                             font_color=(240, 105, 80))
    # my_gif = thorpy.AnimatedGif.make("data/pirates.gif", colorkey=None, low=2)
    background = thorpy.Background.make(image=None, elements=[text1, text2])
    background.set_main_color((145, 205, 255))
    background.add_reaction(my_reaction)
    thorpy.store(background)
    menu = thorpy.Menu(background)
    menu.play()


def test_failed():
    text1 = thorpy.make_text("Ты сам виноват дружище!", font_size=30,
                             font_color=(240, 105, 80))
    text2 = thorpy.make_text("Гони все из трюма!", font_size=30,
                             font_color=(240, 105, 80))
    text3 = thorpy.make_text("И 10% твоих монет!", font_size=30,
                             font_color=(240, 105, 80))
    #my_gif = thorpy.AnimatedGif.make("data/pirates.gif", colorkey=None, low=2)
    background = thorpy.Background.make(image=None, elements=[text1, text2, text3])
    background.set_main_color((145, 205, 255))
    background.add_reaction(my_reaction)
    thorpy.store(background)
    menu = thorpy.Menu(background)
    menu.play()
