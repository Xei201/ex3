from django.contrib import admin

from .models import Accrual, Payment


@admin.register(Accrual)
class AccrualAdmin(admin.ModelAdmin):
    list_display = ("date", "month")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("date", "month")