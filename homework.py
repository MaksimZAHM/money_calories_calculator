import datetime as dt


class Record():

    def __init__(self, amount, comment, date = None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if date is None:
            date = dt.datetime.today()
        else:
            date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Cохраняет новую запись."""
        self.records.append(record)

    def get_today_stats(self):
        """Считает сегодняшнюю сумму."""
        day_today = dt.datetime.today()
        day_amount = 0
        for x in self.records:
            if x.date == day_today:
                day_amount += x.amount
        return day_amount

    def get_week_stats(self):
        """Считает статистику за 7 дней."""
        week_amount = 0
        today = dt.datetime.today()
        week_date_delta = today - dt.timedelta(weeks=1)
        for y in self.records:
            if week_date_delta <= y.date <= today:
                week_amount += y.amount
        return week_amount

    def get_balance(self):
        """Считает остаток дневного лимита."""
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        """Возвращает совет оринтируясь на остаток дневного лимита."""
        if self.get_balance() > 0:
            return ('Сегодня можно съесть что-нибудь еще, но с общей'
                    f' калорийностью не более {self.get_balance()} кКал')
        else:
            return ('Хватит есть!')


class CashCalculator(Calculator):

    EURO_RATE = 86.50
    USD_RATE = 74.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        """Возвращает совет учитывая валюту и курс,
         оринтируясь на остаток дневного лимита.
        """
        money = {
            'eur': (self.EURO_RATE, 'Euro'),
            'usd': (self.USD_RATE, 'USD'),
            'rub': (self.RUB_RATE, 'руб')
        }

        change_rate, short_name = money[currency]
        todays_balance = self.get_balance()
        rest_of_money = round(todays_balance / change_rate, 2)
        if currency not in money:
            return ('Валюта не определена')
        else:
            if self.get_balance() > 0:
                return('На сегодня осталось '
                       f'{rest_of_money}{short_name}')
            elif self.get_balance() == 0:
                return ('Денег нет, держись')
            else:
                return ('Денег нет, держись: твой долг - '
                        f'{abs(rest_of_money)}{short_name}')


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))
