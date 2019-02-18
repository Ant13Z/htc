from django.apps import AppConfig


class AccountingOfPersonalExpensesConfig(AppConfig):
    name = 'accountingOfPersonalExpenses'
    # adaptive\increment
    script = 'increment'
    limit_months = {
        "02.2019": 100,
        "03.2019": 100,
        "04.2019": 100,
        "05.2019": 100,
    }
