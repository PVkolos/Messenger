import requests

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from SETTINGS import URL
from PyQt5.QtGui import QPixmap
import main


class Set(QMainWindow):
    def __init__(self):
        """  info о сервере  """
        super().__init__()
        uic.loadUi('UI/set.ui', self)
        try:
            r = requests.get(f'{URL}users')
        except Exception:
            return

        name = ''
        for el in r.json()['users']:
            print(el, main.id2)
            if str(el[2]) == main.id2:
                name = el[0]
                self.pixmap = QPixmap(el[-1])
                self.label.setPixmap(self.pixmap)
                self.pushButton.clicked.connect(self.image)
        self.lineEdit.setText(name)
        self.pushButton_2.clicked.connect(self.nick)

    def image(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')
        self.pixmap = QPixmap(fname[0])
        self.label.setPixmap(self.pixmap)
        try:
            name = ''
            r = requests.get(f'{URL}users')
            for user in r.json()['users']:
                if str(user[2]) == main.id2:
                    name = user[0]
            r = requests.get(f'{URL}insert_users',
                             json={'path': fname[0], 'name': name})
        except Exception as e:
            print(e, 4)
            return

    def nick(self):
        try:
            self.lineEdit.setText(self.lineEdit.text())
            name = ''
            r = requests.get(f'{URL}users')
            for user in r.json()['users']:
                if str(user[2]) == main.id2:
                    name = user[0]
            r = requests.get(f'{URL}insert_users',
                             json={'name2': self.lineEdit.text(), 'name': name})
        except Exception:
            return



