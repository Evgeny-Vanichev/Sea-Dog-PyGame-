from PyQt5.QtWidgets import QMainWindow, QApplication
import sqlite3
from login_ui import Ui_MainWindow


class Login(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.log)

    def log(self):
        con = sqlite3.connect('login_db.db')
        cur = con.cursor()
        result = cur.execute("SELECT * FROM users WHERE name=?",
                             (self.lineEdit.text(),)).fetchall()
        if not result:
            cur.execute('INSERT INTO users(score, name, level) VALUES(0,?,0)',
                        (self.lineEdit.text(),))
            con.commit()
        else:
            cur.execute('UPDATE users SET score=0, level=0 WHERE name=?',
                        (self.lineEdit.text(),))
            con.commit()
        self.close()
