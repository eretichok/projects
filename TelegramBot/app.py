import telebot
from telebot import types
import config as conf
from extensions import APIException, Request

TOKEN = conf.TOKEN

bot = telebot.TeleBot(TOKEN)


# Телебот: начальный экран
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Курсы')
    btn2 = types.KeyboardButton('Валюта')
    btn3 = types.KeyboardButton('Помощь')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, f'Приветствую тебя, {message.chat.first_name}!\n'
                                      'Что мне сконвертировать для Вас?\n'
                                      'Пример запроса: \n'
                                      'USD RUB 100 \n'
                                      '(получите 100 долларов в рублях по курсу ЦБ)', reply_markup=markup)


# Телебот: обработка команды /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Этот бот умеет конвертировать валюту.\n'
                                      'Ввод через пробел в формате:\n'
                                      '<код начальной валюты>\n'
                                      '<код валюты перевода>\n '
                                      '<сумма начальной валюты>, например:\n'
                                      'USD RUB 100 (получите 100 долларов в рублях);\n'
                                      'Кнопки меню:\n'
                                      '"Курсы" - покажет "код валюты - курс"\n'
                                      '"Валюта" - покажет "код валюты - название валюты"\n'
                                      '"Помощь" - покажет данную инструкцию.')


# Телебот: обработка команды /values. Выводит: код валюты - наименование валюты
@bot.message_handler(commands=['values'])
def values(message):
    result = ''
    for code, name in Request.get_dict().items():
        result += f'{code} - {name[0]}\n'
    bot.send_message(message.chat.id, result)


# Телебот: обработка команды /exchange_rate. Выводит: код валюты - курс
@bot.message_handler(commands=['exchange_rate'])
def exchange_rate(message):
    result = ''
    for code, value in Request.get_dict().items():
        result += f'{value[1]} {code} - {round(value[2], 4)} RUB\n'
    bot.send_message(message.chat.id, result)


@bot.message_handler(content_types=['text'])
def request(message):
    if len(message.text.split()) == 3:
        try:
            answer = Request.get_price(*message.text.split())
        except APIException as e:
            bot.reply_to(message, f'Oшибка:\n{e}')
        except Exception as e:
            bot.reply_to(message, f'Oшибка:\n{e}')
        else:
            bot.reply_to(message, answer)
    elif len(message.text.split()) == 1:
        text = message.text.capitalize()
        if text in ['Курс', 'Курсы']:
            exchange_rate(message)
        elif text in ['Валюта', 'Валюты']:
            values(message)
        elif text in ['Помощь', 'Help']:
            help(message)
        else:
            bot.reply_to(message, f'Неверный формат ввода! Запрос {text} не распознан.')
    else:
        bot.reply_to(message, f'Неверный формат ввода! Должно быть три значения.')


bot.polling(none_stop=True)
