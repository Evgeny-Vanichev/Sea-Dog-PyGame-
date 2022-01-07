import pygame
from PyQt5.QtWidgets import QApplication
import os
import sys

from PyQt5.QtWidgets import QMainWindow
import sqlite3
from login_ui import Ui_MainWindow

current_player = None


class Login(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.log)

    def log(self):
        global current_player
        con = sqlite3.connect('data/login_db.db')
        cur = con.cursor()
        result = cur.execute("SELECT * FROM users WHERE name=?",
                             (self.lineEdit.text(),)).fetchall()
        if not result:
            cur.execute('INSERT INTO users(name, level, score, money) VALUES(?,0,0,10000)',
                        (self.lineEdit.text(),))
            name_id = cur.execute('SELECT id FROM users WHERE name=?',
                                  (self.lineEdit.text(),)).fetchone()
            cur.execute('INSERT INTO passwords(id, password) VALUES(?,?)',
                        (name_id[0], self.lineEdit_2.text()))
            x = cur.execute('SELECT * FROM passwords WHERE id=?',
                            (name_id[0],)).fetchall()
            print(x)
            con.commit()
            current_player = self.lineEdit.text()
            os.mkdir(f'data/{current_player}')
            path = os.path.abspath('data')
            for file in os.listdir('data/basic_profile'):
                os.system(
                    f'copy "{path}\\basic_profile\\{file}" "{path}\\{current_player}\\{file}"')
            self.close()
        else:
            password = cur.execute('SELECT password FROM passwords '
                                   'WHERE id=('
                                   'SELECT id FROM users '
                                   'WHERE name = ?)',
                                   (self.lineEdit.text(),)).fetchone()
            if str(password[0]) == self.lineEdit_2.text():
                cur.execute('UPDATE users SET score=0, level=0 WHERE name=?',
                            (self.lineEdit.text(),))
                con.commit()
                current_player = self.lineEdit.text()
                self.close()
            else:
                self.label_3.setText("Неправильный пароль")


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


def start_screen():
    global size
    global screen
    global current_player

    current_player = None

    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    fon = pygame.transform.scale(load_image('icons/background.jpg'), (663, 520))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    name = font.render("Игра <<Sea Dog>>", True, (10, 20, 80))
    name_x = 40
    name_y = 50
    screen.blit(name, (name_x, name_y))
    image = load_image("icons/big_player.png")
    screen.blit(image, (100, 100))
    font = pygame.font.Font(None, 30)
    pygame.draw.rect(screen, pygame.Color(50, 50, 230), (105, 300, 300, 50), 0)
    text = font.render("Start the game!", True, (173, 216, 230))
    text_x = 180
    text_y = 315
    screen.blit(text, (text_x, text_y))
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    login = Login()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 105 <= event.pos[0] <= 405 and 300 <= event.pos[1] <= 350:
                    login.show()  # THIS CODE WORKS!!!
                    app.exec()  # THIS CODE WORKS!!!
                    return current_player
        pygame.display.flip()
        clock.tick(FPS)


def except_hook(a, b, c):
    sys.__excepthook__(a, b, c)


start_screen()
