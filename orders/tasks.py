from celery import shared_task

import time
from pathlib import Path

from opentelemetry import trace

from .models import Order, OrderStatus

import logging

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


@shared_task(auto_retry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def process_new_order(order_id):
    with tracer.start_as_current_span("process_new_order") as span:
        logger.info("Iniciando processamento de novo pedido %s", order_id)
        span.set_attribute("order.id", order_id)

        time.sleep(5)

        with tracer.start_as_current_span("db.fetch_order"):
            order = Order.objects.get(id=order_id)

        send_order_confirmation_email(order)

        create_invoice_preview(order)


@shared_task(auto_retry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        logger.info("Iniciando processamento do pedido %s", order_id)
        span.set_attribute("order.id", order_id)

        time.sleep(5)

        with tracer.start_as_current_span("db.fetch_order"):
            order = Order.objects.get(id=order_id)

        # State Machine (Máquina de estados) - Evitar processamento de pedidos não pagos.
        if order.status != OrderStatus.PAID:
            logger.info(
                "Pedido %s ignorado. Status atual: %s",
                order.id,
                order.status,
            )
            span.set_attribute("order.status", str(order.status))
            return

        send_order_confirmation_email(order)

        create_invoice(order)

        update_order_status(order, OrderStatus.PROCESSING)

        # update_order_status(order, OrderStatus.SHIPPED)

        # update_order_status(order, OrderStatus.DELIVERED)


def create_invoice_preview(order):
    with tracer.start_as_current_span("create_invoice_preview") as span:
        folder = Path("invoices")
        folder.mkdir(exist_ok=True)

        invoice = folder / f"invoice_preview_{order.id}.txt"

        invoice.write_text(
            f"""
            Pedido: {order.id}

            Status: Preview
            """
        )

        logger.info("Pré-visualização da fatura criada para o pedido %s em %s", order.id, invoice)
        span.set_attribute("order.id", order.id)
        span.set_attribute("invoice.path", str(invoice))


def send_order_confirmation_email(order):
    with tracer.start_as_current_span("send_order_confirmation_email") as span:
        logger.info("E-mail enviado para %s confirmando o pedido %s", order.customer, order.id)
        span.set_attribute("order.id", order.id)
        span.set_attribute("order.customer", str(order.customer))
        return order


def create_invoice(order):
    with tracer.start_as_current_span("create_invoice") as span:
        folder = Path("invoices")
        folder.mkdir(exist_ok=True)

        invoice = folder / f"invoice_{order.id}.txt"

        invoice.write_text(
            f"""
            Pedido: {order.id}

            Cliente: {order.customer}

            Status: {order.status}
            """
        )

        logger.info("Fatura criada para o pedido %s em %s", order.id, invoice)
        span.set_attribute("order.id", order.id)
        span.set_attribute("invoice.path", str(invoice))


def update_order_status(order, status):
    with tracer.start_as_current_span("update_order_status") as span:
        time.sleep(5)
        order.status = status
        order.save()
        logger.info("Pedido %s atualizado para %s", order.id, status)
        span.set_attribute("order.id", order.id)
        span.set_attribute("order.status", str(status))
