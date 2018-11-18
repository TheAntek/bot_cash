# https://github.com/eternnoir/pyTelegramBotAPI
import telebot
from bot_cash.constants import my_token
from bot_cash.db_operations import *
from bot_cash.useful_functions import *
from bot_cash.markups import home_markup, start_markup, y_n_markup
import time

bot = telebot.TeleBot(my_token)


@bot.message_handler(commands=['start'])
def handle_first_start(message):
    """ Хендлер команды старт """
    # Если первый раз нажимается старт - добавляем в бд нового юзера
    if user_not_exist(message.from_user.id):
        new_user(message.from_user.username, message.from_user.id)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.username}!')
        return
    # Если юзер уже находится в бд - сброс статуса
    change_status(message.from_user.id, 0)
    bot.send_message(message.chat.id, f'Рад снова тебя видеть, {message.from_user.username}!', reply_markup=home_markup)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Главное меню')
def handle_minus_money(message):
    """ Главное меню """
    change_status(message.from_user.id, 0)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=home_markup)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Баланс')
def handle_plus_money(message):
    """ Проверить баланс """
    plus = calculate_plus(message.from_user.id)
    minus = calculate_minus(message.from_user.id)
    bot.send_message(message.chat.id, f'Доходы: {plus}\nРасходы: {minus}\n\n*Баланс: {plus-minus}*',
                     reply_markup=start_markup, parse_mode='Markdown')


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
            bot.send_message(message.chat.id, 'Введите комментарий к расходу')
        else:
            change_status(message.from_user.id, 'p2')
            bot.send_message(message.chat.id, 'Введите комментарий к доходу')
    else:
        bot.send_message(message.chat.id, 'Введите коректную сумму!\n(Целое число от 0 до миллиона)')


@bot.message_handler(content_types=['text'], func=lambda message: user_status(message.from_user.id) in ('m2', 'p2'))
def handle_message_3(message):
    """ Обрабатывается сообщение, в котором юзер вводит комментарий """
    if message.text == 'Главное меню':
        handle_first_start(message)
        return
    change_cache(message.from_user.id, message.text)
    values = all_user_cache(message.from_user.id)
    if user_status(message.from_user.id) == 'm2':
        change_status(message.from_user.id, 'ma')
        bot.send_message(message.chat.id, f'Добавить расход\n\nСумма: {values[0]}\nКомментарий: {values[1]}',
                         reply_markup=y_n_markup)
    else:
        change_status(message.from_user.id, 'pa')
        bot.send_message(message.chat.id, f'Добавить доход\n\nСумма: {values[0]}\nКомментарий: {values[1]}',
                         reply_markup=y_n_markup)


@bot.message_handler(content_types=['text'], func=lambda message: user_status(message.from_user.id) in ('ma', 'pa'))
def handle_message_approve(message):
    """ Добавить новый расход """
    if message.text == 'Главное меню':
        handle_first_start(message)
        return
    if message.text == 'Да':
        date = time.strftime("%d.%m.%Y", time.localtime(int(message.date)))
        values = all_user_cache(message.from_user.id)  # все введённые данные юзера (money, comment)
        if user_status(message.from_user.id) == 'ma':
            new_expense(message.from_user.id, date, values[0], values[1])  # добавляем новый расход
            bot.send_message(message.from_user.id, 'Расход добавлен!', reply_markup=home_markup)
        else:
            new_income(message.from_user.id, date, values[0], values[1])  # добавляем новый доход
            bot.send_message(message.from_user.id, 'Доход добавлен!', reply_markup=home_markup)
        change_status(message.from_user.id, 0)  # сбрасываем статус юзера
    elif message.text == 'Нет':
        change_status(message.from_user.id, 0)
        bot.send_message(message.from_user.id, 'Операция отменена', reply_markup=home_markup)
    else:
        bot.send_message(message.from_user, 'Введите коректные данные')


if __name__ == '__main__':
    bot.polling(none_stop=True)
