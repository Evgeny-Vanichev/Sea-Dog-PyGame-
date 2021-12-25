from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys
from pirate_test_ui import Ui_MainWindow
from questions import *


class Test(QMainWindow, Ui_MainWindow, QApplication):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.count = 1
        self.label.setText(f"Вопрос № {self.count}")
        self.pushButton.clicked.connect(self.check)

    def check(self):
        if (self.radioButton.isChecked() and questions[self.count][1][1]) \
                or (self.radioButton_2.isChecked() and questions[self.count][2][1]) \
                or (self.radioButton_3.isChecked() and questions[self.count][3][1]) \
                or (self.radioButton_4.isChecked() and questions[self.count][4][1]):
            self.sender().setEnabled(False)

            self.count += 1
            if self.count == 5:
                self.close()
            self.label_2.setText(questions[self.count][0])
            self.radioButton.setText(questions[self.count][1][0])
            self.radioButton_2.setText(questions[self.count][2][0])
            self.radioButton_3.setText(questions[self.count][3][0])
            self.radioButton_4.setText(questions[self.count][4][0])
        else:
            sys.exit()
