import thorpy, pygame, random
from questions import *
from game_over import *
from random import sample
from pirate_attack import *


class PirateTest(object):
    def __init__(self, count):
        if count == 0:
            attack()
            self.test_passed = False
            self.time = 10
            self.numbers = list(sample(list(questions), 5))
            # вызов словаря в таком виде эквивалентен questions.keys()
        self.count = count
        self.label = thorpy.make_text(text=f'Вопрос №{self.count + 1}',
                                      font_color=(0, 0, 255))
        q_number = self.numbers[self.count]
        self.radioButton1 = thorpy.Checker(questions[q_number][1][0], type_="radio")
        self.radioButton2 = thorpy.Checker(questions[q_number][2][0], type_="radio")
        self.radioButton3 = thorpy.Checker(questions[q_number][3][0], type_="radio")
        self.radioButton4 = thorpy.Checker(questions[q_number][4][0], type_="radio")
        self.checkButton = thorpy.make_button("Проверить", func=self.check)
        self.e_group_menu = thorpy.make_group([self.radioButton1, self.radioButton2,
                                               self.radioButton3, self.radioButton4])
        thorpy.store(self.e_group_menu, mode='v')

        self.questionText = thorpy.make_text(text=questions[q_number][0],
                                             font_color=(0, 0, 255))
        UPDATE_TIMER_EVENT = pygame.USEREVENT + 1
        self.timer = thorpy.Element(str(self.time))
        self.timer.set_font_size(50)
        self.timer.set_font_color((255, 0, 0))
        self.timer.scale_to_text()
        pygame.time.set_timer(UPDATE_TIMER_EVENT, 1000)
        self.timer.add_reaction(thorpy.Reaction(reacts_to=UPDATE_TIMER_EVENT,
                                                reac_func=self.change_timer))
        self.e_background = thorpy.Background(color=(200, 200, 255),
                                              elements=[self.timer,
                                                        self.questionText,
                                                        self.e_group_menu,
                                                        self.checkButton])
        thorpy.store(self.e_background, gap=50)

    def check(self):
        q_number = self.numbers[self.count]
        if (self.radioButton1.get_value() and questions[q_number][1][1]) \
                or (self.radioButton2.get_value() and questions[q_number][2][1]) \
                or (self.radioButton3.get_value() and questions[q_number][3][1]) \
                or (self.radioButton4.get_value() and questions[q_number][4][1]):
            self.count += 1
            if self.count >= 5:
                thorpy.functions.quit_menu_func()
                self.test_passed = True
                test_passed()
                return
            else:
                self.e_background.update()
                self.e_background.blit()
                self.__init__(self.count)
                thorpy.functions.quit_menu_func()
                self.launch_game()
        else:
            thorpy.functions.quit_menu_func()
            test_failed()

    def change_timer(self, *args):
        self.time = int(self.timer.get_text()) - 1
        if self.time > 0:
            self.timer.set_text(str(self.time))
            self.timer.blit()
            self.timer.update()
        else:
            test_failed()
            thorpy.functions.quit_menu_func()

    def launch_game(self):
        menu = thorpy.Menu(self.e_background)
        menu.play()
        return self.test_passed

