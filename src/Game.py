import ast
import os
import time


class Game:
    chat_id = 0
    number = 0
    users = []
    isActive = False

    def __init__(self, chat_id=0, number=0):
        if chat_id:
            d = read_game(chat_id)
            if d:
                self.chat_id = int(d['chat_id'])
                self.number = int(d['number'])
                self.users = list(map(dict, d['users']))
                self.isActive = bool(d['isActive'])
            else:
                self.chat_id = chat_id
                self.number = 0
                self.users = []
                self.isActive = False
        else:
            self.number = number

    def set_id_chat(self, chat_id):
        self.chat_id = chat_id

    def is_active(self):
        return self.isActive

    def get_users_list(self):
        return self.users

    def activate(self):
        '''
            isActive = True and save()
        '''
        self.isActive = True
        self.save()

    def deactivate(self):
        '''
            isActive = False
            clear data
            and save()
        '''
        self.isActive = False
        self.users = []
        self.number = 0
        self.save()

    def add_user(self, user_id, user_name):
        self.number += 1
        user = {
            'id': user_id,
            'name': user_name
        }
        self.users.append(user)

    def get_message_text(self):
        user_names = [str('<b>'+u['name']+'</b>') for u in self.users]
        user_str = ', '.join(user_names)
        return 'Зареєстровано <b>{n}</b>\n{user_text}'.format(n=self.number, user_text=user_str)

    def save(self):
        data = {
            "chat_id": self.chat_id,
            "number": self.number,
            "users": self.users,
            "isActive": self.isActive
        }
        name = str(self.chat_id)
        with open(f'src/data/{name}.txt', 'w') as f:
            f.write(str(data))

    def isUser(self, id):
        rez = False
        if self.chat_id != 0:
            d = read_game(self.chat_id)
            l = list(map(dict, d['users']))
            for item in l:
                if item['id'] == id:
                    rez = True
                    break

        return rez

    def get_users(self):
        users_str = ''
        for user in self.users:
            users_str += f'<a href="tg://user?id={user["id"]}">{user["name"]}</a>\n'
        return users_str


def read_game(chat_id):
    data = ''
    if os.path.exists(f'src/data/{chat_id}.txt'):
        with open(f'src/data/{chat_id}.txt', 'r') as f:
            data = f.read()
        data = ast.literal_eval(data)
    return data
