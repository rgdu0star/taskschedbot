# -*- coding: utf-8 -*-

import datetime
import locale
import os

import telebot
import yaml

bot = telebot.TeleBot(os.environ['TOKEN'])

main_btns = ('📘 Сьогодні', '📗 Завтра', '📅 Загальний розклад на тиждень', '🔔 Розклад дзвінків')
week_btns = ('Пн', 'Ві', 'Ср', 'Чт', 'Пт', 'Субота', 'Неділя')

main_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.row(*main_btns[:2])
main_markup.row(main_btns[2])
main_markup.row(main_btns[3])

week_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
week_markup.row(*week_btns[:5])
week_markup.row(week_btns[5])
week_markup.row(week_btns[6])


def parser(src):
    return ['{}\n`({}, {})`'.format(*x) if isinstance(x, list) else x for x in src]


@bot.message_handler(commands=['start'])
def welcome(message):
    text = 'Привіт! Я допоможу тобі дізнатись розклад  😉'
    bot.send_message(message.chat.id, text, reply_markup=main_markup)


@bot.message_handler(func=lambda msg: msg.text in main_btns[:2])
def today_timetable(message):
    with open('timetable.yml', 'r') as f:
        timetable = yaml.load(f)
    tomorrow = message.text == main_btns[1]
    today = datetime.date.today() + datetime.timedelta(days=tomorrow)
    is_numerator = today.isocalendar()[0] % 2
    text = '*Розклад на {}:*\n'.format(message.text[2:].lower())
    text += '\n'.join(parser(timetable[today.strftime("%A")][is_numerator]))
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == main_btns[2])
def week_msg(message):
    bot.send_message(message.chat.id, 'Виберіть день тижня:', reply_markup=week_markup)


@bot.message_handler(func=lambda msg: msg.text in week_btns)
def week_timetable(message):
    with open('timetable.yml', 'r') as f:
        timetable = yaml.load(f)
    index = week_btns.index(message.text)
    ru = ('Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота', 'Неділя')
    text = '*{}:*\n'.format(ru[index])
    timetable = tuple(timetable.values())[index]
    if timetable[0] == timetable[1]:
        text += '\n'.join(parser(timetable[0]))
    else:
        text += '*НІ:*\n{}\n\n'.format('\n'.join(parser(timetable[0])))
        text += '*ДІ:*\n{}'.format('\n'.join(parser(timetable[1])))
    bot.send_message(message.chat.id, text, reply_markup=main_markup, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == main_btns[3])
def bells_msg(message):
    text = (
        '*Розклад дзвінків:*\n'
        '1. 8:00 - 9:20\n'
        '2. 9:35 - 10:55\n'
        '3. 11:10 - 12:30\n'
        '4. 12:45 - 14:05\n')
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: True)
def error_msg(message):
    bot.reply_to(message, 'Щось я тебе не розумію, нажаль 😢', reply_markup=main_markup)


bot.polling()
