import os
import ast


class WordGame:
    chat_id = 0
    users = []
    users_stat = {}
    words = []

    def __init__(self, chat_id):
        self.chat_id = chat_id
        d = read_word_game(chat_id)
        if d:
            print("WS  ", d)
            self.chat_id = int(d['chat_id'])
            self.users = list(map(dict, d['users']))
            self.users_stat = dict(d['users_stat'])
            self.words = list(map(str, d['words']))
        else:
            self.chat_id = chat_id
            self.users = []
            self.users_stat = {}
            self.words = []
            self.save()

    def set_users(self, users):
        self.users = users
        self.users_stat = {u['id']: 0 for u in users}
        self.words = []
        self.save()

    def add_word(self, word):
        self.words.append(word.lower())
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
            else:
                return 1
        else:
            return 1

    def last_word(self):
        if self.words:
            return self.words[-1]

    def get_top(self):
        users_str = ''
        for user in self.users:
            val = self.users_stat[user['id']]
            users_str += f'<a href="tg://user?id={user["id"]}">{user["name"]}</a> - {val}\n'
        return users_str

    def save(self):
        data = {
            "chat_id": self.chat_id,
            "users": self.users,
            "users_stat": self.users_stat,
            "words": self.words
        }
        name = str(self.chat_id)
        with open(f'src/data/start_games/{name}.txt', 'w') as f:
            f.write(str(data))


def read_word_game(chat_id):
    data = ''
    if os.path.exists(f'src/data/start_games/{chat_id}.txt'):
        with open(f'src/data/start_games/{chat_id}.txt', 'r') as f:
            data = f.read()
        data = ast.literal_eval(data)
    return data

