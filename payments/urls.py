from django.urls import path

from payments.views import PaymentWebhookView

urlpatterns = [
    path('', PaymentWebhookView.as_view(), name='payments_webhook'),
]