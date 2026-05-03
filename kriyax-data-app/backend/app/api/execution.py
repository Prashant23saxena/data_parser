from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.execution import get_script, list_scripts, run_script

router = APIRouter()


class RunScriptRequest(BaseModel):
    scriptName: str = Field(min_length=1)
    code: str = Field(min_length=1)


@router.post("/run")
def run_python_script(request: RunScriptRequest) -> dict[str, object]:
    return run_script(script_name=request.scriptName, code=request.code)


@router.get("/scripts")
def get_saved_scripts() -> dict[str, list[dict[str, object]]]:
    return {"scripts": list_scripts()}


@router.get("/scripts/{script_name}")
def get_saved_script(script_name: str) -> dict[str, object]:
    try:
        return get_script(script_name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
