import requests
from datetime import datetime

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow
import main


class Chat(QMainWindow):
    def __init__(self, nm):
        super().__init__()
        uic.loadUi('UI/chat.ui', self).setFixedSize(1158, 844)
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
                              json={'otpr': main.name2, 'messege': self.messege, 'name': self.nm})
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
                if el[0] == main.name2:
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