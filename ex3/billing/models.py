from django.db import models


class Accrual(models.Model):
    date = models.DateField()
    month = models.IntegerField()

    class Meta:
        ordering = ["date"]


class Payment(models.Model):
    date = models.DateField()
    month = models.IntegerField()
    accrual = models.ForeignKey(
        Accrual,
        on_delete=models.SET_NULL,
        default=None,
        null=True
    )

    class Meta:
        ordering = ["date"]

