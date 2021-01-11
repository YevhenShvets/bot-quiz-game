import os
import ast
from string import punctuation

from .database_commands import *


class WordGame:
    game_id = 0
    chat_id = 0
    users = []
    users_stat = {}
    words = []
    answer_id = 0

    def __init__(self, chat_id):
        self.chat_id = chat_id
        d = select_game(chat_id)
        if d:
            self.chat_id = int(d['chat_id'])
            self.game_id = int(d['id'])
            self.users = select_user_list(d['id'])
            self.users_stat = select_game_stat(d['id'])
            self.words = select_game_words(d['id'])
            self.answer_id = int(d['last_user_id'])
        else:
            self.chat_id = chat_id
            self.users = []
            self.users_stat = {}
            self.words = []
            self.answer_id = 0
            self.save()

    def set_users(self, users):
        self.users = users
        self.users_stat = {u['id']: 0 for u in users}
        self.words = []
        self.save()

    def get_next_answer_user(self, b=True):
        if not b:
            if self.answer_id == -1:
                self.answer_id = 0
        else:
            if self.answer_id == -1:
                self.answer_id = 0
            elif self.answer_id == len(self.users) - 1:
                self.answer_id = 0
            else:
                self.answer_id = self.answer_id + 1

        user = self.users[self.answer_id]
        s = f'<a href="tg://user?id={user["id"]}">{user["name"]}</a>\n'
        self.save()
        return s

    def get_answer_user_id(self):
        if self.answer_id >= 0:
            return self.users[self.answer_id]['id']
        return None

    def add_word(self, word, user_id):
        self.words.append(word.lower())
        insert_word(self.game_id, word.lower(), user_id)
        update_user_stat(self.game_id, user_id, len(word))
        self.save()

    def set_user_stat(self, id_user, stat):
        if id_user in self.users_stat.keys():
            self.users_stat[id_user] = self.users_stat[id_user] + stat
            self.save()

    def word_right(self, word):
        if self.words:
            last_word = self.words[-1].lower()
            word = word.lower()
            if word in self.words:
                return 3
            elif last_word[-1] != word[0]:
                return 2
            elif len(word) <= 2:
                return 4
            elif len_ch(word) < 2:
                return 4
            elif word[-1] in punctuation:
                return 4
            elif askiii(word) == False:
                return 4
            else:
                return 1
        else:
            if len(word) <= 2:
                return 4
            elif word[-1] in punctuation:
                return 4
            elif len_ch(word) < 2:
                return 4
            elif askiii(word) == False:
                return 4
            else:
                return 1

    def last_word(self):
        if self.words:
            return self.words[-1]

    def get_top(self):
        users_str = ''
        for user in self.users:
            val = self.users_stat[user['id']]
            users_str += f'<a href="tg://user?id={user["id"]}">{user["name"]}</a> - {val} балів\n'
        return users_str

    def save(self):
        update_game(self.game_id, len(select_user_list(self.game_id)), self.answer_id)


def askiii(word):
    for w in word:
        if 1040 <= ord(w) < 1120:
            continue
        else:
            return False
    return True


def len_ch(word):
    l = []
    for w in word:
        if w not in l:
            l.append(w)
    return len(l)
