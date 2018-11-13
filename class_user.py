class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.incomes = {}
        self.expenses = {}
        self.status = 0

    def new_expense(self, date, money, category, comment=None):
        """ Добавить новый расход """
        from bot_cash.classes_cash import Expense
        self.expenses[len(self.expenses)+1] = Expense(date, money, category, len(self.expenses)+1, comment)

    def new_income(self, date, money, comment=None):
        """ Добавить новый доход """
        from bot_cash.classes_cash import Income
        self.incomes[len(self.incomes)+1] = Income(date, money, len(self.expenses)+1, comment)

    def __str__(self):
        """ Красиво вывести объект """
        return f'< {self.__class__.__name__} - {self.name} (id={self.user_id}) >'


if __name__ == '__main__':
    from bot_cash.classes_cash import Expense, Income

    new_user = User('Anton', 247)

    print(new_user)
    print(new_user.incomes)
    print(new_user.expenses)

    new_user.new_income('12.11.2018', 300, 'зп за урок пайтона')
    new_user.new_income('19.11.2018', 300, 'зп за урок пайтона')

    print(new_user.incomes[1])
    print(new_user.incomes[2])

    print(new_user.incomes)
