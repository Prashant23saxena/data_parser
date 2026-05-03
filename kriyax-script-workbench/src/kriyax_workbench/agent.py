from __future__ import annotations

from pathlib import Path
from typing import Any

from kriyax_workbench.audit import audit_event
from kriyax_workbench.catalog import list_tables
from kriyax_workbench.execution import read_script, script_file
from kriyax_workbench.llm import complete_text

import hashlib


def generate_code(prompt: str, save_as: str | None = None) -> dict[str, Any]:
    schema = _schema_context()
    llm_prompt = (
        "Generate only executable Python/pandas code for the KriyaX Script Workbench. "
        "Use helpers: load_table(name), save_table(df, name, schema='curated'), show(df, name='result'). "
        f"Available schema: {schema}. User request: {prompt}"
    )
    code = _strip_fence(complete_text(llm_prompt))
    path = _save_if_requested(code, save_as)
    audit_event("agent.code.generated", {"promptSha256": _sha(prompt), "codeSha256": _sha(code), "savedPath": path, "schemaTableCount": len(schema)})
    return {"code": code, "savedPath": path, "schemaContext": schema}


def correct_code(script_name: str, traceback_text: str, save: bool = False) -> dict[str, Any]:
    script = read_script(script_name)
    prompt = (
        "Correct this KriyaX Script Workbench Python script. Return only executable Python code. "
        f"Script:\n{script['code']}\n\nTraceback:\n{traceback_text}"
    )
    code = _strip_fence(complete_text(prompt))
    path = _save_if_requested(code, script_name if save else None)
    audit_event("agent.code.corrected", {"scriptName": script_name, "tracebackSha256": _sha(traceback_text), "codeSha256": _sha(code), "savedPath": path})
    return {"code": code, "savedPath": path}


def follow_up(script_name: str, request: str, save: bool = False) -> dict[str, Any]:
    script = read_script(script_name)
    prompt = (
        "Update this KriyaX Script Workbench Python script for the follow-up. Return only executable Python code. "
        f"Script:\n{script['code']}\n\nFollow-up:\n{request}"
    )
    code = _strip_fence(complete_text(prompt))
    path = _save_if_requested(code, script_name if save else None)
    audit_event("agent.code.follow_up", {"scriptName": script_name, "requestSha256": _sha(request), "codeSha256": _sha(code), "savedPath": path})
    return {"code": code, "savedPath": path}


def _schema_context() -> list[dict[str, Any]]:
    return [
        {
            "qualifiedName": table["qualifiedName"],
            "columns": [{"name": column["name"], "type": column.get("type", "")} for column in table.get("columns", [])],
        }
        for table in list_tables()
    ]


def _save_if_requested(code: str, save_as: str | None) -> str | None:
    if not save_as:
        return None
    path = script_file(save_as)
    path.write_text(code, encoding="utf-8")
    return str(path)


def _strip_fence(value: str) -> str:
    text = value.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text + "\n"


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
