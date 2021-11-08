import requests
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from SETTINGS import URL


class Info(QMainWindow):
    def __init__(self):
        """  info о сервере  """
        super().__init__()
        uic.loadUi('UI/info.ui', self).setFixedSize(1567, 863)
        try:
            r = requests.get(f'{URL}users')
        except Exception:
            return
        self.label_5.setText(str(r.json()['users'][-1][-1]))
        try:
            r = requests.get(f'{URL}status')
        except Exception:
            return
        time = str(datetime.fromtimestamp(r.json()['time'])).split()[1].split(':')
        time = f'{time[0]}:{time[1]}'
        self.label_6.setText(str(time))
        try:
            r = requests.get(f'{URL}messages?after=0')
        except Exception:
            return
        try:
            if r.json()['messages'][-1][0]:
                self.label_7.setText(str(r.json()['messages'][-1][0]))
            else:
                self.label_7.setText(str(0))
        except Exception:
            return

