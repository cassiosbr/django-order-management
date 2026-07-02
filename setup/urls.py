from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('customers/', include('customers.urls')), 
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('admin/', admin.site.urls),
]
