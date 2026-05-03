import { expect, test } from "@playwright/test";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

test("exports and manages a catalog table", async ({ page }) => {
  const tableName = `manage_orders_${Date.now()}`;
  const renamedName = `${tableName}_renamed`;
  const csvPath = path.join(os.tmpdir(), `${tableName}.csv`);
  fs.writeFileSync(csvPath, "Customer,Amount\nAcme,12.50\n");

  await page.goto("/connectors/file-import");
  await page.locator('input[type="file"]').setInputFiles(csvPath);
  await page.getByLabel("New table name").fill(tableName);
  await page.getByRole("button", { name: "Create table" }).click();
  await expect(page.getByText(`Created raw_files.${tableName} with 1 rows.`)).toBeVisible();

  await page.getByRole("button", { name: "Catalog" }).click();
  const row = page.getByRole("row", { name: new RegExp(`raw_files\\.${tableName}`) });
  await row.getByRole("button", { name: "Open" }).click();
  await page.getByRole("button", { name: "Export CSV" }).click();
  await page.getByRole("button", { name: "Prepare CSV" }).click();
  await expect(page.locator("pre").filter({ hasText: "customer,amount" })).toBeVisible();

  await page.getByRole("button", { name: "Catalog" }).click();
  await row.getByRole("button", { name: "Open" }).click();
  await page.getByRole("button", { name: "Manage table" }).click();
  await page.getByLabel("New table name").fill(renamedName);
  await page.getByRole("button", { name: "Rename" }).click();
  await expect(page.getByText(`Renamed to raw_files.${renamedName}.`)).toBeVisible();
  await page.getByLabel("Confirm qualified name").fill(`raw_files.${renamedName}`);
  await page.getByRole("button", { name: "Truncate" }).click();
  await expect(page.getByText(`raw_files.${renamedName} truncated.`)).toBeVisible();
});

test("generates agent code and inserts it into the editor", async ({ page }) => {
  await page.goto("/code/agent");
  await page.getByLabel("Request").fill("Create a curated copy");
  await page.getByRole("button", { name: "Generate code" }).click();
  await expect(page.getByText("Generated Python code.")).toBeVisible();
  await expect(page.locator(".agent-dock textarea.code-textarea")).toContainText("load_table");
  await page.getByRole("button", { name: "Insert into editor" }).click();
  await expect(page.getByRole("heading", { name: "Python Editor" })).toBeVisible();
  await expect(page.locator("textarea.code-textarea").first()).toContainText("save_table");
});

test("storage exposes LLM playground without leaking keys", async ({ page }) => {
  await page.route("**/api/llm/playground", async (route) => {
    await route.fulfill({
      json: {
        provider: "openai",
        model: "local",
        latencyMs: 0,
        status: "fallback",
        responseText: "Fallback runtime is active for hello from e2e"
      }
    });
  });
  await page.goto("/storage");
  await page.getByLabel("Prompt").fill("hello from e2e");
  await page.getByRole("button", { name: "Test prompt" }).click();
  await expect(page.getByText("Fallback runtime", { exact: false })).toBeVisible();
  await expect(page.locator(".playground-output")).toContainText("hello from e2e");
  await expect(page.getByText("sk-secret")).not.toBeVisible();
});
