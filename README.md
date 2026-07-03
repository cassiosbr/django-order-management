# Django Order Management

Backend desenvolvido com Django REST Framework para gerenciamento de pedidos, utilizando PostgreSQL, Redis, Celery, Webhooks e OpenTelemetry.

## Tecnologias

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker
- OpenTelemetry
- Jaeger

## Arquitetura do Fluxo de Pedidos

```text
Cliente
   │
   ▼
POST /orders
   │
   ▼
OrderService
   │
transaction.atomic
   │
   ▼
PostgreSQL
   │
transaction.on_commit
   │
   ▼
Redis (Broker)
   │
   ▼
Celery Worker
   ├── Envio de e-mail
   ├── Geração de nota fiscal
   └── Atualização de status
         │
         ▼
Webhook de Pagamento
         │
         ▼
Novo processamento assíncrono
