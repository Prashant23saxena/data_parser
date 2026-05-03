from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field

from app.services.file_import import drop_table, export_table_csv, list_catalog_tables, preview_table, rename_table, truncate_table

router = APIRouter()


class RenameTableRequest(BaseModel):
    newTableName: str = Field(min_length=1)


class ConfirmTableRequest(BaseModel):
    confirmation: str = Field(min_length=1)


@router.get("/tables")
def list_tables() -> dict[str, list[dict[str, object]]]:
    return {"tables": list_catalog_tables()}


@router.patch("/tables/{schema}/{table_name}/rename")
def rename_catalog_table(schema: str, table_name: str, request: RenameTableRequest) -> dict[str, object]:
    try:
        return rename_table(schema, table_name, request.newTableName)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/tables/{schema}/{table_name}/truncate")
def truncate_catalog_table(schema: str, table_name: str, request: ConfirmTableRequest) -> dict[str, object]:
    try:
        return truncate_table(schema, table_name, request.confirmation)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/tables/{schema}/{table_name}")
def drop_catalog_table(schema: str, table_name: str, request: ConfirmTableRequest) -> dict[str, object]:
    try:
        return drop_table(schema, table_name, request.confirmation)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/tables/{schema}/{table_name}/export")
def export_catalog_table(schema: str, table_name: str) -> Response:
    try:
        filename, csv_text = export_table_csv(schema, table_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/tables/{schema}/{table_name}/preview")
def get_table_preview(schema: str, table_name: str) -> dict[str, object]:
    return preview_table(schema, table_name)
