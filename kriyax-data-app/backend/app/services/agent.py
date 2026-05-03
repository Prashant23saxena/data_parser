import re
from typing import Any

from app.services.file_import import list_catalog_tables
from app.services.llm_gateway import complete_text, runtime_status


def generate_code(prompt: str, include_samples: bool = False) -> dict[str, Any]:
    context = _schema_context(include_samples=include_samples)
    llm_code = _llm_code(
        "Generate only executable Python code for this KriyaX data workspace. "
        "Available helpers: load_table(name), save_table(df, name, schema='curated'), show(df, name='result'). "
        f"Catalog context: {context}. User request: {prompt.strip()}"
    )
    if llm_code:
        return {
            "status": "success",
            "message": "Generated Python code with configured LLM.",
            "code": llm_code,
            "schemaContext": context,
            "runtime": runtime_status(),
        }
    raise ValueError("LLM_KEY_MISSING: Configure an API key before running agent generation.")


def correct_code(code: str, traceback: str, attempt: int = 1) -> dict[str, Any]:
    if attempt > 3:
        raise ValueError("Maximum correction attempts reached.")
    llm_code = _llm_code(
        "Correct this Python data-workspace script. Return only executable Python code. "
        f"Script:\n{code}\n\nTraceback:\n{traceback}"
    )
    if llm_code:
        return {
            "status": "success",
            "message": "Generated correction with configured LLM.",
            "code": llm_code,
            "attempt": attempt,
            "tracebackSummary": traceback.strip().splitlines()[-1] if traceback.strip() else "No traceback supplied.",
            "runtime": runtime_status(),
        }
    raise ValueError("LLM_KEY_MISSING: Configure an API key before running agent correction.")


def follow_up(prompt: str, prior_code: str | None = None) -> dict[str, Any]:
    if prior_code:
        llm_code = _llm_code(
            "Update this Python data-workspace script for the follow-up request. Return only executable Python code. "
            f"Script:\n{prior_code}\n\nFollow-up:\n{prompt.strip()}"
        )
        if llm_code:
            return {
                "status": "success",
                "message": "Updated code with configured LLM.",
                "code": llm_code,
                "schemaContext": _schema_context(include_samples=False),
                "runtime": runtime_status(),
            }
    raise ValueError("LLM_KEY_MISSING: Configure an API key before running agent follow-up.")


def chat(
    *,
    messages: list[dict[str, str]],
    current_code: str | None = None,
    selected_table: str | None = None,
    last_run_error: str | None = None,
) -> dict[str, Any]:
    if not messages:
        raise ValueError("At least one chat message is required.")

    prompt = _chat_prompt(
        messages=messages,
        current_code=current_code,
        selected_table=selected_table,
        last_run_error=last_run_error,
    )
    response = complete_text(prompt)
    if not response:
        raise ValueError("LLM_KEY_MISSING: Configure an API key before running agent chat.")

    code = _extract_code_block(response)
    return {
        "status": "success",
        "message": response.strip(),
        "code": code,
        "hasCode": code is not None,
        "schemaContext": _schema_context(include_samples=False),
        "runtime": runtime_status(),
    }


def _schema_context(include_samples: bool = False) -> dict[str, Any]:
    tables = []
    for table in list_catalog_tables():
        tables.append(
            {
                "qualifiedName": table["qualifiedName"],
                "rowCount": table.get("rowCount", 0),
                "columns": [{"name": column["name"], "type": column["type"]} for column in table.get("columns", [])],
            }
        )
    return {"includeSamples": include_samples, "tables": tables}


def _chat_prompt(
    *,
    messages: list[dict[str, str]],
    current_code: str | None,
    selected_table: str | None,
    last_run_error: str | None,
) -> str:
    normalized_messages = []
    for message in messages[-12:]:
        role = message.get("role", "user")
        content = (message.get("content") or "").strip()
        if content:
            normalized_messages.append(f"{role}: {content}")

    context = _schema_context(include_samples=False)
    return (
        "You are the KriyaX data workspace assistant. Answer normal questions directly. "
        "When code is useful, return a concise explanation and a Python fenced code block. "
        "Use only these helpers in generated code: load_table(name), save_table(df, name, schema='curated'), "
        "show(df, name='result'). Do not invent local fallback behavior.\n\n"
        f"Catalog context:\n{context}\n\n"
        f"Selected table: {selected_table or 'none'}\n\n"
        f"Current editor code:\n{current_code or ''}\n\n"
        f"Last run error:\n{last_run_error or 'none'}\n\n"
        "Conversation:\n"
        + "\n".join(normalized_messages)
    )


def _llm_code(prompt: str) -> str | None:
    response = complete_text(prompt)
    if not response:
        return None
    return _strip_code_fence(response)


def _strip_code_fence(value: str) -> str:
    stripped = value.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip() + "\n"
    return stripped + "\n"


def _extract_code_block(value: str) -> str | None:
    match = re.search(r"```(?:python)?\s*(.*?)```", value, flags=re.S | re.I)
    if not match:
        return None
    code = match.group(1).strip()
    return code + "\n" if code else None
