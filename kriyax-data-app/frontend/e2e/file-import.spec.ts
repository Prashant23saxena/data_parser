import { expect, test } from "@playwright/test";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

test("imports a CSV through the UI and exposes it in catalog preview", async ({ page }) => {
  const tableName = `ui_orders_${Date.now()}`;
  const csvPath = path.join(os.tmpdir(), `${tableName}.csv`);
  fs.writeFileSync(csvPath, "Customer,Order Date,Amount\nAcme,2026-05-01,12.50\nBravo,2026-05-02,20.00\n");

  await page.goto("/connectors/file-import");
  await page.locator('input[type="file"]').setInputFiles(csvPath);

  await expect(page.getByText(`${tableName}.csv · 2 rows`)).toBeVisible();
  await expect(page.getByRole("cell", { name: "Customer", exact: true })).toBeVisible();
  await expect(page.locator('input[value="customer"]')).toBeVisible();
  await expect(page.getByRole("cell", { name: "date", exact: true })).toBeVisible();
  await expect(page.getByRole("cell", { name: "decimal", exact: true })).toBeVisible();
  await expect(page.getByRole("cell", { name: "Acme" })).toBeVisible();

  await page.getByLabel("New table name").fill(tableName);
  await page.getByRole("button", { name: "Create table" }).click();

  await expect(page.getByText(`Created raw_files.${tableName} with 2 rows.`)).toBeVisible();

  await page.getByRole("button", { name: "Catalog" }).click();
  await expect(page.getByRole("cell", { name: `raw_files.${tableName}`, exact: true })).toBeVisible();
  await expect(page.getByRole("cell", { name: `${tableName}.csv` })).toBeVisible();

  await page.getByRole("row", { name: new RegExp(`raw_files\\.${tableName}`) }).getByRole("button", { name: "Open" }).click();
  await page.getByRole("button", { name: "Full detail" }).click();
  await expect(page.getByRole("heading", { name: `raw_files.${tableName}` })).toBeVisible();
  await expect(page.getByText("Catalog > Table Detail")).toBeVisible();
  await page.getByRole("button", { name: "Columns" }).click();
  await expect(page.getByRole("cell", { name: "order_date" })).toBeVisible();
  await page.getByRole("button", { name: "Preview" }).click();
  await expect(page.getByRole("cell", { name: "Acme" })).toBeVisible();
  await page.getByRole("button", { name: "Back" }).click();
  await expect(page.getByRole("heading", { name: "Catalog" })).toBeVisible();

  await page.getByRole("button", { name: "Code Workspace" }).click();
  await expect(page.getByRole("button", { name: new RegExp(`raw_files\\.${tableName}`) })).toBeVisible();
});

test("blocks duplicate target column names until the user renames them", async ({ page }) => {
  const tableName = `ui_duplicate_orders_${Date.now()}`;
  const csvPath = path.join(os.tmpdir(), `${tableName}.csv`);
  fs.writeFileSync(csvPath, "Customer,Customer,Amount\nAcme,A-001,12.50\nBravo,B-002,20.00\n");

  await page.goto("/connectors/file-import");
  await page.locator('input[type="file"]').setInputFiles(csvPath);

  await expect(page.getByText("Duplicate source column names found. Rename the target columns before import.")).toBeVisible();
  await expect(page.getByRole("button", { name: "Create table" })).toBeDisabled();

  const customerInputs = page.locator('input[value="customer"]');
  await customerInputs.nth(1).fill("customer_code");
  await page.getByLabel("New table name").fill(tableName);

  await expect(page.getByRole("button", { name: "Create table" })).toBeEnabled();
  await page.getByRole("button", { name: "Create table" }).click();
  await expect(page.getByText(`Created raw_files.${tableName} with 2 rows.`)).toBeVisible();
});
