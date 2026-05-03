from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.services.file_import import commit_import, inspect_file
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
        return inspect_file(target_path, display_name=original_name)
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


def _validated_upload_path(value: str) -> Path:
    uploads = workspace_paths()["uploads"].resolve()
    file_path = Path(value).resolve()
    if uploads not in file_path.parents:
        raise HTTPException(status_code=400, detail="Import file must be inside the uploads folder.")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Uploaded file was not found.")
    return file_path
