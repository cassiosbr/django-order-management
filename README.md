# Django Order Management

Backend desenvolvido com Django REST Framework para gerenciamento de pedidos, utilizando PostgreSQL, Redis, Celery, Webhooks e observabilidade com OpenTelemetry.

## Tecnologias

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker
- OpenTelemetry

## Principais Recursos

- API REST para gerenciamento de pedidos
- Processamento assíncrono com Celery
- Cache com Redis
- Webhook para confirmação de pagamento
- Transações atômicas (`transaction.atomic`)
- Processamento pós-commit (`transaction.on_commit`)
- Observabilidade completa (Logs, Métricas e Traces)

## Observabilidade

- Instrumentação distribuída com **OpenTelemetry**
- Coleta e exportação de telemetria com **OpenTelemetry Collector**
- Métricas com **Prometheus**
- Dashboards com **Grafana**
- Tracing distribuído com **Grafana Tempo**
- Logs centralizados com **Grafana Loki**

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
```

## Arquitetura de Observabilidade

```text
                 OpenTelemetry
                       │
                       ▼
               OpenTelemetry Collector
                 ┌────────┼────────┐
                 ▼        ▼        ▼
            Prometheus   Tempo    Loki
                 │        │        │
                 └────────┴────────┘
                          │
                          ▼
                       Grafana
```

## Boas Práticas Implementadas

- Arquitetura em camadas (Views, Services e Tasks)
- Separação entre processamento síncrono e assíncrono
- Uso de `transaction.atomic` para garantir consistência
- Uso de `transaction.on_commit` para evitar envio de mensagens antes da confirmação da transação
- Cache com Redis para otimização de consultas
- Instrumentação distribuída com OpenTelemetry
- Correlação entre Logs, Métricas e Traces