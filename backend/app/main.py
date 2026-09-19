from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.logging_config import setup_logging

setup_logging()

from app.core.config import settings
from app.api.routes import query
from app.services import retrieval


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: runs once, before the app starts accepting requests
    print("Loading vector store...")
    retrieval.load_vector_store()
    print("Vector store loaded. Ready to serve requests.")

    yield  # the app runs here, handling requests, until shutdown

    # Shutdown: runs once, when the server is stopping
    print("Shutting down.")


app = FastAPI(
    title="NutriChat API",
    description="RAG-powered nutrition assistant backend",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)