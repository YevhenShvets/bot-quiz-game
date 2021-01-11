import os
import json
import asyncio
import logging

import time
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from aiogram.utils.markdown import hbold, hlink, quote_html

from src.Game import Game
from src.WordGame import WordGame
from string import punctuation

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    logger.info('start/  Chat_id:' + str(chat_id) + " Name: " + str(message.from_user.full_name))
    await message.reply(f"Дай боже {hbold(message.from_user.full_name)}\n"
                        f"Я бот для ігри в слова\n/game - для реєстрації\n"
                        f"/startgame - розпочати гру\n/top - Рейтинг гравців\n"
                        f"/stopgame - закінити гру", parse_mode=types.ParseMode.HTML)


async def pre_start_game(message: types.Message):
    await message.answer("3")
    await asyncio.sleep(0.5)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text='2')
    await asyncio.sleep(0.5)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text='<b>1</b>',
                                parse_mode=types.ParseMode.HTML)
    await asyncio.sleep(0.5)
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=message.message_id + 1,
                                text='<code>Гра починається</code>',
                                parse_mode=types.ParseMode.HTML)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)


async def game_presentation(message: types.Message):
    await message.answer("<u>Гра в слова</u>\n"
                         "Приклад:\n1 грацець: <i>Україна</i>\n"
                         "2 гравець: <i>Англія</i>", parse_mode=types.ParseMode.HTML)


async def game_players(message: types.Message, game: Game):
    text = "<b>Гравці: </b>\n" + game.get_users()
    await message.answer(text=text, parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=['game'])
async def new_game(message: types.Message):
    logger.info('game/  Chat_id:' + str(message.chat.id) + " Name: " + str(message.from_user.full_name))
    g = Game(message.chat.id)
    if g.is_active():
        await message.reply("<b>Гра ще активна</b>\n/stopgame - для виходу з поточної гри",
                            parse_mode=types.ParseMode.HTML)
    else:
        g.save()
        inline_markup = types.InlineKeyboardMarkup()
        c_data = '{"message_id":' + str(message.message_id + 1) + ', "name":"add" }'
        button_in = types.InlineKeyboardButton("Приєднатись", callback_data=c_data)
        inline_markup.add(button_in)
        await message.answer(g.get_message_text(),
                             reply_markup=inline_markup,
                             parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=['startgame'])
async def start_game(message: types.Message):
    logger.info('startgame/  Chat_id:' + str(message.chat.id) +
                " Name: " + str(message.from_user.full_name))
    id_chat = message.chat.id
    g = Game(chat_id=id_chat)
    if g.get_users():
        g.activate()
        await pre_start_game(message)
        await game_presentation(message)
        w = WordGame(chat_id=id_chat)
        w.set_users(g.get_users_list())
        await game_players(message, g)
        username_link = w.get_next_answer_user()
        await message.answer(text=f'Першим ходить {username_link}', parse_mode=types.ParseMode.HTML)
    else:
        await message.reply("<b>В грі 0 гравців</b>\n/game - для реєстрації гравців",
                            parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=['stopgame'])
async def stop_game(message: types.Message):
    logger.info('stopgame/  Chat_id:' + str(message.chat.id) +
                " Name: " + str(message.from_user.full_name))
    id_chat = message.chat.id
    g = Game(chat_id=id_chat)
    if g.is_active():
        g.deactivate()
        await message.answer("<i>Активну ігру зупинено</i>", parse_mode=types.ParseMode.HTML)
    else:
        await message.reply("<i>Активної ігри не знайдено</i>", parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=['top'])
async def top_game(message: types.Message):
    logger.info('top/  Chat_id:' + str(message.chat.id) + " Name: " + str(message.from_user.full_name))
    id_chat = message.chat.id
    g = Game(chat_id=id_chat)
    if g.is_active():
        wg = WordGame(chat_id=id_chat)
        await message.answer(text=wg.get_top(), parse_mode=types.ParseMode.HTML)
    else:
        await message.reply(text="<b>Інформація відсутня</b>, так як гра не активна",
                            parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.id:
        _dict = json.loads(callback_query.data)
        logger.info("chat id: " + str(callback_query.message.chat.id))
        g = Game(chat_id=int(callback_query.message.chat.id))
        if _dict['name'] == 'add':
            if not g.isUser(callback_query.from_user.id):
                g.add_user(callback_query.from_user.id, callback_query.from_user.full_name)
                g.save()
                inline_markup = types.InlineKeyboardMarkup()
                c_data = '{"message_id":' + str(callback_query.message.message_id) + ', "name":"add"}'
                button_in = types.InlineKeyboardButton("Приєднатись", callback_data=c_data)
                inline_markup.add(button_in)

                m_id = _dict['message_id']
                await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=m_id,
                                            text=g.get_message_text(), reply_markup=inline_markup,
                                            parse_mode=types.ParseMode.HTML)

            else:
                await bot.answer_callback_query(callback_query.id, "Ви вже в грі")


@dp.message_handler()
async def check(message: types.Message):
    logger.info('message  Chat_id:' + str(message.chat.id) +
                " Name: " + str(message.from_user.full_name) + " Message: " + message.text)

    g = Game(chat_id=message.chat.id)
    if correct_message(message.text) and g.is_active():
        id_user = message.from_user.id
        stat = len(message.text)
        word = message.text
        wg = WordGame(chat_id=message.chat.id)
        if wg.get_answer_user_id() == id_user:
            is_add = wg.word_right(word)
            username_link = wg.get_next_answer_user(b=False)
            if is_add == 1:
                wg.set_user_stat(id_user=id_user, stat=stat)
                username_link = wg.get_next_answer_user()
                wg.add_word(word, id_user)
                await message.answer(f"Далі на букву <b>{word[-1].upper()}</b>\nВідповідає {username_link}",
                                     parse_mode=types.ParseMode.HTML)
            elif is_add == 2:
                await message.reply("<i>Дане слово не відповідає вимогам гри</i>",
                                    parse_mode=types.ParseMode.HTML)
                await message.answer(
                    f"Повторно на букву <b>{wg.last_word()[-1].upper()}</b>\nВідповідає {username_link}",
                    parse_mode=types.ParseMode.HTML)
            elif is_add == 3:
                await message.reply("<i>Дане слово вже використовувалося</i>",
                                    parse_mode=types.ParseMode.HTML)
                await message.answer(f"Повторно на букву <b>{wg.last_word()[-1].upper()}</b>\n"
                                     f"Відповідає {username_link}", parse_mode=types.ParseMode.HTML)
            elif is_add == 4:
                await message.reply("<i>Ви використали символи а не слово</i>",
                                    parse_mode=types.ParseMode.HTML)
                await message.answer(f"Відповідає {username_link}", parse_mode=types.ParseMode.HTML)
        else:
            await message.reply('<b>Не ваш хід</b>', parse_mode=types.ParseMode.HTML)
            username_link = wg.get_next_answer_user()
            await message.answer(f"Повторно на букву <b>{wg.last_word()[-1].upper()}</b>\n"
                                 f"Відповідає {username_link}",
                                 parse_mode=types.ParseMode.HTML)


def correct_message(text):
    if text[0] not in punctuation:
        return True
    return False


async def main():
    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
