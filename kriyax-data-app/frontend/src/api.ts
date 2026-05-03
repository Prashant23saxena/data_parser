export type StorageStatus = {
  status: "ready" | "unreachable";
  databaseReady: boolean;
  databasePath: string;
  workspaceRoot: string;
  checkedAt: string;
  error: string | null;
};

export type ImportColumn = {
  sourceIndex: number;
  sourceName: string;
  targetName: string;
  inferredType: string;
  selectedType: string;
  status: "ready" | "needs_rename";
};

export type ImportInspection = {
  draftId?: string;
  draft?: ImportDraft;
  fileName: string;
  filePath: string;
  rowCount: number;
  columns: ImportColumn[];
  requiresRename: boolean;
  previewRows: Record<string, string | number | boolean | null>[];
};

export type ImportDraft = {
  id: string;
  createdAt: string;
  updatedAt: string;
  fileName: string;
  filePath: string;
  rowCount: number;
  columns: ImportColumn[];
  requiresRename: boolean;
  previewRows: Record<string, string | number | boolean | null>[];
};

export type CatalogTable = {
  qualifiedName: string;
  schema: string;
  tableName: string;
  rowCount: number;
  columnCount: number;
  createdAt: string;
  source: {
    kind: string;
    fileName?: string;
    filePath?: string;
  };
  columns: Array<{
    name: string;
    sourceName: string;
    type: string;
  }>;
};

export type TablePreview = {
  schema: string;
  tableName: string;
  columns: string[];
  rows: Record<string, string | number | boolean | null>[];
};

export type RunScriptResult = {
  status: "success" | "error";
  scriptName: string;
  scriptPath: string | null;
  persistedScript: boolean;
  stdout: string;
  stderr: string;
  returnCode: number;
  savedTables: string[];
  resultTables: ResultArtifact[];
  displayFrames: ResultArtifact[];
  preview?: ResultArtifact | null;
};

export type ResultArtifact = {
  name?: string;
  qualifiedName?: string;
  rowCount: number;
  columnCount: number;
  columns: string[];
  rows: Record<string, string | number | boolean | null>[];
};

export type SavedScript = {
  name: string;
  path: string;
  size: number;
  updatedAt: string;
};

export type SavedScriptDetail = SavedScript & {
  code: string;
};

export type PipelineRun = {
  id: string;
  pipelineId: string;
  pipelineName: string;
  scriptId: string;
  trigger?: "manual" | "schedule";
  status: "success" | "error" | "running";
  startedAt: string;
  endedAt: string;
  durationMs: number;
  stdout: string;
  stderr: string;
  returnCode: number;
  savedTables: string[];
  preStep?: {
    type: "odoo_sync";
    syncCursorId: string;
    status: "success" | "error" | "no-changes";
    targetQualifiedName?: string;
    inserted?: number;
    updated?: number;
    lastCursorValue?: string | null;
    message: string;
  } | null;
};

export type PipelineScheduleType = "hourly" | "daily" | "weekly" | "cron";

export type PipelineSchedule = {
  type: PipelineScheduleType;
  cronExpression?: string;
  timeOfDay?: string;
  weekday?: string;
  timezone: string;
  nextRunAt: string;
  updatedAt: string;
};

export type PipelineSchedulePayload = {
  type: PipelineScheduleType;
  cronExpression?: string;
  timeOfDay?: string;
  weekday?: string;
  timezone?: string;
};

export type Pipeline = {
  id: string;
  name: string;
  scriptId: string;
  connectorSyncId?: string | null;
  enabled: boolean;
  schedule?: PipelineSchedule | null;
  createdAt: string;
  updatedAt: string;
  lastRun?: PipelineRun | null;
};

export type PipelineFailure = {
  pipelineId: string;
  pipelineName: string;
  runId: string;
  status: "active" | "acknowledged";
  createdAt: string;
  acknowledgedAt?: string | null;
  message: string;
};

export type OdooConnectionPayload = {
  connectionName: string;
  odooUrl: string;
  dbName: string;
  username: string;
  apiKey: string;
};

export type OdooConnectionResult = {
  status: "success" | "error";
  message: string;
  code?: string;
  odooUrl?: string;
  version?: string;
  uid?: number;
};

export type OdooModel = {
  model: string;
  name: string;
  fieldCount: number;
};

export type OdooField = {
  name: string;
  label: string;
  type: string;
  required: boolean;
  readonly: boolean;
  relation?: string | null;
  supported: boolean;
  warning?: string;
  computed?: boolean;
};

export type AgentResult = {
  status: "success";
  message: string;
  code: string;
  schemaContext?: unknown;
  attempt?: number;
  tracebackSummary?: string;
};

export type AgentChatMessage = {
  role: "system" | "user" | "assistant";
  content: string;
};

export type AgentChatResult = {
  status: "success";
  message: string;
  code: string | null;
  hasCode: boolean;
  schemaContext?: unknown;
  runtime?: unknown;
};

export type LlmProvider = "openai" | "kimi" | "anthropic" | "azure-openai";

export type LlmProfile = {
  id: string;
  tenant_id: string;
  provider: LlmProvider;
  label: string;
  model: string;
  base_url: string;
  is_default: boolean;
  is_enabled: boolean;
  created_at: string;
  updated_at: string;
};

export type LlmConfig = {
  provider: LlmProvider;
  model: string;
  base_url: string;
  masked_key_status: string;
  source: "env" | "vault" | "session" | "missing";
};

export type LlmVaultKeyPayload = {
  provider: LlmProvider;
  api_key: string;
  model?: string;
  base_url?: string;
};

export type LlmProfilePayload = {
  label: string;
  provider: LlmProvider;
  model?: string;
  base_url?: string;
  is_enabled?: boolean;
};

export type LlmRunResult = {
  provider: LlmProvider;
  model: string;
  response: string | null;
  latency_ms: number;
  success: boolean;
  error: string | null;
};

export type LlmRuntimeStatus = {
  provider?: LlmProvider | null;
  label: string;
  model: string;
  hasApiKey: boolean;
  status: "ready" | "missing_key";
  message: string;
};

export type LlmPlaygroundResult = {
  provider?: LlmProvider | null;
  model: string;
  latencyMs: number;
  status: "success" | "error";
  responseText: string;
};

export async function fetchStorageStatus(): Promise<StorageStatus> {
  const response = await fetch("/api/storage/status");
  if (!response.ok) {
    throw new Error(`Storage status failed: ${response.status}`);
  }
  return response.json();
}

export async function getLlmConfig(provider: LlmProvider): Promise<LlmConfig> {
  const response = await fetch(`/api/v1/developer/llm/config?provider=${encodeURIComponent(provider)}`);
  if (!response.ok) throw new Error(await errorMessage(response, "LLM config load failed"));
  return response.json();
}

export async function saveLlmVaultKey(payload: LlmVaultKeyPayload): Promise<LlmConfig> {
  const response = await fetch("/api/v1/developer/llm/vault-key", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error(await errorMessage(response, "LLM key save failed"));
  return response.json();
}

export async function testLlm(params: { provider?: LlmProvider; model?: string; message: string }): Promise<LlmRunResult> {
  const response = await fetch("/api/v1/developer/llm/test", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) throw new Error(await errorMessage(response, "LLM test failed"));
  return response.json();
}

export async function fetchLlmStatus(): Promise<LlmRuntimeStatus> {
  const response = await fetch("/api/llm/status");
  if (!response.ok) throw new Error(`LLM status failed: ${response.status}`);
  return response.json();
}

export async function runLlmPlayground(params: { provider?: LlmProvider; prompt: string; model?: string }): Promise<LlmPlaygroundResult> {
  const response = await fetch("/api/v1/developer/llm/playground", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ provider: params.provider, model: params.model, message: params.prompt })
  });
  if (!response.ok) throw new Error(await errorMessage(response, "LLM playground failed"));
  const result: LlmRunResult = await response.json();
  return {
    provider: result.provider,
    model: result.model,
    latencyMs: result.latency_ms,
    status: result.success ? "success" : "error",
    responseText: result.response ?? result.error ?? ""
  };
}

export async function getLlmProfiles(): Promise<LlmProfile[]> {
  const response = await fetch("/api/v1/developer/llm/profiles");
  if (!response.ok) throw new Error(await errorMessage(response, "LLM profiles load failed"));
  return (await response.json()).items;
}

export async function createLlmProfile(payload: LlmProfilePayload): Promise<LlmProfile> {
  const response = await fetch("/api/v1/developer/llm/profiles", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error(await errorMessage(response, "LLM profile create failed"));
  return response.json();
}

export async function setDefaultLlmProfile(id: string): Promise<LlmProfile> {
  const response = await fetch(`/api/v1/developer/llm/profiles/${id}/default`, { method: "POST" });
  if (!response.ok) throw new Error(await errorMessage(response, "LLM profile default failed"));
  return response.json();
}

export async function deleteLlmProfile(id: string): Promise<{ deleted: boolean }> {
  const response = await fetch(`/api/v1/developer/llm/profiles/${id}`, { method: "DELETE" });
  if (!response.ok) throw new Error(await errorMessage(response, "LLM profile delete failed"));
  return response.json();
}

export async function generateAgentCode(prompt: string): Promise<AgentResult> {
  const response = await fetch("/api/agent/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt })
  });
  if (!response.ok) throw new Error(await errorMessage(response, "Agent generate failed"));
  return response.json();
}

export async function correctAgentCode(code: string, traceback: string, attempt = 1): Promise<AgentResult> {
  const response = await fetch("/api/agent/correct", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code, traceback, attempt })
  });
  if (!response.ok) throw new Error(await errorMessage(response, "Agent correction failed"));
  return response.json();
}

export async function followUpAgentCode(prompt: string, priorCode: string): Promise<AgentResult> {
  const response = await fetch("/api/agent/follow-up", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, priorCode })
  });
  if (!response.ok) throw new Error(await errorMessage(response, "Agent follow-up failed"));
  return response.json();
}

export async function chatWithAgent(params: {
  messages: AgentChatMessage[];
  currentCode?: string;
  selectedTable?: string | null;
  lastRunError?: string | null;
}): Promise<AgentChatResult> {
  const response = await fetch("/api/agent/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) throw new Error(await errorMessage(response, "Agent chat failed"));
  return response.json();
}

export async function uploadImportFile(file: File): Promise<ImportInspection> {
  const body = new FormData();
  body.append("file", file);
  const response = await fetch("/api/imports/upload", {
    method: "POST",
    body
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "File upload failed"));
  }
  return response.json();
}

export async function fetchImportDrafts(): Promise<ImportDraft[]> {
  const response = await fetch("/api/imports/drafts");
  if (!response.ok) throw new Error(await errorMessage(response, "Import drafts load failed"));
  return (await response.json()).drafts;
}

export async function fetchImportDraft(draftId: string): Promise<ImportDraft> {
  const response = await fetch(`/api/imports/drafts/${encodeURIComponent(draftId)}`);
  if (!response.ok) throw new Error(await errorMessage(response, "Import draft load failed"));
  return response.json();
}

export async function deleteImportDraft(draftId: string): Promise<{ deleted: boolean; id: string }> {
  const response = await fetch(`/api/imports/drafts/${encodeURIComponent(draftId)}`, { method: "DELETE" });
  if (!response.ok) throw new Error(await errorMessage(response, "Import draft delete failed"));
  return response.json();
}

export async function commitImport(params: {
  filePath: string;
  targetSchema: string;
  tableName: string;
  columns: ImportColumn[];
  draftId?: string;
}): Promise<CatalogTable> {
  const response = await fetch("/api/imports/commit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Import failed"));
  }
  return response.json();
}

export async function fetchCatalogTables(): Promise<CatalogTable[]> {
  const response = await fetch("/api/catalog/tables");
  if (!response.ok) {
    throw new Error(`Catalog load failed: ${response.status}`);
  }
  const payload = await response.json();
  return payload.tables;
}

export async function fetchCatalogSchemas(): Promise<string[]> {
  const response = await fetch("/api/catalog/schemas");
  if (!response.ok) throw new Error(await errorMessage(response, "Schema load failed"));
  return (await response.json()).schemas;
}

export async function createCatalogSchema(schemaName: string): Promise<{ schema: string; schemas: string[] }> {
  const response = await fetch("/api/catalog/schemas", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ schemaName })
  });
  if (!response.ok) throw new Error(await errorMessage(response, "Schema create failed"));
  return response.json();
}

export async function fetchTablePreview(schema: string, tableName: string): Promise<TablePreview> {
  const response = await fetch(`/api/catalog/tables/${schema}/${tableName}/preview`);
  if (!response.ok) {
    throw new Error(`Preview load failed: ${response.status}`);
  }
  return response.json();
}

export async function renameCatalogTable(schema: string, tableName: string, newTableName: string): Promise<CatalogTable> {
  const response = await fetch(`/api/catalog/tables/${schema}/${tableName}/rename`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ newTableName })
  });
  if (!response.ok) throw new Error(await errorMessage(response, "Table rename failed"));
  return response.json();
}

export async function truncateCatalogTable(schema: string, tableName: string, confirmation: string): Promise<CatalogTable> {
  const response = await fetch(`/api/catalog/tables/${schema}/${tableName}/truncate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ confirmation })
  });
  if (!response.ok) throw new Error(await errorMessage(response, "Table truncate failed"));
  return response.json();
}

export async function dropCatalogTable(schema: string, tableName: string, confirmation: string): Promise<{ dropped: boolean; qualifiedName: string }> {
  const response = await fetch(`/api/catalog/tables/${schema}/${tableName}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ confirmation })
  });
  if (!response.ok) throw new Error(await errorMessage(response, "Table drop failed"));
  return response.json();
}

export async function exportCatalogTable(schema: string, tableName: string): Promise<{ filename: string; text: string }> {
  const response = await fetch(`/api/catalog/tables/${schema}/${tableName}/export`);
  if (!response.ok) throw new Error(await errorMessage(response, "Table export failed"));
  const disposition = response.headers.get("Content-Disposition") ?? "";
  const match = disposition.match(/filename="([^"]+)"/);
  return { filename: match?.[1] ?? `${schema}_${tableName}.csv`, text: await response.text() };
}

export async function runPythonScript(params: {
  scriptName: string;
  code: string;
  persistScript?: boolean;
}): Promise<RunScriptResult> {
  const response = await fetch("/api/execution/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Script run failed"));
  }
  return response.json();
}

export async function savePythonScript(params: {
  scriptName: string;
  code: string;
}): Promise<SavedScriptDetail> {
  const response = await fetch("/api/execution/scripts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) throw new Error(await errorMessage(response, "Script save failed"));
  return response.json();
}

export async function fetchSavedScripts(): Promise<SavedScript[]> {
  const response = await fetch("/api/execution/scripts");
  if (!response.ok) {
    throw new Error(`Saved scripts load failed: ${response.status}`);
  }
  const payload = await response.json();
  return payload.scripts;
}

export async function fetchSavedScript(scriptName: string): Promise<SavedScriptDetail> {
  const response = await fetch(`/api/execution/scripts/${encodeURIComponent(scriptName)}`);
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Saved script load failed"));
  }
  return response.json();
}

export async function testOdooConnection(payload: OdooConnectionPayload): Promise<OdooConnectionResult> {
  const response = await fetch("/api/odoo/test-connection", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Odoo connection test failed"));
  }
  return response.json();
}

export async function saveOdooConnection(payload: OdooConnectionPayload): Promise<OdooConnectionPayload> {
  const response = await fetch("/api/odoo/connections", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Odoo connection save failed"));
  }
  return response.json();
}

export async function fetchOdooModels(payload: OdooConnectionPayload, search = ""): Promise<OdooModel[]> {
  const params = new URLSearchParams();
  if (search.trim()) params.set("search", search.trim());
  const response = await fetch(`/api/odoo/models${params.toString() ? `?${params.toString()}` : ""}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Odoo model load failed"));
  }
  const payloadJson = await response.json();
  return payloadJson.models;
}

export async function fetchOdooFields(payload: OdooConnectionPayload, modelName: string): Promise<OdooField[]> {
  const response = await fetch(`/api/odoo/models/${encodeURIComponent(modelName)}/fields`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Odoo field load failed"));
  }
  const payloadJson = await response.json();
  return payloadJson.fields;
}

export async function fetchOdooRecords(params: {
  connection: OdooConnectionPayload;
  modelName: string;
  fields: string[];
  targetSchema: string;
  tableName: string;
  domainFilter: unknown[];
  recordLimit: number;
}): Promise<CatalogTable & { warnings?: string[] }> {
  const response = await fetch("/api/odoo/fetch", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Odoo fetch failed"));
  }
  return response.json();
}

export async function fetchPipelines(): Promise<Pipeline[]> {
  const response = await fetch("/api/pipelines");
  if (!response.ok) {
    throw new Error(`Pipeline load failed: ${response.status}`);
  }
  const payload = await response.json();
  return payload.pipelines;
}

export async function createPipeline(params: {
  pipelineName: string;
  scriptId: string;
  connectorSyncId?: string | null;
}): Promise<Pipeline> {
  const response = await fetch("/api/pipelines", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Pipeline create failed"));
  }
  return response.json();
}

export async function setPipelineEnabled(pipelineId: string, enabled: boolean): Promise<Pipeline> {
  const response = await fetch(`/api/pipelines/${pipelineId}/enabled`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ enabled })
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Pipeline update failed"));
  }
  return response.json();
}

export async function setPipelineSchedule(pipelineId: string, schedule: PipelineSchedulePayload): Promise<PipelineSchedule> {
  const response = await fetch(`/api/pipelines/${pipelineId}/schedule`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(schedule)
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Pipeline schedule update failed"));
  }
  const payload = await response.json();
  return payload.schedule;
}

export async function fetchPipelineRuns(status = "all", pipelineId?: string): Promise<PipelineRun[]> {
  const params = new URLSearchParams({ status });
  const endpoint = pipelineId
    ? `/api/pipelines/${encodeURIComponent(pipelineId)}/runs?${params.toString()}`
    : `/api/pipelines/runs?${params.toString()}`;
  const response = await fetch(endpoint);
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Pipeline run history failed"));
  }
  const payload = await response.json();
  return payload.runs;
}

export async function fetchPipelineFailures(activeOnly = true): Promise<PipelineFailure[]> {
  const params = new URLSearchParams({ activeOnly: String(activeOnly) });
  const response = await fetch(`/api/pipelines/failures?${params.toString()}`);
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Pipeline failures load failed"));
  }
  const payload = await response.json();
  return payload.failures;
}

export async function acknowledgePipelineFailure(runId: string): Promise<{ acknowledged: boolean; runId: string }> {
  const response = await fetch(`/api/pipelines/failures/${encodeURIComponent(runId)}/ack`, {
    method: "POST"
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Pipeline failure acknowledge failed"));
  }
  return response.json();
}

export async function runPipelineNow(pipelineId: string): Promise<PipelineRun> {
  const response = await fetch(`/api/pipelines/${pipelineId}/run`, {
    method: "POST"
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Pipeline run failed"));
  }
  return response.json();
}

export async function fetchPipelineRun(runId: string): Promise<PipelineRun> {
  const response = await fetch(`/api/pipelines/runs/${encodeURIComponent(runId)}`);
  if (!response.ok) {
    throw new Error(await errorMessage(response, "Pipeline run detail failed"));
  }
  return response.json();
}

async function errorMessage(response: Response, fallback: string): Promise<string> {
  try {
    const payload = await response.json();
    return payload.detail ?? `${fallback}: ${response.status}`;
  } catch {
    return `${fallback}: ${response.status}`;
  }
}
