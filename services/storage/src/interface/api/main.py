from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.metrics import setup_metrics
from shared.tracing import setup_tracing
from .routes import router

app = FastAPI(
    title="Storage Service",
    docs_url="/docs",
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

app.include_router(router, prefix="/api")
