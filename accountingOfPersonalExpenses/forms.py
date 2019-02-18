from django import forms
from django.db.models import Count
from .models import Expenses, Categories


class FormExpenses(forms.Form):
    categories = forms.ChoiceField(
        choices=(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Категория"
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control datepicker"}),
        input_formats=('%d-%m-%Y',),
        label="Дата"
    )
    expenses = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Расход",
        min_value=0.01,
        max_value=1e9,
        decimal_places=2
    )

    def __init__(self, *args, **kwargs):
        super(FormExpenses, self).__init__(*args, **kwargs)
        self.fields["categories"].choices = tuple(Categories.objects.values_list(named=True).all())


class FormCategories(forms.Form):
    categories = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Категория",
        max_length=255
    )


class FormExpensesMonth(forms.Form):
    month = forms.ChoiceField(
        choices=(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Месяц"
    )

    def __init__(self, *args, **kwargs):
        super(FormExpensesMonth, self).__init__(*args, **kwargs)
        # orm без агрегатной функции никак не хочет делать group by
        # возможно, имеет смысл перенести это во views, но с точки зрения логики это более верно
        # скорее всего подход не особо правильный, но в документации ничего нет
        # (https://docs.djangoproject.com/en/2.1/ref/forms/api/#bound-and-unbound-forms)
        ans_form = Expenses.objects.values('dateY', 'dateM').order_by('dateY', 'dateM').annotate(Count('dateY'))
        list_form = []
        for val in ans_form:
            temp = '{}.{}'.format(val["dateM"], val["dateY"])
            list_form.append([temp, temp])
        self.fields["month"].choices = list_form
