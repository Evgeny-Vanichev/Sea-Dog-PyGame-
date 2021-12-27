from PyQt5.QtWidgets import QMainWindow
from pirate_test_ui import Ui_MainWindow
from questions import *
from game_over import *
from sea_travel import *


class Test(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.count = 0
        self.pushButton.clicked.connect(self.check)

    def check(self):
        if (self.radioButton.isChecked() and questions[self.count + 1][1][1]) \
                or (self.radioButton_2.isChecked() and questions[self.count + 1][2][1]) \
                or (self.radioButton_3.isChecked() and questions[self.count + 1][3][1]) \
                or (self.radioButton_4.isChecked() and questions[self.count + 1][4][1]):
            self.count += 1
            if self.count == 5:
                self.close()
                sea_travel()
            self.label_2.setText(questions[self.count + 1][0])
            self.radioButton.setText(questions[self.count + 1][1][0])
            self.radioButton_2.setText(questions[self.count + 1][2][0])
            self.radioButton_3.setText(questions[self.count + 1][3][0])
            self.radioButton_4.setText(questions[self.count + 1][4][0])
        else:
            self.close()
            game_over()