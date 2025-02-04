"""
Module to configure tracing instrumentation with OpenTelemetry in FastAPI applications.
"""

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracing(app: FastAPI) -> None:
    """
    Configure traceability in a FastAPI application.

    Args:
        app (FastAPI): FastAPI application instance.
    """
    provider = TracerProvider()
    trace.set_tracer_provider(provider)
    otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
    span_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)
    FastAPIInstrumentor.instrument_app(app)
