import requests
from SETTINGS import URL


class Messengers:
    def __init__(self, id_one, id_two):
        self.id1 = id_one
        self.id2 = id_two
        self.lis = [id_one, id_two]

    def newchat(self):
        """  добавление нового личного чата в БД сервера  """
        try:
            requests.post(f'{URL}add_chat',
                          json={'id_one': self.id1, 'id_two': self.id2})
        except Exception as e:
            print('Ошибка добваления чата', e)
            return
