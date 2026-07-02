import logging

from django.db import transaction

from orders.models import Order, OrderStatus

from orders.tasks import process_order

logger = logging.getLogger(__name__)


class PaymentService:

    @transaction.atomic
    def confirm_payment(self, validated_data):

        order = Order.objects.get(
            id=validated_data["order_id"]
        )

        if validated_data['status'] != 'approved':
            logger.info(
                "Pagamento do pedido %s não aprovado. Status: %s",
                order.id,
                validated_data['status'],
            )
            return

        # idepotência: se o pagamento for confirmado mais de uma vez, não processa novamente.
        if order.status != OrderStatus.PENDING_PAYMENT:
            logger.info(
            "Pedido %s já foi processado. Status: %s",
            order.id,
            order.status,
            )
            return

        order.status = OrderStatus.PAID
        order.save(update_fields=["status"])

        transaction.on_commit(
            lambda: process_order.delay(order.id)
        )

        return order