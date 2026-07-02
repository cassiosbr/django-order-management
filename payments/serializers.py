from rest_framework import serializers


class PaymentWebhookSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    status = serializers.ChoiceField(
        choices=["approved", "failed"]
    )
