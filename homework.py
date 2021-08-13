import datetime as dt

DATE_FORMAT = '%d.%m.%Y'

class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.today().date()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Cохраняет новую запись."""
        self.records.append(record)

    def get_today_stats(self):
        """Считает сегодняшнюю сумму."""
        today = dt.datetime.today().date()
        return sum(x.amount for x in self.records if x.date == today)

    def get_week_stats(self):
        """Считает статистику за 7 дней."""
        today = dt.datetime.today().date()
        week_delta = today - dt.timedelta(days=7)
        return sum(y.amount for y in self.records
                   if y.date > week_delta and y.date <= today)

    def get_balance(self):
        """Считает остаток от дневного лимита."""
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        """Возвращает совет, оринтируясь на остаток от дневного лимита."""
        if self.get_balance() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.get_balance()} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):

    EURO_RATE = 86.50
    USD_RATE = 74.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        """Возвращает совет, учитывая валюту и курс,
         оринтируясь на остаток от дневного лимита.
        """
        money = {
            'eur': (self.EURO_RATE, 'Euro'),
            'usd': (self.USD_RATE, 'USD'),
            'rub': (self.RUB_RATE, 'руб')
        }

        if currency not in money:
            return 'Валюта не определена'
        else:
            change_rate, short_name = money[currency]
            rest_of_money = round(self.get_balance() / change_rate, 2)
            if self.get_balance() > 0:
                return('На сегодня осталось '
                       f'{rest_of_money} {short_name}')
            elif self.get_balance() == 0:
                return 'Денег нет, держись'
            return ('Денег нет, держись: твой долг - '
                        f'{abs(rest_of_money)} {short_name}')

