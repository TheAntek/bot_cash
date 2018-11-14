def check_money(message):
    """ Проверяем коректность данных для введёных денег
        Должно быть целое число от 0 до миллиона """
    try:
        message = int(message)
    except ValueError:
        return False

    if message > 1000001 or message <= 0:
        return False

    return True


if __name__ == '__main__':

    while True:
        print(check_money(input()))
