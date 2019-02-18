from django.db import models
from datetime import date, timedelta
import calendar


class Categories(models.Model):
    name = models.CharField(max_length=255)


class ExpensesManager(models.Manager):
    def get_expenses_months(self):
        ans_expenses = self.values('dateY', 'dateM')\
            .order_by('dateY', 'dateM')\
            .annotate(expenses_sum=models.Sum('expenses'))
        resp_expenses = {}
        for val in ans_expenses:
            resp_expenses[date(val['dateY'], val['dateM'], 1).strftime("%m.%Y")] = round(val['expenses_sum'], 2)
        return resp_expenses

    # из за того что метод фактически ничего не делает (adaptive), будет вывод только в консоль
    # про хранение состояния я вопрос задавал - мне сказали не надо (возможно хранить состояние нужно, но
    # не в конфиге)
    def overrun(self, script, expenses_months, limit_months, expense, input_date):
        date_expense = input_date.strftime("%m.%Y")
        if date_expense in limit_months:
            if date_expense not in expenses_months:
                expenses_months[date_expense] = 0
            if limit_months[date_expense] >= expenses_months[date_expense] + expense:
                print(
                    'Все ок, расходы ({}) за {} не превысили лимит {}'.format(
                        expenses_months[date_expense] + expense,
                        date_expense,
                        limit_months[date_expense]
                    )
                )
            else:
                overrun = expenses_months[date_expense] + expense - limit_months[date_expense]
                if script == "adaptive":
                    days = calendar.monthrange(input_date.year, input_date.month)[1]
                    print('Перерасход за {}, на {}, перенос на след месяц'.format(date_expense, overrun))
                    self.overrun_adaptive(expenses_months, limit_months, overrun, input_date + timedelta(days=days))
                if script == "increment":
                    print('Перерасход за {}, на {}, вывод нотиса пользователю'.format(date_expense, overrun))
                    return True
        else:
            print('Лимиты расходов за {}, не установлены'.format(date_expense))
        return False


# сделаем date через избыточность данных
class Expenses(models.Model):
    objects = ExpensesManager()

    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    date = models.DateField()
    dateD = models.PositiveSmallIntegerField()
    dateM = models.PositiveSmallIntegerField()
    dateY = models.PositiveSmallIntegerField()
    expenses = models.DecimalField(max_digits=12, decimal_places=2)



