from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracing(app):
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer_provider()
    otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")

    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer.add_span_processor(span_processor)

    FastAPIInstrumentor.instrument_app(app)
