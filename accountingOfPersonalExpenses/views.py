from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Sum
from .forms import FormExpenses, FormCategories, FormExpensesMonth
from .models import Expenses, Categories
from django.apps import apps
import json
from datetime import date


def index(request):
    return render(request, "index.html", {
        "back": False
    })


def add(request):
    status_overrun = {"status": "ok"}
    if request.method == "POST":
        form = FormExpenses(request.POST)
        if form.is_valid():
            config = apps.get_containing_app_config("accountingOfPersonalExpenses")
            if hasattr(config, 'script') and hasattr(config, 'limit_months'):
                status_overrun = Expenses.objects.overrun(
                    config.script,
                    Expenses.objects.get_expenses_months(),
                    config.limit_months,
                    form.cleaned_data['expenses'],
                    date(form.cleaned_data['date'].year, form.cleaned_data['date'].month, 1)
                )
            if status_overrun["status"] not in "current-overrun":
                category = Categories.objects.get(id=form.cleaned_data['categories'])
                expense = category.expenses_set.create(
                    date=form.cleaned_data['date'],
                    dateD=form.cleaned_data['date'].day,
                    dateM=form.cleaned_data['date'].month,
                    dateY=form.cleaned_data['date'].year,
                    expenses=form.cleaned_data['expenses']
                )
                print("Ид нового расхода: ", expense.id)
        else:
            print(json.dumps(form.errors))

    return render(request, "add.html", {
        "form": FormExpenses(),
        "back": True,
        "notice": status_overrun,
        "statuses": ('current-overrun', 'increment-overrun', 'adaptive-overrun')
    })


def categories(request):
    if request.method == "POST":
        form = FormCategories(request.POST)
        if form.is_valid():
            # про уникальность ничего не сказано
            category, insert = Categories.objects.get_or_create(name=form.cleaned_data['categories'])
            # обработка "ошибки", если нужно
            print("Вставка новой категории: ", insert)
        else:
            print(json.dumps(form.errors))
        # "очистим" запрос с браузера
        return HttpResponseRedirect(request.get_full_path())

    return render(request, "categories.html", {
        "form": FormCategories(),
        "back": True,
        "categories": Categories.objects.all()
    })


def categories_del(request, id_categories):
    Categories.objects.get(id=id_categories).delete()
    # request.META.get('HTTP_REFERER'); спорный редирект
    return HttpResponseRedirect("/categories/")


def view_month(request):
    dict_result = {}
    dict_categories = {}
    input_date = ""
    if request.method == "POST":
        form = FormExpensesMonth(request.POST)
        if form.is_valid():
            # получаем данные для таблицы
            input_date = form.cleaned_data['month']
            ans_expenses = Expenses.objects\
                .values('dateD', 'categories_id')\
                .filter(dateY=input_date.split(".")[1], dateM=input_date.split(".")[0])\
                .annotate(expenses_sum=Sum('expenses'))

            # преобразуем данные для быстро поиска + получим список используемых категорий
            dict_expenses = {}
            list_categories = []
            for val in ans_expenses:
                if val['dateD'] not in dict_expenses:
                    dict_expenses[val['dateD']] = {}
                if val['categories_id'] not in dict_expenses[val['dateD']]:
                    dict_expenses[val['dateD']][val['categories_id']] = {}
                # словарь на манер дерева
                dict_expenses[val['dateD']][val['categories_id']] = round(val['expenses_sum'], 2)
                # используемые категории
                list_categories.append(val['categories_id'])

            # получим названия для используемых категорий
            # потенциально можно сделать одним запросом, а нужно?
            list_categories = sorted(list_categories)
            ans_categories = Categories.objects.filter(id__in=list_categories).order_by("id")
            for val in ans_categories:
                dict_categories[val.id] = val.name

            # заполнение нулями пустых дней-категорий + псевдо сортировка
            # вариант без пустых дней-категорий (не особо ясен этот момент)
            for day_expenses in dict_expenses:
                if day_expenses not in dict_result:
                    dict_result[day_expenses] = {}
                for category in ans_categories:
                    if category.id in dict_categories:
                        if category.id in dict_expenses[day_expenses]:
                            dict_result[day_expenses][category.id] = dict_expenses[day_expenses][category.id]
                        else:
                            dict_result[day_expenses][category.id] = 0
            # для простоты чтения разделения логики (на деле можно объеденить с предыдущим циклом)
            # итоговые столбцы
            days_result = {}
            for day, day_expenses in dict_result.items():
                for id_categories, category_expense in day_expenses.items():
                    if id_categories not in days_result:
                        days_result[id_categories] = 0
                    days_result[id_categories] += category_expense
                dict_result[day]["0"] = sum(day_expenses.values())

            days_result["0"] = "Всего: {}".format(sum(days_result.values()))
            dict_result["Сумм категории"] = days_result
            dict_categories["0"] = "Сумм дни"
        else:
            print(json.dumps(form.errors))

    return render(request, "view.month.html", {
        "form": FormExpensesMonth(initial={'month': input_date}),
        "back": True,
        "categories": dict_categories,
        "expenses": dict_result
    })


def view_all(request):
    return render(request, "view.all.html", {
        'back': True,
        'expenses': Expenses.objects.get_expenses_months()
    })
