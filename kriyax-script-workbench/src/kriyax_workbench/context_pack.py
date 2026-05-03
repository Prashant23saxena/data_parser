from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from kriyax_workbench.audit import read_events
from kriyax_workbench.catalog import list_tables
from kriyax_workbench.db_viewer import connection_info
from kriyax_workbench.execution import list_scripts
from kriyax_workbench.pipelines import list_failures, list_pipelines, list_runs
from kriyax_workbench.workspace import ensure_workspace, workspace_paths


def build_context(limit: int = 10) -> dict[str, Any]:
    paths = ensure_workspace()
    tables = list_tables()
    scripts = list_scripts()
    pipelines = list_pipelines()
    failures = list_failures(active_only=True)
    audit = read_events(limit=limit)
    runs = list_runs()[:limit]
    db_viewer = connection_info()
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "workspace": {
            "root": paths["root"],
            "database": paths["database"],
            "catalog": paths["catalog"],
            "scripts": paths["scripts"],
            "runs": paths["runs"],
            "audit": paths["audit_log"],
            "uploads": paths["uploads"],
            "exports": paths["exports"],
        },
        "tables": tables,
        "scripts": scripts,
        "pipelines": pipelines,
        "pipelineFailures": failures,
        "recentRuns": runs,
        "recentAudit": audit,
        "dbViewer": db_viewer,
        "recommendedCommands": recommended_commands(tables, scripts, failures),
    }


def render_markdown(context: dict[str, Any]) -> str:
    lines = [
        "# KriyaX Script Workbench Context",
        "",
        f"Generated: `{context['generatedAt']}`",
        "",
        "## Workspace",
        "",
    ]
    for key, value in context["workspace"].items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## DB Viewer", ""])
    lines.append(f"- Driver: `{context['dbViewer']['driver']}`")
    lines.append(f"- Database file: `{context['dbViewer']['databasePath']}`")
    lines.append(f"- Metadata file: `{context['dbViewer']['metadataPath']}`")
    lines.append(f"- Locking note: {context['dbViewer']['lockingNote']}")
    if context["dbViewer"]["sampleQueries"]:
        lines.append("- Suggested SQL:")
        for query in context["dbViewer"]["sampleQueries"]:
            lines.append(f"  - `{query}`")

    lines.extend(["", "## Tables", ""])
    if context["tables"]:
        for table in context["tables"]:
            columns = ", ".join(column["name"] for column in table.get("columns", [])[:12])
            if len(table.get("columns", [])) > 12:
                columns += ", ..."
            lines.append(
                f"- `{table['qualifiedName']}` rows={table.get('rowCount', 0)} "
                f"source={table.get('source', {}).get('kind', 'unknown')} columns={columns}"
            )
    else:
        lines.append("- No tables registered.")

    lines.extend(["", "## Scripts", ""])
    if context["scripts"]:
        for script in context["scripts"]:
            lines.append(f"- `{script['name']}` size={script['size']} updated={script['updatedAt']}")
    else:
        lines.append("- No saved scripts.")

    lines.extend(["", "## Pipelines", ""])
    if context["pipelines"]:
        for pipeline in context["pipelines"]:
            last = pipeline.get("lastRun") or {}
            lines.append(
                f"- `{pipeline['name']}` id={pipeline['id']} script={pipeline['script']} "
                f"enabled={pipeline['enabled']} last={last.get('status', 'none')}"
            )
    else:
        lines.append("- No pipelines.")

    lines.extend(["", "## Active Failures", ""])
    if context["pipelineFailures"]:
        for failure in context["pipelineFailures"]:
            lines.append(f"- run={failure['runId']} pipeline={failure['pipelineName']} status={failure['status']}")
    else:
        lines.append("- No active pipeline failures.")

    lines.extend(["", "## Recent Audit", ""])
    if context["recentAudit"]:
        for event in context["recentAudit"]:
            label = event.get("scriptName") or event.get("qualifiedName") or event.get("runId") or ""
            status = event.get("status", "")
            lines.append(f"- `{event['createdAt']}` {event['eventType']} {status} {label}")
    else:
        lines.append("- No audit events yet.")

    lines.extend(["", "## Recommended Next Commands", ""])
    for command in context["recommendedCommands"]:
        lines.append(f"- `{command}`")

    return "\n".join(lines) + "\n"


def recommended_commands(tables: list[dict[str, Any]], scripts: list[dict[str, Any]], failures: list[dict[str, Any]]) -> list[str]:
    commands = [
        ".venv/bin/python tools/workspace_status.py",
        ".venv/bin/python tools/catalog_list.py",
        ".venv/bin/python tools/audit_tail.py --limit 20",
    ]
    if tables:
        table = tables[0]["qualifiedName"]
        commands.extend(
            [
                f".venv/bin/python tools/table_describe.py {table}",
                f".venv/bin/python tools/table_view.py {table} --limit 20",
                ".venv/bin/python tools/db_viewer_info.py",
            ]
        )
    if scripts:
        script = scripts[0]["name"]
        commands.extend(
            [
                f".venv/bin/python tools/script_show.py {script}",
                f".venv/bin/python tools/script_run.py {script}",
            ]
        )
    if failures:
        commands.append(f".venv/bin/python tools/pipeline_ack_failure.py {failures[0]['runId']}")
    return commands
