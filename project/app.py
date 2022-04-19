from functools import partial

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from project.components.exceptions import ServiceException
from project.components.exceptions import UnhandledException
from project.components.health import health_router
from project.components.project import project_router
from project.components.resource_request import resource_request_router
from project.components.workbench import workbench_router
from project.config import Settings
from project.config import get_settings


def create_app() -> FastAPI:
    """Initialize and configure the application."""

    settings = get_settings()

    app = FastAPI(
        title='Project Service',
        description='Service for managing projects.',
        docs_url='/v1/api-doc',
        version=settings.VERSION,
    )

    setup_routers(app)
    setup_middlewares(app, settings)
    setup_dependencies(app, settings)
    setup_exception_handlers(app)
    setup_tracing(app, settings)

    return app


def setup_routers(app: FastAPI) -> None:
    """Configure the application routers."""

    app.include_router(health_router, prefix='/v1')
    app.include_router(project_router, prefix='/v1')
    app.include_router(resource_request_router, prefix='/v1')
    app.include_router(workbench_router, prefix='/v1')


def setup_middlewares(app: FastAPI, settings: Settings) -> None:
    """Configure the application middlewares."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def setup_dependencies(app: FastAPI, settings: Settings) -> None:
    """Perform dependencies setup/teardown at the application startup/shutdown events."""

    app.add_event_handler('startup', partial(startup_event, settings))


async def startup_event(settings: Settings) -> None:
    """Initialise dependencies at the application startup event."""


def setup_exception_handlers(app: FastAPI) -> None:
    """Configure the application exception handlers."""

    app.add_exception_handler(ServiceException, service_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)


def service_exception_handler(request: Request, exception: ServiceException) -> JSONResponse:
    """Return the default response structure for service exceptions."""

    return JSONResponse(status_code=exception.status, content={'error': exception.dict()})


def unexpected_exception_handler(request: Request, exception: Exception) -> JSONResponse:
    """Return the default unhandled exception response structure for all unexpected exceptions."""

    return service_exception_handler(request, UnhandledException())


def setup_tracing(app: FastAPI, settings: Settings) -> None:
    """Instrument the application with OpenTelemetry tracing."""

    if not settings.OPEN_TELEMETRY_ENABLED:
        return

    tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: settings.APP_NAME}))
    trace.set_tracer_provider(tracer_provider)

    FastAPIInstrumentor.instrument_app(app)

    jaeger_exporter = JaegerExporter(
        agent_host_name=settings.OPEN_TELEMETRY_HOST, agent_port=settings.OPEN_TELEMETRY_PORT
    )

    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
