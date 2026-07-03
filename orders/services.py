import logging

from django.db import transaction
from opentelemetry import trace

from .models import Order, OrderItem
from .tasks import process_new_order


logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


class OrderService:

    @transaction.atomic
    def create_order(self, validated_data):
        with tracer.start_as_current_span("create_order") as span:
            total_amount = sum(
                item["product"].price * item["quantity"] for item in validated_data["items"]
            )

            with tracer.start_as_current_span("db.create_order"):
                order = Order.objects.create(
                    customer=validated_data["customer"],
                    total_amount=total_amount
                )

            with tracer.start_as_current_span("db.create_order_items") as db_span:
                for item in validated_data["items"]:
                    OrderItem.objects.create(
                        order=order,
                        product=item["product"],
                        quantity=item["quantity"],
                        unit_price=item["product"].price
                    )
                db_span.set_attribute("order.items_count", len(validated_data["items"]))

            span.set_attribute("order.id", order.id)
            span.set_attribute("order.total_amount", float(total_amount))
            span.set_attribute("order.items_count", len(validated_data["items"]))

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
