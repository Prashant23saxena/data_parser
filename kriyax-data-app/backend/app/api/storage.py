from fastapi import APIRouter

from app.services.storage import storage_status
from app.services.workspace import ensure_workspace

router = APIRouter()


@router.get("/status")
def get_storage_status() -> dict[str, object]:
    return storage_status()


@router.post("/bootstrap")
def bootstrap_storage() -> dict[str, object]:
    paths = ensure_workspace()
    return {"status": "ready", "paths": paths}
