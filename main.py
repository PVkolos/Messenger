import sys
import requests
from datetime import datetime

from PyQt5 import uic, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtWidgets import QApplication
import entrance
from New_Messenger import Messengers
from SETTINGS import URL
from Chats import Chat
from info import Info
from settuser import Set
id2 = ''


class Main(QMainWindow):
    def __init__(self):
        """  инициализация и настройка главного окна  """
        super().__init__()
        uic.loadUi('UI/main.ui', self).setFixedSize(1567, 863)
        global id2
        self.after = 0
        self.pushButton.clicked.connect(self.send)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_mess)
        self.timer.start(1000)
        self.pushButton_2.clicked.connect(self.search)
        self.pushButton.setIcon(QIcon('Разное/Снимок.PNG'))
        self.pushButton.setIconSize(QSize(200, 200))
        self.pushButton_3.clicked.connect(self.info)
        self.pushButton_4.clicked.connect(self.set)
        f = open('Разное/name.txt', 'r', encoding='utf8')
        self.id = f.readline()
        f.close()
        id2 = self.id
        r = requests.get(f'{URL}users')
        for el in r.json()['users']:
            if str(el[2]) == self.id:
                self.label_2.setText(el[0])
        r = requests.get(f'{URL}users')
        i = 230
        for el in r.json()['users']:
            if str(el[2]) != self.id:
                self.btn = QPushButton(el[0], self)
                self.btn.setGeometry(10, i, 300, 40)
                self.btn.clicked.connect(self.ck)
                i += 50
                self.btn.setStyleSheet("""QWidget {border: 5px solid gray; border-radius: 10px; 
                                            background-color: rgb(255, 255, 255); font-size: 25px;} """)

    def info(self):
        self.pr = Info()
        self.pr.show()

    def set(self):
        self.pr = Set()
        self.pr.show()

    def search(self):
        """   поиск пользователей  """
        try:
            r = requests.get(f'{URL}users')
            text = self.lineEdit.text()
            for el in r.json()['users']:
                if str(el[2]) != self.id and text == el[0]:
                    self.new_w(str(el[2]))
        except Exception as e:
            print(e)
            return

    def ck(self):
        try:
            r = requests.get(f'{URL}users')
            for el in r.json()['users']:
                if self.sender().text() == el[0]:
                    self.new_w(str(el[2]))
        except Exception as e:
            print(e, 111)
            return

    def new_w(self, id):
        """  открытие окна личного чата  """
        a = Messengers(id, self.id)
        a.newchat()
        f = open('Разное/name.txt', 'w')
        f.write(id)
        f.close()
        self.lis = [id, self.id]
        self.lis.sort()
        nm = f'{self.lis[0]}_{self.lis[1]}'
        self.pr = Chat(nm)
        self.pr.show()

    def get_mess(self):
        """  поиск новых сообщений на сервере  """
        try:
            r = requests.get(f'{URL}users')
            for el in r.json()['users']:
                if str(el[2]) == self.id:
                    self.label_2.setText(el[0])
        except:
            pass
        try:
            r = requests.get(f'{URL}messages?after={self.after}')
        except Exception as e:
            print(e)
            return
        try:
            messages = r.json()['messages']
            self.print_m(messages)
        except Exception as e:
            print(e)

    def print_m(self, messages):
        """  отрисовка новых сообщений с сервера
             ВНИМАНИЕ, внизу плохой, но рабочий код!
        """
        try:
            for el in messages:
                time = str(datetime.fromtimestamp(el[-1])).split()[1].split(':')
                if str(el[1]) == self.id:
                    j = 40
                    self.textBrowser.append('\t\t\t\t\t\t' + time[0] + ':' + time[1])
                    for i in range(0, len(el[2]), 40):
                        if '\n' in el[2][i:j]:
                            el2 = el[2].split('\n')
                            for k in range(len(el2)):
                                if el2[k]:
                                    m = 40
                                    for n in range(0, len(el2[k]), 40):
                                        self.textBrowser.append('\t\t\t\t\t\t' + el2[k][n:m])
                                        m += 40
                        else:
                            self.textBrowser.append('\t\t\t\t\t\t' + el[2][i:j])
                            j += 40
                    self.after = el[-1]

                else:
                    name = ''
                    r = requests.get(f'{URL}users')
                    for user in r.json()['users']:
                        if user[2] == el[1]:
                            name = user[0]
                    self.textBrowser.append(name + ' ' + time[0] + ':' + time[1])
                    j = 35
                    for i in range(0, len(el[2]), 35):
                        self.textBrowser.append((el[2][i:j]).rstrip())
                        j += 40
                    self.after = el[-1]
                self.textBrowser.append('')
        except Exception as e:
            print(e, 123)

    def send(self):
        """  отправка сообщений на сервер  """
        try:
            name = ''
            r = requests.get(f'{URL}users')
            for el in r.json()['users']:
                if str(el[2]) == self.id:
                    name = el[2]
            r = requests.post(f'{URL}send',
                              json={'text': self.textEdit.toPlainText(), 'name': str(name)})
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = entrance.Avtoriz()
    ex.show()
    sys.exit(app.exec_())
