# https://github.com/eternnoir/pyTelegramBotAPI
import telebot
from bot_cash.constants import my_token
from bot_cash.db_operations import *
from bot_cash.useful_functions import *
from bot_cash.markups import home_markup, start_markup, y_n_markup

bot = telebot.TeleBot(my_token)


@bot.message_handler(commands=['start'])
def handle_first_start(message):
    """ Хендлер команды старт """
    # Если первый раз нажимается старт - добавляем в бд нового юзера
    if user_not_exist(message.from_user.id):
        new_user(message.from_user.username, message.from_user.id)
        bot.send_message(message.chat.id, f'Hello, new user, {message.from_user.username}!')
        return
    # Если юзер уже находится в бд - сброс статуса
    change_status(message.from_user.id, 0)
    bot.send_message(message.chat.id, f'Welcome back, {message.from_user.username}!', reply_markup=home_markup)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Главное меню')
def handle_minus_money(message):
    """ Главное меню """
    change_status(message.from_user.id, 0)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=home_markup)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Новый расход')
def handle_minus_money(message):
    """ Новый расход """
    change_status(message.from_user.id, 'm1')
    bot.send_message(message.chat.id, 'Введите сумму расхода', reply_markup=start_markup)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Новый доход')
def handle_plus_money(message):
    """ Новый доход """
    change_status(message.from_user.id, 'p1')
    bot.send_message(message.chat.id, 'Введите сумму дохода', reply_markup=start_markup)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Все расходы')
def handle_expenses(message):
    """ Выводит все расходы """
    values = all_expenses(message.from_user.id)

    for j in range(len(values)):
        bot.send_message(message.chat.id, values[j], parse_mode='Markdown', reply_markup=start_markup)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Все доходы')
def handle_incomes(message):
    """ Выводит все доходы """
    values = all_incomes(message.from_user.id)

    for j in range(len(values)):
        bot.send_message(message.chat.id, values[j], parse_mode='Markdown', reply_markup=start_markup)


@bot.message_handler(content_types=['text'], func=lambda message: user_status(message.from_user.id) in ('m1', 'p1'))
def handle_message_1(message):
    """ Обрабатывается сообщение, в котором юзер вводит сумму расхода/дохода """
    if message.text == 'Главное меню':
        handle_first_start(message)
        return
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
    if message.text == 'Главное меню':
        handle_first_start(message)
        return
    change_cache(message.from_user.id, message.text)
    change_status(message.from_user.id, 'm3')
    bot.send_message(message.chat.id, 'Введите комментарий к расходу')


@bot.message_handler(content_types=['text'], func=lambda message: user_status(message.from_user.id) in ('m3', 'p3'))
def handle_message_3(message):
    """ Обрабатывается сообщение, в котором юзер вводит комментарий """
    if message.text == 'Главное меню':
        handle_first_start(message)
        return
    change_cache(message.from_user.id, message.text)
    if user_status(message.from_user.id) == 'm3':
        change_status(message.from_user.id, 'ma')
        bot.send_message(message.chat.id, f'Добавить расход\n{all_user_cache(message.from_user.id, "m")}',
                         reply_markup=y_n_markup)
    else:
        change_status(message.from_user.id, 'pa')
        bot.send_message(message.chat.id, f'Добавить доход\n{all_user_cache(message.from_user.id, "p")}',
                         reply_markup=y_n_markup)


@bot.message_handler(content_types=['text'], func=lambda message: user_status(message.from_user.id) in ('ma', 'pa'))
def handle_message_approve(message):
    """ Добавить новый расход """
    if message.text == 'Главное меню':
        handle_first_start(message)
        return
    if message.text == 'Да':
        if user_status(message.from_user.id) == 'ma':
            values = all_user_cache(message.from_user.id, 'm')  # все введённые данные юзера (money, category, comment)
            new_expense(message.from_user.id, message.date, values[0], values[1], values[2])  # добавляем новый расход
            bot.send_message(message.from_user.id, 'Расход добавлен!', reply_markup=home_markup)
        else:
            values = all_user_cache(message.from_user.id, 'p')  # все введённые данные юзера (money, comment)
            new_income(message.from_user.id, message.date, values[0], values[1])  # добавляем новый доход
            bot.send_message(message.from_user.id, 'Доход добавлен!', reply_markup=home_markup)
        change_status(message.from_user.id, 0)  # сбрасываем статус юзера
    elif message.text == 'Нет':
        change_status(message.from_user.id, 0)
        bot.send_message(message.from_user.id, 'Операция отменена', reply_markup=home_markup)
    else:
        bot.send_message(message.from_user, 'Введите коректные данные')


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
