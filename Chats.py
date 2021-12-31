import requests
from datetime import datetime
from PIL import Image

from PyQt5 import uic, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow
import main
from SETTINGS import URL


class Chat(QMainWindow):
    def __init__(self, nm):
        """  инициализация и настройка главного окна  """
        super().__init__()
        uic.loadUi('UI/chat.ui', self).setFixedSize(1158, 844)
        self.after = 0
        f = open('Разное/name.txt', 'r', encoding='utf8')
        self.nm = nm
        self.id = f.readline()
        f.close()
        r = requests.get(f'{URL}users')
        for el in r.json()['users']:
            if str(el[2]) == self.id:
                self.label.setText(el[0])
        self.pushButton_2.clicked.connect(self.send)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_mess)
        self.timer.start(1000)
        self.pushButton_2.setIcon(QIcon('Разное/Снимок.PNG'))
        self.pushButton_2.setIconSize(QSize(300, 300))
        try:
            try:
                r = requests.get(f'{URL}users')
            except Exception:
                return
            for el in r.json()['users']:
                if str(el[2]) == self.id:
                    img = Image.open(el[-1])
                    img = img.resize((80, 50), Image.ANTIALIAS)
                    img.save('Разное/ava2.png')
                    self.pixmap = QPixmap('Разное/ava2.png')
                    self.label_3.setPixmap(self.pixmap)
                    self.pushButton.clicked.connect(self.image)
        except Exception:
            pass

    def send(self):
        """  отправка сообщений на сервер  """
        self.messege = self.textEdit_2.toPlainText()
        try:
            r = requests.post(f'{URL}send_ch',
                              json={'otpr': main.id2, 'messege': self.messege, 'name': self.nm})
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
        """  поиск новых сообщений на сервере  """
        print(1)
        try:
            r = requests.get(f'{URL}get_messages?after={self.after}',
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
        """  отрисовка новых сообщений с сервера
             ВНИМАНИЕ, внизу плохой, но рабочий код!
        """
        try:
            for el in messages:
                time = str(datetime.fromtimestamp(el[-1])).split()[1].split(':')
                if str(el[0]) == main.id2:
                    j = 40
                    self.textBrowser.append('\t\t\t\t\t\t' + time[0] + ':' + time[1])
                    for i in range(0, len(el[1]), 40):
                        if '\n' in el[1][i:j]:
                            el2 = el[1].split('\n')
                            for k in range(len(el2)):
                                if el2[k]:
                                    m = 40
                                    for n in range(0, len(el2[k]), 40):
                                        self.textBrowser.append('\t\t\t\t\t\t' + el2[k][n:m])
                                        m += 40
                        else:
                            self.textBrowser.append('\t\t\t\t\t\t' + el[1][i:j])
                            j += 40
                    self.after = el[-1]

                else:
                    self.textBrowser.append(time[0] + ':' + time[1])
                    j = 35
                    for i in range(0, len(el[1]), 35):
                        self.textBrowser.append((el[1][i:j]).rstrip())
                        j += 40
                    self.after = el[-1]
                self.textBrowser.append('')
        except Exception as e:
            print(e)
