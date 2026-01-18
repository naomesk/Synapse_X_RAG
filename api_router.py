from fastapi import APIRouter
from query_controller import router as query_router
from ingestion_controller import router as ingestion_router

router = APIRouter()

router.include_router(
    query_router,
    prefix="/query",
    tags=["Query"]
)

router.include_router(
    ingestion_router,
    prefix="/ingest",
    tags=["Ingestion"]
)
