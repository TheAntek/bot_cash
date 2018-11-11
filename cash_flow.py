class Income:
    """ Новый доход """
    def __init__(self, date, money, comment=None):
        self.date = date
        self.money = money
        self.comment = comment

    def __str__(self):
        """ print() выводит все атрибуты объекта """
        return f'{self.__class__.__name__}\ndate: {self.date}\nmoney: {self.money}\ncomment: {self.comment}'


class Expense(Income):
    """ Новый расход. Расширяем клас Income добавлением атрибута category """
    def __init__(self, date, money, category, comment=None):
        Income.__init__(self, date, money, comment)
        self.category = category

    def __str__(self):
        """ Добавление категории при выводе """
        return Income.__str__(self) + f'\ncategory: {self.category}'


if __name__ == '__main__':

    i1 = Income('12.11.2018', 5000, 'зп за стажировку')
    print(i1, '\n')

    e1 = Expense('12.11.2018', 40, 'Еда', 'Шаурма')
    print(e1)
