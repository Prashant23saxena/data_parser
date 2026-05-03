from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any

from app.services import odoo

router = APIRouter()


class OdooConnectionRequest(BaseModel):
    connectionName: str = Field(min_length=1, max_length=64)
    odooUrl: str = Field(min_length=1)
    dbName: str = Field(min_length=1)
    username: str = Field(min_length=1)
    apiKey: str = Field(min_length=1)


class OdooFetchRequest(BaseModel):
    connection: OdooConnectionRequest
    modelName: str = Field(min_length=1)
    fields: list[str] = Field(min_length=1)
    targetSchema: str = Field(default="raw_odoo", min_length=1)
    tableName: str = Field(min_length=1)
    domainFilter: list[Any] = Field(default_factory=list)
    recordLimit: int = Field(default=0, ge=0)
    cursorField: str | None = None


class OdooSyncCursorRequest(BaseModel):
    connection: OdooConnectionRequest
    modelName: str = Field(min_length=1)
    fields: list[str] = Field(min_length=1)
    targetSchema: str = Field(default="raw_odoo", min_length=1)
    tableName: str = Field(min_length=1)
    cursorField: str = "write_date"
    domainFilter: list[Any] = Field(default_factory=list)
    recordLimit: int = Field(default=0, ge=0)


@router.post("/test-connection")
def test_odoo_connection(request: OdooConnectionRequest) -> dict[str, object]:
    return odoo.test_connection(request.model_dump())


@router.post("/connections")
def create_odoo_connection(request: OdooConnectionRequest) -> dict[str, object]:
    try:
        return odoo.save_connection(request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/connections")
def get_odoo_connections() -> dict[str, list[dict[str, object]]]:
    return {"connections": odoo.list_connections()}


@router.post("/models")
def list_odoo_models(request: OdooConnectionRequest, search: str | None = None) -> dict[str, list[dict[str, object]]]:
    try:
        return {"models": odoo.list_models(request.model_dump(), search_query=search)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/models/{model_name}/fields")
def get_odoo_model_fields(model_name: str, request: OdooConnectionRequest) -> dict[str, list[dict[str, object]]]:
    try:
        return {"fields": odoo.get_model_fields(request.model_dump(), model_name)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/fetch")
def fetch_odoo_records(request: OdooFetchRequest) -> dict[str, object]:
    try:
        return odoo.fetch_records_to_table(
            request.connection.model_dump(),
            model_name=request.modelName,
            fields=request.fields,
            target_schema=request.targetSchema,
            table_name=request.tableName,
            domain_filter=request.domainFilter,
            record_limit=request.recordLimit,
            cursor_field=request.cursorField,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/sync-cursors")
def create_odoo_sync_cursor(request: OdooSyncCursorRequest) -> dict[str, object]:
    try:
        return odoo.create_sync_cursor(
            request.connection.model_dump(),
            model_name=request.modelName,
            fields=request.fields,
            target_schema=request.targetSchema,
            table_name=request.tableName,
            cursor_field=request.cursorField,
            domain_filter=request.domainFilter,
            record_limit=request.recordLimit,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/sync/{sync_cursor_id}")
def sync_odoo_cursor(sync_cursor_id: str) -> dict[str, object]:
    try:
        return odoo.sync_cursor(sync_cursor_id)
    except ValueError as exc:
        status_code = 404 if str(exc) == "Sync cursor not found." else 400
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc
