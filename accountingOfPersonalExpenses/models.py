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

    def overrun(self, script, expenses_months, limit_months, expense, input_date):
        date_expense = input_date.strftime("%m.%Y")
        if date_expense in limit_months:
            if date_expense not in expenses_months:
                expenses_months[date_expense] = 0
            status_overrun = {
                "date": date_expense,
                "overrun": expenses_months[date_expense] - limit_months[date_expense],
                "current_months_expenses": expenses_months[date_expense],
                "limit": limit_months[date_expense],
            }

            if script == 'adaptive':
                lost_months = (input_date - timedelta(days=1)).strftime("%m.%Y")
                lost_months_overrun = 0
                if lost_months in limit_months and expenses_months[lost_months]:
                    lost_months_overrun = expenses_months[lost_months] - limit_months[lost_months]
                status_overrun["overrun"] += lost_months_overrun
                status_overrun["lost_months_overrun"] = lost_months_overrun
                status_overrun["limit"] -= lost_months_overrun

            if status_overrun["overrun"] > 0:
                status_overrun["status"] = "current-overrun"
                return status_overrun
            status_overrun["overrun"] += expense
            status_overrun["current_months_expenses"] += expense
            if status_overrun["overrun"] > 0:
                status_overrun["status"] = "increment-overrun" if script == "increment" else "adaptive-overrun"
                return status_overrun

            return {"status": "ok"}
        return {"status": "no-set-limit"}


# сделаем date через избыточность данных
class Expenses(models.Model):
    objects = ExpensesManager()

    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    date = models.DateField()
    dateD = models.PositiveSmallIntegerField()
    dateM = models.PositiveSmallIntegerField()
    dateY = models.PositiveSmallIntegerField()
    expenses = models.DecimalField(max_digits=12, decimal_places=2)



