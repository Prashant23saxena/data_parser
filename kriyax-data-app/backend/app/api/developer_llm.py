from fastapi import APIRouter, Query

from app.llm.schemas import LLMProfileCreate, LLMTestRequest, LlmProvider, VaultKeyRequest
from app.services import developer_llm

router = APIRouter()


@router.get("/config")
def get_config(provider: LlmProvider | None = Query(default=None)) -> dict[str, object]:
    return developer_llm.get_config(provider)


@router.post("/vault-key")
def save_vault_key(payload: VaultKeyRequest) -> dict[str, object]:
    return developer_llm.save_vault_key(
        payload.provider,
        api_key=payload.api_key,
        model=payload.model,
        base_url=payload.base_url,
    )


@router.post("/test")
def test_llm(payload: LLMTestRequest) -> dict[str, object]:
    return developer_llm.test_llm(payload)


@router.post("/playground")
def playground(payload: LLMTestRequest) -> dict[str, object]:
    return developer_llm.playground(payload)


@router.get("/profiles")
def get_profiles() -> dict[str, object]:
    return {"items": developer_llm.list_profiles()}


@router.post("/profiles")
def create_profile(payload: LLMProfileCreate) -> dict[str, object]:
    return developer_llm.create_profile(payload)


@router.post("/profiles/{profile_id}/default")
def set_default_profile(profile_id: str) -> dict[str, object]:
    return developer_llm.set_default_profile(profile_id)


@router.delete("/profiles/{profile_id}")
def delete_profile(profile_id: str) -> dict[str, object]:
    return developer_llm.delete_profile(profile_id)


@router.get("/audit")
def get_audit() -> dict[str, object]:
    return developer_llm.list_audit()


@router.post("/clear-vault")
def clear_vault() -> dict[str, object]:
    return developer_llm.clear_vault()
