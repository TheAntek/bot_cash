def get_value(text):
    text = text.split()

    if len(text) == 2:
        money = text[0]
        category = text[1]
        return money, category

    elif len(text) == 3:
        money = text[0]
        category = text[1]
        comment = text[2]
        return money, category, comment

    return False


if __name__ == '__main__':
    print(get_value('45 food shaurma'))