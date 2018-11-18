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


def user_status(user_id):
    """ Вернуть статус юзера """
    db = shelve.open('users-shelve-test')
    if str(user_id) not in db:
        return False
    status = db[str(user_id)].status
    db.close()
    return status


def change_status(user_id, new_status):
    """ Изменить статус юзера """
    db = shelve.open('users-shelve-test')
    user = db[str(user_id)]
    user.status = new_status
    db[str(user_id)] = user
    db.close()


def change_cache(user_id, new_cache):
    """ Изменить временный кэш юзера (деньги, коментарий) """
    db = shelve.open('users-shelve-test')
    user = db[str(user_id)]

    if user.status == 'm1' or user.status == 'p1':
        user.cache_money = new_cache
    elif user.status == 'm2' or user.status == 'p2':
        user.cache_comment = new_cache

    db[str(user_id)] = user
    db.close()


def all_user_cache(user_id):
    """ Вернуть всю кєшированную инфу (Данные, которые ввел юзер) ..деньги, комент """
    db = shelve.open('users-shelve-test')
    user = db[str(user_id)]
    result = user.cache_money, user.cache_comment
    db.close()
    return result


def clean_cache(user_id):
    """ Чистим весь кєш юзера. А зачем? Пока не чистим """
    db = shelve.open('users-shelve-test')
    user = db[str(user_id)]
    user.cache_money, user.cache_comment = None, None
    db[str(user_id)] = user
    db.close()


def new_expense(user_id, date, money, comment):
    """ Добавить новый расход """
    db = shelve.open('users-shelve-test')
    user = db[str(user_id)]
    user.new_expense(date, money, comment)
    db[str(user_id)] = user
    db.close()


def all_expenses(user_id):
    """ Возвращает все расходы юзера """
    db = shelve.open('users-shelve-test')
    user_expenses = db[str(user_id)].expenses
    result = tuple(user_expenses.values())
    db.close()
    return result


def new_income(user_id, date, money, comment):
    """ Добавить новый доход """
    db = shelve.open('users-shelve-test')
    user = db[str(user_id)]
    user.new_income(date, money, comment)
    db[str(user_id)] = user
    db.close()


def all_incomes(user_id):
    """ Возвращает все доходы юзера """
    db = shelve.open('users-shelve-test')
    user_incomes = db[str(user_id)].incomes
    result = tuple(user_incomes.values())
    db.close()
    return result


def calculate_minus(user_id):
    """ Возвращает суму всех расходов """
    db = shelve.open('users-shelve-test')
    user_expenses = tuple(db[str(user_id)].expenses.values())
    result = 0
    for exp in user_expenses:
        result += int(exp.money)
    db.close()
    return result


def calculate_plus(user_id):
    """ Возвращает суму всех доходов """
    db = shelve.open('users-shelve-test')
    user_incomes = tuple(db[str(user_id)].incomes.values())
    result = 0
    for exp in user_incomes:
        result += int(exp.money)
    db.close()
    return result


if __name__ == '__main__':
    # change_status(322, 'm1')
    # new_user('elonmusk', 199694594)
    database = shelve.open('users-shelve-test')

    for i in database:
        print(database[i], database[i].name, database[i].user_id, database[i].incomes, database[i].expenses,
              database[i].status)

    # new_expense(my, 14066947, 45, 'food', 'shaurma')
    database.close()
    my = 255146705
    spam = all_expenses(my)
    for i in spam:
        print(i)
    print(spam)
    www = calculate_minus(my)
    print(f'expenses sum: {www}')
    print(f'incomes sum: {calculate_plus(my)}')
    print(f'all incomes: {all_incomes(my)}')
