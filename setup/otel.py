from __future__ import annotations
import logging
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased


class OTLPLoggingHandler(LoggingHandler):
    def __init__(self, level=logging.INFO):
        global logger_provider
        if logger_provider is None:
            logger_provider = LoggerProvider(resource=resource)
            if OTEL_LOGS_ENDPOINT:
                logger_provider.add_log_record_processor(
                    BatchLogRecordProcessor(
                        OTLPLogExporter(endpoint=OTEL_LOGS_ENDPOINT, insecure=True)
                    )
                )
        super().__init__(level=level, logger_provider=logger_provider)

SERVICE_NAME_VALUE = os.getenv("OTEL_SERVICE_NAME", "django-order-management")
OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
OTEL_LOGS_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_LOGS_ENDPOINT", "otel-collector:4317")
SAMPLER_RATIO = float(os.getenv("OTEL_TRACES_SAMPLER_ARG", "1.0"))

os.environ.setdefault("OTEL_PYTHON_DJANGO_EXCLUDED_URLS", "/metrics,/metrics/")

resource = Resource.create({SERVICE_NAME: SERVICE_NAME_VALUE})
logger_provider = None
provider = TracerProvider(
    resource=resource,
    sampler=ParentBased(TraceIdRatioBased(SAMPLER_RATIO)),
)

if OTEL_ENDPOINT:
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=OTEL_ENDPOINT)
        )
    )
else:
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

trace.set_tracer_provider(provider)

# Instrumentação de logging
LoggingInstrumentor().instrument(set_logging_format=True)

DjangoInstrumentor().instrument()
CeleryInstrumentor().instrument()
Psycopg2Instrumentor().instrument()
RedisInstrumentor().instrument()
