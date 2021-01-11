import ast
import os
import time

from .database_commands import *


class Game:
    game_id = 0
    chat_id = 0
    number = 0
    users = []
    isActive = False

    def __init__(self, chat_id=0, number=0):
        if chat_id:
            if is_active_game(chat_id):
                data = select_game(chat_id)
                self.game_id = data['id']
                self.chat_id = data['chat_id']
                self.number = data['number']
                self.users = select_user_list(self.game_id)
                self.isActive = data['isActive']
            else:
                create_game(chat_id)
                data = select_game(chat_id)
                self.game_id = data['id']
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
        start_game(self.game_id)

    def deactivate(self):
        stop_game(self.game_id)

    def add_user(self, user_id, user_name):
        self.number += 1
        user = {
            'id': user_id,
            'name': user_name
        }
        self.users.append(user)
        create_user(user_id, user_name)
        insert_user_to_game(self.game_id, user_id)

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
        update_game(self.game_id, self.number, -1)


    def isUser(self, id):
        rez = False
        if self.chat_id != 0:
            d = select_user_list(self.game_id)
            print(self.game_id)
            print(d)
            for item in d:
                if item['id'] == id:
                    rez = True
                    break

        return rez

    def get_users(self):
        users_str = ''
        for user in self.users:
            users_str += f'<a href="tg://user?id={user["id"]}">{user["name"]}</a>\n'
        return users_str
