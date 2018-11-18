from telebot import types

home_markup = types.ReplyKeyboardMarkup(selective=False, resize_keyboard=True)
item1 = types.KeyboardButton('Новый доход')
item2 = types.KeyboardButton('Новый расход')
item3 = types.KeyboardButton('Все доходы')
item4 = types.KeyboardButton('Все расходы')
item5 = types.KeyboardButton('Баланс')
home_markup.row(item1, item2)
home_markup.row(item3, item4)
home_markup.row(item5)

start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_item = types.KeyboardButton('Главное меню')
start_markup.add(start_item)

y_n_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
yes = types.KeyboardButton('Да')
no = types.KeyboardButton('Нет')
home = types.KeyboardButton('Главное меню')
y_n_markup.row(yes, no)
y_n_markup.row(home)
