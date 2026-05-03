from fastapi import APIRouter

router = APIRouter()


SCREENS = [
    {"id": "S-01", "route": "/", "name": "Home / Operations Overview"},
    {"id": "S-02", "route": "/connectors", "name": "Connectors"},
    {"id": "S-03", "route": "/connectors/file-import", "name": "File Import Wizard"},
    {"id": "S-04", "route": "/connectors/odoo", "name": "Odoo Import Workspace"},
    {"id": "S-05", "route": "/catalog", "name": "Catalog"},
    {"id": "S-06", "route": "/catalog/table", "name": "Table Detail"},
    {"id": "S-07", "route": "/catalog/table/manage", "name": "Table Management Confirmation"},
    {"id": "S-08", "route": "/catalog/table/export", "name": "Export Table Modal"},
    {"id": "S-09", "route": "/code", "name": "Code Workspace"},
    {"id": "S-10", "route": "/code/agent", "name": "Agent Panel"},
    {"id": "S-11", "route": "/scripts", "name": "Saved Scripts"},
    {"id": "S-12", "route": "/pipelines", "name": "Pipelines"},
    {"id": "S-13", "route": "/pipelines/run", "name": "Pipeline Run Detail"},
    {"id": "S-14", "route": "/storage", "name": "Storage Settings"},
]


@router.get("")
def list_screens() -> dict[str, list[dict[str, str]]]:
    return {"screens": SCREENS}
