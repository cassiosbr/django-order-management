from django.urls import path

from customers.views import CustomersView

urlpatterns = [
    path('', CustomersView.as_view(), name='customers'),
]
