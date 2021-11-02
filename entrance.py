from hashlib import sha256
import requests

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import main


class Avtoriz(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/avt_reg.ui', self).setFixedSize(1374, 866)
        self.pushButton.clicked.connect(self.reg)
        self.pushButton_2.clicked.connect(self.avt)
        self.label_3.setAutoFillBackground(True)
        self.label_4.setAutoFillBackground(True)

    def reg(self):
        try:
            r = requests.post('http://127.0.0.1:5000/add_user',
                              json={'name': self.lineEdit_3.text(), 'password': self.lineEdit_4.text()})
        except Exception as e:
            print('Ошибка сервера, попробуйте позднее!', e)
            return

        if r.status_code == 500:
            self.label_3.setText('Пользователь с таким именем уже существует!')
            self.label_3.setStyleSheet("QLabel { background-color: rgba(255, 0, 0, 140); }")
        elif r.status_code != 200:
            print(f'Статус код сервера: {r.status_code}')
            return
        else:
            f = open('name.txt', 'w')
            f.write(self.lineEdit_3.text())
            f.close()
            self.second_form = main.Main()
            self.second_form.show()
            self.hide()

    def avt(self):
        r = requests.get(f'http://127.0.0.1:5000/users')
        for el in r.json()['users']:
            password = sha256(self.lineEdit_2.text().encode('utf-8')).hexdigest()
            if el[0] in self.lineEdit.text() and el[1] == password:
                f = open('name.txt', 'w')
                f.write(self.lineEdit.text())
                f.close()
                self.second_form = main.Main()
                self.second_form.show()
                self.hide()
                return
        self.label_4.setText('Неверный логин или пароль!')
        self.label_4.setStyleSheet("QLabel { background-color: rgba(255, 0, 0, 140); }")
