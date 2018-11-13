class Income:
    """ Новый доход """
    def __init__(self, date, money, num, comment=None):
        self.date = date
        self.money = money
        self.comment = comment
        self.num = num

    def __str__(self):
        """ print() выводит все атрибуты объекта """
        return f'*{self.__class__.__name__} {self.num}*\ndate: {self.date}\nmoney: {self.money}\n' \
               f'comment: {self.comment}'


class Expense(Income):
    """ Новый расход. Расширяем клас Income добавлением атрибута category """
    def __init__(self, date, money, category, num, comment=None):
        Income.__init__(self, date, money, num, comment)
        self.category = category

    def __str__(self):
        """ Добавление категории при выводе """
        return f'*{self.__class__.__name__} {self.num}*\ndate: {self.date}\nmoney: {self.money}\n' \
               f'category: {self.category}\ncomment: {self.comment}'


if __name__ == '__main__':

    i1 = Income('12.11.2018', 5000, 1, 'зп за стажировку')
    print(i1, '\n')

    e1 = Expense('12.11.2018', 40, 'Еда', 1)
    print(e1)
