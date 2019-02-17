from django.apps import AppConfig


# не особо понятно "предельная сумма месячных расходов" -
# это лимит на каждый месяц или общий на все месяцы (сделаем на каждый)
class LimitConfig(AppConfig):
    name = 'accountingOfPersonalExpenses'
    # adaptive\increment
    script = 'adaptive'
    limit_months = {
        "02.2019": 100,
        "03.2019": 100,
        "04.2019": 100,
        "05.2019": 100,
    }
