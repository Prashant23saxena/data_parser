from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.services.file_import import (
    commit_import,
    delete_import_draft,
    get_import_draft,
    inspect_file,
    list_import_drafts,
    save_import_draft,
)
from app.services.workspace import ensure_workspace, workspace_paths

router = APIRouter()


class ImportColumn(BaseModel):
    sourceIndex: int
    sourceName: str
    targetName: str
    inferredType: str
    selectedType: str = "text"
    status: str = "ready"


class CommitImportRequest(BaseModel):
    filePath: str
    targetSchema: str = Field(min_length=1)
    tableName: str = Field(min_length=1)
    columns: list[ImportColumn]
    draftId: str | None = None


@router.post("/upload")
async def upload_file(file: UploadFile) -> dict[str, object]:
    ensure_workspace()
    original_name = Path(file.filename or "upload.csv").name
    suffix = Path(original_name).suffix.lower()
    if suffix not in {".csv", ".xlsx"}:
        raise HTTPException(status_code=400, detail="Only CSV and XLSX files are supported.")

    target_path = workspace_paths()["uploads"] / f"{uuid4().hex}-{original_name}"
    target_path.write_bytes(await file.read())

    try:
        inspection = inspect_file(target_path, display_name=original_name)
        draft = save_import_draft(inspection)
        return {**inspection, "draftId": draft["id"], "draft": draft}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/commit")
def commit_file_import(request: CommitImportRequest) -> dict[str, object]:
    file_path = _validated_upload_path(request.filePath)
    try:
        return commit_import(
            file_path=file_path,
            target_schema=request.targetSchema,
            table_name=request.tableName,
            columns=[column.model_dump() for column in request.columns],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/drafts")
def get_import_drafts() -> dict[str, list[dict[str, object]]]:
    return {"drafts": list_import_drafts()}


@router.get("/drafts/{draft_id}")
def resume_import_draft(draft_id: str) -> dict[str, object]:
    try:
        return get_import_draft(draft_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/drafts/{draft_id}")
def remove_import_draft(draft_id: str) -> dict[str, object]:
    try:
        return delete_import_draft(draft_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


def _validated_upload_path(value: str) -> Path:
    uploads = workspace_paths()["uploads"].resolve()
    file_path = Path(value).resolve()
    if uploads not in file_path.parents:
        raise HTTPException(status_code=400, detail="Import file must be inside the uploads folder.")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Uploaded file was not found.")
    return file_path
