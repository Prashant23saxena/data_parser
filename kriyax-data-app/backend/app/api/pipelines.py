from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services import pipelines

router = APIRouter()


class CreatePipelineRequest(BaseModel):
    pipelineName: str = Field(min_length=1, max_length=80)
    scriptId: str = Field(min_length=1)
    connectorSyncId: str | None = None


class SetPipelineEnabledRequest(BaseModel):
    enabled: bool


class SetPipelineScheduleRequest(BaseModel):
    type: str = Field(min_length=1)
    cronExpression: str | None = None
    timeOfDay: str | None = None
    weekday: str | None = None
    timezone: str | None = None


@router.post("")
def create_pipeline(request: CreatePipelineRequest) -> dict[str, object]:
    try:
        return pipelines.create_pipeline(
            pipeline_name=request.pipelineName,
            script_id=request.scriptId,
            connector_sync_id=request.connectorSyncId,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("")
def list_pipelines() -> dict[str, list[dict[str, object]]]:
    return {"pipelines": pipelines.list_pipelines()}


@router.get("/runs")
def list_all_pipeline_runs(status: str = "all") -> dict[str, list[dict[str, object]]]:
    return {"runs": pipelines.list_runs(status_filter=status)}


@router.get("/failures")
def list_pipeline_failures(activeOnly: bool = True) -> dict[str, list[dict[str, object]]]:
    return {"failures": pipelines.list_failures(active_only=activeOnly)}


@router.post("/failures/{run_id}/ack")
def acknowledge_pipeline_failure(run_id: str) -> dict[str, object]:
    try:
        return pipelines.acknowledge_failure(run_id)
    except ValueError as exc:
        status_code = 404 if str(exc) == "Pipeline run not found." else 400
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc


@router.patch("/{pipeline_id}/enabled")
def set_pipeline_enabled(pipeline_id: str, request: SetPipelineEnabledRequest) -> dict[str, object]:
    try:
        return pipelines.set_pipeline_enabled(pipeline_id, request.enabled)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/{pipeline_id}/schedule")
def set_pipeline_schedule(pipeline_id: str, request: SetPipelineScheduleRequest) -> dict[str, object]:
    try:
        payload = request.model_dump(exclude_none=True)
        pipeline = pipelines.set_pipeline_schedule(pipeline_id, payload)
        return {"schedule": pipeline["schedule"]}
    except ValueError as exc:
        status_code = 404 if str(exc) == "Pipeline not found." else 400
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc


@router.post("/{pipeline_id}/run")
def run_pipeline_now(pipeline_id: str) -> dict[str, object]:
    try:
        return pipelines.run_pipeline_now(pipeline_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{pipeline_id}/runs")
def list_pipeline_runs(pipeline_id: str, status: str = "all") -> dict[str, list[dict[str, object]]]:
    return {"runs": pipelines.list_runs(pipeline_id, status_filter=status)}


@router.get("/runs/{run_id}")
def get_pipeline_run(run_id: str) -> dict[str, object]:
    try:
        return pipelines.get_run(run_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
