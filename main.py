import sys
from hashlib import sha256
import requests

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/main.ui', self)
        self.after = 0
        self.chats = ['messeges']
        self.pushButton.clicked.connect(self.send)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_mess)
        self.timer.start(1000)
        f = open('name.txt', 'r', encoding='utf8')
        self.name = f.readline()
        f.close()
        self.label_2.setText(self.name)

    def get_mess(self):
        try:
            r = requests.get(f'http://127.0.0.1:5000/messages?after={self.after}')
        except Exception:
            return
        try:
            messages = r.json()['messages']
            self.print_m(messages)
        except Exception as e:
            print(e)

    def print_m(self, messages):
        try:
            for el in messages:
                self.textBrowser.append(el[1])
                self.textBrowser.append(el[2])
                self.textBrowser.append('')
                self.after = el[-1]
        except Exception as e:
            print(e)

    def send(self):
        try:
            r = requests.post('http://127.0.0.1:5000/send',
                              json={'text': self.textEdit.toPlainText(), 'name': self.name})
        except Exception:
            self.textBrowser.append('Ошибка сервера, попробуйте позднее!')
            self.textBrowser.append('')
            return

        if r.status_code != 200:
            print(r.status_code)
            self.textBrowser.append('Проверьте данные или поробуйте позднее!')
            self.textBrowser.append('')
            return

        self.textEdit.setText('')


class Avtoriz(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/avt_reg.ui', self)
        self.pushButton.clicked.connect(self.reg)
        self.pushButton_2.clicked.connect(self.avt)
        self.label_3.setAutoFillBackground(True)
        self.label_4.setAutoFillBackground(True)

    def reg(self):
        try:
            r = requests.post('http://127.0.0.1:5000//add_user',
                              json={'name': self.lineEdit_3.text(), 'password': self.lineEdit_4.text()})
        except Exception:
            print('Ошибка сервера, попробуйте позднее!')
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
            self.second_form = Main()
            self.second_form.show()
            ex.hide()


    def avt(self):
        r = requests.get(f'http://127.0.0.1:5000/users')
        for el in r.json()['users']:
            print(el)
            password = sha256(self.lineEdit_2.text().encode('utf-8')).hexdigest()
            if el[0] in self.lineEdit.text() and el[1] == password:
                f = open('name.txt', 'w')
                f.write(self.lineEdit.text())
                f.close()
                self.second_form = Main()
                self.second_form.show()
                ex.hide()
                return
        self.label_4.setText('Неверный логин или пароль!')
        self.label_4.setStyleSheet("QLabel { background-color: rgba(255, 0, 0, 140); }")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Avtoriz()
    ex.show()
    sys.exit(app.exec_())

