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
