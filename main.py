import ast

import telebot
import json
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    rmk = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(telebot.types.KeyboardButton("1"),
            telebot.types.KeyboardButton("2"),
            telebot.types.KeyboardButton("3"))

    msg = bot.send_message(message.chat.id,
                           f'Сколько у вас оппонентов, <b>{message.from_user.first_name}</b>?',
                           parse_mode='html', reply_markup=rmk)
    bot.register_next_step_handler(msg, first_answer)


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
                     "♠️Этот бот показывает игроку в покер какой у него шанс выиграть с его картами до первой раздачи"
                     "♦️Нужно сначала выбрать количество соперников, потом ввести свои карты"
                     "️️♣️Вводить карты нужно в определенном формате. Пример: 'A7' 'KQ' '1010' '98'"
                     "♥️Самые младшие карты для которых выдается вероятность это '98'")


def first_answer(message):
    msg = bot.send_message(message.chat.id,
                           f'Какие у вас карты, <b>{message.from_user.first_name}</b>?',
                           parse_mode='html')
    if message.text == "1":
        file = "one_opponent.txt"
    if message.text == "2":
        file = "two_opponents.txt"
    elif message.text == "3":
        file = "three_opponents.txt"
    bot.register_next_step_handler(msg, second_answer, file)

    telebot.types.ReplyKeyboardRemove(selective=False)


def second_answer(message, file):
    with open(file) as f:
        data = f.read()
    d = ast.literal_eval(data)
    if d.get(message.text):
        bot.send_message(message.chat.id, d.get(message.text), parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Неправильный формат/Слишком слабые карты :)", parse_mode='html')


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(none_stop=True)
