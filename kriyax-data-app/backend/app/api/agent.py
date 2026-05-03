from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services import agent

router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1)
    includeSamples: bool = False


class CorrectRequest(BaseModel):
    code: str = Field(min_length=1)
    traceback: str = Field(min_length=1)
    attempt: int = Field(default=1, ge=1)


class FollowUpRequest(BaseModel):
    prompt: str = Field(min_length=1)
    priorCode: str | None = None


@router.post("/generate")
def generate_code(request: GenerateRequest) -> dict[str, object]:
    try:
        return agent.generate_code(request.prompt, include_samples=request.includeSamples)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/correct")
def correct_code(request: CorrectRequest) -> dict[str, object]:
    try:
        return agent.correct_code(request.code, request.traceback, attempt=request.attempt)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/follow-up")
def follow_up(request: FollowUpRequest) -> dict[str, object]:
    try:
        return agent.follow_up(request.prompt, prior_code=request.priorCode)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
