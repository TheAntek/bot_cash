import telebot
from bot_cash.constants import my_token
from bot_cash.db_operations import *
from bot_cash.useful_functions import *

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
    bot.send_message(message.chat.id, 'Введите сумму расхода')


@bot.message_handler(commands=['plus'])
def handle_plus_money(message):
    """ Новый доход """
    change_status(message.from_user.id, 'p1')
    bot.send_message(message.chat.id, 'Введите сумму дохода')


@bot.message_handler(content_types=['text'], func=lambda message: user_status(message.from_user.id) in ('m1', 'p1'))
def handle_message_1(message):
    """ Обрабатывается сообщение, в котором юзер вводит сумму расхода/дохода """
    if check_money(message.text):
        change_cache(message.from_user.id, message.text)  # добавить в временный кэш юзера введённые деньги
        if user_status(message.from_user.id) == 'm1':
            change_status(message.from_user.id, 'm2')
            bot.send_message(message.chat.id, 'Введите категорию расхода')
        else:
            change_status(message.from_user.id, 'p3')
            bot.send_message(message.chat.id, 'Введите комментарий к доходу')
    else:
        bot.send_message(message.chat.id, 'Введите коректную сумму!\n(Целое число от 0 до миллиона)')


@bot.message_handler(content_types=['text'], func=lambda message: user_status(message.from_user.id) == 'm2')
def handle_message_2(message):
    """ Обрабатывается сообщение, в котором юзер вводит категорию (выбирает) """
    change_cache(message.from_user.id, message.text)
    change_status(message.from_user.id, 'm3')
    bot.send_message(message.chat.id, 'Введите комментарий к расходу')


@bot.message_handler(content_types=['text'], func=lambda message: user_status(message.from_user.id) in ('m3', 'p3'))
def handle_message_3(message):
    """ Обрабатывается сообщение, в котором юзер вводит комментарий """
    change_cache(message.from_user.id, message.text)
    if user_status(message.from_user.id) == 'm3':
        change_status(message.from_user.id, 'ma')
        bot.send_message(message.chat.id, f'Добавить расход\n{all_user_cache(message.from_user.id, "m")}')
    else:
        change_status(message.from_user.id, 'pa')
        bot.send_message(message.chat.id, f'Добавить доход\n{all_user_cache(message.from_user.id, "p")}')


@bot.message_handler(content_types=['text'], func=lambda message: user_status(message.from_user.id) in ('ma', 'pa'))
def handle_message_approve(message):
    """ Добавить новый расход """
    if message.text == 'Да':
        if user_status(message.from_user.id) == 'ma':
            values = all_user_cache(message.from_user.id, 'm')  # все введённые данные юзера (money, category, comment)
            new_expense(message.from_user.id, message.date, values[0], values[1], values[2])  # добавляем новый расход
            bot.send_message(message.from_user.id, 'Расход добавлен!')
        else:
            values = all_user_cache(message.from_user.id, 'p')  # все введённые данные юзера (money, comment)
            new_income(message.from_user.id, message.date, values[0], values[1])  # добавляем новый доход
            bot.send_message(message.from_user.id, 'Доход добавлен!')
        change_status(message.from_user.id, 0)  # сбрасываем статус юзера
    elif message.text == 'Нет':
        change_status(message.from_user.id, 0)
        bot.send_message(message.from_user.id, 'Операция отменена')
    else:
        bot.send_message(message.from_user, 'Введите коректные данные')


@bot.message_handler(commands=['expenses'])
def handle_expenses(message):
    """ Выводит все расходы """
    values = all_expenses(message.from_user.id)

    for j in range(len(values)):
        bot.send_message(message.chat.id, values[j], parse_mode='Markdown')


@bot.message_handler(commands=['incomes'])
def handle_incomes(message):
    """ Выводит все доходы """
    values = all_incomes(message.from_user.id)

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
