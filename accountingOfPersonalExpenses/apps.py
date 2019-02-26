from django.apps import AppConfig


class AccountingOfPersonalExpensesConfig(AppConfig):
    name = 'accountingOfPersonalExpenses'
    # adaptive\increment
    script = 'adaptive'
    limit_months = {
        "02.2019": 10,
        "03.2019": 10,
        "04.2019": 10,
        "05.2019": 10,
    }
