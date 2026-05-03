import { expect, test } from "@playwright/test";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

test("runs a Python script that loads a table and saves a derived table", async ({ page }) => {
  const tableName = `code_orders_${Date.now()}`;
  const derivedTable = `big_orders_${Date.now()}`;
  const csvPath = path.join(os.tmpdir(), `${tableName}.csv`);
  fs.writeFileSync(csvPath, "Customer,Amount\nAcme,12.50\nBravo,20.00\n");

  await page.goto("/connectors/file-import");
  await page.locator('input[type="file"]').setInputFiles(csvPath);
  await page.getByRole("button", { name: "Create table" }).click();
  await expect(page.getByText(`Created raw_files.${tableName} with 2 rows.`)).toBeVisible();

  await page.getByRole("button", { name: "Code Workspace" }).click();
  await expect(page.getByRole("button", { name: new RegExp(`raw_files\\.${tableName}`) })).toBeVisible();

  await page.getByLabel("Script name").fill(`${derivedTable}.py`);
  await page.locator("textarea").fill(
    `df = load_table("raw_files.${tableName}")\n` +
      `print(f"loaded {len(df)} rows")\n` +
      `save_table(df[df["amount"] > 15], "${derivedTable}", schema="curated")`
  );
  await page.getByRole("button", { name: "Run script" }).click();

  await expect(page.getByText("Success")).toBeVisible();
  await expect(page.getByText("loaded 2 rows")).toBeVisible();
  await expect(page.getByText(`Saved: curated.${derivedTable}`)).toBeVisible();
  await expect(page.getByRole("cell", { name: "Bravo" })).toBeVisible();
  await expect(page.getByRole("button", { name: new RegExp(`curated\\.${derivedTable}`) })).toBeVisible();

  await page.getByRole("button", { name: "Saved Scripts" }).click();
  await expect(page.getByRole("cell", { name: `${derivedTable}.py`, exact: true })).toBeVisible();
  await page.getByRole("button", { name: `Open ${derivedTable}.py` }).click();
  await expect(page.getByLabel("Script name")).toHaveValue(`${derivedTable}.py`);
  await expect(page.locator("textarea")).toContainText(`raw_files.${tableName}`);
  await page.getByRole("button", { name: "Run script" }).click();
  await expect(page.getByText("loaded 2 rows")).toBeVisible();
});

test("sidebar hover expands and auto-collapses", async ({ page }) => {
  await page.goto("/catalog");
  await expect(page.locator(".app-shell")).toHaveClass(/sidebar-collapsed/);
  await page.locator(".sidebar").hover();
  await expect(page.locator(".app-shell")).not.toHaveClass(/sidebar-collapsed/);
  await page.locator("main").hover();
  await expect(page.locator(".app-shell")).toHaveClass(/sidebar-collapsed/, { timeout: 3500 });
});
