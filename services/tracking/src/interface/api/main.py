from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.metrics import setup_metrics
from shared.tracing import setup_tracing
from .routes import router
from ...infrastructure.messaging.kafka_producer import kafka_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_manager.start()
    yield
    await kafka_manager.stop()


app = FastAPI(
    title="User Data Tracking Service",
    docs_url="/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_metrics(app)
setup_tracing(app)

app.include_router(router)
