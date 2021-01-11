from .database_connect import *


def create_game(chat_id):
    cursor = database_connect.cursor()
    if is_active_game(chat_id):
        return False
    else:
        cursor.execute('INSERT INTO "Game" (chat_id, number, "isActive", last_user_id) '
                       'VALUES(%s, %s, %s, %s)', (chat_id, 0, True, 0))

        database_connect.commit()
        cursor.close()
        return True


def is_active_game(chat_id):
    cursor = database_connect.cursor()
    cursor.execute('SELECT * FROM "Game" WHERE chat_id=%s AND "isActive"=%s;', (chat_id, True))

    game = cursor.fetchall()
    cursor.close()
    if len(game) > 0:
        return True
    else:
        return False


def select_game(chat_id):
    cursor = database_connect.cursor()
    cursor.execute('SELECT id, chat_id, number, "isActive", last_user_id FROM "Game" '
                   'WHERE chat_id=%s AND "isActive"=%s ORDER BY id ASC', (chat_id, True))

    row = cursor.fetchone()
    game = {
        "id": row[0],
        "chat_id": row[1],
        "number": row[2],
        "isActive": row[3],
        "last_user_id": row[4]
    }
    cursor.close()
    return game


def select_user_list(game_id):
    cursor = database_connect.cursor()
    cursor.execute('SELECT telegram_id, full_name FROM "Users" INNER JOIN "GameUsers" ON '
                   '"Users".telegram_id="GameUsers".user_id WHERE "GameUsers".game_id=%s', (game_id,))

    results = cursor.fetchall()
    users = []
    for row in results:
        user = {
            'id': row[0],
            'name': row[1]
        }
        users.append(user)
    return users


def select_game_stat(game_id):
    cursor = database_connect.cursor()
    cursor.execute('SELECT user_id, user_stat FROM "GameUsers" WHERE game_id=%s;', (game_id,))

    results = cursor.fetchall()
    stats = {}
    for row in results:
        stats[row[0]] = row[1]
    return stats


def select_game_words(game_id):
    cursor = database_connect.cursor()
    cursor.execute('SELECT word FROM "GameWords" WHERE game_id=%s;', (game_id,))

    results = cursor.fetchall()
    words = []
    for row in results:
        words.append(row[0])
    return words


def select_last_game_user_answer(game_id):
    cursor = database_connect.cursor()
    cursor.execute('SELECT telegram_id, full_name FROM "Users" INNER JOIN "GameWords" ON'
                   '"GameWords".user_id="Users".telegram_id WHERE "GameWords".game_id=%s '
                   'ORDER BY "GameWords".id ASC;', (game_id,))

    results = cursor.fetchone()
    r = {}
    if not results: return r
    for row in results:
        r = {
            'id': row[0],
            'name': row[1]
        }
        break
    return r


def is_word(game_id, word):
    cursor = database_connect.cursor()
    cursor.execute('SELECT * FROM "GameWords" WHERE game_id=%s AND word=%s', (game_id, word))

    result = cursor.fetchall()
    if len(result) > 0:
        return True
    else:
        return False


def insert_user_to_game(game_id, user_id):
    cursor = database_connect.cursor()
    cursor.execute('INSERT INTO "GameUsers" (game_id, user_id, user_stat) VALUES(%s, %s, 0)', (game_id, user_id))

    database_connect.commit()
    cursor.close()


def insert_word(game_id, word, user_id):
    cursor = database_connect.cursor()
    cursor.execute('INSERT INTO "GameWords" (game_id, word, user_id) VALUES(%s, %s, %s)',
                   (game_id, word, user_id))

    database_connect.commit()
    cursor.close()


def create_user(user_id, full_name):
    cursor = database_connect.cursor()
    cursor.execute('INSERT INTO "Users" (telegram_id, full_name) VALUES(%s, %s) '
                   'ON CONFLICT (telegram_id) DO NOTHING;', (user_id, full_name))

    database_connect.commit()
    cursor.close()


def update_user_stat(game_id, user_id, value):
    cursor = database_connect.cursor()
    cursor.execute('UPDATE "GameUsers" SET user_stat=user_stat+%s WHERE game_id=%s AND user_id=%s;',
                   (value, game_id, user_id))

    database_connect.commit()
    cursor.close()


def update_game(game_id, number, last_user_id):
    cursor = database_connect.cursor()
    cursor.execute('UPDATE "Game" SET number=%s, last_user_id=%s WHERE id=%s', (number, last_user_id, game_id))

    database_connect.commit()
    cursor.close()


def start_game(game_id):
    cursor = database_connect.cursor()
    cursor.execute('UPDATE "Game" SET "isActive"=true WHERE id=%s', (game_id,))

    database_connect.commit()
    cursor.close()


def stop_game(game_id):
    cursor = database_connect.cursor()
    cursor.execute('UPDATE "Game" SET "isActive"=%s WHERE id=%s', (False, game_id,))

    database_connect.commit()
    cursor.close()



