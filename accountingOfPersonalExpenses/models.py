from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=255)


# сделаем date через избыточность данных
class Expenses(models.Model):
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    date = models.DateField()
    dateD = models.PositiveSmallIntegerField()
    dateM = models.PositiveSmallIntegerField()
    dateY = models.PositiveSmallIntegerField()
    expenses = models.DecimalField(max_digits=12, decimal_places=2)



