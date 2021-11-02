import requests


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
