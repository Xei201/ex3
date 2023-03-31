from django.views import generic

from .logic import UnionOrder
from .models import Accrual, Payment


class OrderListView(generic.ListView):

    template_name = 'list_payments.html'
    context_object_name = "payments"

    def get_queryset(self):
        orders = UnionOrder(Payment, Accrual)
        payments = orders.get_update_payments()

        return payments
