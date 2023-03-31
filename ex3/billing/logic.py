from django.db import transaction


class UnionOrder():
    """Совершает поиск платежей для долгов"""

    def __init__(self, class_payment, class_accrual):
        self.class_payment = class_payment
        self.class_accrual = class_accrual
        self.payments = self.get_payment(class_payment)
        self.accruals = self.get_accrual(class_accrual, class_payment)

    @classmethod
    def get_payment(cls, class_payment):
        """Запрос платежей с учётом уже обработанных платежей"""

        payments = class_payment.objects.filter(accrual__isnull=True).order_by("date").values()
        return payments

    @classmethod
    def get_accrual(cls, class_accrual, class_payment):
        """Запрос долгов с учётом уже присвоенных к платежам"""

        # Получаем список ID занятых долгов
        id_rezerved_acc = class_payment.objects.filter(accrual__isnull=False).values_list("accrual_id", flat=True)
        # Ищем по нему свободные долги
        accruals = list(class_accrual.objects.exclude(id__in=id_rezerved_acc).order_by("date").values())

        return accruals

    def search_payment_in_month_and_date(self):
        """С начало поиск оплат и долгов по месяцу и дате"""

        for payment in self.payments:
            if payment["accrual_id"]:
                continue
            for index in range(len(self.accruals)):
                if self.accruals[index]["month"] == payment["month"] and payment["date"] > self.accruals[index]["date"]:
                    payment["accrual_id"] = self.accruals[index]["id"]
                    self.accruals.pop(index)
                    break

    def search_payment_in_date(self):
        """Далее поиск только по дате"""

        for payment in self.payments:
            if payment["accrual_id"]:
                continue
            for index in range(len(self.accruals)):
                if payment["date"] > self.accruals[index]["date"]:
                    payment["accrual_id"] = self.accruals[index]["id"]
                    self.accruals.pop(index)
                    break

    def update_payment_bd(self):
        """Обновление данных в БД"""

        with transaction.atomic():
            for payment in self.payments:
                if payment["accrual_id"]:
                    pk = payment["id"]
                    accrual = payment["accrual_id"]
                    self.class_payment.objects.filter(pk=pk).update(accrual=accrual)

    def get_update_payments(self):
        self.search_payment_in_month_and_date()
        self.search_payment_in_date()
        self.update_payment_bd()

        payments = self.class_payment.objects.select_related("accrual").all()

        return payments
