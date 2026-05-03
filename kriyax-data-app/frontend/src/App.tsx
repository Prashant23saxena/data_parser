import {
  Activity,
  ArrowLeft,
  Boxes,
  Braces,
  ChevronDown,
  ChevronRight,
  Copy,
  Database,
  FileSpreadsheet,
  FileUp,
  FileInput,
  HardDrive,
  Home as HomeIcon,
  KeyRound,
  Network,
  PlugZap,
  RefreshCcw,
  Save,
  ScrollText,
  Send,
  Settings,
  ShieldCheck,
  Table2,
  Upload,
  Workflow
} from "lucide-react";
import type { ChangeEvent, ComponentType, ReactNode } from "react";
import { Fragment, useEffect, useMemo, useRef, useState } from "react";
import {
  acknowledgePipelineFailure,
  chatWithAgent,
  commitImport,
  createCatalogSchema,
  createLlmProfile,
  createPipeline,
  deleteImportDraft,
  deleteLlmProfile,
  fetchCatalogSchemas,
  fetchCatalogTables,
  fetchImportDrafts,
  fetchOdooFields,
  fetchOdooModels,
  fetchOdooRecords,
  fetchPipelineRun,
  fetchPipelineRuns,
  fetchPipelineFailures,
  fetchPipelines,
  fetchSavedScript,
  fetchSavedScripts,
  fetchStorageStatus,
  fetchTablePreview,
  getLlmConfig,
  getLlmProfiles,
  dropCatalogTable,
  exportCatalogTable,
  renameCatalogTable,
  runPipelineNow,
  runLlmPlayground,
  runPythonScript,
  saveLlmVaultKey,
  savePythonScript,
  saveOdooConnection,
  setDefaultLlmProfile,
  setPipelineEnabled,
  setPipelineSchedule,
  testLlm,
  truncateCatalogTable,
  testOdooConnection,
  uploadImportFile,
  type AgentChatMessage,
  type CatalogTable,
  type ImportDraft,
  type ImportColumn,
  type ImportInspection,
  type LlmProfile,
  type LlmProvider,
  type LlmPlaygroundResult,
  type LlmConfig,
  type OdooConnectionPayload,
  type OdooField,
  type OdooModel,
  type Pipeline,
  type PipelineFailure,
  type PipelineRun,
  type PipelineSchedulePayload,
  type ResultArtifact,
  type RunScriptResult,
  type SavedScript,
  type StorageStatus,
  type TablePreview
} from "./api";

type NavItem = {
  id: string;
  label: string;
  path: string;
  icon: ComponentType<{ size?: number }>;
};

const navItems: NavItem[] = [
  { id: "S-01", label: "Home", path: "/", icon: HomeIcon },
  { id: "S-02", label: "Connectors", path: "/connectors", icon: PlugZap },
  { id: "S-05", label: "Catalog", path: "/catalog", icon: Table2 },
  { id: "S-09", label: "Code Workspace", path: "/code", icon: Braces },
  { id: "S-11", label: "Saved Scripts", path: "/scripts", icon: ScrollText },
  { id: "S-12", label: "Pipelines", path: "/pipelines", icon: Workflow },
  { id: "S-14", label: "Storage", path: "/storage", icon: Settings }
];

function topNavForPath(path: string) {
  path = canonicalPath(path);
  if (path.startsWith("/connectors")) return navItems.find((item) => item.path === "/connectors") ?? navItems[0];
  if (path.startsWith("/catalog")) return navItems.find((item) => item.path === "/catalog") ?? navItems[0];
  if (path.startsWith("/code")) return navItems.find((item) => item.path === "/code") ?? navItems[0];
  if (path.startsWith("/pipelines")) return navItems.find((item) => item.path === "/pipelines") ?? navItems[0];
  return navItems.find((item) => item.path === path) ?? navItems[0];
}

function canonicalPath(path: string) {
  if (path === "/file-import") return "/connectors/file-import";
  if (path === "/odoo-import") return "/connectors/odoo";
  if (path === "/code-workspace") return "/code";
  if (path === "/saved-scripts") return "/scripts";
  return path;
}

type RouteMeta = {
  id: string;
  label: string;
  subtitle: string;
  parentPath?: string;
  parentLabel?: string;
  breadcrumb: string[];
};

function titleForPath(path: string): RouteMeta {
  if (path === "/connectors/file-import") return { id: "S-03", label: "File Import Wizard", subtitle: "Inspect, map, and create local tables.", parentPath: "/connectors", parentLabel: "Connectors", breadcrumb: ["Connectors", "File Import"] };
  if (path === "/connectors/odoo") return { id: "S-04", label: "Odoo Import Workspace", subtitle: "Test connections, browse models, and sync records.", parentPath: "/connectors", parentLabel: "Connectors", breadcrumb: ["Connectors", "Odoo"] };
  if (path === "/catalog/table") return { id: "S-06", label: "Table Detail", subtitle: "Metadata, columns, and bounded row preview.", parentPath: "/catalog", parentLabel: "Catalog", breadcrumb: ["Catalog", "Table Detail"] };
  if (path === "/catalog/table/manage") return { id: "S-07", label: "Manage Table", subtitle: "Rename, truncate, or drop a selected table.", parentPath: "/catalog", parentLabel: "Catalog", breadcrumb: ["Catalog", "Manage Table"] };
  if (path === "/catalog/table/export") return { id: "S-08", label: "Export Table", subtitle: "Prepare a local CSV export from DuckDB.", parentPath: "/catalog", parentLabel: "Catalog", breadcrumb: ["Catalog", "Export Table"] };
  if (path === "/code/agent") return { id: "S-09", label: "Code Workspace", subtitle: "Python editor with schema browser and agent workbench.", parentPath: "/code", parentLabel: "Code", breadcrumb: ["Code Workspace", "Agent"] };
  if (path === "/pipelines/run") return { id: "S-13", label: "Pipeline Run Detail", subtitle: "Inspect the latest run, logs, and saved outputs.", parentPath: "/pipelines", parentLabel: "Pipelines", breadcrumb: ["Pipelines", "Run Detail"] };
  const item = topNavForPath(path);
  return { id: item.id, label: item.label, subtitle: "Local-first enterprise data workspace.", breadcrumb: [item.label] };
}

function usePath() {
  const [path, setPath] = useState(window.location.pathname);

  useEffect(() => {
    const update = () => setPath(window.location.pathname);
    window.addEventListener("popstate", update);
    return () => window.removeEventListener("popstate", update);
  }, []);

  const navigate = (nextPath: string) => {
    window.history.pushState({}, "", nextPath);
    setPath(new URL(nextPath, window.location.origin).pathname);
  };

  return { path, navigate };
}

export function App() {
  const { path, navigate } = usePath();
  const canonical = canonicalPath(path);
  const [storage, setStorage] = useState<StorageStatus | null>(null);
  const [storageError, setStorageError] = useState<string | null>(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(true);
  const sidebarTimer = useRef<number | null>(null);

  useEffect(() => {
    fetchStorageStatus()
      .then(setStorage)
      .catch((error: Error) => setStorageError(error.message));
  }, []);

  const active = useMemo(() => topNavForPath(canonical), [canonical]);
  const title = useMemo(() => titleForPath(canonical), [canonical]);

  const expandSidebar = () => {
    if (sidebarTimer.current) window.clearTimeout(sidebarTimer.current);
    setSidebarCollapsed(false);
  };

  const scheduleSidebarCollapse = () => {
    if (sidebarTimer.current) window.clearTimeout(sidebarTimer.current);
    sidebarTimer.current = window.setTimeout(() => setSidebarCollapsed(true), 2000);
  };

  useEffect(() => () => {
    if (sidebarTimer.current) window.clearTimeout(sidebarTimer.current);
  }, []);

  return (
    <div className={sidebarCollapsed ? "app-shell sidebar-collapsed" : "app-shell"}>
      <aside className="sidebar" onMouseEnter={expandSidebar} onMouseLeave={scheduleSidebarCollapse}>
        <div className="brand">
          <Database size={24} />
          <div>
            <strong>KriyaX</strong>
            <span>Data Layer</span>
          </div>
        </div>
        <nav>
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                className={item.path === active.path ? "nav-item active" : "nav-item"}
                key={item.path}
                onClick={() => navigate(item.path)}
                title={`${item.id} ${item.label}`}
              >
                <Icon size={17} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
        <div className="sidebar-status">
          <span className={storage?.databaseReady ? "dot ready" : "dot"} />
          <div>
            <strong>{storage?.databaseReady ? "Storage ready" : "Storage checking"}</strong>
            <span>{storageError ?? "DuckDB workspace"}</span>
          </div>
        </div>
      </aside>

      <main>
        <header className="topbar">
          <div className="topbar-title">
            <div className="breadcrumb-row">
              {title.parentPath ? (
                <button className="back-button" onClick={() => navigate(title.parentPath!)} title={`Back to ${title.parentLabel}`}>
                  <ArrowLeft size={16} />
                  <span>Back</span>
                </button>
              ) : null}
              <span className="screen-id">{title.id}</span>
              <span className="breadcrumb">{title.breadcrumb.join(" > ")}</span>
            </div>
            <h1>{title.label}</h1>
            <p>{title.subtitle}</p>
          </div>
          <div className="status-pill">
            {storage?.status ?? "checking"}
          </div>
        </header>
        <Screen path={canonical} storage={storage} navigate={navigate} />
      </main>
    </div>
  );
}

function Screen({ path, storage, navigate }: { path: string; storage: StorageStatus | null; navigate: (nextPath: string) => void }) {
  if (path === "/connectors") return <Connectors navigate={navigate} />;
  if (path === "/connectors/file-import") return <FileImport />;
  if (path === "/connectors/odoo") return <OdooImport />;
  if (path === "/catalog") return <Catalog navigate={navigate} />;
  if (path === "/catalog/table") return <TableDetail />;
  if (path === "/catalog/table/manage") return <TableManagement />;
  if (path === "/catalog/table/export") return <ExportTable />;
  if (path === "/code") return <CodeWorkspace />;
  if (path === "/code/agent") return <CodeWorkspace initialAgentOpen />;
  if (path === "/scripts") return <SavedScripts />;
  if (path === "/pipelines") return <Pipelines navigate={navigate} />;
  if (path === "/pipelines/run") return <RunDetail />;
  if (path === "/storage") return <StorageSettings storage={storage} />;
  return <Home storage={storage} navigate={navigate} />;
}

function Home({ storage, navigate }: { storage: StorageStatus | null; navigate: (nextPath: string) => void }) {
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);
  const [failures, setFailures] = useState<PipelineFailure[]>([]);
  const [tableCount, setTableCount] = useState(0);
  const [scriptCount, setScriptCount] = useState(0);

  useEffect(() => {
    Promise.all([fetchPipelines(), fetchPipelineFailures(), fetchCatalogTables(), fetchSavedScripts()])
      .then(([nextPipelines, nextFailures, nextTables, nextScripts]) => {
        setPipelines(nextPipelines);
        setFailures(nextFailures);
        setTableCount(nextTables.length);
        setScriptCount(nextScripts.length);
      })
      .catch(() => {
        setPipelines([]);
        setFailures([]);
        setTableCount(0);
        setScriptCount(0);
      });
  }, []);

  const scheduledCount = pipelines.filter((pipeline) => pipeline.schedule).length;

  return (
    <section className="screen-grid">
      <div className="summary-band">
        <Metric label="Tables" value={String(tableCount)} detail={tableCount ? "catalog registered" : "waiting for first import"} />
        <Metric label="Scripts" value={String(scriptCount)} detail="saved .py files" />
        <Metric label="Pipelines" value={String(pipelines.length)} detail={`${scheduledCount} active schedules`} />
        <Metric label="Storage" value={storage?.databaseReady ? "Ready" : "..." } detail="local DuckDB" />
      </div>
      {failures.length ? (
        <div className="notice error">
          {failures.length} active pipeline failure{failures.length === 1 ? "" : "s"} need attention.
        </div>
      ) : null}
      <Panel title="Start Here">
        <div className="launch-grid">
          <button className="launch-action" onClick={() => navigate("/connectors/file-import")}>
            <FileInput size={18} />
            <span><strong>Import a table</strong><small>CSV or Excel into a chosen schema</small></span>
          </button>
          <button className="launch-action" onClick={() => navigate("/code")}>
            <Braces size={18} />
            <span><strong>Open Code Workspace</strong><small>Write Python, chat with the agent, run results</small></span>
          </button>
          <button className="launch-action" onClick={() => navigate("/scripts")}>
            <ScrollText size={18} />
            <span><strong>Saved Scripts</strong><small>Only scripts explicitly saved by you</small></span>
          </button>
          <button className="launch-action" onClick={() => navigate("/pipelines")}>
            <Workflow size={18} />
            <span><strong>Pipelines</strong><small>Schedule saved scripts when they are ready</small></span>
          </button>
        </div>
      </Panel>
    </section>
  );
}

function Connectors({ navigate }: { navigate: (nextPath: string) => void }) {
  const { tables } = useCatalogTables();
  const fileImports = tables.filter((table) => table.source.kind === "file").slice(0, 3);
  const odooTables = tables.filter((table) => table.source.kind === "odoo").slice(0, 3);

  return (
    <section className="connectors-page">
      <div className="capability-strip">
        <span>Auto schema detection</span>
        <span>Preview before import</span>
        <span>Incremental sync</span>
        <span>Table auto-creation</span>
      </div>
      <div className="source-card-grid">
        <div className="source-card">
          <div className="source-card-header">
            <FileSpreadsheet size={22} />
            <div>
              <strong>File Upload</strong>
              <span>CSV and Excel into local DuckDB tables</span>
            </div>
          </div>
          <div className="source-badges"><span>CSV</span><span>XLSX</span><span>schema map</span></div>
          <div className="source-status">
            <strong>{fileImports.length ? "Recent imports" : "Ready for first import"}</strong>
            {fileImports.length ? fileImports.map((table) => <span key={table.qualifiedName}>{table.qualifiedName} · {table.rowCount} rows</span>) : <span>Drop a file, inspect columns, and create a governed raw table.</span>}
          </div>
          <div className="panel-actions">
            <button className="primary-button" onClick={() => navigate("/connectors/file-import")}><FileUp size={15} />Start file import</button>
          </div>
        </div>
        <div className="source-card">
          <div className="source-card-header">
            <Network size={22} />
            <div>
              <strong>Odoo</strong>
              <span>Operational models with saved connection testing</span>
            </div>
          </div>
          <div className="source-badges"><span>model browse</span><span>delta sync</span><span>raw_odoo</span></div>
          <div className="source-status">
            <strong>{odooTables.length ? "Synced tables" : "Connection workspace"}</strong>
            {odooTables.length ? odooTables.map((table) => <span key={table.qualifiedName}>{table.qualifiedName} · {table.rowCount} rows</span>) : <span>Test credentials, select fields, and land source records into the warehouse.</span>}
          </div>
          <div className="panel-actions">
            <button className="primary-button" onClick={() => navigate("/connectors/odoo")}><Boxes size={15} />Open Odoo workspace</button>
          </div>
        </div>
      </div>
    </section>
  );
}

function FileImport() {
  const [inspection, setInspection] = useState<ImportInspection | null>(null);
  const [targetSchema, setTargetSchema] = useState("raw_files");
  const [schemas, setSchemas] = useState<string[]>(["raw_files", "staging", "curated"]);
  const [newSchemaName, setNewSchemaName] = useState("");
  const [drafts, setDrafts] = useState<ImportDraft[]>([]);
  const [tableName, setTableName] = useState("sales_orders_raw");
  const [isUploading, setIsUploading] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refreshImportState = async () => {
    const [nextSchemas, nextDrafts] = await Promise.all([fetchCatalogSchemas(), fetchImportDrafts()]);
    setSchemas(nextSchemas);
    setDrafts(nextDrafts);
  };

  useEffect(() => {
    refreshImportState().catch((value: Error) => setError(value.message));
  }, []);

  const chooseFile = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setError(null);
    setMessage(null);
    try {
      const nextInspection = await uploadImportFile(file);
      setInspection(nextInspection);
      setTableName(suggestTableName(file.name));
      await refreshImportState();
    } catch (uploadError) {
      setError(uploadError instanceof Error ? uploadError.message : "Upload failed");
    } finally {
      setIsUploading(false);
      event.target.value = "";
    }
  };

  const updateColumn = (index: number, patch: Partial<ImportColumn>) => {
    setInspection((current) => {
      if (!current) return current;
      return {
        ...current,
        columns: current.columns.map((column, columnIndex) =>
          columnIndex === index ? { ...column, ...patch } : column
        )
      };
    });
  };

  const duplicateTargets = useMemo(() => {
    if (!inspection) return new Set<string>();
    const counts = new Map<string, number>();
    inspection.columns.forEach((column) => {
      counts.set(column.targetName, (counts.get(column.targetName) ?? 0) + 1);
    });
    return new Set([...counts.entries()].filter(([, count]) => count > 1).map(([name]) => name));
  }, [inspection]);

  const canImport = Boolean(inspection && tableName.trim() && duplicateTargets.size === 0 && !isImporting);

  const createTable = async () => {
    if (!inspection) return;
    setIsImporting(true);
    setError(null);
    setMessage(null);
    try {
      const result = await commitImport({
        filePath: inspection.filePath,
        targetSchema,
        tableName,
        columns: inspection.columns,
        draftId: inspection.draftId
      });
      setMessage(`Created ${result.qualifiedName} with ${result.rowCount} rows.`);
      setInspection(null);
      await refreshImportState();
    } catch (commitError) {
      setError(commitError instanceof Error ? commitError.message : "Import failed");
    } finally {
      setIsImporting(false);
    }
  };

  const resumeDraft = (draft: ImportDraft) => {
    setInspection({ ...draft, draftId: draft.id });
    setTableName(suggestTableName(draft.fileName));
    setMessage(`Resumed ${draft.fileName}.`);
    setError(null);
  };

  const removeDraft = async (draft: ImportDraft) => {
    setError(null);
    setMessage(null);
    try {
      await deleteImportDraft(draft.id);
      if (inspection?.draftId === draft.id) setInspection(null);
      await refreshImportState();
      setMessage(`Removed draft ${draft.fileName}.`);
    } catch (value) {
      setError(value instanceof Error ? value.message : "Draft delete failed");
    }
  };

  const addSchema = async () => {
    if (!newSchemaName.trim()) return;
    setError(null);
    setMessage(null);
    try {
      const created = await createCatalogSchema(newSchemaName);
      setSchemas(created.schemas);
      setTargetSchema(created.schema);
      setNewSchemaName("");
      setMessage(`Schema '${created.schema}' is ready.`);
    } catch (value) {
      setError(value instanceof Error ? value.message : "Schema create failed");
    }
  };

  return (
    <section className="workspace-layout">
      <Panel title="1. Upload">
        <label className="drop-zone file-picker">
          <Upload size={22} />
          <strong>{isUploading ? "Reading file..." : "Choose CSV/XLSX file"}</strong>
          <span>{inspection ? `${inspection.fileName} · ${inspection.rowCount} rows` : "The file is inspected before a table is created."}</span>
          <input type="file" accept=".csv,.xlsx" onChange={chooseFile} />
        </label>
        <div className="form-grid">
          <SchemaPicker
            label="Target schema"
            value={targetSchema}
            schemas={schemas}
            newSchemaName={newSchemaName}
            onChange={setTargetSchema}
            onNewSchemaName={setNewSchemaName}
            onAddSchema={addSchema}
          />
          <label>New table name<input value={tableName} onChange={(event) => setTableName(event.target.value)} placeholder="sales_orders_raw" /></label>
        </div>
        {drafts.length ? (
          <div className="draft-list">
            <strong>Import drafts</strong>
            {drafts.map((draft) => (
              <div className="draft-row" key={draft.id}>
                <span>{draft.fileName} · {draft.rowCount} rows</span>
                <div className="row-actions">
                  <button className="table-link-button" onClick={() => resumeDraft(draft)}>Resume</button>
                  <button className="table-link-button" onClick={() => removeDraft(draft)}>Remove</button>
                </div>
              </div>
            ))}
          </div>
        ) : null}
        {inspection?.requiresRename ? <div className="notice warning">Duplicate source column names found. Rename the target columns before import.</div> : null}
        {error ? <div className="notice error">{error}</div> : null}
        {message ? <div className="notice success">{message}</div> : null}
      </Panel>
      <Panel title="2. Map Columns">
        {inspection ? (
          <>
            <table>
              <thead><tr><th>Source</th><th>New name</th><th>Type</th><th>Status</th></tr></thead>
              <tbody>
                {inspection.columns.map((column, index) => {
                  const duplicate = duplicateTargets.has(column.targetName);
                  return (
                    <tr key={`${column.sourceIndex}-${column.sourceName}`}>
                      <td>{column.sourceName}</td>
                      <td><input value={column.targetName} onChange={(event) => updateColumn(index, { targetName: event.target.value })} /></td>
                      <td>
                        <select value={column.selectedType} onChange={(event) => updateColumn(index, { selectedType: event.target.value })}>
                          <option value="text">text</option>
                          <option value="integer">integer</option>
                          <option value="decimal">decimal</option>
                          <option value="date">date</option>
                          <option value="datetime">datetime</option>
                          <option value="boolean">boolean</option>
                        </select>
                      </td>
                      <td><span className={duplicate || column.status === "needs_rename" ? "status-text warning-text" : "status-text"}>{duplicate ? "rename" : column.status}</span></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            <div className="panel-actions">
              <button className="primary-button" onClick={createTable} disabled={!canImport}>{isImporting ? "Creating..." : "Create table"}</button>
            </div>
          </>
        ) : (
          <div className="empty-state">Upload a file to review and edit column names and types.</div>
        )}
      </Panel>
      <Panel title="3. Preview">
        {inspection ? <DataPreview rows={inspection.previewRows} /> : <div className="table-preview">Preview rows will render here after upload parsing.</div>}
      </Panel>
    </section>
  );
}

function OdooImport() {
  const [connection, setConnection] = useState<OdooConnectionPayload>({
    connectionName: "Client Odoo",
    odooUrl: "",
    dbName: "",
    username: "",
    apiKey: ""
  });
  const [testResult, setTestResult] = useState<string | null>(null);
  const [connectionReady, setConnectionReady] = useState(false);
  const [models, setModels] = useState<OdooModel[]>([]);
  const [modelSearch, setModelSearch] = useState("");
  const [selectedModel, setSelectedModel] = useState<OdooModel | null>(null);
  const [fields, setFields] = useState<OdooField[]>([]);
  const [selectedFields, setSelectedFields] = useState<Set<string>>(new Set());
  const [targetSchema, setTargetSchema] = useState("raw_odoo");
  const [schemas, setSchemas] = useState<string[]>(["raw_odoo", "staging", "curated"]);
  const [newSchemaName, setNewSchemaName] = useState("");
  const [tableName, setTableName] = useState("res_partner");
  const [domainFilter, setDomainFilter] = useState("[]");
  const [recordLimit, setRecordLimit] = useState("1000");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<string | null>(null);
  const updateConnection = (field: keyof OdooConnectionPayload, value: string) => {
    setConnection((current) => ({ ...current, [field]: value }));
    setConnectionReady(false);
    setTestResult(null);
  };

  const canTest = Object.values(connection).every((value) => value.trim());
  const supportedFields = fields.filter((field) => field.supported);
  const canFetch = Boolean(connectionReady && selectedModel && selectedFields.size > 0 && tableName.trim() && !loading);

  useEffect(() => {
    fetchCatalogSchemas()
      .then(setSchemas)
      .catch((value: Error) => setError(value.message));
  }, []);

  const addSchema = async () => {
    if (!newSchemaName.trim()) return;
    setError(null);
    setMessage(null);
    try {
      const created = await createCatalogSchema(newSchemaName);
      setSchemas(created.schemas);
      setTargetSchema(created.schema);
      setNewSchemaName("");
      setMessage(`Schema '${created.schema}' is ready.`);
    } catch (value) {
      setError(value instanceof Error ? value.message : "Schema create failed");
    }
  };

  const testConnection = async () => {
    setLoading("connection");
    setError(null);
    setMessage(null);
    try {
      const result = await testOdooConnection(connection);
      setTestResult(result.message);
      if (result.status === "success") {
        await saveOdooConnection(connection);
        setConnectionReady(true);
        setMessage(`Connection '${connection.connectionName}' saved.`);
        await loadModels(modelSearch);
      } else {
        setConnectionReady(false);
        setError(result.message);
      }
    } catch (value) {
      setError(value instanceof Error ? value.message : "Odoo connection failed");
    } finally {
      setLoading(null);
    }
  };

  const loadModels = async (search: string) => {
    setLoading("models");
    setError(null);
    try {
      const nextModels = await fetchOdooModels(connection, search);
      setModels(nextModels);
    } catch (value) {
      setError(value instanceof Error ? value.message : "Odoo model load failed");
    } finally {
      setLoading(null);
    }
  };

  const openModel = async (model: OdooModel) => {
    setSelectedModel(model);
    setFields([]);
    setSelectedFields(new Set());
    setTableName(suggestTableName(model.model));
    setLoading("fields");
    setError(null);
    try {
      const nextFields = await fetchOdooFields(connection, model.model);
      setFields(nextFields);
      setSelectedFields(new Set(nextFields.filter((field) => field.supported).slice(0, 6).map((field) => field.name)));
    } catch (value) {
      setError(value instanceof Error ? value.message : "Odoo field load failed");
    } finally {
      setLoading(null);
    }
  };

  const toggleField = (fieldName: string) => {
    setSelectedFields((current) => {
      const next = new Set(current);
      if (next.has(fieldName)) {
        next.delete(fieldName);
      } else {
        next.add(fieldName);
      }
      return next;
    });
  };

  const fetchRecords = async () => {
    setLoading("fetch");
    setError(null);
    setMessage(null);
    try {
      const parsedDomain = JSON.parse(domainFilter || "[]");
      if (!Array.isArray(parsedDomain)) {
        throw new Error("Invalid filter syntax");
      }
      const result = await fetchOdooRecords({
        connection,
        modelName: selectedModel?.model ?? "",
        fields: [...selectedFields],
        targetSchema,
        tableName,
        domainFilter: parsedDomain,
        recordLimit: Number.parseInt(recordLimit, 10) || 0
      });
      const warningText = result.warnings?.length ? ` ${result.warnings.join(" ")}` : "";
      setMessage(`Table '${result.qualifiedName}' created with ${result.rowCount} rows.${warningText}`);
    } catch (value) {
      setError(value instanceof Error ? value.message : "Odoo fetch failed");
    } finally {
      setLoading(null);
    }
  };

  return (
    <section className="odoo-grid">
      <Panel title="1. Connection">
        <div className="form-grid">
          <label>Connection name<input value={connection.connectionName} onChange={(event) => updateConnection("connectionName", event.target.value)} /></label>
          <label>Odoo URL<input value={connection.odooUrl} onChange={(event) => updateConnection("odooUrl", event.target.value)} placeholder="https://your-company.odoo.com" /></label>
          <label>Database<input value={connection.dbName} onChange={(event) => updateConnection("dbName", event.target.value)} placeholder="client database" /></label>
          <label>Username<input value={connection.username} onChange={(event) => updateConnection("username", event.target.value)} placeholder="admin@example.com" /></label>
          <label>API key<input type="password" value={connection.apiKey} onChange={(event) => updateConnection("apiKey", event.target.value)} placeholder="api key" /></label>
        </div>
        <div className="panel-actions">
          <button className="primary-button" onClick={testConnection} disabled={!canTest || loading === "connection"}>{loading === "connection" ? "Connecting..." : "Test connection"}</button>
        </div>
        {testResult ? <div className="notice success">{testResult}</div> : null}
        {message ? <div className="notice success">{message}</div> : null}
        {error ? <div className="notice error">{error}</div> : null}
      </Panel>

      <Panel title="2. Models">
        <div className="inline-controls">
          <label>Search models<input value={modelSearch} onChange={(event) => setModelSearch(event.target.value)} placeholder="sale, partner, stock" /></label>
          <button className="table-link-button" onClick={() => loadModels(modelSearch)} disabled={!connectionReady || loading === "models"}>{loading === "models" ? "Loading..." : "Load models"}</button>
        </div>
        {models.length ? (
          <table>
            <thead><tr><th>Model</th><th>Name</th><th>Fields</th><th>Action</th></tr></thead>
            <tbody>
              {models.map((model) => (
                <tr key={model.model}>
                  <td>{model.model}</td>
                  <td>{model.name}</td>
                  <td>{model.fieldCount}</td>
                  <td><button className="table-link-button" onClick={() => openModel(model)}>Open {model.model}</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">{connectionReady ? "Load Odoo models to browse available tables." : "Test and save a connection before browsing models."}</div>
        )}
      </Panel>

      <Panel title="3. Fields">
        {selectedModel ? <ActionRow icon={<Boxes size={18} />} title={selectedModel.model} meta={`${selectedModel.name} · ${supportedFields.length} supported fields`} /> : null}
        {fields.length ? (
          <div className="field-list">
            {fields.map((field) => (
              <label className={field.supported ? "field-row" : "field-row disabled-field"} key={field.name}>
                <input type="checkbox" checked={selectedFields.has(field.name)} onChange={() => toggleField(field.name)} disabled={!field.supported} />
                <span><strong>{field.name}</strong>{field.label} · {field.type}{field.relation ? ` -> ${field.relation}` : ""}{field.required ? " · required" : ""}{field.readonly ? " · readonly" : ""}{field.computed ? " · computed" : ""}{field.warning ? ` · ${field.warning}` : ""}</span>
              </label>
            ))}
          </div>
        ) : (
          <div className="empty-state">{loading === "fields" ? "Loading Odoo fields..." : "Open a model to inspect its fields."}</div>
        )}
      </Panel>

      <Panel title="4. Fetch Records">
        <div className="form-grid">
          <SchemaPicker
            label="Target schema"
            value={targetSchema}
            schemas={schemas}
            newSchemaName={newSchemaName}
            onChange={setTargetSchema}
            onNewSchemaName={setNewSchemaName}
            onAddSchema={addSchema}
          />
          <label>New table name<input value={tableName} onChange={(event) => setTableName(event.target.value)} placeholder="res_partner" /></label>
          <label>Domain filter<input value={domainFilter} onChange={(event) => setDomainFilter(event.target.value)} placeholder='[["customer","=",true]]' /></label>
          <label>Record limit<input value={recordLimit} onChange={(event) => setRecordLimit(event.target.value)} inputMode="numeric" /></label>
        </div>
        <div className="panel-actions">
          <button className="primary-button" onClick={fetchRecords} disabled={!canFetch}>{loading === "fetch" ? "Fetching..." : "Fetch records"}</button>
        </div>
      </Panel>
    </section>
  );
}

function Catalog({ navigate }: { navigate: (nextPath: string) => void }) {
  const { tables, error } = useCatalogTables();
  const [expandedTable, setExpandedTable] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [schemaFilter, setSchemaFilter] = useState("all");
  const [sourceFilter, setSourceFilter] = useState("all");
  const schemas = useMemo(() => [...new Set(tables.map((table) => table.schema))].sort(), [tables]);
  const sources = useMemo(() => [...new Set(tables.map((table) => table.source.kind))].sort(), [tables]);
  const totalRows = useMemo(() => tables.reduce((sum, table) => sum + table.rowCount, 0), [tables]);
  const filteredTables = useMemo(
    () =>
      tables.filter((table) => {
        const matchesQuery = `${table.qualifiedName} ${table.source.fileName ?? table.source.kind}`.toLowerCase().includes(query.trim().toLowerCase());
        const matchesSchema = schemaFilter === "all" || table.schema === schemaFilter;
        const matchesSource = sourceFilter === "all" || table.source.kind === sourceFilter;
        return matchesQuery && matchesSchema && matchesSource;
      }),
    [query, schemaFilter, sourceFilter, tables]
  );

  return (
    <section className="screen-grid">
      <Panel title="Table Registry">
        <div className="catalog-toolbar">
          <label>Search tables<input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="table, source, schema" /></label>
          <label>Schema
            <select value={schemaFilter} onChange={(event) => setSchemaFilter(event.target.value)}>
              <option value="all">All schemas</option>
              {schemas.map((schema) => <option value={schema} key={schema}>{schema}</option>)}
            </select>
          </label>
          <label>Source
            <select value={sourceFilter} onChange={(event) => setSourceFilter(event.target.value)}>
              <option value="all">All sources</option>
              {sources.map((source) => <option value={source} key={source}>{source}</option>)}
            </select>
          </label>
          <button className="icon-button" onClick={() => void window.location.reload()} title="Refresh catalog"><RefreshCcw size={16} /></button>
          <div className="catalog-stat"><strong>{filteredTables.length}</strong><span>shown</span></div>
          <div className="catalog-stat"><strong>{tables.length}</strong><span>total</span></div>
          <div className="catalog-stat"><strong>{schemas.length}</strong><span>schemas</span></div>
          <div className="catalog-stat"><strong>{totalRows}</strong><span>rows</span></div>
        </div>
        {error ? <div className="notice error">{error}</div> : null}
        {tables.length ? (
          <div className="catalog-table-wrap">
            <table>
              <thead><tr><th>Table</th><th>Schema</th><th>Rows</th><th>Columns</th><th>Source</th><th>Action</th></tr></thead>
              <tbody>
                {filteredTables.map((table) => (
                  <Fragment key={table.qualifiedName}>
                    <tr key={table.qualifiedName}>
                      <td>{table.qualifiedName}</td>
                      <td>{table.schema}</td>
                      <td>{table.rowCount}</td>
                      <td>{table.columnCount}</td>
                      <td>{table.source.fileName ?? table.source.kind}</td>
                      <td>
                        <button className="table-link-button" onClick={() => setExpandedTable((current) => current === table.qualifiedName ? null : table.qualifiedName)}>
                          {expandedTable === table.qualifiedName ? "Close" : "Open"}
                        </button>
                      </td>
                    </tr>
                    {expandedTable === table.qualifiedName ? (
                      <tr key={`${table.qualifiedName}-detail`}>
                        <td colSpan={6}>
                          <div className="inline-detail">
                            <div className="inline-detail-overview">
                              <strong>{table.qualifiedName}</strong>
                              <span>{table.source.fileName ?? table.source.kind} · {table.rowCount} rows · {table.columnCount} columns</span>
                            </div>
                            <div className="inline-column-preview">
                              {table.columns.slice(0, 8).map((column) => <span key={column.name}>{column.name}:{column.type}</span>)}
                            </div>
                            <div className="row-actions">
                              <button className="table-link-button" onClick={() => navigate(tableDetailPath(table))}>Full detail</button>
                              <button className="table-link-button" onClick={() => navigate(tableManagePath(table))}>Manage table</button>
                              <button className="table-link-button" onClick={() => navigate(tableExportPath(table))}>Export CSV</button>
                              <button className="table-link-button" onClick={() => insertLoadTable(table)}>Use in Python</button>
                            </div>
                          </div>
                        </td>
                      </tr>
                    ) : null}
                  </Fragment>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">No tables yet. Import a CSV or Excel file to populate the registry.</div>
        )}
      </Panel>
    </section>
  );
}

function TableDetail() {
  const { tables, error } = useCatalogTables();
  const selected = selectedTableFromLocation();
  const table = selected
    ? tables.find((item) => item.schema === selected.schema && item.tableName === selected.tableName)
    : tables[0];
  const [preview, setPreview] = useState<TablePreview | null>(null);
  const [previewError, setPreviewError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"overview" | "columns" | "preview">("overview");

  useEffect(() => {
    setPreview(null);
    setPreviewError(null);
    if (!table) return;
    fetchTablePreview(table.schema, table.tableName)
      .then(setPreview)
      .catch((loadError: Error) => setPreviewError(loadError.message));
  }, [table]);

  if (!table) {
    return (
      <section className="screen-grid">
        <Panel title="Table Detail">
          {error ? <div className="notice error">{error}</div> : <div className="empty-state">Import a table to see metadata and preview rows here.</div>}
        </Panel>
      </section>
    );
  }

  return (
    <section className="screen-grid">
      <Panel title={table.qualifiedName}>
        <div className="tab-list">
          <button className={activeTab === "overview" ? "active" : ""} onClick={() => setActiveTab("overview")}>Overview</button>
          <button className={activeTab === "columns" ? "active" : ""} onClick={() => setActiveTab("columns")}>Columns</button>
          <button className={activeTab === "preview" ? "active" : ""} onClick={() => setActiveTab("preview")}>Preview</button>
        </div>
        {activeTab === "overview" ? (
          <dl className="details">
            <dt>Rows</dt><dd>{table.rowCount}</dd>
            <dt>Columns</dt><dd>{table.columnCount}</dd>
            <dt>Source</dt><dd>{table.source.fileName ?? table.source.kind}</dd>
            <dt>Created</dt><dd>{table.createdAt}</dd>
          </dl>
        ) : null}
        {activeTab === "columns" ? (
          <table className="data-table">
            <thead><tr><th>Name</th><th>Type</th><th>Source column</th></tr></thead>
            <tbody>
              {table.columns.map((column) => (
                <tr key={column.name}><td>{column.name}</td><td>{column.type}</td><td>{column.sourceName}</td></tr>
              ))}
            </tbody>
          </table>
        ) : null}
        {activeTab === "preview" ? (
          previewError ? <div className="notice error">{previewError}</div> : preview ? <DataPreview rows={preview.rows} /> : <div className="table-preview">Loading preview...</div>
        ) : null}
        <div className="panel-actions">
          <button className="table-link-button" onClick={() => pushRoute(tableManagePath(table))}>Manage table</button>
          <button className="table-link-button" onClick={() => pushRoute(tableExportPath(table))}>Export CSV</button>
        </div>
      </Panel>
    </section>
  );
}

function TableManagement() {
  const { tables, reload } = useCatalogTables();
  const selected = selectedTableFromLocation();
  const table = selected ? tables.find((item) => item.schema === selected.schema && item.tableName === selected.tableName) : tables[0];
  const [newName, setNewName] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runAction = async (action: "rename" | "truncate" | "drop") => {
    if (!table) return;
    setMessage(null);
    setError(null);
    try {
      if (action === "rename") {
        const renamed = await renameCatalogTable(table.schema, table.tableName, newName);
        setMessage(`Renamed to ${renamed.qualifiedName}.`);
        pushRoute(tableManagePath(renamed));
      } else if (action === "truncate") {
        await truncateCatalogTable(table.schema, table.tableName, confirmation);
        setMessage(`${table.qualifiedName} truncated.`);
      } else {
        await dropCatalogTable(table.schema, table.tableName, confirmation);
        setMessage(`${table.qualifiedName} dropped.`);
        pushRoute("/catalog");
      }
      await reload();
    } catch (value) {
      setError(value instanceof Error ? value.message : "Table action failed");
    }
  };

  if (!table) return <Placeholder title="Table Management Confirmation" items={["Import a table before managing storage."]} />;
  return (
    <section className="screen-grid">
      <Panel title={`Manage ${table.qualifiedName}`}>
        <div className="form-grid">
          <label>New table name<input value={newName} onChange={(event) => setNewName(event.target.value)} placeholder={table.tableName} /></label>
          <label>Confirm qualified name<input value={confirmation} onChange={(event) => setConfirmation(event.target.value)} placeholder={table.qualifiedName} /></label>
        </div>
        <div className="panel-actions row-actions">
          <button className="table-link-button" onClick={() => runAction("rename")} disabled={!newName.trim()}>Rename</button>
          <button className="table-link-button" onClick={() => runAction("truncate")} disabled={confirmation !== table.qualifiedName}>Truncate</button>
          <button className="table-link-button danger-button" onClick={() => runAction("drop")} disabled={confirmation !== table.qualifiedName}>Drop</button>
        </div>
        {message ? <div className="notice success">{message}</div> : null}
        {error ? <div className="notice error">{error}</div> : null}
      </Panel>
    </section>
  );
}

function ExportTable() {
  const { tables } = useCatalogTables();
  const selected = selectedTableFromLocation();
  const table = selected ? tables.find((item) => item.schema === selected.schema && item.tableName === selected.tableName) : tables[0];
  const [result, setResult] = useState<{ filename: string; text: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runExport = async () => {
    if (!table) return;
    setError(null);
    try {
      setResult(await exportCatalogTable(table.schema, table.tableName));
    } catch (value) {
      setError(value instanceof Error ? value.message : "Export failed");
    }
  };

  if (!table) return <Placeholder title="Export Table Modal" items={["Import a table before exporting."]} />;
  return (
    <section className="screen-grid">
      <Panel title={`Export ${table.qualifiedName}`}>
        <div className="details">
          <dt>Format</dt><dd>CSV with header row</dd>
          <dt>Rows</dt><dd>{table.rowCount}</dd>
        </div>
        <div className="panel-actions">
          <button className="primary-button" onClick={runExport}>Prepare CSV</button>
        </div>
        {error ? <div className="notice error">{error}</div> : null}
        {result ? (
          <div className="terminal">
            <strong>{result.filename}</strong>
            <pre>{result.text.slice(0, 1200)}</pre>
          </div>
        ) : null}
      </Panel>
    </section>
  );
}

function CodeWorkspace({ initialAgentOpen = true }: { initialAgentOpen?: boolean }) {
  const { tables, error, reload } = useCatalogTables();
  const [scriptName, setScriptName] = useState("analysis.py");
  const [code, setCode] = useState(defaultPythonCode(tables[0]?.qualifiedName));
  const [result, setResult] = useState<RunScriptResult | null>(null);
  const [runError, setRunError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);
  const [agentOpen, setAgentOpen] = useState(initialAgentOpen);
  const [previewTable, setPreviewTable] = useState<TablePreview | null>(null);
  const [selectedTableName, setSelectedTableName] = useState<string | null>(tables[0]?.qualifiedName ?? null);
  const [outputTab, setOutputTab] = useState<"result" | "stdout" | "stderr" | "saved">("result");

  useEffect(() => {
    if (!tables[0]) return;
    setSelectedTableName((current) => current ?? tables[0].qualifiedName);
    setCode((current) =>
      current.includes("raw_files.sales_orders_raw")
        ? defaultPythonCode(tables[0].qualifiedName)
        : current
    );
  }, [tables]);

  useEffect(() => {
    const selectedScript = new URLSearchParams(window.location.search).get("script");
    const agentCode = window.sessionStorage.getItem("agentCodeDraft");
    if (agentCode) {
      setCode(agentCode);
      window.sessionStorage.removeItem("agentCodeDraft");
    }
    if (!selectedScript) return;
    fetchSavedScript(selectedScript)
      .then((script) => {
        setScriptName(script.name);
        setCode(script.code);
      })
      .catch((errorValue: Error) => setRunError(errorValue.message));
  }, []);

  const runCode = async () => {
    setIsRunning(true);
    setRunError(null);
    setResult(null);
    try {
      const nextResult = await runPythonScript({ scriptName, code });
      setResult(nextResult);
      setOutputTab("result");
      await reload();
    } catch (errorValue) {
      setRunError(errorValue instanceof Error ? errorValue.message : "Script run failed");
    } finally {
      setIsRunning(false);
    }
  };

  const saveCurrentScript = async () => {
    setIsSaving(true);
    setRunError(null);
    setSaveMessage(null);
    try {
      const saved = await savePythonScript({ scriptName, code });
      setScriptName(saved.name);
      setSaveMessage(`${saved.name} saved.`);
    } catch (errorValue) {
      setRunError(errorValue instanceof Error ? errorValue.message : "Script save failed");
    } finally {
      setIsSaving(false);
    }
  };

  const insertAtEnd = (nextCode: string) => {
    setCode((current) => `${current.trim()}\n\n${nextCode.trim()}\n`);
  };

  return (
    <section className={agentOpen ? "code-grid agent-open" : "code-grid"}>
      <SchemaBrowser
        tables={tables}
        error={error}
        onInsertLoad={(table) => {
          setSelectedTableName(table.qualifiedName);
          setCode((current) => `${current.trim()}\n\ndf = load_table("${table.qualifiedName}")\nshow(df.head(), name="${table.tableName}_preview")\n`);
        }}
        onPreview={(table) => {
          setSelectedTableName(table.qualifiedName);
          setPreviewTable(null);
          fetchTablePreview(table.schema, table.tableName).then(setPreviewTable).catch(() => setPreviewTable({ schema: table.schema, tableName: table.tableName, columns: [], rows: [] }));
        }}
        onOpenCatalog={(table) => pushRoute(tableDetailPath(table))}
      />
      <div className="code-main-column">
        <Panel title="Python Editor">
          <div className="editor-toolbar">
            <label>Script name<input value={scriptName} onChange={(event) => setScriptName(event.target.value)} /></label>
            <div className="row-actions">
              <button className="icon-button" onClick={saveCurrentScript} disabled={isSaving || !scriptName.trim() || !code.trim()} title="Save script">
                <Save size={15} />{isSaving ? "Saving" : "Save"}
              </button>
              <button className="icon-button" onClick={() => setAgentOpen((current) => !current)} title={agentOpen ? "Hide agent" : "Show agent"}><Send size={15} />Agent</button>
              <button className="primary-button" onClick={runCode} disabled={isRunning || !scriptName.trim() || !code.trim()}>{isRunning ? "Running..." : "Run"}</button>
            </div>
          </div>
          <textarea className="editor code-textarea" value={code} onChange={(event) => setCode(event.target.value)} />
          {saveMessage ? <div className="notice success">{saveMessage}</div> : null}
        </Panel>
        <Panel title="Run Output">
          {runError ? <div className="notice error">{runError}</div> : null}
          {previewTable ? (
            <div className="preview-callout">
              <strong>{previewTable.schema}.{previewTable.tableName}</strong>
              <DataPreview rows={previewTable.rows} />
            </div>
          ) : null}
          {result ? (
            <div className={result.status === "success" ? "result-explorer success-terminal" : "result-explorer error-terminal"}>
              <div className="result-summary">
                <strong>{result.status === "success" ? "Success" : "Error"}</strong>
                <span>Return code: {result.returnCode}</span>
                {result.savedTables.length ? <span>Saved: {result.savedTables.join(", ")}</span> : null}
                {result.stdout.trim() ? <span>{result.stdout.trim().slice(0, 120)}</span> : null}
              </div>
              <div className="tab-list">
                <button className={outputTab === "result" ? "active" : ""} onClick={() => setOutputTab("result")}>Result</button>
                <button className={outputTab === "stdout" ? "active" : ""} onClick={() => setOutputTab("stdout")}>stdout</button>
                <button className={outputTab === "stderr" ? "active" : ""} onClick={() => setOutputTab("stderr")}>stderr</button>
                <button className={outputTab === "saved" ? "active" : ""} onClick={() => setOutputTab("saved")}>Saved tables</button>
              </div>
              {outputTab === "result" ? <ResultGrid artifact={result.preview ?? null} /> : null}
              {outputTab === "stdout" ? <pre className="terminal-pre">{result.stdout || "(empty)"}</pre> : null}
              {outputTab === "stderr" ? <pre className="terminal-pre">{result.stderr || "(empty)"}</pre> : null}
              {outputTab === "saved" ? <SavedTableList result={result} /> : null}
            </div>
          ) : (
            <div className="terminal">Ready to run with local project Python.</div>
          )}
        </Panel>
      </div>
      {agentOpen ? (
        <AgentPanel
          embedded
          onInsertCode={insertAtEnd}
          onReplaceCode={setCode}
          priorCode={code}
          selectedTable={selectedTableName}
          lastError={result?.stderr || runError || ""}
        />
      ) : null}
    </section>
  );
}

function AgentPanel({
  embedded = false,
  onInsertCode,
  onReplaceCode,
  priorCode = "",
  selectedTable,
  lastError = ""
}: {
  embedded?: boolean;
  onInsertCode?: (code: string) => void;
  onReplaceCode?: (code: string) => void;
  priorCode?: string;
  selectedTable?: string | null;
  lastError?: string;
}) {
  const [draft, setDraft] = useState("Create a cleaned curated table from the selected table");
  const [messages, setMessages] = useState<AgentChatMessage[]>([
    { role: "assistant", content: "Ask a question or ask me to write Python for the editor." }
  ]);
  const [generatedCode, setGeneratedCode] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!draft.trim() || loading) return;
    const nextMessages: AgentChatMessage[] = [...messages, { role: "user", content: draft.trim() }];
    setMessages(nextMessages);
    setDraft("");
    setLoading(true);
    setError(null);
    try {
      const result = await chatWithAgent({
        messages: nextMessages,
        currentCode: priorCode,
        selectedTable,
        lastRunError: lastError
      });
      setMessages([...nextMessages, { role: "assistant", content: result.message }]);
      if (result.code) setGeneratedCode(result.code);
    } catch (value) {
      setError(value instanceof Error ? value.message : "Agent chat failed");
    } finally {
      setLoading(false);
    }
  };

  const copyGeneratedCode = async () => {
    if (!generatedCode.trim()) return;
    await navigator.clipboard.writeText(generatedCode);
  };

  const insertGeneratedCode = () => {
    if (!generatedCode.trim()) return;
    if (onInsertCode) onInsertCode(generatedCode);
    else {
      window.sessionStorage.setItem("agentCodeDraft", generatedCode);
      pushRoute("/code");
    }
  };

  const replaceEditor = () => {
    if (!generatedCode.trim()) return;
    if (onReplaceCode) onReplaceCode(generatedCode);
    else {
      window.sessionStorage.setItem("agentCodeDraft", generatedCode);
      pushRoute("/code");
    }
  };

  const content = (
    <Panel title="Agent Chat">
      <div className="agent-meta-row">
        <span>{selectedTable ?? "No table selected"}</span>
        {lastError ? <button className="table-link-button" onClick={() => setDraft(`Fix this error in the current code:\n${lastError}`)}>Use last error</button> : null}
      </div>
      <div className="chat-stream">
        {messages.map((message, index) => (
          <div className={`chat-message ${message.role}`} key={`${message.role}-${index}`}>
            <strong>{message.role === "assistant" ? "Agent" : "You"}</strong>
            <span>{message.content}</span>
          </div>
        ))}
        {loading ? <div className="chat-message assistant"><strong>Agent</strong><span>Working...</span></div> : null}
      </div>
      <label>Message<textarea className="editor compact-editor" value={draft} onChange={(event) => setDraft(event.target.value)} /></label>
      <div className="panel-actions row-actions">
        <button className="primary-button" onClick={sendMessage} disabled={loading || !draft.trim()}><Send size={14} />Send</button>
      </div>
      {error ? <div className="notice error">{error}</div> : null}
      <div className="generated-code-box">
        <div className="generated-code-header">
          <strong>Code from chat</strong>
          <div className="row-actions">
            <button className="icon-button" onClick={copyGeneratedCode} disabled={!generatedCode.trim()} title="Copy code"><Copy size={14} />Copy</button>
            <button className="icon-button" onClick={insertGeneratedCode} disabled={!generatedCode.trim()} title="Insert code">Insert</button>
            <button className="icon-button" onClick={replaceEditor} disabled={!generatedCode.trim()} title="Replace editor">Replace</button>
          </div>
        </div>
        <textarea className="editor generated-code-textarea" value={generatedCode} onChange={(event) => setGeneratedCode(event.target.value)} placeholder="Generated Python appears here." />
      </div>
    </Panel>
  );

  return embedded ? <div className="agent-dock">{content}</div> : <section className="code-grid">{content}</section>;
}

function SchemaBrowser({
  tables,
  error,
  onInsertLoad,
  onPreview,
  onOpenCatalog
}: {
  tables: CatalogTable[];
  error: string | null;
  onInsertLoad: (table: CatalogTable) => void;
  onPreview: (table: CatalogTable) => void;
  onOpenCatalog: (table: CatalogTable) => void;
}) {
  const [query, setQuery] = useState("");
  const groups = useMemo(() => {
    const grouped = new Map<string, CatalogTable[]>();
    tables.forEach((table) => {
      const current = grouped.get(table.schema) ?? [];
      current.push(table);
      grouped.set(table.schema, current);
    });
    return [...grouped.entries()].sort(([left], [right]) => left.localeCompare(right));
  }, [tables]);
  const [openSchemas, setOpenSchemas] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (!groups.length) return;
    setOpenSchemas((current) => current.size ? current : new Set(groups.map(([schema]) => schema)));
  }, [groups]);

  return (
    <Panel title="Schema Browser">
      <label>Find table<input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="orders, curated, raw" /></label>
      {error ? <div className="notice error">{error}</div> : null}
      {groups.length ? (
        <div className="object-browser">
          {groups.map(([schema, schemaTables]) => {
            const open = openSchemas.has(schema);
            const visibleTables = schemaTables.filter((table) => table.tableName.toLowerCase().includes(query.trim().toLowerCase()) || table.qualifiedName.toLowerCase().includes(query.trim().toLowerCase()));
            if (!visibleTables.length && query.trim()) return null;
            return (
              <div className="schema-group" key={schema}>
                <button className="schema-row" onClick={() => setOpenSchemas((current) => {
                  const next = new Set(current);
                  if (next.has(schema)) next.delete(schema);
                  else next.add(schema);
                  return next;
                })}>
                  {open ? <ChevronDown size={15} /> : <ChevronRight size={15} />}
                  <strong>{schema}</strong>
                  <span>{schemaTables.length}</span>
                </button>
                {open ? visibleTables.map((table) => (
                  <div className="object-row" key={table.qualifiedName}>
                    <Table2 size={14} />
                    <button aria-label={table.qualifiedName} onClick={() => onInsertLoad(table)} title={`Insert load_table("${table.qualifiedName}")`}>
                      <strong>{table.tableName}</strong>
                      <span>{table.rowCount} rows · {table.columnCount} cols</span>
                    </button>
                    <div className="object-actions">
                      <button onClick={() => onPreview(table)} title={`Preview ${table.qualifiedName}`}>Preview</button>
                      <button onClick={() => onOpenCatalog(table)} title={`Open ${table.qualifiedName} in Catalog`}>Open catalog</button>
                    </div>
                  </div>
                )) : null}
              </div>
            );
          })}
        </div>
      ) : (
        <div className="empty-state">Imported and derived tables will appear here.</div>
      )}
    </Panel>
  );
}

function ResultGrid({ artifact }: { artifact: ResultArtifact | null }) {
  if (!artifact) {
    return <div className="table-preview">No dataframe preview yet. Use save_table(df, ...) or show(df, name="result").</div>;
  }
  return (
    <div className="result-grid">
      <div className="result-grid-meta">
        <strong>{artifact.qualifiedName ?? artifact.name ?? "result"}</strong>
        <span>{artifact.rowCount} rows · {artifact.columnCount} columns</span>
      </div>
      <DataPreview rows={artifact.rows} />
    </div>
  );
}

function SavedTableList({ result }: { result: RunScriptResult }) {
  if (!result.resultTables.length && !result.savedTables.length) {
    return <div className="table-preview">No saved tables from this run.</div>;
  }
  return (
    <div className="saved-table-list">
      {result.resultTables.map((table) => (
        <div className="saved-table-row" key={table.qualifiedName}>
          <strong>{table.qualifiedName}</strong>
          <span>{table.rowCount} rows · {table.columnCount} columns</span>
          {table.qualifiedName ? <button className="table-link-button" onClick={() => {
            const [schema, tableName] = table.qualifiedName!.split(".", 2);
            pushRoute(`/catalog/table?${new URLSearchParams({ schema, table: tableName }).toString()}`);
          }}>Open in Catalog</button> : null}
        </div>
      ))}
    </div>
  );
}

function SavedScripts() {
  const [scripts, setScripts] = useState<SavedScript[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchSavedScripts()
      .then(setScripts)
      .catch((errorValue: Error) => setError(errorValue.message));
  }, []);

  const openScript = (scriptName: string) => {
    window.history.pushState({}, "", `/code?script=${encodeURIComponent(scriptName)}`);
    window.dispatchEvent(new PopStateEvent("popstate"));
  };

  return (
    <section className="screen-grid">
      <Panel title="Saved Scripts">
        {error ? <div className="notice error">{error}</div> : null}
        {scripts.length ? (
          <table>
            <thead><tr><th>Name</th><th>Updated</th><th>Size</th><th>Action</th></tr></thead>
            <tbody>
              {scripts.map((script) => (
                <tr key={script.name}>
                  <td>{script.name}</td>
                  <td>{formatDate(script.updatedAt)}</td>
                  <td>{script.size}</td>
                  <td>
                    <button className="table-link-button" onClick={() => openScript(script.name)}>
                      Open
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">No saved scripts yet. Use Save Script in Code Workspace when a script is ready.</div>
        )}
      </Panel>
    </section>
  );
}

function Pipelines({ navigate }: { navigate: (nextPath: string) => void }) {
  const [scripts, setScripts] = useState<SavedScript[]>([]);
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);
  const [runs, setRuns] = useState<PipelineRun[]>([]);
  const [failures, setFailures] = useState<PipelineFailure[]>([]);
  const [statusFilter, setStatusFilter] = useState("all");
  const [pipelineName, setPipelineName] = useState("");
  const [scriptId, setScriptId] = useState("");
  const [connectorSyncId, setConnectorSyncId] = useState("");
  const [scheduleDrafts, setScheduleDrafts] = useState<Record<string, PipelineSchedulePayload>>({});
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<string | null>(null);

  const reload = async () => {
    setError(null);
    try {
      const [nextScripts, nextPipelines, nextRuns, nextFailures] = await Promise.all([
        fetchSavedScripts(),
        fetchPipelines(),
        fetchPipelineRuns(statusFilter),
        fetchPipelineFailures()
      ]);
      setScripts(nextScripts);
      setPipelines(nextPipelines);
      setRuns(nextRuns);
      setFailures(nextFailures);
      setScriptId((current) => current || nextScripts[0]?.name || "");
    } catch (value) {
      setError(value instanceof Error ? value.message : "Pipeline load failed");
    }
  };

  useEffect(() => {
    void reload();
  }, [statusFilter]);

  const createNewPipeline = async () => {
    setLoading("create");
    setError(null);
    setMessage(null);
    try {
      const pipeline = await createPipeline({ pipelineName, scriptId, connectorSyncId: connectorSyncId.trim() || null });
      setMessage(`Pipeline '${pipeline.name}' saved.`);
      await reload();
    } catch (value) {
      setError(value instanceof Error ? value.message : "Pipeline create failed");
    } finally {
      setLoading(null);
    }
  };

  const togglePipeline = async (pipeline: Pipeline) => {
    setLoading(`toggle-${pipeline.id}`);
    setError(null);
    setMessage(null);
    try {
      const updated = await setPipelineEnabled(pipeline.id, !pipeline.enabled);
      setMessage(`${updated.name} is now ${updated.enabled ? "enabled" : "disabled"}.`);
      await reload();
    } catch (value) {
      setError(value instanceof Error ? value.message : "Pipeline update failed");
    } finally {
      setLoading(null);
    }
  };

  const runNow = async (pipeline: Pipeline) => {
    setLoading(`run-${pipeline.id}`);
    setError(null);
    setMessage(null);
    try {
      const run = await runPipelineNow(pipeline.id);
      setMessage(`Run ${run.status}: ${pipeline.name}`);
      await reload();
      navigate(`/pipelines/run?run=${encodeURIComponent(run.id)}`);
    } catch (value) {
      setError(value instanceof Error ? value.message : "Pipeline run failed");
    } finally {
      setLoading(null);
    }
  };

  const updateScheduleDraft = (pipeline: Pipeline, patch: Partial<PipelineSchedulePayload>) => {
    setScheduleDrafts((current) => ({
      ...current,
      [pipeline.id]: {
        ...pipelineScheduleDraft(pipeline),
        ...current[pipeline.id],
        ...patch
      }
    }));
  };

  const saveSchedule = async (pipeline: Pipeline) => {
    setLoading(`schedule-${pipeline.id}`);
    setError(null);
    setMessage(null);
    try {
      const schedule = await setPipelineSchedule(pipeline.id, scheduleDrafts[pipeline.id] ?? pipelineScheduleDraft(pipeline));
      setMessage(`${pipeline.name} schedule saved. Next run ${formatDate(schedule.nextRunAt)}.`);
      await reload();
    } catch (value) {
      setError(value instanceof Error ? value.message : "Pipeline schedule update failed");
    } finally {
      setLoading(null);
    }
  };

  const ackFailure = async (failure: PipelineFailure) => {
    setLoading(`ack-${failure.runId}`);
    setError(null);
    setMessage(null);
    try {
      await acknowledgePipelineFailure(failure.runId);
      setMessage(`${failure.pipelineName} failure acknowledged.`);
      await reload();
    } catch (value) {
      setError(value instanceof Error ? value.message : "Pipeline failure acknowledge failed");
    } finally {
      setLoading(null);
    }
  };

  return (
    <section className="screen-grid">
      <Panel title="Create Pipeline">
        <div className="form-grid">
          <label>Pipeline name<input value={pipelineName} onChange={(event) => setPipelineName(event.target.value)} /></label>
          <label>Saved script
            <select value={scriptId} onChange={(event) => setScriptId(event.target.value)}>
              <option value="">Select a script</option>
              {scripts.map((script) => <option value={script.name} key={script.name}>{script.name}</option>)}
            </select>
          </label>
          <label>Odoo sync cursor ID<input value={connectorSyncId} onChange={(event) => setConnectorSyncId(event.target.value)} placeholder="optional" /></label>
        </div>
        <div className="panel-actions">
          <button className="primary-button" onClick={createNewPipeline} disabled={!pipelineName.trim() || !scriptId || loading === "create"}>{loading === "create" ? "Saving..." : "Create pipeline"}</button>
        </div>
        {message ? <div className="notice success">{message}</div> : null}
        {error ? <div className="notice error">{error}</div> : null}
      </Panel>

      {failures.length ? (
        <Panel title="Active Failures">
          <div className="failure-list">
            {failures.map((failure) => (
              <div className="failure-item" key={failure.runId}>
                <div>
                  <strong>{failure.pipelineName}</strong>
                  <span>{failure.message}</span>
                  <small>{formatDate(failure.createdAt)}</small>
                </div>
                <button className="table-link-button" onClick={() => ackFailure(failure)} disabled={loading === `ack-${failure.runId}`}>{loading === `ack-${failure.runId}` ? "Acknowledging..." : "Acknowledge"}</button>
              </div>
            ))}
          </div>
        </Panel>
      ) : null}

      <Panel title="Pipeline List">
        {pipelines.length ? (
          <table>
            <thead><tr><th>Name</th><th>Script</th><th>Status</th><th>Schedule</th><th>Last run</th><th>Actions</th></tr></thead>
            <tbody>
              {pipelines.map((pipeline) => {
                const draft = scheduleDrafts[pipeline.id] ?? pipelineScheduleDraft(pipeline);
                return (
                  <tr key={pipeline.id}>
                    <td>{pipeline.name}</td>
                    <td>{pipeline.scriptId}</td>
                    <td>
                      <span className={pipeline.enabled ? "status-text" : "status-text warning-text"}>{pipeline.enabled ? "enabled" : "disabled"}</span>
                      {failures.some((failure) => failure.pipelineId === pipeline.id) ? <span className="status-text danger-text">failure</span> : null}
                    </td>
                    <td>
                      <div className="schedule-controls">
                        <span className="schedule-summary">{pipeline.schedule ? `${pipeline.schedule.type} · next ${formatDate(pipeline.schedule.nextRunAt)}` : "Not scheduled"}</span>
                        <select aria-label={`Schedule type for ${pipeline.name}`} value={draft.type} onChange={(event) => updateScheduleDraft(pipeline, { type: event.target.value as PipelineSchedulePayload["type"] })}>
                          <option value="hourly">Hourly</option>
                          <option value="daily">Daily</option>
                          <option value="weekly">Weekly</option>
                          <option value="cron">Cron</option>
                        </select>
                        {draft.type === "daily" || draft.type === "weekly" ? (
                          <input aria-label={`Time of day for ${pipeline.name}`} value={draft.timeOfDay ?? "06:00"} onChange={(event) => updateScheduleDraft(pipeline, { timeOfDay: event.target.value })} />
                        ) : null}
                        {draft.type === "weekly" ? (
                          <select aria-label={`Weekday for ${pipeline.name}`} value={draft.weekday ?? "monday"} onChange={(event) => updateScheduleDraft(pipeline, { weekday: event.target.value })}>
                            {["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].map((weekday) => <option value={weekday} key={weekday}>{weekday}</option>)}
                          </select>
                        ) : null}
                        {draft.type === "cron" ? (
                          <input aria-label={`Cron expression for ${pipeline.name}`} value={draft.cronExpression ?? "0 6 * * *"} onChange={(event) => updateScheduleDraft(pipeline, { cronExpression: event.target.value })} />
                        ) : null}
                        <input aria-label={`Timezone for ${pipeline.name}`} value={draft.timezone ?? "Asia/Kolkata"} onChange={(event) => updateScheduleDraft(pipeline, { timezone: event.target.value })} />
                        <button className="table-link-button" onClick={() => saveSchedule(pipeline)} disabled={loading === `schedule-${pipeline.id}`}>{loading === `schedule-${pipeline.id}` ? "Saving..." : "Save schedule"}</button>
                      </div>
                    </td>
                    <td>{pipeline.lastRun ? `${pipeline.lastRun.status} · ${formatDate(pipeline.lastRun.startedAt)}` : "No runs"}</td>
                    <td>
                      <div className="row-actions">
                        <button className="table-link-button" onClick={() => runNow(pipeline)} disabled={loading === `run-${pipeline.id}`}>{loading === `run-${pipeline.id}` ? "Running..." : "Run now"}</button>
                        <button className="table-link-button" onClick={() => togglePipeline(pipeline)} disabled={loading === `toggle-${pipeline.id}`}>{pipeline.enabled ? "Disable" : "Enable"}</button>
                        {pipeline.lastRun ? <button className="table-link-button" onClick={() => navigate(`/pipelines/run?run=${encodeURIComponent(pipeline.lastRun!.id)}`)}>Open run</button> : null}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">{scripts.length ? "Create a pipeline from a saved script." : "Save a script from Code Workspace before creating a pipeline."}</div>
        )}
      </Panel>

      <Panel title="Run History">
        <div className="inline-controls">
          <label>Status filter
            <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
              <option value="all">All</option>
              <option value="success">Success</option>
              <option value="error">Error</option>
            </select>
          </label>
        </div>
        {runs.length ? (
          <table>
            <thead><tr><th>Pipeline</th><th>Status</th><th>Trigger</th><th>Started</th><th>Action</th></tr></thead>
            <tbody>
              {runs.map((run) => (
                <tr key={run.id}>
                  <td>{run.pipelineName}</td>
                  <td><span className={run.status === "error" ? "status-text danger-text" : "status-text"}>{run.status}</span></td>
                  <td>{run.trigger ?? "manual"}</td>
                  <td>{formatDate(run.startedAt)}</td>
                  <td><button className="table-link-button" onClick={() => navigate(`/pipelines/run?run=${encodeURIComponent(run.id)}`)}>Open run</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">No {statusFilter === "all" ? "" : statusFilter} runs yet.</div>
        )}
      </Panel>
    </section>
  );
}

function RunDetail() {
  const [run, setRun] = useState<PipelineRun | null>(null);
  const [error, setError] = useState<string | null>(null);
  const runId = new URLSearchParams(window.location.search).get("run");

  useEffect(() => {
    setRun(null);
    setError(null);
    if (!runId) return;
    fetchPipelineRun(runId)
      .then(setRun)
      .catch((value: Error) => setError(value.message));
  }, [runId]);

  return (
    <section className="screen-grid">
      <Panel title="Pipeline Run Detail">
        {error ? <div className="notice error">{error}</div> : null}
        {!runId ? <div className="empty-state">Open a run from Pipelines to see logs and status.</div> : null}
        {run ? (
          <dl className="details">
            <dt>Pipeline</dt><dd>{run.pipelineName}</dd>
            <dt>Status</dt><dd>{run.status}</dd>
            <dt>Script</dt><dd>{run.scriptId}</dd>
            <dt>Odoo sync step</dt><dd>{run.preStep ? `${run.preStep.status} · ${run.preStep.message}` : "none"}</dd>
            <dt>Started</dt><dd>{formatDate(run.startedAt)}</dd>
            <dt>Duration</dt><dd>{run.durationMs} ms</dd>
            <dt>Saved tables</dt><dd>{run.savedTables.length ? run.savedTables.join(", ") : "none"}</dd>
          </dl>
        ) : runId && !error ? (
          <div className="table-preview">Loading run detail...</div>
        ) : null}
      </Panel>
      {run ? (
        <Panel title="Logs">
          <div className={run.status === "success" ? "terminal success-terminal" : "terminal error-terminal"}>
            <strong>{run.status === "success" ? "Success" : "Error"}</strong>
            <span>Return code: {run.returnCode}</span>
            <pre>{run.stdout || run.stderr || "No output"}</pre>
          </div>
        </Panel>
      ) : null}
    </section>
  );
}

function StorageSettings({ storage }: { storage: StorageStatus | null }) {
  return (
    <section className="storage-layout">
      <div className="summary-band health-band">
        <Metric label="Storage status" value={storage?.databaseReady ? "Healthy" : "..."} detail={storage?.error ?? "DuckDB workspace"} />
        <Metric label="Database" value={storage?.status ?? "checking"} detail="local warehouse" />
        <Metric label="LLM vault" value="Encrypted" detail="project metadata folder" />
        <Metric label="Restart behavior" value="Auto-load" detail="picked up by backend" />
      </div>

      <Panel title="Workspace Paths">
        <dl className="details">
          <dt>Status</dt><dd>{storage?.status ?? "checking"}</dd>
          <dt>Database</dt><dd>{storage?.databasePath ?? "checking"}</dd>
          <dt>Workspace</dt><dd>{storage?.workspaceRoot ?? "checking"}</dd>
          <dt>Checked</dt><dd>{storage?.checkedAt ?? "checking"}</dd>
        </dl>
      </Panel>

      <LlmSettingsPanel />

      <Panel title="Maintenance">
        <div className="maintenance-grid">
          <ActionRow icon={<HardDrive size={18} />} title="Local warehouse" meta="DuckDB files stay inside this project workspace." />
          <ActionRow icon={<ShieldCheck size={18} />} title="Encrypted credentials" meta="LLM keys are never returned to the browser after save." />
          <ActionRow icon={<Activity size={18} />} title="Health check" meta={storage?.databaseReady ? "Storage is reachable." : "Storage is still checking."} />
        </div>
      </Panel>
    </section>
  );
}

function LlmSettingsPanel() {
  const defaults: Record<LlmProvider, { label: string; model: string; base_url: string }> = {
    openai: { label: "OpenAI", model: "gpt-4o-mini", base_url: "https://api.openai.com/v1" },
    kimi: { label: "Kimi", model: "kimi-for-coding", base_url: "https://api.kimi.com/coding/v1/chat/completions" },
    anthropic: { label: "Anthropic", model: "claude-3-5-sonnet-20241022", base_url: "https://api.anthropic.com" },
    "azure-openai": { label: "Azure OpenAI", model: "", base_url: "" }
  };
  const [config, setConfig] = useState<LlmConfig | null>(null);
  const [profiles, setProfiles] = useState<LlmProfile[]>([]);
  const [provider, setProvider] = useState<LlmProvider>("kimi");
  const [label, setLabel] = useState("Kimi");
  const [model, setModel] = useState("kimi-for-coding");
  const [baseUrl, setBaseUrl] = useState("https://api.kimi.com/coding/v1/chat/completions");
  const [apiKey, setApiKey] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<string | null>(null);
  const [playgroundPrompt, setPlaygroundPrompt] = useState("Say hello from the active KriyaX data workspace provider.");
  const [playgroundResult, setPlaygroundResult] = useState<LlmPlaygroundResult | null>(null);
  const [fullTestSteps, setFullTestSteps] = useState<Array<{ label: string; status: string }>>([]);

  useEffect(() => {
    Promise.all([getLlmConfig(provider), getLlmProfiles()])
      .then(([nextConfig, nextProfiles]) => {
        setConfig(nextConfig);
        setProfiles(nextProfiles);
      })
      .catch((value: Error) => setError(value.message));
  }, [provider]);

  useEffect(() => {
    const profile = profiles.find((item) => item.provider === provider && item.is_default);
    setLabel(profile?.label ?? defaults[provider].label);
    setModel(profile?.model ?? config?.model ?? defaults[provider].model);
    setBaseUrl(profile?.base_url ?? config?.base_url ?? defaults[provider].base_url);
    setApiKey("");
  }, [provider, config, profiles]);

  const refresh = async () => {
    const [nextConfig, nextProfiles] = await Promise.all([getLlmConfig(provider), getLlmProfiles()]);
    setConfig(nextConfig);
    setProfiles(nextProfiles);
  };

  const saveProvider = async () => {
    setLoading("save");
    setError(null);
    setMessage(null);
    try {
      if (apiKey.trim()) {
        await saveLlmVaultKey({
          provider,
          api_key: apiKey.trim(),
          model: model.trim() || undefined,
          base_url: baseUrl.trim() || undefined
        });
      }
      const profile = await createLlmProfile({
        label,
        provider,
        model: model.trim() || undefined,
        base_url: baseUrl.trim() || undefined
      });
      await setDefaultLlmProfile(profile.id);
      await refresh();
      setApiKey("");
      setMessage(`${profile.label} profile saved.`);
    } catch (value) {
      setError(value instanceof Error ? value.message : "LLM settings save failed");
    } finally {
      setLoading(null);
    }
  };

  const testProvider = async () => {
    setLoading("test");
    setError(null);
    setMessage(null);
    try {
      const result = await testLlm({ provider, model: model.trim() || undefined, message: "Say OK for the LLM test runner." });
      setMessage(result.success ? `Test response: ${result.response}` : result.error);
    } catch (value) {
      setError(value instanceof Error ? value.message : "LLM settings test failed");
    } finally {
      setLoading(null);
    }
  };

  const testPlayground = async () => {
    setLoading("playground");
    setError(null);
    setMessage(null);
    try {
      setPlaygroundResult(await runLlmPlayground({ provider, prompt: playgroundPrompt, model: model.trim() || undefined }));
    } catch (value) {
      setError(value instanceof Error ? value.message : "LLM playground failed");
    } finally {
      setLoading(null);
    }
  };

  const runFullTest = async () => {
    setLoading("full-test");
    setError(null);
    setMessage(null);
    setFullTestSteps([]);
    try {
      setFullTestSteps([{ label: "Config", status: "running" }]);
      await getLlmConfig(provider);
      setFullTestSteps([{ label: "Config", status: "ok" }, { label: "Save", status: apiKey.trim() ? "running" : "skipped" }]);
      if (apiKey.trim()) {
        await saveLlmVaultKey({ provider, api_key: apiKey.trim(), model: model.trim() || undefined, base_url: baseUrl.trim() || undefined });
      }
      setFullTestSteps([{ label: "Config", status: "ok" }, { label: "Save", status: apiKey.trim() ? "ok" : "skipped" }, { label: "Test", status: "running" }]);
      const test = await testLlm({ provider, model: model.trim() || undefined, message: "Say OK for the LLM test runner." });
      if (!test.success) throw new Error(test.error ?? "LLM test failed");
      setFullTestSteps([{ label: "Config", status: "ok" }, { label: "Save", status: apiKey.trim() ? "ok" : "skipped" }, { label: "Test", status: "ok" }, { label: "Chat", status: "running" }]);
      const chat = await runLlmPlayground({ provider, model: model.trim() || undefined, prompt: "Write one sentence confirming the KriyaX LLM playground is using a live provider." });
      setPlaygroundResult(chat);
      setFullTestSteps([{ label: "Config", status: "ok" }, { label: "Save", status: apiKey.trim() ? "ok" : "skipped" }, { label: "Test", status: "ok" }, { label: "Chat", status: "ok" }]);
      await refresh();
      setApiKey("");
      setMessage("Full LLM test completed.");
    } catch (value) {
      setError(value instanceof Error ? value.message : "Run full test failed");
    } finally {
      setLoading(null);
    }
  };

  const makeDefault = async (id: string) => {
    await setDefaultLlmProfile(id);
    await refresh();
  };

  const removeProfile = async (id: string) => {
    await deleteLlmProfile(id);
    await refresh();
  };

  return (
    <Panel title="LLM & Playground">
      <div className="llm-grid">
        <div className="llm-form">
          <div className="form-grid">
            <label>Provider
              <select value={provider} onChange={(event) => setProvider(event.target.value as LlmProvider)}>
                <option value="openai">OpenAI</option>
                <option value="kimi">Kimi</option>
                <option value="anthropic">Anthropic</option>
                <option value="azure-openai">Azure OpenAI</option>
              </select>
            </label>
            <label>Profile label<input value={label} onChange={(event) => setLabel(event.target.value)} /></label>
            <label>Model<input value={model} onChange={(event) => setModel(event.target.value)} placeholder="gpt-4.1-mini or claude-3-5-sonnet-latest" /></label>
            <label>API URL / endpoint<input value={baseUrl} onChange={(event) => setBaseUrl(event.target.value)} /></label>
            <label className="full-width-field">API key
              <input type="password" value={apiKey} onChange={(event) => setApiKey(event.target.value)} placeholder={config?.masked_key_status !== "missing" ? "Saved key exists. Enter a new key to replace it." : "Paste provider API key"} />
            </label>
          </div>
          <div className="credential-note">
            <ShieldCheck size={16} />
            <span>Keys are encrypted server-side in the project workspace and are not echoed back to the UI.</span>
          </div>
          <div className="panel-actions row-actions">
            <button className="primary-button" onClick={saveProvider} disabled={loading !== null || !label.trim() || !model.trim() || !baseUrl.trim()}>{loading === "save" ? "Saving..." : "Save"}</button>
            <button className="table-link-button" onClick={testProvider} disabled={loading !== null}>{loading === "test" ? "Testing..." : "Test"}</button>
            <button className="table-link-button" onClick={runFullTest} disabled={loading !== null}>{loading === "full-test" ? "Running..." : "Run full test"}</button>
          </div>
          {fullTestSteps.length ? <div className="profile-badges">{fullTestSteps.map((step) => <span className="status-text" key={step.label}>{step.label}: {step.status}</span>)}</div> : null}
          {message ? <div className="notice success">{message}</div> : null}
          {error ? <div className="notice error">{error}</div> : null}
        </div>

        <div className="profile-stack">
          {profiles.map((profile) => <LlmProfileCard profile={profile} key={profile.id} onDefault={makeDefault} onDelete={removeProfile} />)}
          <div className="vault-card">
            <KeyRound size={17} />
            <div>
              <strong>Key status</strong>
              <span>{config ? `${config.source} · ${config.masked_key_status}` : "Loading config..."}</span>
            </div>
          </div>
          <div className="vault-card">
            <ShieldCheck size={17} />
            <div>
              <strong>Runtime model</strong>
              <span>{config?.model ?? "Loading model..."}</span>
            </div>
          </div>
        </div>
      </div>
      <div className="llm-playground">
        <div>
          <strong>LLM Playground</strong>
          <span>Test the selected provider without exposing the saved key.</span>
        </div>
        <label>Prompt<textarea className="editor compact-editor" value={playgroundPrompt} onChange={(event) => setPlaygroundPrompt(event.target.value)} /></label>
        <div className="panel-actions row-actions">
          <button className="primary-button" onClick={testPlayground} disabled={loading !== null || !playgroundPrompt.trim()}>{loading === "playground" ? "Testing..." : "Test prompt"}</button>
          {playgroundResult ? <span className="status-chip">{playgroundResult.status} · {playgroundResult.model} · {playgroundResult.latencyMs}ms</span> : null}
        </div>
        {playgroundResult ? <div className="playground-output">{playgroundResult.responseText}</div> : null}
      </div>
    </Panel>
  );
}

function LlmProfileCard({ profile, onDefault, onDelete }: { profile: LlmProfile; onDefault: (id: string) => void; onDelete: (id: string) => void }) {
  return (
    <div className="profile-card">
      <div>
        <strong>{profile.label}</strong>
        <span>{profile.model}</span>
        <small>{profile.base_url}</small>
      </div>
      <div className="profile-badges">
        {profile.is_default ? <span className="status-text">default</span> : <button className="table-link-button" onClick={() => onDefault(profile.id)}>Default</button>}
        <span className={profile.is_enabled ? "status-text" : "status-text warning-text"}>{profile.is_enabled ? "enabled" : "disabled"}</span>
        <button className="table-link-button danger-button" onClick={() => onDelete(profile.id)}>Delete</button>
      </div>
    </div>
  );
}

function Placeholder({ title, items }: { title: string; items: string[] }) {
  return (
    <section className="screen-grid">
      <Panel title={title}>
        <div className="lane-list">
          {items.map((item) => <ActionRow key={item} icon={<Database size={18} />} title={item} meta="Planned from frozen L5/L6 contract" />)}
        </div>
      </Panel>
    </section>
  );
}

function Panel({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="panel">
      <h2>{title}</h2>
      {children}
    </section>
  );
}

function SchemaPicker({
  label,
  value,
  schemas,
  newSchemaName,
  onChange,
  onNewSchemaName,
  onAddSchema
}: {
  label: string;
  value: string;
  schemas: string[];
  newSchemaName: string;
  onChange: (value: string) => void;
  onNewSchemaName: (value: string) => void;
  onAddSchema: () => void;
}) {
  return (
    <label className="schema-picker">
      {label}
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {schemas.map((schema) => <option value={schema} key={schema}>{schema}</option>)}
      </select>
      <span className="schema-add-row">
        <input value={newSchemaName} onChange={(event) => onNewSchemaName(event.target.value)} placeholder="new_schema" />
        <button type="button" className="icon-button" onClick={onAddSchema} disabled={!newSchemaName.trim()} title="Add schema">
          <Database size={14} />
        </button>
      </span>
    </label>
  );
}

function DataPreview({ rows }: { rows: Record<string, string | number | boolean | null>[] }) {
  const columns = rows[0] ? Object.keys(rows[0]) : [];

  if (!rows.length) {
    return <div className="table-preview">No preview rows available.</div>;
  }

  return (
    <div className="preview-scroll">
      <table>
        <thead>
          <tr>{columns.map((column) => <th key={column}>{column}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((column) => <td key={column}>{String(row[column] ?? "")}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function useCatalogTables() {
  const [tables, setTables] = useState<CatalogTable[]>([]);
  const [error, setError] = useState<string | null>(null);

  const reload = async () => {
    setError(null);
    try {
      const items = await fetchCatalogTables();
      setTables(
        [...items].sort(
          (left, right) =>
            new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime()
        )
      );
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "Catalog load failed");
    }
  };

  useEffect(() => {
    void reload();
  }, []);

  return { tables, error, reload };
}

function defaultPythonCode(tableName = "raw_files.sales_orders_raw") {
  const outputName = `${tableName.split(".").pop() ?? "table"}_curated`;
  return `df = load_table("${tableName}")\nprint(f"loaded {len(df)} rows")\nsave_table(df, "${outputName}", schema="curated")`;
}

function suggestTableName(fileName: string) {
  return fileName
    .replace(/\.[^.]+$/, "")
    .trim()
    .toLowerCase()
    .replace(/[^0-9a-zA-Z_]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .replace(/_+/g, "_") || "imported_table";
}

function tableDetailPath(table: CatalogTable) {
  const params = new URLSearchParams({
    schema: table.schema,
    table: table.tableName
  });
  return `/catalog/table?${params.toString()}`;
}

function tableManagePath(table: CatalogTable) {
  const params = new URLSearchParams({ schema: table.schema, table: table.tableName });
  return `/catalog/table/manage?${params.toString()}`;
}

function tableExportPath(table: CatalogTable) {
  const params = new URLSearchParams({ schema: table.schema, table: table.tableName });
  return `/catalog/table/export?${params.toString()}`;
}

function pushRoute(path: string) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

function insertLoadTable(table: CatalogTable) {
  window.sessionStorage.setItem("agentCodeDraft", `df = load_table("${table.qualifiedName}")\nprint(df.head())\n`);
  pushRoute("/code");
}

function selectedTableFromLocation() {
  const params = new URLSearchParams(window.location.search);
  const schema = params.get("schema");
  const tableName = params.get("table");
  return schema && tableName ? { schema, tableName } : null;
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

function pipelineScheduleDraft(pipeline: Pipeline): PipelineSchedulePayload {
  return {
    type: pipeline.schedule?.type ?? "daily",
    timeOfDay: pipeline.schedule?.timeOfDay ?? "06:00",
    weekday: pipeline.schedule?.weekday ?? "monday",
    cronExpression: pipeline.schedule?.cronExpression ?? "0 6 * * *",
    timezone: pipeline.schedule?.timezone ?? "Asia/Kolkata"
  };
}

function Metric({ label, value, detail }: { label: string; value: string; detail: string }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </div>
  );
}

function ActionRow({ icon, title, meta }: { icon: ReactNode; title: string; meta: string }) {
  return (
    <div className="action-row">
      <span className="action-icon">{icon}</span>
      <div>
        <strong>{title}</strong>
        <span>{meta}</span>
      </div>
    </div>
  );
}
