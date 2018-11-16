import shelve
from bot_cash.class_user import User


def new_user(username, user_id):
    """ Добавить нового юзера в базу данных """
    db = shelve.open('users-shelve-test')
    user = User(username, user_id)
    db[str(user_id)] = user
    db.close()


def user_not_exist(user_id):
    """ Проверить, существует ли юзер в базе данных """
    db = shelve.open('users-shelve-test')
    status = str(user_id) not in db
    db.close()
    return status


def change_cache(user_id, new_cache, number):
    """ Изменить временный кэш юзера (деньги, категория, коментарий) """
    db = shelve.open('users-shelve-test')
    user = db[str(user_id)]
    user_cache = ['cache_money', 'cache_category', 'cache_comment']
    setattr(user, user_cache[number], new_cache)
    db[str(user_id)] = user
    db.close()


def all_user_cache(user_id):
    """ Вернуть всю кєшированную инфу (Данные, которые ввел юзер) ..деньги, категория, комент """
    db = shelve.open('users-shelve-test')
    user = db[str(user_id)]
    result = user.cache_money, user.cache_category, user.cache_comment
    db.close()
    return result


# def clean_cache(user_id):
#     """ Чистим весь кєш юзера. А зачем? Пока не чистим """
#     db = shelve.open('users-shelve-test')
#     user = db[str(user_id)]
#     user.cache_money, user.cache_category, user.cache_comment = None, None, None
#     db.close()


def new_expense(user_id, date, money, category, comment=None):
    """ Добавить новый расход """
    db = shelve.open('users-shelve-test')
    user = db[str(user_id)]
    user.new_expense(date, money, category, comment)
    db[str(user_id)] = user
    db.close()


def all_expenses(user_id):
    """ Возвращает все расходы юзера """
    db = shelve.open('users-shelve-test')
    user_expenses = db[str(user_id)].expenses
    result = list(user_expenses.values())
    db.close()
    return result


# def calculate_minus(user_id):
#     """ Возвращает суму всех расходов """
#     db = shelve.open('users-shelve-test')
#     user_expenses = list(db[str(user_id)].expenses.values())
#     result = 0
#     for exp in user_expenses:
#         result += int(exp.money)
#     db.close()
#     return result


if __name__ == '__main__':
    # change_status(322, 'm1')
    # new_user('elonmusk', 199694594)
    database = shelve.open('users-shelve-test')

    for i in database:
        print(database[i], database[i].name, database[i].user_id, database[i].incomes, database[i].expenses)

    # new_expense(my, 14066947, 45, 'food', 'shaurma')
    database.close()
    my = 255146705
    spam = all_expenses(my)
    for i in spam:
        print(i)
    print(spam)
    # www = calculate_minus(my)
    # print(www)
