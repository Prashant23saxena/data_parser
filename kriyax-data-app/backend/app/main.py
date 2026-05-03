from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.catalog import router as catalog_router
from app.api.agent import router as agent_router
from app.api.developer_llm import router as developer_llm_router
from app.api.execution import router as execution_router
from app.api.imports import router as imports_router
from app.api.llm import router as llm_router
from app.api.odoo import router as odoo_router
from app.api.pipelines import router as pipelines_router
from app.api.screens import router as screens_router
from app.api.storage import router as storage_router
from app.services.pipeline_scheduler import start_scheduler
from app.services.workspace import ensure_workspace

app = FastAPI(title="KriyaX Data Layer API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def bootstrap_workspace() -> None:
    ensure_workspace()
    start_scheduler()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "kriyax-data-layer"}


app.include_router(storage_router, prefix="/api/storage", tags=["storage"])
app.include_router(screens_router, prefix="/api/screens", tags=["screens"])
app.include_router(catalog_router, prefix="/api/catalog", tags=["catalog"])
app.include_router(agent_router, prefix="/api/agent", tags=["agent"])
app.include_router(imports_router, prefix="/api/imports", tags=["imports"])
app.include_router(execution_router, prefix="/api/execution", tags=["execution"])
app.include_router(odoo_router, prefix="/api/odoo", tags=["odoo"])
app.include_router(pipelines_router, prefix="/api/pipelines", tags=["pipelines"])
app.include_router(llm_router, prefix="/api/llm", tags=["llm"])
app.include_router(developer_llm_router, prefix="/api/v1/developer/llm", tags=["developer-llm"])
