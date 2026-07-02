import logging

from django.db import transaction

from .models import Order, OrderItem
from .tasks import process_new_order


logger = logging.getLogger(__name__)


class OrderService:

    @transaction.atomic
    def create_order(self, validated_data):

        total_amount = sum(
            item["product"].price * item["quantity"] for item in validated_data["items"]
        )
        
        order = Order.objects.create(
            customer=validated_data["customer"],
            total_amount=total_amount
        )

        for item in validated_data["items"]:

            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                unit_price=item["product"].price
            )

        # Dispara a task apos commit; se fila indisponivel nao quebra a API.
        def enqueue_order_task():
            try:
                process_new_order.delay(order.id)
            except Exception as exc:
                logger.warning(
                    'Falha ao enfileirar processamento do pedido %s: %s',
                    order.id,
                    exc,
                )

        transaction.on_commit(enqueue_order_task)

        return order