class Income:
    """ Новый доход """
    name = 'Доход'

    def __init__(self, date, money, num, comment):
        self.date = date
        self.money = money
        self.comment = comment
        self.num = num

    def __str__(self):
        """ print() выводит все атрибуты объекта """
        return f'*{self.name} {self.num}*\nсумма: {self.money}\nдата: {self.date}\nкоментарий: {self.comment}'


class Expense(Income):
    """ Новый расход """
    name = 'Расход'

    def __init__(self, date, money, num, comment):
        Income.__init__(self, date, money, num, comment)

    def __str__(self):
        """ Добавление категории при выводе """
        return Income.__str__(self)


if __name__ == '__main__':

    i1 = Income('12.11.2018', 5000, 1, 'зп за стажировку')
    print(i1, '\n')

    e1 = Expense('12.11.2018', 40, 1, 'hello 1')
    print(e1)
    e2 = Expense('13.11.2018', 50, 2, 'hello 2')
    print(e2)
