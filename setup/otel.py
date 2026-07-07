from __future__ import annotations
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased

SERVICE_NAME_VALUE = os.getenv("OTEL_SERVICE_NAME", "django-order-management")
OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
SAMPLER_RATIO = float(os.getenv("OTEL_TRACES_SAMPLER_ARG", "0.1"))

os.environ.setdefault("OTEL_PYTHON_DJANGO_EXCLUDED_URLS", "/metrics,/metrics/")

resource = Resource.create({SERVICE_NAME: SERVICE_NAME_VALUE})
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

DjangoInstrumentor().instrument()
CeleryInstrumentor().instrument()
Psycopg2Instrumentor().instrument()
RedisInstrumentor().instrument()
