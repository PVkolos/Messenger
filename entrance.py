from hashlib import sha256
import requests

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import main
from SETTINGS import URL


class Avtoriz(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/avt_reg.ui', self).setFixedSize(1374, 866)
        self.pushButton.clicked.connect(self.reg)
        self.pushButton_2.clicked.connect(self.avt)
        self.label_3.setAutoFillBackground(True)
        self.label_4.setAutoFillBackground(True)

    def reg(self):
        """  регистрация пользователя в мессенджере  """
        try:
            r = requests.post(f'{URL}add_user',
                              json={'name': self.lineEdit_3.text(), 'password': self.lineEdit_4.text()})
        except Exception:
            self.label_3.setText('Ошибка сервера, попробуйте позднее!')
            self.label_3.setStyleSheet("QLabel { background-color: rgba(255, 0, 0, 140); }")
            return

        if r.status_code == 500:
            self.label_3.setText('Пользователь с таким именем уже существует!')
            self.label_3.setStyleSheet("QLabel { background-color: rgba(255, 0, 0, 140); }")
        elif r.status_code != 200:
            print(f'Статус код сервера: {r.status_code}')
            return
        else:
            f = open('Разное/name.txt', 'w')
            f.write(self.lineEdit_3.text())
            f.close()
            self.second_form = main.Main()
            self.second_form.show()
            self.hide()

    def avt(self):
        """  вход в аккаунт, проверка данных на валидность и верность  """
        try:
            r = requests.get(f'{URL}users')
        except Exception:
            self.label_4.setText('Ошибка сервера, попробуйте позднее!')
            self.label_4.setStyleSheet("QLabel { background-color: rgba(255, 0, 0, 140); }")
            return
        for el in r.json()['users']:
            password = sha256(self.lineEdit_2.text().encode('utf-8')).hexdigest()
            if el[0] in self.lineEdit.text() and el[1] == password:
                f = open('Разное/name.txt', 'w')
                f.write(self.lineEdit.text())
                f.close()
                self.second_form = main.Main()
                self.second_form.show()
                self.hide()
                return
        self.label_4.setText('Неверный логин или пароль!')
        self.label_4.setStyleSheet("QLabel { background-color: rgba(255, 0, 0, 140); }")