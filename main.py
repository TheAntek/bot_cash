import telebot
from bot_cash.constants import my_token
from bot_cash.db_operations import *
from bot_cash.values_from_message import get_value

bot = telebot.TeleBot(my_token)


@bot.message_handler(commands=['start'], func=lambda message: user_not_exist(message.from_user.id))
def handle_first_start(message):
    """ Первый раз нажимается старт. Добавляем в бд нового юзера """
    new_user(message.from_user.username, message.from_user.id)
    bot.send_message(message.chat.id, f'Hello, new user, {message.from_user.username}!')


@bot.message_handler(commands=['start'])
def handle_first_start(message):
    """ Юзер уже находится в бд """
    change_status(message.from_user.id, 0)
    bot.send_message(message.chat.id, f'Welcome back, {message.from_user.username}!')


@bot.message_handler(commands=['minus'])
def handle_minus_money(message):
    """ Новый расход """
    change_status(message.from_user.id, 'm1')
    bot.send_message(message.chat.id, 'Введите следующие данные: деньги, категория и комент (по желанию)')


@bot.message_handler(content_types=['text'], func=lambda message: user_status(message.from_user.id) == 'm1')
def handle_message(message):
    """ Добавить новый расход"""
    values = get_value(message.text)
    money, category, comment = range(3)
    new_expense(message.from_user.id, message.date, values[money], values[category], values[comment])
    bot.send_message(message.chat.id, 'Расход добавлен!')
    change_status(message.from_user.id, 0)


@bot.message_handler(commands=['expenses'])
def handle_expenses(message):
    """ Выводит все расходы """
    values = all_expenses(message.from_user.id)

    for j in range(len(values)):
        bot.send_message(message.chat.id, values[j], parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def handle_message(message):
    print(message)
    print()
    print(message.from_user.username)
    print(message.from_user.id)
    print(message.date)
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
