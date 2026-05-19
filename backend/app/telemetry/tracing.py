from opentelemetry import trace

from opentelemetry.sdk.resources import (
    SERVICE_NAME,
    Resource,
)

from opentelemetry.sdk.trace import (
    TracerProvider,
)

from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

resource = Resource.create({SERVICE_NAME: "enterprise-ai-ka"})

provider = TracerProvider(resource=resource)

processor = BatchSpanProcessor(ConsoleSpanExporter())

provider.add_span_processor(processor)

trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)
