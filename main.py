import sys
from hashlib import sha256
import requests
from datetime import datetime

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtWidgets import QApplication
name2 = ''


class Chat(QMainWindow):
    def __init__(self, nm):
        super().__init__()
        uic.loadUi('UI/chat.ui', self)
        self.after = 0
        f = open('name.txt', 'r', encoding='utf8')
        self.nm = nm
        self.name = f.readline()
        f.close()
        self.label.setText(self.name)
        self.pushButton_2.clicked.connect(self.send)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_mess)
        self.timer.start(1000)

    def send(self):
        self.messege = self.textEdit_2.toPlainText()
        try:
            r = requests.post('http://127.0.0.1:5000/send_ch',
                              json={'otpr': name2, 'messege': self.messege, 'name': self.nm})
        except Exception as e:
            print(e, 1)
            self.textBrowser.append('Ошибка сервера, попробуйте позднее!')
            self.textBrowser.append('')
            return
        if r.status_code != 200:
            print(r.status_code, '1')
            self.textBrowser.append('Проверьте данные или поробуйте позднее!')
            self.textBrowser.append('')
            return
        self.textEdit_2.setText('')

    def get_mess(self):
        try:
            r = requests.get(f'http://127.0.0.1:5000/get_messages?after={self.after}',
                             json={'name': self.nm})
        except Exception as e:
            print(e)
            return
        try:
            if r:
                messages = r.json()['messages']
                self.print_m(messages)
        except Exception as e:
            print(e)

    def print_m(self, messages):
        try:
            for el in messages:
                time = str(datetime.fromtimestamp(el[-1])).split()[1].split(':')
                if el[0] == name2:
                    self.textBrowser.append('\t\t\t\t\t\t\t\t\t' + time[0] + ':' + time[1])
                    self.textBrowser.append('\t\t\t\t\t\t\t\t\t' + el[1])
                    self.textBrowser.append('')
                    self.after = el[-1]
                else:
                    self.textBrowser.append(time[0] + ':' + time[1])
                    self.textBrowser.append(str(el[1]))
                    self.textBrowser.append('')
                    self.after = el[-1]
        except Exception as e:
            print(e)



class Messengers:
    def __init__(self, nickname_one, nickname_two):
        self.nick1 = nickname_one
        self.nick2 = nickname_two
        self.lis = [nickname_one, nickname_two]

    def newchat(self):
        try:
            r = requests.post('http://127.0.0.1:5000/add_chat',
                              json={'nickname_one': self.nick1, 'nickname_two': self.nick2})
        except Exception as e:
            print('Ошибка добваления чата', e)
            return


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/main.ui', self)
        global name2
        self.after = 0
        self.chats = ['messeges']
        self.pushButton.clicked.connect(self.send)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_mess)
        self.timer.start(1000)
        self.pushButton_2.clicked.connect(self.search)
        f = open('name.txt', 'r', encoding='utf8')
        self.name = f.readline()
        f.close()
        name2 = self.name
        self.label_2.setText(self.name)
        r = requests.get(f'http://127.0.0.1:5000/users')
        i = 200
        for el in r.json()['users']:
            if el[0] != self.name:
                self.btn = QPushButton(el[0], self)
                self.btn.setGeometry(2, i, 300, 40)
                self.btn.clicked.connect(self.ck)
                i += 50
                self.btn.setStyleSheet("""
                        QWidget {
                            border: 5px solid gray;
                            border-radius: 10px;
                            background-color: rgb(255, 255, 255);
                            font-size: 25px;
                            } """)

    def search(self):
        r = requests.get(f'http://127.0.0.1:5000/users')
        text = self.lineEdit.text()
        for el in r.json()['users']:
            if el[0] != self.name and text == el[0]:
                self.new_w(text)

    def ck(self):
        self.new_w(self.sender().text())

    def new_w(self, name):
        a = Messengers(name, self.name)
        a.newchat()
        f = open('name.txt', 'w')
        f.write(name)
        f.close()
        self.lis = [name, self.name]
        self.lis.sort()
        name = self.lis[0] + self.lis[1]
        self.pr = Chat(name)
        self.pr.show()

    def get_mess(self):
        try:
            r = requests.get(f'http://127.0.0.1:5000/messages?after={self.after}')
        except Exception as e:
            print(e)
            return
        try:
            messages = r.json()['messages']
            self.print_m(messages)
        except Exception as e:
            print(e)

    def print_m(self, messages):
        try:
            for el in messages:
                time = str(datetime.fromtimestamp(el[-1])).split()[1].split(':')
                if el[1] == self.name:
                    j = 40
                    self.textBrowser.append('\t\t\t\t\t\t\t' + time[0] + ':' + time[1])
                    for i in range(0, len(el[2]), 40):
                        self.textBrowser.append('\t\t\t\t\t\t\t' + el[2][i:j])
                        j += 40
                    self.textBrowser.append('')
                    self.after = el[-1]
                else:
                    self.textBrowser.append(el[1] + ' ' + time[0] + ':' + time[1])
                    j = 35
                    for i in range(0, len(el[2]), 35):
                        self.textBrowser.append((el[2][i:j]).rstrip())
                        j += 40
                    self.textBrowser.append('')
                    self.after = el[-1]
        except Exception as e:
            print(e)

    def send(self):
        try:
            r = requests.post('http://127.0.0.1:5000/send',
                              json={'text': self.textEdit.toPlainText(), 'name': self.name})
        except Exception as e:
            self.textBrowser.append('Ошибка сервера, попробуйте позднее!')
            self.textBrowser.append('')
            print(e)
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
            self.second_form = Main()
            self.second_form.show()
            ex.hide()

    def avt(self):
        r = requests.get(f'http://127.0.0.1:5000/users')
        for el in r.json()['users']:
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




