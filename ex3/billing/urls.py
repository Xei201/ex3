from django.urls import path

from billing import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name="list-payment"),
]