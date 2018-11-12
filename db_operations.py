import shelve
from bot_cash.user import User


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


def new_expense(user_id, date, money, category, comment=None):
    """ Добавить новый расход """
    db = shelve.open('users-shelve-test')
    user = db[str(user_id)]
    user.new_expense(date, money, category, comment)
    db[str(user_id)] = user
    db.close()


if __name__ == '__main__':
    # change_status(322, 'm1')
    # new_user('elonmusk', 199694594)
    database = shelve.open('users-shelve-test')

    for i in database:
        print(database[i], database[i].name, database[i].user_id, database[i].incomes, database[i].expenses,
              database[i].status)

    # new_expense(my, 14066947, 45, 'food', 'shaurma')

    database.close()
